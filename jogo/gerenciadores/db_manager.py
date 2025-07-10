
import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import namedtuple_row
from utilidades.constantes import *
from entidades.item_inventario import ItemInventario
from entidades.mochila import Mochila
from entidades.kit import KitDoExplorador

import random

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

    def executar_query(self, query, params=None, fetchone=False, fetchall=False, erro_no_rollback=True):
        """
        Executa uma query SQL no banco de dados.
        :param query: A string SQL a ser executada.
        :param params: Uma tupla ou lista de parâmetros para a query (para evitar SQL Injection).
        :param fetchone: Se True, retorna apenas uma linha.
        :param fetchall: Se True, retorna todas as linhas.
        :return: Resultados da query (se for SELECT), True para sucesso, False para falha.
        """
        if not self.conn:
            print("DBManager ERRO: Não há conexão ativa com o banco de dados.")
            return False

        try:
            self.cursor.execute(query, params)
            if fetchone:
                return self.cursor.fetchone()
            elif fetchall:
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return True
        except psycopg.Error as e:
            if erro_no_rollback:
                self.conn.rollback()
            print(f"DBManager ERRO ao executar query '{query}': {e}")
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

        # 5) Retorna dados carregados já prontos
        return self.carregar_dados_do_progresso(id_jogador, id_progresso)



    def carregar_dados_do_progresso(self, id_jogador, identificador_progresso):
        """
        Retorna uma tupla com os dados do jogador, da área atual e dos inimigos na área (se houver arena).
        :return: (jogador, area, inimigos ou None)
        """

        jogador = self.buscar_jogador(id_jogador)
        if not jogador:
            return None, None, None

        mochila = self.carregar_mochila_do_jogador(id_jogador, identificador_progresso)
        kit_jogador = self.carregar_kit_do_jogador(id_jogador)

        area = self.buscar_info_area(jogador.identificador_area, identificador_progresso)

        ilha = self.buscar_info_ilha(area.identificador_ilha, identificador_progresso)

        identificador_inventario = self.buscar_id_inventario(id_jogador, 'moc', identificador_progresso)

        #print(f"Jogador: {jogador.nome}, Área: {area.nome}, Ilha: {ilha.nome if ilha else 'N/A'}")
        return jogador, mochila, kit_jogador, ilha, area, identificador_inventario
    
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

    def carregar_mochila_do_jogador(self, id_jogador, id_progresso):
        resultados = self.buscar_inventario(id_jogador, 'moc', id_progresso)
        mochila = Mochila()

        for row in resultados:
            item = ItemInventario(
                id_item=row.identificador_item,
                nome=row.nome_item,
                descricao=row.descricao,
                tipo=row.tipo_item,
                raridade=row.raridade,
                quantidade=row.quantidade
            )

            efeitos = self.buscar_efeitos_por_item(row.identificador_item)
            for efeito in efeitos:
                item.adicionar_efeito(efeito.efeito_nome, efeito.efeito_valor)

            mochila.adicionar(item)

        return mochila


    def carregar_kit_do_jogador(self, id_jogador):
        resultado_kit = self.buscar_kit_do_explorador(id_jogador, 'kit')
        kit = KitDoExplorador(resultado_kit[0].identificador_inventario)  # Supondo que você tenha uma classe Kit com add_arma, add_fruta, etc.
        print(resultado_kit)
        for row in resultado_kit:
            item = ItemInventario(
                id_item=row.identificador_item,
                nome=row.nome_item,
                descricao=row.descricao,
                tipo=row.tipo_item,
                raridade=row.raridade,
                quantidade=row.quantidade
            )
            efeitos = self.buscar_efeitos_por_item(row.identificador_item)
            for efeito in efeitos:
                item.adicionar_efeito(efeito.efeito_nome, efeito.efeito_valor)

            kit.equipar(item)  # ou separar por tipo, dependendo da implementação

        return kit

    def equipar_item_no_kit(self, identificador_jogador, identificador_item, tipo_item, identificador_progresso):
        """
        Move um item da mochila para o kit, substituindo o anterior (se houver).
        Itens possíveis: arma, fruta, acessório.
        Tudo feito dentro de uma transação.
        """
        if tipo_item not in ("arma", "fruta", "acessorio"):
            print(f"[ERRO] Tipo de item inválido para equipar: {tipo_item}")
            return False

        try:
            with self.conn.transaction():
                # 1. Buscar inventários
                id_kit = self.buscar_id_inventario(identificador_jogador, 'kit', identificador_progresso)
                id_mochila = self.buscar_id_inventario(identificador_jogador, 'moc', identificador_progresso)

                # 2. Verificar se já existe item do mesmo tipo no kit
                query_busca_existente = f"""
                    SELECT identificador_item, quantidade
                    FROM item_inventario
                    JOIN tipo_item USING (identificador_item)
                    WHERE identificador_inventario = %s AND tipo_item.tipo = %s;
                """
                existente = self.executar_query(query_busca_existente, (id_kit, tipo_item), fetchone=True)

                # 3. Se houver, mover do kit para mochila
                if existente:
                    id_antigo = existente.identificador_item
                    qtd_antiga = existente.quantidade

                    # Remover do kit
                    self.executar_query("""
                        DELETE FROM item_inventario
                        WHERE identificador_inventario = %s AND identificador_item = %s;
                    """, (id_kit, id_antigo))

                    # Adicionar na mochila
                    self.executar_query("""
                        INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (identificador_inventario, identificador_item)
                        DO UPDATE SET quantidade = item_inventario.quantidade + EXCLUDED.quantidade;
                    """, (id_mochila, id_antigo, qtd_antiga))

                # 4. Remover item da mochila
                self.remover_item_do_inventario_personagem(id_mochila, identificador_item, quantidade=1)

                # 5. Adicionar item ao kit
                self.executar_query("""
                    INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
                    VALUES (%s, %s, 1)
                    ON CONFLICT (identificador_inventario, identificador_item)
                    DO UPDATE SET quantidade = 1; -- garante que fique como 1
                """, (id_kit, identificador_item))

                return True

        except Exception as e:
            print(f"[ERRO ao equipar item no kit] {e}")
            self.conn.rollback()
            return False

    def buscar_id_inventario(self, identificador_personagem, tipo_inventario, identificador_progresso):
        query = """
            SELECT identificador_inventario
            FROM inventario
            WHERE identificador_personagem = %s AND tipo_inventario = %s AND identificador_progresso = %s
        """
        resultado = self.executar_query(query, (identificador_personagem, tipo_inventario, identificador_progresso), fetchone=True)
        return resultado.identificador_inventario if resultado else None

    def sekishiki_meikai_ha(self, id_inimigo, identificador_progresso):
        """
        Envia um inimigo para o Yomotsu Hirasaka.
        """
        consulta = """
            UPDATE estado_instancia_lacaio
            SET 
                data_da_morte = now(),
                identificador_area_atual = 'are034'
            WHERE 
                identificador_instancia_lacaio = %s
                AND identificador_progresso = %s
                AND data_da_morte IS NULL;
        """
        return self.executar_query(consulta, (id_inimigo, identificador_progresso))


    # ===============================================
    # Métodos de Operações com Jogador
    # ===============================================
    def buscar_jogador(self, id_jogador):
        """Busca os dados de um jogador pelo ID."""
        query = """
            SELECT
                identificador_jogador,
                identificador_area,
                identificador_progresso,
                TRIM(nome) AS nome,
                TRIM(descricao) AS descricao,
                coordenada_x,
                coordenada_y,
                energia AS energia_maxima,
                vida AS vida_maxima,
                nivel,
                sorte,
                energia_atual,
                vida_atual,
                experiencia_atual,
                moedas_totais
            FROM jogador
            WHERE identificador_jogador = %s;
        """
        return self.executar_query(query, (id_jogador,), fetchone=True)

    def atualizar_jogador(self, id_jogador, energia, vida_atual, nivel, experiencia_atual, coord_x, coord_y, id_mapa):
        """Atualiza os dados de um jogador."""
        query = """
            UPDATE jogador
            SET energia = %s, vida_atual = %s, nivel = %s, experiencia_atual = %s,
                coordenada_x = %s, coordenada_y = %s, id_mapa = %s
            WHERE id_jogador = %s;
        """
        params = (energia, vida_atual, nivel, experiencia_atual, coord_x, coord_y, id_mapa, id_jogador)
        return self.executar_query(query, params)
    
    def atualizar_posicao_jogador(self, identificador_jogador, identificador_area, coordenada_x, coordenada_y):
        """Atualiza a posição do jogador"""
        consulta = """
            UPDATE jogador
                SET identificador_area = %s, coordenada_x = %s, coordenada_y = %s
                WHERE identificador_jogador = %s;
        """
        return self.executar_query(consulta, (identificador_area, coordenada_x, coordenada_y, identificador_jogador))

    def atualizar_atributos_de_batalha_do_jogador(self, identificador_jogador, energia_maxima, vida_maxima, nivel,
                                                   sorte, energia_atual, vida_atual,
                                                   experiencia_atual, moedas_totais):
        """
        Atualiza apenas os atributos relevantes de batalha do jogador.
        """
        query = """
            UPDATE jogador
            SET energia = %s,
                vida = %s,
                nivel = %s,
                sorte = %s,
                energia_atual = %s,
                vida_atual = %s,
                experiencia_atual = %s,
                moedas_totais = %s
            WHERE identificador_jogador = %s;
        """
        params = (
            energia_maxima, vida_maxima, nivel, sorte,
            energia_atual, vida_atual, experiencia_atual, moedas_totais,
            identificador_jogador
        )
        return self.executar_query(query, params)

    

    def salvar_novo_jogador(self, nome, descricao, identificador_progresso):
        """Insere um novo jogador no banco de dados e retorna o ID gerado."""
        query = """
            INSERT INTO jogador
                (identificador_area, identificador_progresso, nome, descricao, coordenada_x, coordenada_y,
                energia, vida, nivel, sorte, vida_atual, experiencia_atual, moedas_totais)
            VALUES
                ('are001', %s, %s, %s, 1950, 140, 5, 10, 0, 1, 10, 0, 0)
            RETURNING identificador_jogador;
        """
        return self.executar_query(query, (identificador_progresso, nome, descricao), fetchone=True)[0]

    def salvar_novo_aliado(self, nome, descricao, identificador_progresso):
        """Insere um novo aliado no banco de dados e retorna o ID gerado."""
        query = """
            INSERT INTO aliado
                (identificador_area, identificador_progresso, nome, descricao, coordenada_x, coordenada_y, vida, nivel, vida_atual)
            VALUES
                ('are016', %s, %s, %s, 460, 315, 40, 30, 40)
            RETURNING identificador_aliado;
        """
        return self.executar_query(query, (identificador_progresso, nome, descricao), fetchone=True)[0]

    
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

    
    def buscar_dialogos_sem_missao(self, id_personagem):
        """
        Retorna todos os diálogos de um personagem específico que não estão associados a nenhuma missão (identificador_missao IS NULL).
        :param id_personagem: ID do personagem (jogador, aliado, etc)
        :return: Lista de tuplas com (identificador_dialogo, sequencia_local, genero, dialogo)
        """
        consulta = """
            SELECT 
                identificador_dialogo,
                sequencia_local,
                genero,
                TRIM(dialogo) AS dialogo
            FROM dialogo
            WHERE identificador_personagem = %s
            AND identificador_missao IS NULL
            ORDER BY sequencia_local;
        """
        return self.executar_query(consulta, (id_personagem,), fetchall=True)


    def buscar_missoes_aceitas_do_jogador(self, id_jogador):
        """
        Retorna todas as missões aceitas atualmente pelo jogador.
        :param id_jogador: ID do jogador
        :return: Lista com (identificador_missao, nome, descricao, nivel_de_desbloqueio)
        """
        consulta = """
            SELECT 
                m.identificador_missao,
                TRIM(m.nome) AS nome,
                TRIM(m.descricao) AS descricao,
                m.nivel_de_desbloqueio
            FROM jogador j
            JOIN estado_missao em ON em.identificador_progresso = j.identificador_progresso
            JOIN missao m ON m.identificador_missao = em.identificador_missao
            WHERE j.identificador_jogador = %s
            AND em.estado = 'aceita'
            ORDER BY m.nivel_de_desbloqueio, m.nome;
        """
        return self.executar_query(consulta, (id_jogador,), fetchall=True)


    def buscar_dialogos_da_missao(self, id_missao, genero_jogador):
        """
        Retorna todos os diálogos de uma missão específica, incluindo falas sem personagem definido.
        Se identificador_personagem for NULL, o nome será '???'.
        
        :param id_missao: ID da missão (ex: 'mis011')
        :param genero_jogador: 'F' para Silvie, 'M' para Shuan
        :return: Lista com (identificador_dialogo, nome_personagem, sequencia_local, dialogo)
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
            ORDER BY dialogo.sequencia_local;
        """
        return self.executar_query(consulta, (id_missao, genero_jogador), fetchall=True)

    
    # ===============================================
    # Métodos de Operações com Inventário e Itens
    # ===============================================

    def buscar_kit_do_explorador(self, identificador_jogador, tipo_inventario='kit'):
        """Busca o inventário do kit do explorador de um jogador."""
        query = """
            SELECT
                inventario.identificador_inventario,
                tipo_item.identificador_item,
                tipo_item.tipo AS tipo_item,
                COALESCE(
                    TRIM(acessorio.nome),
                    TRIM(fruta.nome),
                    TRIM(arma.nome)
                ) AS nome_item,
                COALESCE(
                    TRIM(acessorio.raridade),
                    TRIM(fruta.raridade),
                    TRIM(arma.raridade)
                ) AS raridade,
                COALESCE(
                    TRIM(acessorio.descricao),
                    TRIM(fruta.descricao),
                    TRIM(arma.descricao)
                ) AS descricao,
                COALESCE(arma.tipo_arma, '') AS tipo_arma,
                item_inventario.quantidade
            FROM inventario
            LEFT JOIN item_inventario
                ON item_inventario.identificador_inventario = inventario.identificador_inventario
            LEFT JOIN tipo_item
                ON tipo_item.identificador_item = item_inventario.identificador_item

            -- Joins para cada subtipo
            LEFT JOIN acessorio
                ON acessorio.identificador_acessorio = tipo_item.identificador_item
            LEFT JOIN fruta
                ON fruta.identificador_fruta = tipo_item.identificador_item
            LEFT JOIN arma
                ON arma.identificador_arma = tipo_item.identificador_item

			WHERE inventario.identificador_personagem = %s
            AND inventario.tipo_inventario = %s;
        """
        return self.executar_query(query, (identificador_jogador, tipo_inventario), fetchall=True)
        
    def buscar_inventario(self, identificador_personagem, tipo_inventario='moc', identificador_progresso=None):
        """Acessa o inventário de um personagem e seus atributos, filtrando também por progresso."""
        query = """
            SELECT
                inventario.identificador_inventario,
                tipo_item.identificador_item,
                tipo_item.tipo AS tipo_item,
                COALESCE(
                    TRIM(acessorio.nome),
                    TRIM(fruta.nome),
                    TRIM(consumivel.nome),
                    TRIM(nao_consumivel.nome),
                    TRIM(arma.nome)
                ) AS nome_item,
                COALESCE(
                    TRIM(acessorio.raridade),
                    TRIM(fruta.raridade),
                    TRIM(consumivel.raridade),
                    TRIM(nao_consumivel.raridade),
                    TRIM(arma.raridade)
                ) AS raridade,
                COALESCE(
                    TRIM(acessorio.descricao),
                    TRIM(fruta.descricao),
                    TRIM(consumivel.descricao),
                    TRIM(nao_consumivel.descricao),
                    TRIM(arma.descricao)
                ) AS descricao,
                item_inventario.quantidade
            FROM inventario
            LEFT JOIN item_inventario
                ON item_inventario.identificador_inventario = inventario.identificador_inventario
            LEFT JOIN tipo_item
                ON tipo_item.identificador_item = item_inventario.identificador_item

            -- Joins para cada subtipo
            LEFT JOIN acessorio
                ON acessorio.identificador_acessorio = tipo_item.identificador_item
            LEFT JOIN fruta
                ON fruta.identificador_fruta = tipo_item.identificador_item
            LEFT JOIN consumivel
                ON consumivel.identificador_consumivel = tipo_item.identificador_item
            LEFT JOIN nao_consumivel
                ON nao_consumivel.identificador_nao_consumivel = tipo_item.identificador_item
			LEFT JOIN arma
				ON arma.identificador_arma = tipo_item.identificador_item
            
            WHERE inventario.identificador_personagem = %s
            AND inventario.tipo_inventario = %s
            AND inventario.identificador_progresso = %s;
        """
        return self.executar_query(query, (identificador_personagem, tipo_inventario, identificador_progresso), fetchall=True)



    def criar_inventario(self, id_jogador, id_progresso, tipo_inventario='moc'):
        """Cria um novo inventário para um jogador e retorna o ID do inventário."""
        query = """
            INSERT INTO inventario (identificador_personagem, identificador_progresso, tipo_inventario)
            VALUES (%s, %s, %s)
            RETURNING identificador_inventario;
        """
        self.executar_query(query, (id_jogador, id_progresso, tipo_inventario), fetchone=True)

    def buscar_itens_no_inventario(self, id_inventario):
        """
        Ver os tipos de itens no inventário de um jogador.
        Retorna (identificador_item, tipo_item.tipo, nome_do_item_base_no_nao_consumivel/consumivel).
        Adaptado à modelagem atual do seu banco de dados onde ItemInventario referencia TipoItem.
        Os nomes detalhados (ex: "Maçã Lustrosa") não podem ser obtidos diretamente por aqui
        se o ItemInventario só armazena o ID do TIPO de item.
        """
        query = """
            SELECT
                ii.identificador_item,
                ti.tipo AS tipo_geral
            FROM iteminventario ii
            JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
            WHERE ii.id_inventario = %s
            ORDER BY ti.tipo; -- Ordena para melhor visualização
        """
        return self.executar_query(query, (id_inventario,), fetchall=True)

    def adicionar_item_ao_inventario(self, identificador_inventario, identificador_item, quantidade=1):
        """
        Adiciona um item específico ao inventário de um personagem.
        Se o item já existir, incrementa a quantidade.
        """
        consulta = """
            INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
            VALUES (%s, %s, %s)
            ON CONFLICT (identificador_inventario, identificador_item)
            DO UPDATE SET quantidade = item_inventario.quantidade + EXCLUDED.quantidade;
        """
        return self.executar_query(consulta, (identificador_inventario, identificador_item, quantidade))



    def remover_item_do_inventario(self, identificador_inventario, identificador_item, quantidade=1):
        """
        Reduz a quantidade de um item do inventário. Remove o item se a quantidade chegar a 0 ou menos.
        """
        # Primeiro, verificar a quantidade atual
        consulta_quantidade = """
            SELECT quantidade FROM item_inventario
            WHERE identificador_inventario = %s AND identificador_item = %s;
        """
        resultado = self.executar_query(consulta_quantidade, (identificador_inventario, identificador_item), fetchone=True)

        if not resultado:
            print(f"[AVISO] Item {identificador_item} não encontrado no inventário {identificador_inventario}.")
            return False

        quantidade_atual = resultado.quantidade

        if quantidade_atual > quantidade:
            # Apenas reduzir a quantidade
            consulta_update = """
                UPDATE item_inventario
                SET quantidade = quantidade - %s
                WHERE identificador_inventario = %s AND identificador_item = %s;
            """
            return self.executar_query(consulta_update, (quantidade, identificador_inventario, identificador_item))

        else:
            # Remover o item completamente
            consulta_delete = """
                DELETE FROM item_inventario
                WHERE identificador_inventario = %s AND identificador_item = %s;
            """
            return self.executar_query(consulta_delete, (identificador_inventario, identificador_item))

    
    def buscar_item_por_tipo_id(self, id_tipo_item):
        """
        Busca o tipo de um item específico na tabela tipo_item.
        Exemplo: SELECT tipo FROM item WHERE id = 1;
        """
        query = """
            SELECT tipo
            FROM tipo_item
            WHERE identificador_item = %s;
        """
        return self.executar_query(query, (id_tipo_item,), fetchone=True)
    
    def buscar_efeitos_por_item(self, id_item):
        query = """
            SELECT TRIM(efeito.nome) AS efeito_nome, efeito.valor AS efeito_valor
            FROM efeito
                JOIN efeito_consumivel ON efeito_consumivel.identificador_efeito = efeito.identificador_efeito
            WHERE efeito_consumivel.identificador_consumivel = %s;
        """
        return self.executar_query(query, (id_item,), fetchall=True)
    
    def buscar_efeito_por_acessorio(self, id_acessorio):
        """
        Busca os efeitos associados a um acessório específico.
        Exemplo: SELECT TRIM(efeito.nome) AS efeito_nome, efeito.valor AS efeito_valor FROM efeito WHERE identificador_acessorio = 1;
        """
        query = """
            SELECT TRIM(efeito.nome) AS efeito_nome, efeito.valor AS efeito_valor
            FROM efeito
                JOIN efeito_acessorio ON efeito_acessorio.identificador_efeito = efeito.identificador_efeito
            WHERE efeito_acessorio.identificador_acessorio = %s;
        """
        return self.executar_query(query, (id_acessorio,), fetchall=True)


    # ===============================================
    # Métodos de Operações com Personagens (Lacaio, Chefe, Aliado, Habitante)
    # ===============================================

    def buscar_tipo_personagem(self, id_personagem):
        """
        Ver o tipo de uma pessoa (Personagem).
        Adaptado de: SELECT tipo FROM pessoa WHERE id = 3;
        """
        query = """
            SELECT tipo
            FROM tipo_personagem
            WHERE id_personagem = %s;
        """
        return self.executar_query(query, (id_personagem,), fetchone=True)

    def buscar_lacaio(self, id_lacaio):
        """
        Ver atributos de um lacaio específico.
        Exemplo: SELECT habilidade_briga, vida, forca FROM prisioneiro WHERE id = 3;
        (Adaptado para lacaio)
        """
        query = """
            SELECT nome, dano, vida, nivel, experiencia
            FROM lacaio
            WHERE id_lacaio = %s;
        """
        return self.executar_query(query, (id_lacaio,), fetchone=True)
    
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

    def buscar_item_do_lacaio(self, identificador_lacaio):
        """
        Busca os itens que um lacaio específico possui.
        """
        consulta = """
            SELECT
                item_inventario.identificador_item,
                item_inventario.quantidade
        
            FROM inventario
                JOIN item_inventario ON item_inventario.identificador_inventario = inventario.identificador_inventario
             WHERE identificador_personagem = %s;
            """
        return self.executar_query(consulta, (identificador_lacaio,), fetchone=True)

    def buscar_chefe(self, id_chefe):
        """
        Ver atributos de um chefe específico.
        Similar a buscar_lacaio.
        """
        query = """
            SELECT nome, dano, vida, nivel, experiencia
            FROM chefe
            WHERE id_chefe = %s;
        """
        return self.executar_query(query, (id_chefe,), fetchone=True)

    def buscar_aliado(self, id_aliado):
        """
        Ver atributos de um aliado específico.
        """
        query = """
            SELECT nome, vida, nivel, vida_atual, dano_base
            FROM aliado
            WHERE id_aliado = %s;
        """
        return self.executar_query(query, (id_aliado,), fetchone=True)

    def buscar_habitante(self, id_habitante):
        """Busca dados de um habitante pelo ID."""
        query = """
            SELECT nome, tipo, especialidade, coordenada_x, coordenada_y
            FROM habitante
            WHERE id_habitante = %s;
        """
        return self.executar_query(query, (id_habitante,), fetchone=True)
    
    def buscar_habitante_por_area(self, id_area):
        """Busca dados de todos os habitante de uma área específica."""
        query = """
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
        return self.executar_query(query, (id_area,), fetchall=True)
    
    def buscar_habitante_por_ilha(self, id_ilha):
        """Busca dados de todos os habitante de uma ilha específica."""
        query = """
            SELECT h.*
                FROM habitante h
                JOIN area a ON h.identificador_area = a.identificador_area
                WHERE a.identificador_ilha = %s;
        """
        return self.executar_query(query, (id_ilha,), fetchall=True)
    
    def buscar_habilidades_por_personagem(self, identificador_personagem):
        """
        Retorna todas as habilidades associadas a um personagem (jogador, aliado, lacaio etc).
        """
        consulta = """
            SELECT
                habilidade.identificador_habilidade,
                TRIM(habilidade.nome) AS nome,
                TRIM(habilidade.descricao) AS descricao,
                TRIM(habilidade.tipo_de_ataque) AS tipo_de_ataque,
                TRIM(habilidade.tipo_de_alvo) AS tipo_de_alvo,
                habilidade.dano,
                habilidade.custo,
                TRIM(efeito.nome) AS efeito_nome,
                efeito.valor AS efeito_valor
            FROM habilidade_personagem
                JOIN habilidade   ON  habilidade.identificador_habilidade = habilidade_personagem.identificador_habilidade
                LEFT JOIN efeito  ON  efeito.identificador_efeito = habilidade.identificador_efeito
            WHERE habilidade_personagem.identificador_personagem = %s;
        """
        return self.executar_query(consulta, (identificador_personagem,), fetchall=True)
    


    # ===============================================
    # Métodos de Operações com Locais (Mapas, Ilhas, Salas)
    # ===============================================

    def buscar_info_ilha(self, id_ilha, identificador_progresso):
        """
         Retorna dados da ilha e se foi visitada no progresso atual.
        """
        query = """
            SELECT
                i.identificador_ilha,
                TRIM(i.nome) AS nome,
                iv.visitada
            FROM ilha i
            LEFT JOIN ilha_visitada iv
              ON i.identificador_ilha = iv.identificador_ilha AND iv.identificador_progresso = %s
            WHERE i.identificador_ilha = %s;
            """
        return self.executar_query(query, (identificador_progresso, id_ilha), fetchone=True)
    
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
        query = """
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
        return self.executar_query(query, (id_progresso, id_area), fetchone=True)
    
    def buscar_porto_da_ilha(self, id_ilha, id_progresso):
        """
        Busca a área do tipo 'Porto' associada à ilha atual, considerando se já foi visitada no progresso atual.
        """
        query = """
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
        return self.executar_query(query, (id_progresso, id_ilha), fetchone=True)

    
    def buscar_areas_interativas_da_area(self, id_area):
        """
        Busca todos os elementos espaciais do tipo 'Área interativa' da área atual (origem).
        """
        consulta = """
            SELECT
                identificador_area_interativa AS identificador,
                identificador_area_origem AS area_origem,
                identificador_area_destino AS area_destino,
                TRIM(chave_imagem) AS chave_imagem,
                x,
                y,
                largura,
                altura,
                chance_sucesso,
                TRIM(tipo_evento) AS tipo_evento
            FROM area_interativa
            WHERE identificador_area_origem = %s;
        """
        return self.executar_query(consulta, (id_area,), fetchall=True)

    


    def buscar_conexoes_ilha(self, id_ilha_origem, id_progresso):
        """
        Retorna as conexões da ilha atual com outras ilhas, considerando o progresso atual.
        """
        query = """
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
        return self.executar_query(query, (id_ilha_origem, id_progresso, id_ilha_origem, id_progresso), fetchall=True)
   
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

    def buscar_ponto_de_renascimento(self, id_area_destino):
        """
        Retorna uma conexão onde a área de destino é a área atual (ou seja, uma conexão que leva PARA essa área).
        """
        consulta = """
            SELECT
                ponto_geracao_x AS x,
                ponto_geracao_y AS y
            FROM conexao_entre_areas
            WHERE identificador_area_destino = %s
            LIMIT 1;
        """
        return self.executar_query(consulta, (id_area_destino,), fetchone=True)


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
        query = """
            SELECT m.id_mapa, m.total_item_chave
            FROM mapa m
            WHERE m.id_mapa = %s;
        """
        return self.executar_query(query, (id_mapa,), fetchall=True)
    
    def buscar_itens_na_ilha(self, id_ilha, tipo='consumivel'):
        """
        Busca todos os itens coletáveis de um tipo ('consumivel' ou 'nao_consumivel') disponíveis na ilha.
        Compara o campo local_encontrado com o nome da ilha, e exige que e_coletado seja TRUE.
        """
        if tipo == 'consumivel':
            query = """
                SELECT
                    c.identificador_consumivel AS identificador_item,
                    TRIM(c.nome) AS nome_item
                FROM consumivel c
                JOIN ilha i ON c.local_encontrado = i.nome
                WHERE i.identificador_ilha = %s
                AND c.e_coletado = TRUE;
            """
        else:
            query = """
                SELECT
                    nc.identificador_nao_consumivel AS identificador_item,
                    TRIM(nc.nome) AS nome_item
                FROM nao_consumivel nc
                JOIN ilha i ON nc.local_encontrado = i.nome
                WHERE i.identificador_ilha = %s
                AND nc.e_coletado = TRUE;
            """
        return self.executar_query(query, (id_ilha,), fetchall=True)


    # ===============================================
    # Métodos de Operações de Fabricação (Receitas)
    # ===============================================

    def buscar_fabricacao_especifica(self, id_receita):
        """
        Ver uma fabricação específica. (Adaptado para Receita)
        Retorna o consumível produzido e seus ingredientes.
        """
        query = """
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
        return self.executar_query(query, (id_receita, id_receita), fetchall=True)

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
            query = query_base + """
                JOIN ingrediente_consumivel ic ON r.identificador_receita = ic.identificador_receita
                WHERE ic.identificador_consumivel = %s;
            """
        elif tipo_item_ingrediente == 'nao_consumivel':
            query = query_base + """
                JOIN ingrediente_nao_consumivel inc ON r.identificador_receita = inc.identificador_receita
                WHERE inc.identificador_nao_consumivel = %s;
            """
        else:
            return None
        return self.executar_query(query, (id_item_ingrediente,), fetchall=True)

    def buscar_fabricacoes_por_jogador(self, id_jogador):
        """
        Ver todas as fabricações de um livro específico. (Adaptado para Receitas de um jogador)
        Assume que 'livro_fabricacao' do seu exemplo é similar a 'receitas aprendidas por jogador'.
        """
        query = """
            SELECT
                r.identificador_receita,
                cp.nome AS consumivel_produzido_nome
            FROM receita r
            JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
            WHERE r.id_jogador = %s;
        """
        return self.executar_query(query, (id_jogador,), fetchall=True)

    # ===============================================
    # Métodos de Operações com Missões
    # ===============================================
    def buscar_missoes_jogador(self, id_jogador):
        """Busca todas as missões associadas a um jogador."""
        query = """
            SELECT m.nome, m.descricao
            FROM missao m
            WHERE m.id_jogador = %s;
        """
        return self.executar_query(query, (id_jogador,), fetchall=True)

    def buscar_item_recompensa_missao(self, missao_id):
        """
        Ver o item que uma missão X vai dar. (Adaptado para ItemMissao)
        Seu ItemMissao referencia TipoItem.
        """
        query = """
            SELECT
                im.identificador_item,
                ti.tipo AS tipo_geral
            FROM itemmissao im
            JOIN tipo_item ti ON im.identificador_item = ti.identificador_item
            WHERE im.missao_id = %s;
        """
        return self.executar_query(query, (missao_id,), fetchall=True)

    def buscar_local_missao(self, missao_id):
        """
        Ver o lugar que uma missão X está. (Adaptado para Sala de Missão)
        """
        query = """
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
        return self.executar_query(query, (missao_id,), fetchone=True)

    def buscar_detalhes_missao(self, missao_id):
        """
        Ver o (nome, descrição) de uma missão específica.
        """
        query = """
            SELECT nome, descricao
            FROM missao
            WHERE missao_id = %s;
        """
        return self.executar_query(query, (missao_id,), fetchone=True)

    # ===============================================
    # Métodos de Operações com Tipos de Itens Específicos
    # ===============================================


    def tentar_coletar_item_no_mapa(self, id_jogador, id_area_interativa, notificador):
        """
        Processa a tentativa de coletar recompensa por exploração.

        Passos:
            - Verifica restrição de tempo (15 min).
            - Sorteia chance de sucesso.
            - Se sucesso, busca um item aleatório da ilha atual.
            - Adiciona item à mochila do jogador.
        
        Retorna:
            str: mensagem de erro ou sucesso.
        """

        try:
            # Busca a área atual do jogador
            jogador = self.buscar_jogador(id_jogador)
            if not jogador:
                return "Erro: jogador não encontrado."

            id_area_atual = jogador.identificador_area
            id_ilha = self.buscar_info_area(id_area_atual, jogador.identificador_progresso).identificador_ilha

            # Tenta atualizar/inserir a tentativa
            try:
                self.cursor.execute("""
                    INSERT INTO recompensa_de_exploracao
                        (identificador_area_interativa, identificador_jogador)
                    VALUES
                        (%s, %s)
                    ON CONFLICT (identificador_area_interativa, identificador_jogador)
                    DO UPDATE SET data_da_tentativa = now();
                """, (id_area_interativa, id_jogador))
            except psycopg.Error as e:
                self.conn.rollback()
                if "precisa esperar 15 minutos" in str(e):
                    return "Erro: você precisa esperar 15 minutos para interagir novamente."
                print("[ERRO] Falha ao inserir em recompensa_de_exploracao:", str(e))
                return "Erro ao registrar tentativa de recompensa."

            # Busca chance de sucesso da área interativa
            self.cursor.execute("""
                SELECT chance_sucesso
                FROM area_interativa
                WHERE identificador_area_interativa = %s;
            """, (id_area_interativa,))
            resultado = self.cursor.fetchone()
            if not resultado:
                return "Erro: área interativa não encontrada."

            chance_sucesso = float(resultado.chance_sucesso)
            if random.random() > chance_sucesso:
                return "Tentativa registrada, mas nenhum item foi encontrado."

            # Busca todos os itens possíveis da ilha atual
            consumiveis = self.buscar_itens_na_ilha(id_ilha, tipo="consumivel")
            nao_consumiveis = self.buscar_itens_na_ilha(id_ilha, tipo="nao_consumivel")
            todos_itens = consumiveis + nao_consumiveis

            if not todos_itens:
                return "Nenhum item disponível para ser recebido nesta ilha."

            # Escolhe item aleatório
            item_escolhido = random.choice(todos_itens)
            id_item = item_escolhido.identificador_item

            # Pega ID da mochila do jogador
            mochila = self.buscar_inventario(id_jogador, tipo_inventario='moc', identificador_progresso=jogador.identificador_progresso)
            if not mochila:
                return "Erro: mochila do jogador não encontrada."

            id_inventario = mochila[0].identificador_inventario

            # Adiciona o item
            sucesso = self.adicionar_item_ao_inventario(id_inventario, id_item)
            if sucesso:
                notificador.adicionar_item(item_escolhido.nome_item, 1)
                return f"Item '{item_escolhido.nome_item}' adicionado à mochila!"
            else:
                return "Erro ao adicionar o item à mochila."
        except Exception as e:
            self.conn.rollback()
            print(f"[ERRO] executar_recompensa_exploracao: {e}")
            return "Erro inesperado ao tentar coletar recompensa."


    def buscar_arma_atributos(self, id_arma):
         query = """
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
         return self.executar_query(query, (id_arma,), fetchone=True)
    def buscar_consumivel_atributos(self, id_consumivel):
        """
        Ver os atributos de uma comida específica. (Adaptado para Consumivel)
        """
        query = """
            SELECT nome, tipo, raridade, quantidade, preco_compra, preco_venda, efabricavel
            FROM consumivel
            WHERE identificador_consumivel = %s;
        """
        return self.executar_query(query, (id_consumivel,), fetchone=True)

    def buscar_acessorio_atributos(self, id_acessorio):
        """
        Ver os atributos de um medicamento específico. (Adaptado para Acessorio)
        """
        query = """
            SELECT nome, tipo, raridade, preco_compra, preco_venda
            FROM acessorio
            WHERE identificador_acessorio = %s;
        """
        return self.executar_query(query, (id_acessorio,), fetchone=True)

    def buscar_nao_consumivel_atributos(self, id_nao_consumivel):
        """
        Ver os atributos de um utilizável específico. (Adaptado para Não-Consumível geral)
        """
        query = """
            SELECT nome, tipo, raridade, quantidade, preco_compra, preco_venda
            FROM nao_consumivel
            WHERE identificador_nao_consumivel = %s;
        """
        return self.executar_query(query, (id_nao_consumivel,), fetchone=True)

    def buscar_fruta_atributos(self, id_fruta):
        """
        Ver os atributos de uma fruta específica.
        """
        query = """
            SELECT f.nome, f.tipo, f.raridade, f.preco_compra, f.preco_venda, e.nome AS habilidade_nome, e.bravura
            FROM fruta f
            LEFT JOIN efeito e ON f.identificador_habilidade = e.identificador_efeito
            WHERE f.identificador_fruta = %s;
        """
        return self.executar_query(query, (id_fruta,), fetchone=True)

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
        query = """
            SELECT ii.id_inventario, ii.identificador_item
            FROM iteminventario ii
            LEFT JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
            WHERE ti.identificador_item IS NULL; -- Busca itens no inventário que não têm um tipo correspondente
        """
        return self.executar_query(query, fetchall=True)



    # ===============================================
    # Métodos de Operações com Habilidades
    # ===============================================

    def buscar_habilidades_por_arma(self, id_arma):
        query = """
            SELECT
                habilidade.identificador_habilidade,
            	TRIM(habilidade.nome) AS nome,
                TRIM(habilidade.descricao) AS descricao,
                TRIM(habilidade.tipo_de_ataque) AS tipo_de_ataque,
                TRIM(habilidade.tipo_de_alvo) AS tipo_de_alvo,
                habilidade.dano,
                habilidade.custo,
                TRIM(efeito.nome) AS efeito_nome,
                efeito.valor AS efeito_valor
            FROM habilidade_arma
                JOIN habilidade   ON  habilidade.identificador_habilidade = habilidade_arma.identificador_habilidade
            	LEFT JOIN efeito  ON  efeito.identificador_efeito = habilidade.identificador_efeito
            WHERE habilidade_arma.identificador_arma = %s;
        """
        return self.executar_query(query, (id_arma,), fetchall=True)
    
    def buscar_habilidades_por_fruta(self, id_arma):
        query = """
            SELECT
                habilidade.identificador_habilidade,
            	TRIM(habilidade.nome) AS nome,
                TRIM(habilidade.descricao) AS descricao,
                TRIM(habilidade.tipo_de_ataque) AS tipo_de_ataque,
                TRIM(habilidade.tipo_de_alvo) AS tipo_de_alvo,
                habilidade.dano,
                habilidade.custo,
                TRIM(efeito.nome) AS efeito_nome,
                efeito.valor AS efeito_valor
            FROM habilidade_fruta
                JOIN habilidade   ON  habilidade.identificador_habilidade = habilidade_fruta.identificador_habilidade
            	LEFT JOIN efeito  ON  efeito.identificador_efeito = habilidade.identificador_efeito
            WHERE habilidade_fruta.identificador_fruta = %s;
        """
        return self.executar_query(query, (id_arma,), fetchall=True)
