
import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import namedtuple_row
from utilidades.constantes import *
from typing import Literal

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Constantes de conexão lidas das variáveis de ambiente
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

class DBManager:
    """
    Gerencia a conexão e as operações com o banco de dados do jogo.
    Implementa o padrão Singleton para garantir uma única instância.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance.conn = None
            cls._instance.cursor = None
            cls._instance._conectar()
        return cls._instance

    def _conectar(self):
        """Tenta estabelecer e retornar uma conexão com o banco de dados PostgreSQL."""
        try:
            self.conn = psycopg.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT,
                row_factory=namedtuple_row
            )
            self.cursor = self.conn.cursor()
            print("DBManager: Conexão com o PostgreSQL estabelecida.")
        except psycopg.OperationalError as e:
            print(f"DBManager ERRO: Não foi possível conectar ao banco de dados: {e}")
            self.conn = None
            self.cursor = None

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("DBManager: Conexão com o PostgreSQL fechada.")
        DBManager._instance = None # Reseta a instância Singleton

    def executar_query(self, consulta, params=None, fetchone=False, fetchall=False):
        """
        Executa uma consulta SQL no banco de dados.
        :param consulta: A string SQL a ser executada.
        :param params: Uma tupla ou lista de parâmetros para a consulta (para evitar SQL Injection).
        :param fetchone: Se True, retorna apenas uma linha.
        :param fetchall: Se True, retorna todas as linhas.
        :return: Resultados da consulta (se for SELECT), True para sucesso, False para falha.
        """
        if not self.conn:
            print("DBManager ERRO: Não há conexão ativa com o banco de dados.")
            return False

        try:
            self.cursor.execute(consulta, params)
            if fetchone:
                return self.cursor.fetchone()
            elif fetchall:
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return True
        except psycopg.Error as e:
            self.conn.rollback()
            print(f"DBManager ERRO ao executar consulta '{consulta}': {e}")
            return False

    # ===============================================
    # Métodos de Operações com progresso salvo
    # ===============================================
    def carregar_dados_dos_slots(self):
        """
        Busca os dados dos slots salvos.
        """
        consulta = """
            SELECT
                progresso.identificador_progresso,
                progresso.numero_do_slot,
                progresso.data_ultimo_salvamento,
                progresso.ocupado,
                TRIM(jogador.nome) AS nome_jogador,
                jogador.identificador_jogador,
                ROUND(
                    100.0 * COUNT(CASE WHEN estado_missao.estado = 'concluida' THEN 1 END) 
                    / NULLIF(COUNT(estado_missao.identificador_missao), 0),
                    1
                ) AS percentual_concluido
            FROM progresso
            LEFT JOIN jogador ON jogador.identificador_progresso = progresso.identificador_progresso
            LEFT JOIN estado_missao ON estado_missao.identificador_progresso = progresso.identificador_progresso
            GROUP BY 
                progresso.identificador_progresso, 
                progresso.numero_do_slot, 
                progresso.data_ultimo_salvamento, 
                progresso.ocupado, 
                jogador.nome, 
                jogador.identificador_jogador
            ORDER BY progresso.numero_do_slot;
        """
        return self.executar_query(consulta, fetchall=True)

    

    
    def criar_novo_jogo(self, personagem_selecionado, id_progresso):
        """
        Cria dados iniciais de jogador e aliado.
        """
        descricao_silvie = "Silvie é energia em forma de pessoa — fala rápido, pensa mais rápido ainda e dificilmente fica parada. Se algo está calmo demais, é só uma questão de tempo até ela causar um furacão de ideias (ou problemas). Adora improvisar e não leva desaforo pra casa... aliás, raramente volta pra casa."
        descricao_shuan = "Shuan prefere observar antes de agir, mas quando fala, vale a pena ouvir. Metódico, detalhista e dono de um sarcasmo discreto, ele sempre tem um plano — mesmo que ninguém tenha pedido. Se o mundo for um tabuleiro, Shuan já está três jogadas à frente."
        
        # 1) Cria o jogador e o aliado
        if personagem_selecionado == SILVIE:
            id_jogador, id_aliado = (
                self.salvar_novo_jogador(SILVIE, descricao_silvie, id_progresso),
                self.salvar_novo_aliado(SHUAN, descricao_shuan, id_progresso)
            )
            habilidades_jogador = ['hab003','hab004']
            habilidades_aliado = ['hab001','hab002']
        else:
            id_jogador, id_aliado = (
                self.salvar_novo_jogador(SHUAN, descricao_shuan, id_progresso),
                self.salvar_novo_aliado(SILVIE, descricao_silvie, id_progresso)
            )
            habilidades_jogador = ['hab001','hab002']
            habilidades_aliado = ['hab003','hab004']

        # 2) Habilidades
        for habilidade in habilidades_jogador:
            self.inserir_habilidades(id_jogador, habilidade)
        for habilidade in habilidades_aliado:
            self.inserir_habilidades(id_aliado, habilidade)

        dialogos_do_jogador = {
            SILVIE: [
                {
                    'id_missao': 'mis001',
                    'genero': 'F',
                    'sequencia': 4,
                    'dialogo': 'Você... quem é você?',
                },
                {
                    'id_missao': 'mis001',
                    'genero': 'F',
                    'sequencia': 7,
                    'dialogo': 'Eu... não sei como vim parar aqui.',
                },
                {
                    'id_missao': 'mis002',
                    'genero': 'F',
                    'sequencia': 1,
                    'dialogo': 'Tsc... sério?',
                },
                {
                    'id_missao': 'mis003',
                    'genero': 'F',
                    'sequencia': 3,
                    'dialogo': 'Só alguém procurando respostas... e talvez um pouco de água.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 3,
                    'dialogo': '(Olhando ao redor): — Gertrudes é... uma senhora?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 6,
                    'dialogo': '(Pegando um garfo): — Ok... então essa vila tem galinhas vingativas, cozinheiras dramáticas e um senhor que tempera a terra com orégano?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 9,
                    'dialogo': '(Provando o Omurice): — Uau. Isso é... surpreendentemente bom. Tipo “não esperava gostar tanto de arroz com ovo” bom.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 12,
                    'dialogo': '(Sorrindo): — Eu só queria água. Agora tô jantando com filósofos, artistas e galinhas vingativas.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 14,
                    'dialogo': '(Recuando): — Ah não. É ela. Essa aí me seguiu desde o campo. Ela quer vingança.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 17,
                    'dialogo': '(Entregando o pão com reverência): — Trégua, senhora Gertrudes. Que nossos caminhos se cruzem apenas no café da manhã.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 23,
                    'dialogo': 'E ninguém tentou detê-la?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 26,
                    'dialogo': 'Eu vou enfrentá-la.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'F',
                    'sequencia': 3,
                    'dialogo': 'Foi por pouco. Mas está feito.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'F',
                    'sequencia': 5,
                    'dialogo': 'Eu... estou procurando alguém. Minha irmã. Preciso continuar.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'F',
                    'sequencia': 7,
                    'dialogo': 'Isso é ótimo... mas como eu chego lá?',
                },
            ],
            SHUAN: [
                {
                    'id_missao': 'mis001',
                    'genero': 'M',
                    'sequencia': 4,
                    'dialogo': 'Você... quem é você?',
                },
                {
                    'id_missao': 'mis001',
                    'genero': 'M',
                    'sequencia': 7,
                    'dialogo': 'Eu... não sei como vim parar aqui.',
                },
                {
                    'id_missao': 'mis002',
                    'genero': 'M',
                    'sequencia': 1,
                    'dialogo': 'Tsc... sério?',
                },
                {
                    'id_missao': 'mis003',
                    'genero': 'M',
                    'sequencia': 3,
                    'dialogo': 'Só alguém procurando respostas... e talvez um pouco de água.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 3,
                    'dialogo': '(Olhando ao redor): — Gertrudes é... uma senhora?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 6,
                    'dialogo': '(Pegando um garfo): — Ok... então essa vila tem galinhas vingativas, cozinheiras dramáticas e um senhor que tempera a terra com orégano?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 9,
                    'dialogo': '(Provando o Omurice): — Uau. Isso é... surpreendentemente bom. Tipo “não esperava gostar tanto de arroz com ovo” bom.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 12,
                    'dialogo': '(Sorrindo): — Eu só queria água. Agora tô jantando com filósofos, artistas e galinhas vingativas.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 14,
                    'dialogo': '(Recuando): — Ah não. É ela. Essa aí me seguiu desde o campo. Ela quer vingança.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 17,
                    'dialogo': '(Entregando o pão com reverência): — Trégua, senhora Gertrudes. Que nossos caminhos se cruzem apenas no café da manhã.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 23,
                    'dialogo': 'E ninguém tentou detê-la?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 26,
                    'dialogo': 'Eu vou enfrentá-la.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'M',
                    'sequencia': 3,
                    'dialogo': 'Foi por pouco. Mas está feito.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'M',
                    'sequencia': 5,
                    'dialogo': 'Eu... estou procurando alguém. Minha irmã. Preciso continuar.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'M',
                    'sequencia': 7,
                    'dialogo': 'Isso é ótimo... mas como eu chego lá?',
                },
            ]
        }

        # 3) Diálogos
        self.inserir_dialogos_personagem(id_jogador, dialogos_do_jogador[personagem_selecionado])

        # 4) Inventário
        self.criar_inventario(id_jogador, id_progresso)
        self.criar_inventario(id_jogador, id_progresso, 'kit')

        self.atualizar_espaco_salvamento(id_progresso)

        # 5) Aceita a primeira missão
        self.atualizar_estado_missao('mis001', id_progresso, 'aceita')

        # 6) Retorna dados carregados já prontos
        return self.carregar_dados_do_progresso(id_jogador, id_progresso)



    def carregar_dados_do_progresso(self, id_jogador, identificador_progresso):
        """
        Retorna uma tupla com os dados do jogador, da área atual e dos inimigos na área (se houver arena).
        :return: (jogador, area, inimigos ou None)
        """

        jogador = self.buscar_jogador(id_jogador)
        if not jogador:
            return None, None, None

        mochila_jogador = self.buscar_inventario(id_jogador, 'moc')
        kit_jogador = self.buscar_inventario(id_jogador, 'kit')

        area = self.buscar_info_area(jogador.identificador_area, identificador_progresso)

        ilha = self.buscar_info_ilha(area.identificador_ilha, identificador_progresso)

        return jogador, mochila_jogador, kit_jogador, ilha, area



    def atualizar_espaco_salvamento(self, identificador_progresso):
        """
        Atualiza a data e hora do último dado salvo
        """
        consulta = """
            UPDATE progresso
            SET ocupado = TRUE,
                data_ultimo_salvamento = now()
            WHERE identificador_progresso = %s;
        """
        return self.executar_query(consulta, (identificador_progresso,))



    # ===============================================
    # Métodos de Operações com Jogador
    # ===============================================
    def buscar_jogador(self, id_jogador):
        """Busca os dados de um jogador pelo ID."""
        consulta = """
            SELECT
                identificador_jogador,
                identificador_area,
                TRIM(nome) AS nome,
                TRIM(descricao) AS descricao,
                coordenada_x,
                coordenada_y,
                energia,
                vida,
                nivel,
                sorte,
                vida_atual,
                experiencia_atual
            FROM jogador
            WHERE identificador_jogador = %s;
        """
        return self.executar_query(consulta, (id_jogador,), fetchone=True)

    def atualizar_jogador(self, id_jogador, energia, vida_atual, nivel, experiencia_atual, coord_x, coord_y, id_mapa):
        """Atualiza os dados de um jogador."""
        consulta = """
            UPDATE jogador
            SET energia = %s, vida_atual = %s, nivel = %s, experiencia_atual = %s,
                coordenada_x = %s, coordenada_y = %s, id_mapa = %s
            WHERE id_jogador = %s;
        """
        params = (energia, vida_atual, nivel, experiencia_atual, coord_x, coord_y, id_mapa, id_jogador)
        return self.executar_query(consulta, params)
    
    def atualizar_posicao_jogador(self, identificador_jogador, identificador_area, coordenada_x, coordenada_y):
        """Atualiza a posição do jogador"""
        consulta = """
            UPDATE jogador
                SET identificador_area = %s, coordenada_x = %s, coordenada_y = %s
                WHERE identificador_jogador = %s;
        """
        return self.executar_query(consulta, (identificador_area, coordenada_x, coordenada_y, identificador_jogador))

    def salvar_novo_jogador(self, nome, descricao, identificador_progresso):
        """Insere um novo jogador no banco de dados e retorna o ID gerado."""
        consulta = """
            INSERT INTO jogador
                (identificador_area, identificador_progresso, nome, descricao, coordenada_x, coordenada_y,
                energia, vida, nivel, sorte, vida_atual, experiencia_atual, moedas_totais)
            VALUES
                ('are001', %s, %s, %s, 1950, 140, 5, 10, 0, 1, 10, 0, 0)
            RETURNING identificador_jogador;
        """
        return self.executar_query(consulta, (identificador_progresso, nome, descricao), fetchone=True)[0]

    def salvar_novo_aliado(self, nome, descricao, identificador_progresso):
        """Insere um novo aliado no banco de dados e retorna o ID gerado."""
        consulta = """
            INSERT INTO aliado
                (identificador_area, identificador_progresso, nome, descricao, coordenada_x, coordenada_y, vida, nivel, vida_atual)
            VALUES
                ('are016', %s, %s, %s, 460, 315, 40, 30, 40)
            RETURNING identificador_aliado;
        """
        return self.executar_query(consulta, (identificador_progresso, nome, descricao), fetchone=True)[0]

    
    def inserir_habilidades(self, id_personagem, id_habilidade):
        """Insere habilidades para um personagem específico"""

        consulta = """
            INSERT INTO habilidade_personagem
                (identificador_personagem, identificador_habilidade)
            VALUES
                (%s, %s)
            RETURNING (identificador_personagem, identificador_habilidade);
        """
        self.executar_query(consulta, (id_personagem, id_habilidade), fetchone=True)

    def inserir_dialogos_personagem(self, id_jogador, dialogos):
        """
        Insere uma lista de diálogos para um personagem jogador.
        :param id_jogador: ID do jogador que falará os diálogos
        :param dialogos: Lista de dicionários com chaves:
                        'id_missao', 'sequencia', 'genero', 'dialogo'
        """
        consulta = """
            INSERT INTO dialogo (identificador_personagem, identificador_missao, sequencia_local, genero, dialogo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING identificador_dialogo;
        """
        for dialogo in dialogos:
            parametros = (
                id_jogador,
                dialogo['id_missao'],
                dialogo['sequencia'],
                dialogo['genero'],
                dialogo['dialogo']
            )
            self.executar_query(consulta, parametros, fetchone=True)

    
    def buscar_dialogos_sem_missao(self, id_personagem, genero):
        """
        Retorna todos os diálogos de um personagem específico que não estão associados a nenhuma missão.
        Inclui o nome do personagem que está falando.

        :param id_personagem: ID do personagem (jogador, aliado, etc)
        :return: Lista de tuplas com (identificador_dialogo, sequencia_local, genero, nome_personagem, dialogo)
        """
        consulta = """
            SELECT 
                d.identificador_dialogo,
                d.sequencia_local,
                d.genero,
                COALESCE(
                    TRIM(j.nome),
                    TRIM(a.nome),
                    TRIM(h.nome),
                    '???'
                ) AS nome_personagem,
                TRIM(d.dialogo) AS dialogo
            FROM dialogo d
            LEFT JOIN jogador j ON d.identificador_personagem = j.identificador_jogador
            LEFT JOIN aliado a ON d.identificador_personagem = a.identificador_aliado
            LEFT JOIN habitante h ON d.identificador_personagem = h.identificador_habitante
            WHERE d.identificador_personagem = %s
                AND d.identificador_missao IS NULL
                AND d.genero = %s
            ORDER BY d.sequencia_local;
        """
        return self.executar_query(consulta, (id_personagem, genero), fetchall=True)



    def buscar_missoes_aceitas_pelo_jogador(self, id_jogador):
        """
        Retorna todas as missões aceitas atualmente pelo jogador,
        incluindo o nome do item de recompensa (se houver) e o ID da área da missão.
        
        :param id_jogador: ID do jogador
        :return: Lista com (id_missao, nome_missao, descricao, nivel_de_desbloqueio, id_area, id_item, nome_item)
        """
        consulta = """
            SELECT 
                m.identificador_missao,
                TRIM(m.nome) AS nome,
                TRIM(m.descricao) AS descricao,
                m.nivel_de_desbloqueio,
                m.identificador_area,
                im.identificador_item,
                COALESCE(
                    TRIM(a.nome),
                    TRIM(f.nome),
                    TRIM(ac.nome),
                    TRIM(c.nome),
                    TRIM(nc.nome)
                ) AS nome_item
            FROM jogador j
            JOIN estado_missao em ON em.identificador_progresso = j.identificador_progresso
            JOIN missao m ON m.identificador_missao = em.identificador_missao
            LEFT JOIN item_missao im ON im.identificador_missao = m.identificador_missao
            LEFT JOIN arma a ON a.identificador_arma = im.identificador_item
            LEFT JOIN fruta f ON f.identificador_fruta = im.identificador_item
            LEFT JOIN acessorio ac ON ac.identificador_acessorio = im.identificador_item
            LEFT JOIN consumivel c ON c.identificador_consumivel = im.identificador_item
            LEFT JOIN nao_consumivel nc ON nc.identificador_nao_consumivel = im.identificador_item
            WHERE j.identificador_jogador = %s
            AND em.estado = 'aceita'
            ORDER BY m.nivel_de_desbloqueio, m.nome;
        """
        return self.executar_query(consulta, (id_jogador,), fetchall=True)


    

    def buscar_estado_da_missao(self, id_missao, id_progresso):
        """
        Retorna o estado atual de uma missão específica para um progresso de jogo.

        :param id_missao: ID da missão (ex: 'mis001')
        :param id_progresso: ID do progresso do jogador
        :return: Estado da missão (ex: 'pendente', 'aceita', 'concluida') ou None
        """
        consulta = """
            SELECT TRIM(estado) AS estado
            FROM estado_missao
            WHERE identificador_missao = %s
            AND identificador_progresso = %s;
        """
        resultado = self.executar_query(consulta, (id_missao, id_progresso), fetchone=True)
        return resultado.estado if resultado else None



    def atualizar_estado_missao(self, id_missao, id_progresso, novo_estado: Literal['aceita', 'pendente', 'concluida']):
        """
        Atualiza o estado de uma missão específica no progresso do jogador.
        
        :param id_missao: ID da missão (ex: 'mis012')
        :param id_progresso: ID do progresso (vinculado ao jogador)
        :param novo_estado: Novo estado ('pendente', 'aceita' ou 'concluida')
        :return: True se atualizado com sucesso, False se falhou
        """
        if novo_estado not in ('pendente', 'aceita', 'concluida'):
            print(f"Estado inválido: {novo_estado}")
            return False

        consulta = """
            UPDATE estado_missao
            SET estado = %s
            WHERE identificador_missao = %s
            AND identificador_progresso = %s;
        """
        return self.executar_query(consulta, (novo_estado, id_missao, id_progresso))



    def buscar_dialogos_da_missao(self, id_missao, genero_jogador, id_jogador):
        """
        Retorna os diálogos da missão com base no gênero do jogador e no identificador do jogador.
        Inclui:
        - Falas do jogador atual
        - Falas de NPCs e do narrador
        Exclui:
        - Falas de outros jogadores do mesmo gênero

        :param id_missao: ID da missão
        :param genero_jogador: 'F' ou 'M'
        :param id_jogador: ID do jogador atual
        :return: Lista com (id_dialogo, nome_personagem, sequencia_local, dialogo)
        """
        consulta = """
            SELECT
                dialogo.identificador_dialogo,
                COALESCE(
                    TRIM(jogador.nome),
                    TRIM(aliado.nome),
                    TRIM(habitante.nome),
                    '???'
                ) AS nome_personagem,
                dialogo.sequencia_local,
                TRIM(dialogo.dialogo) AS dialogo
            FROM dialogo
            LEFT JOIN tipo_personagem ON tipo_personagem.identificador_personagem = dialogo.identificador_personagem
            LEFT JOIN jogador ON tipo_personagem.identificador_personagem = jogador.identificador_jogador
            LEFT JOIN aliado ON tipo_personagem.identificador_personagem = aliado.identificador_aliado
            LEFT JOIN habitante ON tipo_personagem.identificador_personagem = habitante.identificador_habitante
            WHERE dialogo.identificador_missao = %s
            AND dialogo.genero = %s
            AND (
                dialogo.identificador_personagem IS NULL
                OR tipo_personagem.tipo <> 'jog'
                OR dialogo.identificador_personagem = %s
            )
            ORDER BY dialogo.sequencia_local;
        """
        return self.executar_query(consulta, (id_missao, genero_jogador, id_jogador), fetchall=True)


    
    # ===============================================
    # Métodos de Operações com Inventário e Itens
    # ===============================================

    def buscar_inventario(self, identificador_personagem, tipo_inventario='moc', identificador_progresso=None):
        """Acessa o inventário de um personagem e seus atributos, filtrando também por progresso."""
        consulta = """
            SELECT
                inv.identificador_inventario,
                ti.identificador_item,
                ti.tipo AS tipo_item,
                COALESCE(a.nome, f.nome, c.nome, nc.nome) AS nome_item,
                COALESCE(a.raridade, f.raridade, c.raridade, nc.raridade) AS raridade,
                COALESCE(a.descricao, f.descricao, c.descricao, nc.descricao) AS descricao,
                ii.quantidade
            FROM inventario inv
            JOIN item_inventario ii
                ON ii.identificador_inventario = inv.identificador_inventario
            JOIN tipo_item ti
                ON ti.identificador_item = ii.identificador_item

            -- Joins para cada subtipo
            LEFT JOIN acessorio a
                ON a.identificador_acessorio = ti.identificador_item
            LEFT JOIN fruta f
                ON f.identificador_fruta = ti.identificador_item
            LEFT JOIN consumivel c
                ON c.identificador_consumivel = ti.identificador_item
            LEFT JOIN nao_consumivel nc
                ON nc.identificador_nao_consumivel = ti.identificador_item

            WHERE inv.identificador_personagem = %s
            AND inv.tipo_inventario = %s
            AND inv.identificador_progresso = %s;
        """
        return self.executar_query(consulta, (identificador_personagem, tipo_inventario, identificador_progresso), fetchall=True)


    def criar_inventario(self, id_jogador, id_progresso, tipo_inventario='moc'):
        """Cria um novo inventário para um jogador e retorna o ID do inventário."""
        consulta = """
            INSERT INTO inventario (identificador_personagem, identificador_progresso, tipo_inventario)
            VALUES (%s, %s, %s)
            RETURNING identificador_inventario;
        """
        self.executar_query(consulta, (id_jogador, id_progresso, tipo_inventario), fetchone=True)

    def buscar_itens_no_inventario(self, id_inventario):
        """
        Ver os tipos de itens no inventário de um jogador.
        Retorna (identificador_item, tipo_item.tipo, nome_do_item_base_no_nao_consumivel/consumivel).
        Adaptado à modelagem atual do seu banco de dados onde ItemInventario referencia TipoItem.
        Os nomes detalhados (ex: "Maçã Lustrosa") não podem ser obtidos diretamente por aqui
        se o ItemInventario só armazena o ID do TIPO de item.
        """
        consulta = """
            SELECT
                ii.identificador_item,
                ti.tipo AS tipo_geral
            FROM iteminventario ii
            JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
            WHERE ii.id_inventario = %s
            ORDER BY ti.tipo; -- Ordena para melhor visualização
        """
        return self.executar_query(consulta, (id_inventario,), fetchall=True)

    def adicionar_item_ao_inventario(self, id_inventario, identificador_item_tipo):
        """Adiciona um tipo de item ao inventário."""
        consulta = """
            INSERT INTO iteminventario (id_inventario, identificador_item)
            VALUES (%s, %s);
        """
        return self.executar_query(consulta, (id_inventario, identificador_item_tipo))

    def remover_item_do_inventario(self, id_inventario, identificador_item_tipo):
        """Remove um tipo de item específico do inventário."""
        consulta = """
            DELETE FROM iteminventario
            WHERE id_inventario = %s AND identificador_item = %s;
        """
        return self.executar_query(consulta, (id_inventario, identificador_item_tipo))
    
    def buscar_item_por_tipo_id(self, id_tipo_item):
        """
        Busca o tipo de um item específico na tabela tipo_item.
        Exemplo: SELECT tipo FROM item WHERE id = 1;
        """
        consulta = """
            SELECT tipo
            FROM tipo_item
            WHERE identificador_item = %s;
        """
        return self.executar_query(consulta, (id_tipo_item,), fetchone=True)

    # ===============================================
    # Métodos de Operações com Personagens (Lacaio, Chefe, Aliado, Habitante)
    # ===============================================

    def buscar_tipo_personagem(self, id_personagem):
        """
        Ver o tipo de uma pessoa (Personagem).
        Adaptado de: SELECT tipo FROM pessoa WHERE id = 3;
        """
        consulta = """
            SELECT tipo
            FROM tipo_personagem
            WHERE id_personagem = %s;
        """
        return self.executar_query(consulta, (id_personagem,), fetchone=True)

    def buscar_lacaio(self, id_lacaio):
        """
        Ver atributos de um lacaio específico.
        Exemplo: SELECT habilidade_briga, vida, forca FROM prisioneiro WHERE id = 3;
        (Adaptado para lacaio)
        """
        consulta = """
            SELECT nome, dano, vida, nivel, experiencia
            FROM lacaio
            WHERE id_lacaio = %s;
        """
        return self.executar_query(consulta, (id_lacaio,), fetchone=True)
    
    def buscar_lacaios_por_area(self, identificador_progresso, identificador_area):
        """
        Retorna uma lista de lacaios presentes na área atual, vivos no progresso atual.
        Cada lacaio vem com seu estado básico. Habilidades e itens devem ser buscados separadamente.
        """
        consulta = """
            SELECT 
                il.identificador_instancia_lacaio,
                eil.vida_atual,
                il.moedas_totais,
                il.coordenada_x AS x,
                il.coordenada_y AS y,

                l.identificador_lacaio,
                TRIM(l.nome) AS nome_lacaio,
                TRIM(l.descricao) AS descricao_lacaio,
                l.vida AS vida_total,
                l.nivel,
                l.experiencia

            FROM instancia_lacaio il
            JOIN estado_instancia_lacaio eil 
                ON eil.identificador_instancia_lacaio = il.identificador_instancia_lacaio
            AND eil.identificador_progresso = %s
            JOIN lacaio l ON il.identificador_lacaio = l.identificador_lacaio
            WHERE eil.identificador_area_atual = %s
            AND eil.data_da_morte IS NULL;
        """
        return self.executar_query(consulta, (identificador_progresso, identificador_area), fetchall=True)

    def buscar_chefe(self, id_chefe):
        """
        Ver atributos de um chefe específico.
        Similar a buscar_lacaio.
        """
        consulta = """
            SELECT nome, dano, vida, nivel, experiencia
            FROM chefe
            WHERE id_chefe = %s;
        """
        return self.executar_query(consulta, (id_chefe,), fetchone=True)

    def buscar_aliado(self, id_aliado):
        """
        Ver atributos de um aliado específico.
        """
        consulta = """
            SELECT nome, vida, nivel, vida_atual, dano_base
            FROM aliado
            WHERE id_aliado = %s;
        """
        return self.executar_query(consulta, (id_aliado,), fetchone=True)

    def buscar_habitante(self, id_habitante):
        """Busca dados de um habitante pelo ID."""
        consulta = """
            SELECT nome, tipo, especialidade, coordenada_x, coordenada_y
            FROM habitante
            WHERE id_habitante = %s;
        """
        return self.executar_query(consulta, (id_habitante,), fetchone=True)
    
    def buscar_habitante_por_area(self, id_area):
        """Busca dados de todos os habitante de uma área específica."""
        consulta = """
            SELECT
                identificador_habitante,
                identificador_area,
                TRIM(nome) AS nome,
                TRIM(descricao) AS descricao,
                TRIM(chave_imagem) AS chave_imagem,
                tipo_habitante,
                coordenada_x,
                coordenada_y,
                especialidade,
                moedas_totais
                FROM habitante
                WHERE identificador_area = %s;
        """
        return self.executar_query(consulta, (id_area,), fetchall=True)
    
    def buscar_habitante_por_ilha(self, id_ilha):
        """Busca dados de todos os habitante de uma ilha específica."""
        consulta = """
            SELECT h.*
                FROM habitante h
                JOIN area a ON h.identificador_area = a.identificador_area
                WHERE a.identificador_ilha = %s;
        """
        return self.executar_query(consulta, (id_ilha,), fetchall=True)
    
    def buscar_habilidades_por_personagem(self, identificador_personagem):
        """
        Retorna todas as habilidades associadas a um personagem (jogador, aliado, lacaio etc).
        """
        consulta = """
            SELECT 
                h.identificador_habilidade,
                TRIM(h.nome) AS nome_habilidade,
                h.dano,
                h.tipo_de_ataque,
                h.tipo_de_alvo
            FROM habilidade_personagem hp
            JOIN habilidade h ON h.identificador_habilidade = hp.identificador_habilidade
            WHERE hp.identificador_personagem = %s;
        """
        return self.executar_query(consulta, (identificador_personagem,), fetchall=True)
    
    def buscar_lacaio_com_habilidades_por_nome(self, nome_lacaio):
        """
        Busca os dados de um lacaio pelo nome (não instância) e retorna suas habilidades.
        
        :param nome_lacaio: Nome do lacaio (exato)
        :return: Lista de tuplas com dados do lacaio + habilidades (uma linha por habilidade)
        """
        consulta = """
            SELECT
                l.identificador_lacaio,
                TRIM(l.nome) AS nome_lacaio,
                TRIM(l.descricao) AS descricao,
                l.vida,
                l.nivel,
                l.experiencia,
                h.identificador_habilidade,
                TRIM(h.nome) AS nome_habilidade,
                h.dano,
                h.tipo_de_ataque,
                h.tipo_de_alvo
            FROM lacaio l
            LEFT JOIN habilidade_personagem hp ON hp.identificador_personagem = l.identificador_lacaio
            LEFT JOIN habilidade h ON h.identificador_habilidade = hp.identificador_habilidade
            WHERE TRIM(l.nome) = %s;
        """
        return self.executar_query(consulta, (nome_lacaio,), fetchall=True)


    def matar_inimigos_da_area(self, id_area_origem):
        """
        Marca como mortos todos os lacaios vivos da área especificada,
        e os move para a área 'are0034'.

        :param id_area_origem: ID da área onde os lacaios estão atualmente
        """
        consulta = """
            UPDATE estado_instancia_lacaio
            SET 
                data_da_morte = now(),
                identificador_area_atual = 'are0034'
            WHERE 
                identificador_area_atual = %s
                AND data_da_morte IS NULL;
        """
        return self.executar_query(consulta, (id_area_origem,))



    # ===============================================
    # Métodos de Operações com Locais (Mapas, Ilhas, Salas)
    # ===============================================

    def buscar_info_ilha(self, id_ilha, identificador_progresso):
        """
         Retorna dados da ilha e se foi visitada no progresso atual.
        """
        consulta = """
            SELECT
                i.identificador_ilha,
                TRIM(i.nome) AS nome,
                iv.visitada
            FROM ilha i
            LEFT JOIN ilha_visitada iv
              ON i.identificador_ilha = iv.identificador_ilha AND iv.identificador_progresso = %s
            WHERE i.identificador_ilha = %s;
            """
        return self.executar_query(consulta, (identificador_progresso, id_ilha), fetchone=True)
    
    def buscar_caminhos_da_area(self, area):
        consulta = """
            SELECT TRIM(tipo_terreno) AS tipo_terreno, x, y, largura, altura
                FROM caminho
                WHERE identificador_area = %s;
            """
        return self.executar_query(consulta, (area,), fetchall=True)

    def buscar_obstaculos_da_area(self, area):
        consulta = """
            SELECT *
                FROM obstaculo
                WHERE identificador_area = %s;
            """
        return self.executar_query(consulta, (area,), fetchall=True)
    
    def buscar_info_area(self, id_area, id_progresso):
        """
        Busca informações de uma sala específica
        """
        consulta = """
            SELECT
                a.identificador_area,
                a.identificador_ilha,
                TRIM(a.nome) AS nome,
                TRIM(a.tipo_area) AS tipo_area,
                TRIM(a.chave_imagem_fundo) AS chave_imagem_fundo,
                TRIM(a.chave_imagem_frente) AS chave_imagem_frente,
                COALESCE(av.visitada, FALSE) AS visitada
            FROM area a
            LEFT JOIN area_visitada av
                ON a.identificador_area = av.identificador_area
            AND av.identificador_progresso = %s
            WHERE a.identificador_area = %s;

        """
        return self.executar_query(consulta, (id_progresso, id_area), fetchone=True)
    
    def buscar_porto_da_ilha(self, id_ilha, id_progresso):
        """
        Busca a área do tipo 'Porto' associada à ilha atual, considerando se já foi visitada no progresso atual.
        """
        consulta = """
            SELECT
                a.identificador_area,
                a.identificador_ilha,
                TRIM(a.nome) AS nome,
                TRIM(a.tipo_area) AS tipo_area,
                TRIM(a.chave_imagem_fundo) AS chave_imagem_fundo,
                TRIM(a.chave_imagem_frente) AS chave_imagem_frente,
                COALESCE(av.visitada, FALSE) AS visitada
            FROM area a
            LEFT JOIN area_visitada av
                ON av.identificador_area = a.identificador_area
            AND av.identificador_progresso = %s
            WHERE a.identificador_ilha = %s
            AND a.tipo_area = 'Porto';
        """
        return self.executar_query(consulta, (id_progresso, id_ilha), fetchone=True)

    
    def buscar_areas_interativas_da_area(self, id_area):
        """
        Busca todos os elementos espaciais do tipo 'Área interativa' da área atual (origem).
        """
        consulta = """
            SELECT
                identificador_area_interativa,
                identificador_area_origem AS area_origem,
                identificador_area_destino AS area_destino,
                identificador_missao,
                TRIM(chave_imagem) AS chave_imagem,
                x,
                y,
                largura,
                altura,
                chance_sucesso,
                TRIM(tipo_evento) AS tipo_evento,
                TRIM(metodo_ativacao) AS metodo_ativacao,
                ativa
            FROM area_interativa
            WHERE identificador_area_origem = %s;
        """
        return self.executar_query(consulta, (id_area,), fetchall=True)

    

    def inserir_gatilho_de_missao(self, id_area_origem, id_missao, x, y, largura, altura):
        """
        Insere uma nova área interativa no banco de dados.

        :param id_area_origem: ID da área onde a interação ocorre
        :param id_missao: ID da missão associada (ou None)
        :param x: Posição X da área
        :param y: Posição Y da área
        :param largura: Largura da área
        :param altura: Altura da área
        :return: ID da nova área interativa inserida
        """
        consulta = """
            INSERT INTO area_interativa
                (identificador_area_origem, identificador_missao, x, y, largura, altura, tipo_evento, metodo_ativacao)
            VALUES (%s, %s, %s, %s, %s, %s, 'missao', 'passivo')
            RETURNING identificador_area_interativa;
        """
        return self.executar_query(consulta, (id_area_origem, id_missao, x, y, largura, altura), fetchone=True)



    def remover_gatilho_de_missao(self, id_area_origem, id_missao, x, y, largura, altura):
        consulta = """
            WITH alvo AS (
                SELECT identificador_area_interativa
                FROM area_interativa
                WHERE
                    identificador_area_origem = %s
                    AND identificador_missao = %s
                    AND x = %s
                    AND y = %s
                    AND largura = %s
                    AND altura = %s
                    AND tipo_evento = 'missao'
                    AND metodo_ativacao = 'passivo'
                LIMIT 1
            )
            DELETE FROM area_interativa
            WHERE identificador_area_interativa IN (SELECT identificador_area_interativa FROM alvo);
        """
        self.executar_query(consulta, (id_area_origem, id_missao, x, y, largura, altura))




    def buscar_conexoes_ilha(self, id_ilha_origem, id_progresso):
        """
        Retorna as conexões da ilha atual com outras ilhas, considerando o progresso atual.
        """
        consulta = """
            SELECT
                i.identificador_ilha,
                TRIM(i.nome) AS nome,
                COALESCE(iv.visitada, FALSE) AS visitada,
                c.bloqueada
            FROM conexao_entre_ilhas c
            JOIN ilha i ON i.identificador_ilha =
                CASE
                    WHEN c.identificador_ilha_a = %s THEN c.identificador_ilha_b
                    ELSE c.identificador_ilha_a
                END
            LEFT JOIN ilha_visitada iv
                ON iv.identificador_ilha = i.identificador_ilha
            AND iv.identificador_progresso = %s
            WHERE %s IN (c.identificador_ilha_a, c.identificador_ilha_b)
            AND c.identificador_progresso = %s;
        """
        return self.executar_query(consulta, (id_ilha_origem, id_progresso, id_ilha_origem, id_progresso), fetchall=True)
   
    def buscar_conexao_entre_areas(self, id_area_origem, id_area_destino):
        """
        Busca a conexão entre duas áreas específicas 
        """
        consulta = """
            SELECT
                identificador_area_origem,
                identificador_area_destino,
                ponto_geracao_x,
                ponto_geracao_y,
                orientacao
            FROM conexao_entre_areas
            WHERE identificador_area_origem = %s
            AND identificador_area_destino = %s;
        """
        return self.executar_query(consulta, (id_area_origem, id_area_destino), fetchone=True)


    def buscar_pessoas_em_local(self, id_mapa, coord_x=None, coord_y=None):
        """
        Ver quais pessoas estão em um lugar X. (Adaptado para seu esquema)
        Considera jogadores, lacaios, chefes, aliados, habitantes no mapa.
        Se coord_x e coord_y são fornecidos, filtra por coordenadas.
        """
        query_parts = []
        params = [id_mapa]
        
        # Jogadores
        query_parts.append(
            "SELECT id_jogador AS id, nome, 'Jogador' AS tipo_entidade, coordenada_x, coordenada_y FROM jogador WHERE id_mapa = %s"
        )
        # Lacaios
        query_parts.append(
            "SELECT id_lacaio AS id, nome, 'Lacaio' AS tipo_entidade, coordenada_x, coordenada_y FROM lacaio WHERE id_mapa = %s"
        )
        # Chefes
        query_parts.append(
            "SELECT id_chefe AS id, nome, 'Chefe' AS tipo_entidade, coordenada_x, coordenada_y FROM chefe WHERE id_mapa = %s"
        )
        # Aliados
        query_parts.append(
            "SELECT id_aliado AS id, nome, 'Aliado' AS tipo_entidade, coordenada_x, coordenada_y FROM aliado WHERE id_mapa = %s"
        )
        # Habitantes
        query_parts.append(
            "SELECT id_habitante AS id, nome, 'Habitante' AS tipo_entidade, coordenada_x, coordenada_y FROM habitante WHERE id_mapa = %s"
        )
        
        # Adiciona o mapa_id para cada UNION ALL
        params = params * len(query_parts)

        final_query = " UNION ALL ".join(query_parts)
        
        if coord_x is not None and coord_y is not None:
            final_query += " WHERE coordenada_x = %s AND coordenada_y = %s"
            params.extend([coord_x, coord_y])

        final_query += " ORDER BY tipo_entidade, nome;"

        return self.executar_query(final_query, tuple(params), fetchall=True)


    def buscar_itens_em_local(self, id_mapa, tipo_sala=None, sala_id=None):
        """
        Ver quais itens estão em um lugar X. (Adaptado ao seu esquema)
        Seu esquema não tem uma tabela 'instancia_item' com FK para 'lugar'.
        Itens estão no inventário do jogador ou em entidades.
        Para adaptar, buscarei itens no inventário de jogadores e, por exemplo,
        itens que são 'item_chave' em um mapa.
        Isso é uma adaptação, pois seu esquema não liga itens a 'lugares' diretamente.
        Para uma ligação direta de itens a locais, precisaria de uma tabela 'item_no_chao'
        ou similar com uma FK para a sala/mapa.
        """
        # Exemplo adaptado: Contar itens chave por mapa.
        # Se você quiser "itens no chão" (world items), seu schema precisaria de uma tabela para isso.
        # Esta função mostra a quantidade de itens chave associados a um mapa.
        consulta = """
            SELECT m.id_mapa, m.total_item_chave
            FROM mapa m
            WHERE m.id_mapa = %s;
        """
        return self.executar_query(consulta, (id_mapa,), fetchall=True)
    
    # ===============================================
    # Métodos de Operações de Fabricação (Receitas)
    # ===============================================

    def buscar_fabricacao_especifica(self, id_receita):
        """
        Ver uma fabricação específica. (Adaptado para Receita)
        Retorna o consumível produzido e seus ingredientes.
        """
        consulta = """
            SELECT
                r.identificador_receita,
                cp.nome AS consumivel_produzido,
                'Consumível' AS tipo_ingrediente,
                ic.identificador_consumivel AS id_ingrediente,
                ing_c.nome AS nome_ingrediente
            FROM receita r
            JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
            LEFT JOIN ingrediente_consumivel ic ON r.identificador_receita = ic.identificador_receita
            LEFT JOIN consumivel ing_c ON ic.identificador_consumivel = ing_c.identificador_consumivel
            WHERE r.identificador_receita = %s
            UNION ALL
            SELECT
                r.identificador_receita,
                cp.nome AS consumivel_produzido,
                'Não-Consumível' AS tipo_ingrediente,
                inc.identificador_nao_consumivel AS id_ingrediente,
                ing_nc.nome AS nome_ingrediente
            FROM receita r
            JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
            LEFT JOIN ingrediente_nao_consumivel inc ON r.identificador_receita = inc.identificador_receita
            LEFT JOIN nao_consumivel ing_nc ON inc.identificador_nao_consumivel = ing_nc.identificador_nao_consumivel
            WHERE r.identificador_receita = %s;
        """
        return self.executar_query(consulta, (id_receita, id_receita), fetchall=True)

    def buscar_fabricacoes_por_ingrediente(self, id_item_ingrediente, tipo_item_ingrediente):
        """
        Ver fabricações possíveis com um item específico. (Adaptado para Receita e seus ingredientes)
        id_item_ingrediente pode ser identificador_consumivel ou identificador_nao_consumivel.
        tipo_item_ingrediente deve ser 'consumivel' ou 'nao_consumivel'.
        """
        query_base = """
            SELECT
                r.identificador_receita,
                cp.nome AS consumivel_produzido_nome,
                cp.identificador_consumivel AS consumivel_produzido_id
            FROM receita r
            JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
        """
        if tipo_item_ingrediente == 'consumivel':
            consulta = query_base + """
                JOIN ingrediente_consumivel ic ON r.identificador_receita = ic.identificador_receita
                WHERE ic.identificador_consumivel = %s;
            """
        elif tipo_item_ingrediente == 'nao_consumivel':
            consulta = query_base + """
                JOIN ingrediente_nao_consumivel inc ON r.identificador_receita = inc.identificador_receita
                WHERE inc.identificador_nao_consumivel = %s;
            """
        else:
            return None
        return self.executar_query(consulta, (id_item_ingrediente,), fetchall=True)

    def buscar_fabricacoes_por_jogador(self, id_jogador):
        """
        Ver todas as fabricações de um livro específico. (Adaptado para Receitas de um jogador)
        Assume que 'livro_fabricacao' do seu exemplo é similar a 'receitas aprendidas por jogador'.
        """
        consulta = """
            SELECT
                r.identificador_receita,
                cp.nome AS consumivel_produzido_nome
            FROM receita r
            JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
            WHERE r.id_jogador = %s;
        """
        return self.executar_query(consulta, (id_jogador,), fetchall=True)

    # ===============================================
    # Métodos de Operações com Missões
    # ===============================================
    def buscar_missoes_jogador(self, id_jogador):
        """Busca todas as missões associadas a um jogador."""
        consulta = """
            SELECT m.nome, m.descricao
            FROM missao m
            WHERE m.id_jogador = %s;
        """
        return self.executar_query(consulta, (id_jogador,), fetchall=True)
    
    def buscar_missoes_de_habitante_nao_concluidas(self, id_habitante, id_progresso):
        """
        Retorna todas as missões oferecidas por um habitante que ainda não foram concluídas
        por um determinado jogador (progresso).

        :param id_habitante: ID do habitante (recrutador)
        :param id_progresso: ID do progresso do jogador
        :return: Lista com (id_missao, nome, descricao, nivel_de_desbloqueio, id_area)
        """
        consulta = """
            SELECT
                m.identificador_missao,
                TRIM(m.nome) AS nome,
                TRIM(m.descricao) AS descricao,
                m.nivel_de_desbloqueio,
                m.identificador_area
            FROM missao m
            WHERE m.identificador_recrutador = %s
            AND m.identificador_missao NOT IN (
                SELECT em.identificador_missao
                FROM estado_missao em
                WHERE em.identificador_progresso = %s
                    AND em.estado = 'concluida'
            )
            ORDER BY m.nivel_de_desbloqueio, m.identificador_missao;
        """
        return self.executar_query(consulta, (id_habitante, id_progresso), fetchall=True)


    def buscar_item_recompensa_missao(self, missao_id):
        """
        Ver o item que uma missão X vai dar. (Adaptado para ItemMissao)
        Seu ItemMissao referencia TipoItem.
        """
        consulta = """
            SELECT
                im.identificador_item,
                ti.tipo AS tipo_geral
            FROM itemmissao im
            JOIN tipo_item ti ON im.identificador_item = ti.identificador_item
            WHERE im.missao_id = %s;
        """
        return self.executar_query(consulta, (missao_id,), fetchall=True)

    def buscar_local_missao(self, missao_id):
        """
        Ver o lugar que uma missão X está. (Adaptado para Sala de Missão)
        """
        consulta = """
            SELECT
                m.nome AS nome_missao,
                m.tipo_sala,
                m.sala_id,
                CASE
                    WHEN m.tipo_sala = 'campo_batalha' THEN cb.tamanho || ' - ' || cb.tipo_terreno
                    WHEN m.tipo_sala = 'porto' THEN 'Porto - ' || p.capacidade || ' barcos'
                    WHEN m.tipo_sala = 'vila' THEN 'Vila - ' || v.informacoes
                    ELSE 'Local desconhecido'
                END AS detalhes_local
            FROM missao m
            LEFT JOIN campo_batalha cb ON m.tipo_sala = 'campo_batalha' AND m.sala_id = cb.sala_id
            LEFT JOIN porto p ON m.tipo_sala = 'porto' AND m.sala_id = p.sala_id
            LEFT JOIN vila v ON m.tipo_sala = 'vila' AND m.sala_id = v.sala_id
            WHERE m.missao_id = %s;
        """
        return self.executar_query(consulta, (missao_id,), fetchone=True)

    def buscar_detalhes_missao(self, missao_id):
        """
        Ver o (nome, descrição) de uma missão específica.
        """
        consulta = """
            SELECT nome, descricao
            FROM missao
            WHERE missao_id = %s;
        """
        return self.executar_query(consulta, (missao_id,), fetchone=True)

    # ===============================================
    # Métodos de Operações com Tipos de Itens Específicos
    # ===============================================

    def buscar_arma_atributos(self, id_arma):
         consulta = """
            SELECT
                a.nome,
                a.raridade,
                a.preco_compra,
                a.preco_venda,
                h.nome AS habilidade_nome,
                h.dano AS dano_habilidade
            FROM arma a
            LEFT JOIN habilidade h ON a.identificador_habilidade = h.id_habilidade -- This is the correct JOIN for 'dano'
            WHERE a.identificador_arma = %s;
        """
         return self.executar_query(consulta, (id_arma,), fetchone=True)
    def buscar_consumivel_atributos(self, id_consumivel):
        """
        Ver os atributos de uma comida específica. (Adaptado para Consumivel)
        """
        consulta = """
            SELECT nome, tipo, raridade, quantidade, preco_compra, preco_venda, efabricavel
            FROM consumivel
            WHERE identificador_consumivel = %s;
        """
        return self.executar_query(consulta, (id_consumivel,), fetchone=True)

    def buscar_acessorio_atributos(self, id_acessorio):
        """
        Ver os atributos de um medicamento específico. (Adaptado para Acessorio)
        """
        consulta = """
            SELECT nome, tipo, raridade, preco_compra, preco_venda
            FROM acessorio
            WHERE identificador_acessorio = %s;
        """
        return self.executar_query(consulta, (id_acessorio,), fetchone=True)

    def buscar_nao_consumivel_atributos(self, id_nao_consumivel):
        """
        Ver os atributos de um utilizável específico. (Adaptado para Não-Consumível geral)
        """
        consulta = """
            SELECT nome, tipo, raridade, quantidade, preco_compra, preco_venda
            FROM nao_consumivel
            WHERE identificador_nao_consumivel = %s;
        """
        return self.executar_query(consulta, (id_nao_consumivel,), fetchone=True)

    def buscar_fruta_atributos(self, id_fruta):
        """
        Ver os atributos de uma fruta específica.
        """
        consulta = """
            SELECT f.nome, f.tipo, f.raridade, f.preco_compra, f.preco_venda, e.nome AS habilidade_nome, e.bravura
            FROM fruta f
            LEFT JOIN efeito e ON f.identificador_habilidade = e.identificador_efeito
            WHERE f.identificador_fruta = %s;
        """
        return self.executar_query(consulta, (id_fruta,), fetchone=True)

    # ===============================================
    # Outros (Inconsistências)
    # ===============================================
    def verificar_inconsistencia_inventario(self):
        """
        Comando usado para verificar inconsistências no tamanho_ocupado do inventário.
        Adaptado, pois seu schema não tem 'tamanho' para itens e 'inventario_ocupado' em Inventario.
        Isto é uma ADAPTAÇÃO conceitual para o seu schema.
        Vamos verificar se há itens no inventário que não têm um 'tipo' válido.
        """
        consulta = """
            SELECT ii.id_inventario, ii.identificador_item
            FROM iteminventario ii
            LEFT JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
            WHERE ti.identificador_item IS NULL; -- Busca itens no inventário que não têm um tipo correspondente
        """
        return self.executar_query(consulta, fetchall=True)

