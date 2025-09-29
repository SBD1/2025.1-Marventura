
import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import namedtuple_row
from utilidades.constantes import *
from entidades.item_inventario import ItemInventario
from entidades.mochila import Mochila
from entidades.kit import KitDoExplorador

import random
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
        if self.conn and not self.conn.closed:
            try:
                # Força o commit de qualquer transação pendente
                self.conn.commit()
                print("DBManager: Commit final realizado antes de fechar.")
            except psycopg.Error as e:
                print(f"DBManager ERRO ao fazer commit final: {e}")
            
            if self.cursor and not self.cursor.closed:
                self.cursor.close()
            
            self.conn.close()
            print("DBManager: Conexão com o PostgreSQL fechada.")
        
        DBManager._instance = None  # Reseta a instância Singleton


    def executar_query(self, consulta, params=None, fetchone=False, fetchall=False, autocommit=True):
        """
        Executa uma consulta SQL no banco de dados.
        :param consulta: A string SQL a ser executada.
        :param params: Uma tupla ou lista de parâmetros para a consulta (para evitar SQL Injection).
        :param fetchone: Se True, retorna apenas uma linha.
        :param fetchall: Se True, retorna todas as linhas.
        :param autocommit: Se True, executa o commit automaticamente após a execução (para uso dentro de transações explícitas).
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
                if autocommit:
                    self.conn.commit()
                return True
        except psycopg.Error as e:
            if autocommit:
                try:
                    self.conn.rollback()
                except Exception as rollback_e:
                    print(f"DBManager ERRO no rollback: {rollback_e}")
            print(f"DBManager ERRO ao executar query '{consulta}': {e}")
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
                    'fala': 'Você... quem é você?',
                },
                {
                    'id_missao': 'mis001',
                    'genero': 'F',
                    'sequencia': 7,
                    'fala': 'Eu... não sei como vim parar aqui.',
                },
                {
                    'id_missao': 'mis002',
                    'genero': 'F',
                    'sequencia': 3,
                    'fala': 'Só alguém procurando respostas... e talvez um pouco de água.',
                },
                {
                    'id_missao': 'mis003',
                    'genero': 'F',
                    'sequencia': 1,
                    'fala': 'Tsc... sério?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 3,
                    'fala': '(Olhando ao redor): — Gertrudes é... uma senhora?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 6,
                    'fala': '(Pegando um garfo): — Ok... então essa vila tem galinhas vingativas, cozinheiras dramáticas e um senhor que tempera a terra com orégano?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 9,
                    'fala': '(Provando o Omurice): — Uau. Isso é... surpreendentemente bom. Tipo “não esperava gostar tanto de arroz com ovo” bom.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 12,
                    'fala': '(Sorrindo): — Eu só queria água. Agora tô jantando com filósofos, artistas e galinhas vingativas.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 14,
                    'fala': '(Recuando): — Ah não. É ela. Essa aí me seguiu desde o campo. Ela quer vingança.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 17,
                    'fala': '(Entregando o pão com reverência): — Trégua, senhora Gertrudes. Que nossos caminhos se cruzem apenas no café da manhã.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 23,
                    'fala': 'E ninguém tentou detê-la?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'F',
                    'sequencia': 26,
                    'fala': 'Eu vou enfrentá-la.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'F',
                    'sequencia': 3,
                    'fala': 'Foi por pouco. Mas está feito.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'F',
                    'sequencia': 5,
                    'fala': 'Eu... estou procurando alguém. Minha irmã. Preciso continuar.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'F',
                    'sequencia': 7,
                    'fala': 'Isso é ótimo... mas como eu chego lá?',
                },
            ],
            SHUAN: [
                {
                    'id_missao': 'mis001',
                    'genero': 'M',
                    'sequencia': 4,
                    'fala': 'Você... quem é você?',
                },
                {
                    'id_missao': 'mis001',
                    'genero': 'M',
                    'sequencia': 7,
                    'fala': 'Eu... não sei como vim parar aqui.',
                },
                {
                    'id_missao': 'mis002',
                    'genero': 'M',
                    'sequencia': 3,
                    'fala': 'Só alguém procurando respostas... e talvez um pouco de água.',
                },
                {
                    'id_missao': 'mis003',
                    'genero': 'M',
                    'sequencia': 1,
                    'fala': 'Tsc... sério?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 3,
                    'fala': '(Olhando ao redor): — Gertrudes é... uma senhora?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 6,
                    'fala': '(Pegando um garfo): — Ok... então essa vila tem galinhas vingativas, cozinheiras dramáticas e um senhor que tempera a terra com orégano?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 9,
                    'fala': '(Provando o Omurice): — Uau. Isso é... surpreendentemente bom. Tipo “não esperava gostar tanto de arroz com ovo” bom.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 12,
                    'fala': '(Sorrindo): — Eu só queria água. Agora tô jantando com filósofos, artistas e galinhas vingativas.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 14,
                    'fala': '(Recuando): — Ah não. É ela. Essa aí me seguiu desde o campo. Ela quer vingança.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 17,
                    'fala': '(Entregando o pão com reverência): — Trégua, senhora Gertrudes. Que nossos caminhos se cruzem apenas no café da manhã.',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 23,
                    'fala': 'E ninguém tentou detê-la?',
                },
                {
                    'id_missao': 'mis011',
                    'genero': 'M',
                    'sequencia': 26,
                    'fala': 'Eu vou enfrentá-la.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'M',
                    'sequencia': 3,
                    'fala': 'Foi por pouco. Mas está feito.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'M',
                    'sequencia': 5,
                    'fala': 'Eu... estou procurando alguém. Minha irmã. Preciso continuar.',
                },
                {
                    'id_missao': 'mis012',
                    'genero': 'M',
                    'sequencia': 7,
                    'fala': 'Isso é ótimo... mas como eu chego lá?',
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
                quantidade=row.quantidade,
                item_de_missao=row.item_de_missao
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
        consulta = """
            SELECT identificador_inventario
            FROM inventario
            WHERE identificador_personagem = %s AND tipo_inventario = %s AND identificador_progresso = %s
        """
        resultado = self.executar_query(consulta, (identificador_personagem, tipo_inventario, identificador_progresso), fetchone=True)
        return resultado.identificador_inventario if resultado else None



    def sekishiki_meikai_ha(self, id_inimigo, identificador_progresso):
        """
        Envia um inimigo para o Yomotsu Hirasaka.
        """
        # Define a consulta SQL com base no tipo de inimigo
        
        if id_inimigo.startswith('che'):
            consulta = """
                UPDATE estado_chefe
                SET 
                    vida_atual = 0,
                    data_da_morte = now(),
                    identificador_area_atual = 'are034'
                WHERE 
                    identificador_chefe = %s
                    AND identificador_progresso = %s
                    AND data_da_morte IS NULL;
            """
        else:
            consulta = """
                UPDATE estado_lacaio
                SET 
                    vida_atual = 0,
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
        consulta = """
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


    
    def salvar_progresso_jogador(self, id_jogador, vida, vida_atual, energia, energia_atual, experiencia_atual, nivel, moedas_totais, coordenada_x, coordenada_y, orientacao, identificador_area):
        """
        Salva o progresso atual do jogador no banco de dados.
        Esta operação é executada em uma transação para garantir a atomicidade.
        """
        if not self.conn:
            print("DBManager ERRO: Não há conexão ativa para salvar o progresso.")
            return False

        query = """
            UPDATE jogador
            SET 
                vida = %s,
                vida_atual = %s,
                energia = %s,
                energia_atual = %s,
                experiencia_atual = %s,
                nivel = %s,
                moedas_totais = %s,
                coordenada_x = %s,
                coordenada_y = %s,
                orientacao = %s,
                identificador_area = %s
            WHERE identificador_jogador = %s;
        """
        params = (vida, vida_atual, energia, energia_atual, experiencia_atual, nivel, moedas_totais, coordenada_x, coordenada_y, orientacao, identificador_area, id_jogador)
        
        try:
            # Usar uma transação garante que a operação seja atômica.
            with self.conn.transaction():
                with self.conn.cursor() as cur:
                    cur.execute(query, params)
            print(f"Progresso do jogador '{id_jogador}' salvo com sucesso.")
            return True
        except psycopg.Error as e:
            # O rollback é automático ao sair do with self.conn.transaction() em caso de erro.
            print(f"DBManager ERRO ao salvar progresso do jogador '{id_jogador}': {e}")
            return False



    def verificar_progresso_existente(self, id_jogador):
        """
        Verifica de forma rápida se existe um registro para o jogador.
        Retorna True se o jogador existe, False caso contrário.
        """
        query = "SELECT 1 FROM jogador WHERE identificador_jogador = %s;"
        resultado = self.executar_query(query, (id_jogador,), fetchone=True)
        return resultado is not None



    def resetar_ou_criar_jogador(self, jogador_info):
        """
        Reseta o estado do jogo para um "Novo Jogo", incluindo vendedores e jogador,
        dentro de uma única transação para garantir a integridade dos dados.
        """
        if not self.conn or self.conn.closed:
            print("DBManager ERRO: Sem conexão para resetar o jogo.")
            return False

        update_query = """
            UPDATE jogador SET
                nome = %s, descricao = %s, vida_atual = %s, experiencia_atual = %s,
                nivel = %s, moedas_totais = %s, coordenada_x = %s, coordenada_y = %s,
                orientacao = %s, identificador_area = %s, vida = %s, energia = %s, sorte = %s
            WHERE identificador_jogador = %s;
        """
        params = (
            jogador_info.nome, jogador_info.descricao, jogador_info.vida, 0, 1, 
            jogador_info.moedas_totais, jogador_info.coordenada_x, jogador_info.coordenada_y,
            'direita', jogador_info.identificador_area, jogador_info.vida, 
            jogador_info.energia, jogador_info.sorte, jogador_info.identificador_jogador
        )

        try:
            # Abre uma transação e cria um cursor LOCAL para ela.
            with self.conn.transaction():
                with self.conn.cursor() as cursor:
                    # --- Executa todas as operações de reset usando o cursor local ---
                    self._resetar_inventarios_vendedores(cursor)
                    self._resetar_inventario_jogador(cursor, jogador_info.identificador_jogador)
                    
                    # --- Atualiza ou Insere o jogador ---
                    cursor.execute(update_query, params)
                    if cursor.rowcount == 0:
                        insert_query = """
                            INSERT INTO jogador (identificador_jogador, nome, descricao, vida_atual, experiencia_atual, nivel, moedas_totais, coordenada_x, coordenada_y, orientacao, identificador_area, vida, energia, sorte)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """
                        insert_params = (jogador_info.identificador_jogador,) + params[:-1]
                        cursor.execute(insert_query, insert_params)

            # O 'commit' é feito automaticamente ao sair do bloco 'with' sem erros.
            print("SUCESSO: O estado de 'Novo Jogo' foi salvo no banco de dados.")
            return True

        except psycopg.Error as e:
            # O 'rollback' é feito automaticamente se ocorrer um erro.
            print(f"DBManager ERRO CRÍTICO durante o reset. As alterações foram desfeitas: {e}")
            return False



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
        consulta = """
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
        return self.executar_query(consulta, params)

    

    def salvar_novo_jogador(self, nome, descricao, identificador_progresso):
        """Insere um novo jogador no banco de dados e retorna o ID gerado."""
        consulta = """
            INSERT INTO jogador
                (identificador_area, identificador_progresso, nome, descricao, coordenada_x, coordenada_y,
                energia, vida, nivel, sorte, vida_atual, experiencia_atual, moedas_totais)
            VALUES
                ('are001', %s, %s, %s, 1950, 140, 5, 10, 1, 1, 10, 0, 0)
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
                        'id_missao', 'sequencia', 'genero', 'fala'
        """
        consulta = """
            INSERT INTO dialogo (identificador_personagem, identificador_missao, sequencia_local, genero, fala)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING identificador_dialogo;
        """
        for dialogo in dialogos:
            parametros = (
                id_jogador,
                dialogo['id_missao'],
                dialogo['sequencia'],
                dialogo['genero'],
                dialogo['fala']
            )
            self.executar_query(consulta, parametros, fetchone=True)


    
    def buscar_dialogos_sem_missao(self, id_personagem, genero):
        """
        Retorna todos os diálogos de um personagem específico que não estão associados a nenhuma missão.
        Inclui o nome do personagem que está falando.

        :param id_personagem: ID do personagem (jogador, aliado, etc)
        :return: Lista de tuplas com (identificador_dialogo, sequencia_local, genero, nome_personagem, fala)
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
                TRIM(d.fala) AS fala
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
        Retorna todas as missões aceitas atualmente pelo jogador.
        
        :param id_jogador: ID do jogador
        :return: Lista com (identificador_missao, nome, descricao, nivel_de_desbloqueio, passo_atual, identificador_area)
        """
        consulta = """
            SELECT 
                missao.identificador_missao,
                TRIM(missao.nome) AS nome,
                TRIM(missao.descricao) AS descricao,
                missao.nivel_de_desbloqueio,
                estado_missao.passo_atual,
                missao.identificador_area
            FROM jogador
            JOIN estado_missao ON estado_missao.identificador_progresso = jogador.identificador_progresso
            JOIN missao ON missao.identificador_missao = estado_missao.identificador_missao
            WHERE jogador.identificador_jogador = %s
            AND estado_missao.estado = 'aceita'
            ORDER BY missao.nivel_de_desbloqueio, missao.nome;
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



    def atualizar_passo_atual_missao(self, id_missao, id_progresso, novo_passo):
        """
        Atualiza o passo atual de uma missão específica no progresso do jogador.
        
        :param id_missao: ID da missão (ex: 'mis012')
        :param id_progresso: ID do progresso (vinculado ao jogador)
        :param novo_passo: Novo passo atual (inteiro)
        :return: True se atualizado com sucesso, False se falhou
        """
        consulta = """
            UPDATE estado_missao
            SET passo_atual = %s
            WHERE identificador_missao = %s
            AND identificador_progresso = %s;
        """
        return self.executar_query(consulta, (novo_passo, id_missao, id_progresso))



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
        :return: Lista com (id_dialogo, nome_personagem, sequencia_local, fala)
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
                TRIM(dialogo.fala) AS fala
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


    
    def buscar_missoes_desbloqueadas(self, id_progresso):
        """
        Retorna todas as missões desbloqueadas para o progresso do jogador.
        Inclui o nome da missão, descrição e nível de desbloqueio.

        :param id_progresso: ID do progresso do jogador
        :return: Lista de tuplas com (id_missao, nome_missao, descricao, nivel_de_desbloqueio)
        """
        consulta = """
            SELECT 
                missao.identificador_missao,
                TRIM(missao.nome) AS nome,
                TRIM(missao.descricao) AS descricao,
                missao.nivel_de_desbloqueio,
                estado_missao.estado,
                estado_missao.passo_atual
            FROM estado_missao
            JOIN missao ON estado_missao.identificador_missao = missao.identificador_missao
            WHERE estado_missao.identificador_progresso = %s;
        """
        return self.executar_query(consulta, (id_progresso,), fetchall=True)



    # ===============================================
    # Métodos de Operações com Inventário e Itens
    # ===============================================

    def buscar_kit_do_explorador(self, identificador_jogador, tipo_inventario='kit'):
        """Busca o inventário do kit do explorador de um jogador."""
        consulta = """
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
        return self.executar_query(consulta, (identificador_jogador, tipo_inventario), fetchall=True)



    def buscar_inventario(self, identificador_personagem, tipo_inventario='moc', identificador_progresso=None):
        """Acessa o inventário de um personagem e seus atributos, filtrando também por progresso."""
        consulta = """
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
                item_inventario.quantidade,

                -- Preço de compra
                COALESCE(
                    acessorio.preco_de_compra,
                    consumivel.preco_de_compra,
                    nao_consumivel.preco_de_compra,
                    arma.preco_de_compra
                ) AS preco_de_compra,

                -- Preço de venda
                COALESCE(
                    fruta.preco_de_venda,
                    consumivel.preco_de_venda,
                    nao_consumivel.preco_de_venda
                ) AS preco_de_venda,

                -- Indica se o item é de missão (só se aplica a não consumíveis)
                COALESCE(nao_consumivel.item_de_missao, FALSE) AS item_de_missao

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



    def adicionar_item_ao_inventario(self, identificador_inventario, identificador_item, quantidade=1, autocommit=True):
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
        return self.executar_query(consulta, (identificador_inventario, identificador_item, quantidade), autocommit=autocommit)



    def remover_item_do_inventario(self, identificador_inventario, identificador_item, quantidade=1, autocommit=True):
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
            return self.executar_query(consulta_update, (quantidade, identificador_inventario, identificador_item), autocommit=autocommit)

        else:
            # Remover o item completamente
            consulta_delete = """
                DELETE FROM item_inventario
                WHERE identificador_inventario = %s AND identificador_item = %s;
            """
            return self.executar_query(consulta_delete, (identificador_inventario, identificador_item), autocommit=autocommit)



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



    def buscar_item_por_nome(self, nome_item, autocommit=True):
        """
        Busca um item pelo nome em todas as tabelas de itens.
        """

        consulta = """
            (SELECT
                identificador_arma AS identificador,
                nome,
                descricao,
                raridade,
            FROM
                arma
            WHERE
                nome = %s)

            UNION ALL

            (SELECT
                identificador_fruta AS identificador,
                nome,
                descricao,
                raridade,
            FROM
                fruta
            WHERE
                nome = %s)

            UNION ALL

            (SELECT
                identificador_acessorio AS identificador,
                nome,
                descricao,
                raridade,
            FROM
                acessorio
            WHERE
                nome = %s)

            UNION ALL

            (SELECT
                identificador_consumivel AS identificador,
                nome,
                descricao,
                raridade,
            FROM
                consumivel
            WHERE
                nome = %s)

            UNION ALL

            (SELECT
                identificador_nao_consumivel AS identificador,
                nome,
                descricao,
                raridade,
            FROM
                nao_consumivel
            WHERE
                nome = %s);
        """

        return self.executar_query(consulta, 
            (nome_item, nome_item, nome_item, nome_item, nome_item), 
            fetchone=True, autocommit=autocommit
        )



    def buscar_efeitos_por_item(self, id_item):
        consulta = """
            SELECT TRIM(efeito.nome) AS efeito_nome, efeito.valor AS efeito_valor
            FROM efeito
                JOIN efeito_consumivel ON efeito_consumivel.identificador_efeito = efeito.identificador_efeito
            WHERE efeito_consumivel.identificador_consumivel = %s;
        """
        return self.executar_query(consulta, (id_item,), fetchall=True)



    def buscar_efeito_por_acessorio(self, id_acessorio):
        """
        Busca os efeitos associados a um acessório específico.
        Exemplo: SELECT TRIM(efeito.nome) AS efeito_nome, efeito.valor AS efeito_valor FROM efeito WHERE identificador_acessorio = 1;
        """
        consulta = """
            SELECT TRIM(efeito.nome) AS efeito_nome, efeito.valor AS efeito_valor
            FROM efeito
                JOIN efeito_acessorio ON efeito_acessorio.identificador_efeito = efeito.identificador_efeito
            WHERE efeito_acessorio.identificador_acessorio = %s;
        """
        return self.executar_query(consulta, (id_acessorio,), fetchall=True)



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
                el.identificador_instancia_lacaio,
                el.vida_atual,
                el.moedas_totais,
                el.coordenada_x AS x,
                el.coordenada_y AS y,

                l.identificador_lacaio,
                TRIM(l.nome) AS nome_lacaio,
                TRIM(l.descricao) AS descricao_lacaio,
                l.vida AS vida_total,
                l.nivel,
                l.experiencia,
                l.tempo_reacao

            FROM estado_lacaio el
            JOIN lacaio l ON el.identificador_lacaio = l.identificador_lacaio
            WHERE el.identificador_progresso = %s
            AND el.identificador_area_atual = %s
            AND el.data_da_morte IS NULL;
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
        consulta = """
            SELECT
                estado_chefe.identificador_chefe,
                TRIM(chefe.nome) AS nome,
                TRIM(chefe.descricao) AS descricao,
                chefe.vida AS vida_total,
                chefe.nivel,
                chefe.experiencia,
                estado_chefe.vida_atual,
                estado_chefe.identificador_area_atual,
                chefe.coordenada_x,
                chefe.coordenada_y,
                chefe.moedas_totais,
                estado_chefe.data_da_morte
            FROM estado_chefe
            JOIN chefe ON estado_chefe.identificador_chefe = chefe.identificador_chefe
            WHERE estado_chefe.identificador_chefe = %s;
        """
        return self.executar_query(consulta, (id_chefe,), fetchone=True)



    def buscar_chefe_por_area(self, identificador_area, identificador_progresso):
        """
        Busca o chefe presente em uma área específica para um progresso.
        """
        consulta = """
            SELECT
                estado_chefe.identificador_chefe,
                TRIM(chefe.nome) AS nome,
                TRIM(chefe.descricao) AS descricao,
                chefe.vida AS vida_total,
                chefe.nivel,
                chefe.experiencia,
                estado_chefe.vida_atual,
                estado_chefe.identificador_area_atual,
                chefe.coordenada_x,
                chefe.coordenada_y,
                chefe.moedas_totais,
                estado_chefe.data_da_morte
            FROM estado_chefe
            JOIN chefe ON estado_chefe.identificador_chefe = chefe.identificador_chefe
            WHERE estado_chefe.identificador_area_atual = %s
            AND estado_chefe.identificador_progresso = %s
            AND estado_chefe.data_da_morte IS NULL;
        """
        return self.executar_query(consulta, (identificador_area, identificador_progresso), fetchone=True)
  


    def reviver_chefe(self, identificador_chefe, identificador_progresso):
        """
        Revive um chefe morto, restaurando sua vida total e área original.
        """
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cur:
                    # Atualiza o estado do chefe com base na tabela original
                    cur.execute("""
                        UPDATE estado_chefe
                        SET 
                            vida_atual = chefe.vida,
                            identificador_area_atual = chefe.identificador_area,
                            data_da_morte = NULL
                        FROM chefe
                        WHERE 
                            chefe.identificador_chefe = estado_chefe.identificador_chefe AND
                            estado_chefe.identificador_chefe = %s AND
                            estado_chefe.identificador_progresso = %s;
                    """, (identificador_chefe, identificador_progresso))

                    if cur.rowcount == 0:
                        return {'sucesso': False, 'mensagem': 'Chefe não estava morto ou não encontrado.'}

            return {'sucesso': True}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}



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



    def buscar_habitante(self, id_habitante, id_progresso):
        """Busca dados de um habitante pelo ID."""
        consulta = """
            SELECT
                habitante.identificador_habitante,
                habitante.identificador_area,
                TRIM(habitante.nome) AS nome,
                TRIM(habitante.descricao) AS descricao,
                TRIM(habitante.chave_imagem) AS chave_imagem,
                habitante.tipo_habitante,
                habitante.coordenada_x,
                habitante.coordenada_y,
                habitante.especialidade,
                estado_habitante.moedas_totais,
                estado_habitante.conhecido
            FROM habitante
            JOIN estado_habitante
                ON habitante.identificador_habitante = estado_habitante.identificador_habitante
            WHERE habitante.identificador_habitante = %s
            AND estado_habitante.identificador_progresso = %s;
        """
        return self.executar_query(consulta, (id_habitante, id_progresso), fetchone=True)



    def buscar_habitante_pelo_nome(self, nome_habitante, id_progresso):
        """Busca dados de um habitante pelo nome (exato, sem curinga)."""
        consulta = """
            SELECT
                habitante.identificador_habitante,
                habitante.identificador_area,
                TRIM(habitante.nome) AS nome,
                TRIM(habitante.descricao) AS descricao,
                TRIM(habitante.chave_imagem) AS chave_imagem,
                habitante.tipo_habitante,
                habitante.coordenada_x,
                habitante.coordenada_y,
                habitante.especialidade,
                estado_habitante.moedas_totais,
                estado_habitante.conhecido
            FROM habitante
            JOIN estado_habitante
                ON habitante.identificador_habitante = estado_habitante.identificador_habitante
            WHERE TRIM(nome) = %s
            AND estado_habitante.identificador_progresso = %s;
        """
        return self.executar_query(consulta, (nome_habitante, id_progresso), fetchone=True)



    def buscar_habitante_por_area(self, id_area, id_progresso):
        """Busca dados de todos os habitantes de uma área específica, com estado associado ao progresso."""
        consulta = """
            SELECT
                habitante.identificador_habitante,
                habitante.identificador_area,
                TRIM(habitante.nome) AS nome,
                TRIM(habitante.descricao) AS descricao,
                TRIM(habitante.chave_imagem) AS chave_imagem,
                habitante.tipo_habitante,
                habitante.coordenada_x,
                habitante.coordenada_y,
                habitante.especialidade,
                estado_habitante.moedas_totais,
                estado_habitante.conhecido
            FROM habitante
            JOIN estado_habitante
                ON habitante.identificador_habitante = estado_habitante.identificador_habitante
            WHERE habitante.identificador_area = %s
            AND estado_habitante.identificador_progresso = %s;
        """
        return self.executar_query(consulta, (id_area, id_progresso), fetchall=True)
    


    def marcar_habitante_como_conhecido(self, id_habitante, id_progresso):
        """
        Marca um habitante como conhecido no progresso atual.
        Só atualiza se o registro já existir.
        """
        consulta = """
            UPDATE estado_habitante
            SET conhecido = TRUE
            WHERE identificador_habitante = %s
            AND identificador_progresso = %s;
        """
        return self.executar_query(consulta, (id_habitante, id_progresso))


    
    def buscar_habitante_por_ilha(self, id_ilha):
        """Busca dados de todos os habitante de uma ilha específica."""
        consulta = """
            SELECT h.*
                FROM habitante h
                JOIN area a ON h.identificador_area = a.identificador_area
                WHERE a.identificador_ilha = %s;
        """
        return self.executar_query(consulta, (id_ilha,), fetchall=True)
    


    def buscar_vendedor_por_area(self, id_area, id_progresso):
        """Busca vendedores em uma área específica, com estado associado ao progresso."""
        query = """
            SELECT
                h.identificador_habitante,
                TRIM(h.nome) AS nome,
                TRIM(h.descricao) AS descricao,
                h.coordenada_x,
                h.coordenada_y,
                eh.moedas_totais
            FROM habitante h
            JOIN estado_habitante eh 
                ON h.identificador_habitante = eh.identificador_habitante
            WHERE h.identificador_area = %s
            AND h.tipo_habitante = 'ven'
            AND eh.identificador_progresso = %s
        """
        return self.executar_query(query, (id_area, id_progresso), fetchall=True)



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
    


    def buscar_lacaio_por_nome_com_habilidades(self, nome_lacaio):
        """
        Busca os dados de um lacaio pelo nome (não instância) e retorna suas habilidades.
        
        :param nome_lacaio: Nome do lacaio (exato)
        :return: Lista de tuplas com dados do lacaio + habilidades (uma linha por habilidade)
        """
        consulta = """
            SELECT
                lacaio.identificador_lacaio,
                TRIM(lacaio.nome) AS nome_lacaio,
                TRIM(lacaio.descricao) AS descricao,
                lacaio.vida,
                lacaio.nivel,
                lacaio.experiencia,
                habilidade.identificador_habilidade,
                TRIM(habilidade.nome) AS nome_habilidade,
				TRIM(habilidade.descricao) AS descricao_habilidade,
                habilidade.dano,
                TRIM(habilidade.tipo_de_ataque) AS tipo_de_ataque,
                TRIM(habilidade.tipo_de_alvo) AS tipo_de_alvo,
				TRIM(efeito.nome) AS nome_efeito,
				efeito.valor AS valor_efeito
            FROM lacaio
            LEFT JOIN habilidade_personagem ON habilidade_personagem.identificador_personagem = lacaio.identificador_lacaio
            LEFT JOIN habilidade ON habilidade.identificador_habilidade = habilidade_personagem.identificador_habilidade
			LEFT JOIN efeito ON habilidade.identificador_efeito = efeito.identificador_efeito
            WHERE TRIM(lacaio.nome) = %s;
        """
        return self.executar_query(consulta, (nome_lacaio,), fetchall=True)
    


    def buscar_barco_atual(self, identificador_progresso):
        consulta = """
            SELECT
                identificador_barco,
                tipo_barco,
                TRIM(nome) AS nome,
                TRIM(descricao) AS descricao
            FROM barco
            WHERE identificador_progresso = %s AND estado = 'adquirido';
        """
        return self.executar_query(consulta, (identificador_progresso,), fetchone=True)



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



    def buscar_ilhas(self, identificador_progresso):
        """
         Retorna todas as ilhas e se foram visitadas no progresso atual.
        """
        consulta = """
            SELECT
                ilha.identificador_ilha,
                TRIM(ilha.nome) AS nome,
                ilha_visitada.visitada
            FROM ilha
            LEFT JOIN ilha_visitada
              ON ilha.identificador_ilha = ilha_visitada.identificador_ilha AND ilha_visitada.identificador_progresso = %s
            ORDER BY ilha.identificador_ilha;
            """
        return self.executar_query(consulta, (identificador_progresso,), fetchall=True)



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

    

    def buscar_areas_interativas_da_area(self, id_area, id_progresso):
        """
        Busca todos os elementos espaciais do tipo 'Área interativa' da área atual (origem),
        considerando o estado do progresso (se estão ativas ou não).
        """
        consulta = """
            SELECT
                ai.identificador_area_interativa AS identificador,
                ai.identificador_area_origem AS area_origem,
                ai.identificador_area_destino AS area_destino,
                ai.identificador_missao,
                TRIM(ai.chave_imagem) AS chave_imagem,
                ai.x,
                ai.y,
                ai.largura,
                ai.altura,
                ai.chance_sucesso,
                TRIM(ai.tipo_evento) AS tipo_evento,
                TRIM(ai.metodo_ativacao) AS metodo_ativacao,
                eai.ativa
            FROM area_interativa ai
            JOIN estado_area_interativa eai
                ON ai.identificador_area_interativa = eai.identificador_area_interativa
            WHERE ai.identificador_area_origem = %s
            AND eai.identificador_progresso = %s;
        """
        return self.executar_query(consulta, (id_area, id_progresso), fetchall=True)



    def buscar_areas_interativas_de_missao_por_area(self, id_area, id_progresso):
        """
        Busca todos os elementos espaciais do tipo 'Área interativa' da área atual (origem),
        considerando o estado do progresso (se estão ativas ou não) e o tipo de evento = missao.
        """
        consulta = """
            SELECT
                ai.identificador_area_interativa AS identificador,
                ai.identificador_area_origem AS area_origem,
                ai.identificador_area_destino AS area_destino,
                ai.identificador_missao,
                TRIM(ai.chave_imagem) AS chave_imagem,
                ai.x,
                ai.y,
                ai.largura,
                ai.altura,
                ai.chance_sucesso,
                TRIM(ai.tipo_evento) AS tipo_evento,
                TRIM(ai.metodo_ativacao) AS metodo_ativacao,
                eai.ativa
            FROM area_interativa ai
            JOIN estado_area_interativa eai
                ON ai.identificador_area_interativa = eai.identificador_area_interativa
            WHERE ai.identificador_area_origem = %s
            AND eai.identificador_progresso = %s
            AND ai.tipo_evento = 'missao';
        """
        return self.executar_query(consulta, (id_area, id_progresso), fetchall=True)



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
        consulta = """
            SELECT m.id_mapa, m.total_item_chave
            FROM mapa m
            WHERE m.id_mapa = %s;
        """
        return self.executar_query(consulta, (id_mapa,), fetchall=True)
    


    def buscar_itens_na_ilha(self, id_ilha, tipo='consumivel'):
        """
        Busca todos os itens coletáveis de um tipo ('consumivel' ou 'nao_consumivel') disponíveis na ilha.
        Compara o campo local_encontrado com o nome da ilha, e exige que e_coletado seja TRUE.
        """
        if tipo == 'consumivel':
            consulta = """
                SELECT
                    c.identificador_consumivel AS identificador_item,
                    TRIM(c.nome) AS nome_item
                FROM consumivel c
                JOIN ilha i ON c.local_encontrado = i.nome
                WHERE i.identificador_ilha = %s
                AND c.e_coletado = TRUE;
            """
        else:
            consulta = """
                SELECT
                    nc.identificador_nao_consumivel AS identificador_item,
                    TRIM(nc.nome) AS nome_item
                FROM nao_consumivel nc
                JOIN ilha i ON nc.local_encontrado = i.nome
                WHERE i.identificador_ilha = %s
                AND nc.e_coletado = TRUE;
            """
        return self.executar_query(consulta, (id_ilha,), fetchall=True)



    def marcar_ilha_como_visitada(self, id_ilha, id_progresso):
        """
        Marca uma ilha como visitada no progresso atual.
        """

        consulta = """
            UPDATE ilha_visitada
            SET visitada = TRUE
            WHERE identificador_ilha = %s
            AND identificador_progresso = %s;
        """
        return self.executar_query(consulta, (id_ilha, id_progresso))



    def desbloquear_rota(self, identificador_progresso, ilha_a, ilha_b):
        """
        Desbloqueia uma rota entre duas ilhas em um progresso específico.
        """
        if ilha_a is None or ilha_b is None or identificador_progresso is None:
            raise ValueError("Os identificadores das ilhas e do progresso são obrigatórios.")
        
        consulta = """
            UPDATE conexao_entre_ilhas
            SET bloqueada = 'false'
            WHERE identificador_progresso = %s
                AND identificador_ilha_a = %s
                AND identificador_ilha_b = %s;
        """
        self.executar_query(consulta, (identificador_progresso, ilha_a, ilha_b))



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



    def tentar_cozinhar_item(self, id_inventario, id_item1=None, id_item2=None):
        """
        Tenta fabricar um item a partir de 1 ou 2 ingredientes.
        Usa as funções de remover/adicionar já existentes.
        
        Retorna:
            dict: {
                sucesso: bool,
                mensagem: str,
                item_produzido: {id, nome},
                receita: id_receita
            }
        """
        try:
            if id_item1 is None and id_item2 is None:
                raise ValueError("Pelo menos um ingrediente deve ser fornecido.")
            
            with self.conn.transaction():
                # 1. Remover ingredientes do inventário
                if id_item1:
                    if not self.remover_item_do_inventario(id_inventario, id_item1, 1, False):
                        return {'sucesso': False, 'mensagem': f"Item {id_item1} não encontrado no inventário."}

                if id_item2:
                    if not self.remover_item_do_inventario(id_inventario, id_item2, 1, False):
                        return {'sucesso': False, 'mensagem': f"Item {id_item2} não encontrado no inventário."}
                    
                # Define quantos ingredientes devem ser encontrados
                numero_de_ingredientes = 1 if id_item1 is None or id_item2 is None else 2

                # 2. Procurar receita correspondente
                consulta = """
                    WITH ingredientes AS (
                        SELECT identificador_receita, identificador_consumivel AS id_item
                        FROM ingrediente_consumivel
                        UNION ALL
                        SELECT identificador_receita, identificador_nao_consumivel AS id_item
                        FROM ingrediente_nao_consumivel
                    )
                    SELECT receita.identificador_receita,
                        receita.consumivel_produzido,
                        TRIM(consumivel.nome) AS nome
                    FROM receita
                    JOIN consumivel ON receita.consumivel_produzido = consumivel.identificador_consumivel
                    WHERE receita.identificador_receita IN (
                        SELECT identificador_receita
                        FROM ingredientes
                        GROUP BY identificador_receita
                        HAVING COUNT(DISTINCT id_item) = %s
                        AND COUNT(DISTINCT CASE WHEN id_item IN (%s, %s) THEN id_item END) = %s
                    )
                    LIMIT 1;
                """
                receita = self.executar_query(
                    consulta,
                    (numero_de_ingredientes, id_item1, id_item2, numero_de_ingredientes),
                    fetchone=True,
                    autocommit=False
                )

                if not receita:
                    return {'sucesso': False, 'mensagem': "Nenhuma receita corresponde a essa combinação."}

                id_receita = receita.identificador_receita
                id_resultado = receita.consumivel_produzido
                nome_resultado = receita.nome


                # 3. Adicionar o item resultante
                if not self.adicionar_item_ao_inventario(id_inventario, id_resultado, 1, False):
                    return {'sucesso': False, 'mensagem': "Erro ao adicionar item produzido."}

            return {
                'sucesso': True,
                'mensagem': f"Item '{nome_resultado}' fabricado com sucesso!",
                'item_produzido': {'id': id_resultado, 'nome': nome_resultado},
                'receita': id_receita
            }

        except Exception as e:
            return {'sucesso': False, 'mensagem': f"Erro inesperado: {e}"}



    def aprender_receita(self, identificador_receita, identificador_jogador):
        """
        Registra que uma receita no livro de receitas do jogador.
        Se já estiver registrada, não faz nada.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO livro_de_receitas (identificador_jogador, identificador_receita)
                    VALUES (%s, %s)
                    ON CONFLICT (identificador_jogador, identificador_receita) DO NOTHING;
                """, (identificador_jogador, identificador_receita))

            return {'sucesso': True}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}



    def buscar_livro_de_receitas(self, identificador_jogador):
        """
        Busca o livro de receitas de um jogador, retornando as receitas que ele aprendeu.
        Cada receita retorna o nome do consumível produzido e seu identificador.
        """
        consulta = """
            SELECT
                receita.identificador_receita,
                TRIM(consumivel.nome) AS nome,
				consumivel.identificador_consumivel
            FROM livro_de_receitas
            JOIN receita ON livro_de_receitas.identificador_receita = receita.identificador_receita
            JOIN consumivel ON receita.consumivel_produzido = consumivel.identificador_consumivel
            WHERE livro_de_receitas.identificador_jogador = %s
            ORDER BY consumivel.nome;
        """
        return self.executar_query(consulta, (identificador_jogador,), fetchall=True)



    def buscar_ingredientes_da_receita(self, identificador_receita):
        """
        Busca os ingredientes de uma receita específica, retornando tanto consumíveis quanto não-consumíveis.
        """
        consulta = """
            SELECT
                ingrediente_consumivel.identificador_consumivel AS identificador_ingrediente,
                TRIM(consumivel.nome) AS nome_ingrediente
            FROM ingrediente_consumivel
            JOIN consumivel ON ingrediente_consumivel.identificador_consumivel = consumivel.identificador_consumivel
            WHERE ingrediente_consumivel.identificador_receita = %s
            
            UNION ALL
            
            SELECT
                ingrediente_nao_consumivel.identificador_nao_consumivel AS identificador_ingrediente,
                TRIM(nao_consumivel.nome) AS nome_ingrediente
            FROM ingrediente_nao_consumivel
            JOIN nao_consumivel ON ingrediente_nao_consumivel.identificador_nao_consumivel = nao_consumivel.identificador_nao_consumivel
            WHERE ingrediente_nao_consumivel.identificador_receita = %s;
        """
        return self.executar_query(consulta, (identificador_receita, identificador_receita), fetchall=True)



    def buscar_todos_os_itens_fabricaveis(self):
        """
        Busca todos os itens que podem ser fabricados.
        """
        consulta = """
            SELECT
                receita.identificador_receita,
                consumivel.identificador_consumivel,
                tipo_item.identificador_item,
                tipo_item.tipo,
                TRIM(consumivel.nome) AS nome,
                TRIM(consumivel.descricao) AS descricao,
                TRIM(consumivel.raridade) AS raridade,
                consumivel.preco_de_compra,
                consumivel.preco_de_venda,
                consumivel.e_fabricavel
            FROM receita
            JOIN consumivel ON receita.consumivel_produzido = consumivel.identificador_consumivel
            JOIN tipo_item ON tipo_item.identificador_item = consumivel.identificador_consumivel
            ORDER BY consumivel.nome;
        """
        return self.executar_query(consulta, fetchall=True)



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
                item_missao.identificador_item,
                COALESCE(
                    TRIM(consumivel.nome),
                    TRIM(nao_consumivel.nome)
                ) AS nome_item,
                COALESCE(
                    TRIM(consumivel.descricao),
                    TRIM(nao_consumivel.descricao)
                ) AS descricao_item,
                tipo_item.tipo,
                COALESCE(
                    TRIM(consumivel.raridade),
                    TRIM(nao_consumivel.raridade)
                ) AS raridade,
                item_missao.quantidade
            FROM item_missao
            JOIN tipo_item ON item_missao.identificador_item = tipo_item.identificador_item
            LEFT JOIN consumivel ON tipo_item.identificador_item = consumivel.identificador_consumivel
            LEFT JOIN nao_consumivel ON tipo_item.identificador_item = nao_consumivel.identificador_nao_consumivel
            WHERE item_missao.identificador_missao = %s;
        """
        return self.executar_query(consulta, (missao_id,), fetchone=True)



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



    def inserir_gatilho_de_missao(self, id_area_origem, id_missao, x, y, largura, altura, id_progresso):
        """
        Insere uma nova área interativa no banco de dados e seu estado associado ao progresso.

        :param id_area_origem: ID da área onde a interação ocorre
        :param id_missao: ID da missão associada (ou None)
        :param x: Posição X da área
        :param y: Posição Y da área
        :param largura: Largura da área
        :param altura: Altura da área
        :param id_progresso: ID do progresso ao qual o estado da área interativa pertence
        :return: ID da nova área interativa inserida
        """
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cur:
                    # 1. Inserir a área interativa
                    cur.execute("""
                        INSERT INTO area_interativa
                            (identificador_area_origem, identificador_missao, x, y, largura, altura, tipo_evento, metodo_ativacao)
                        VALUES (%s, %s, %s, %s, %s, %s, 'missao', 'passivo')
                        RETURNING identificador_area_interativa;
                    """, (id_area_origem, id_missao, x, y, largura, altura))
                    
                    id_area_interativa = cur.fetchone()[0]

                    # 2. Inserir o estado da área interativa
                    cur.execute("""
                        INSERT INTO estado_area_interativa (identificador_progresso, identificador_area_interativa, ativa)
                        VALUES (%s, %s, TRUE);
                    """, (id_progresso, id_area_interativa))

            return {'sucesso': True, 'id_area_interativa': id_area_interativa}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}



    def remover_gatilho_de_missao(self, id_area_origem, id_missao, x, y, largura, altura, id_progresso):
        """
        Remove uma área interativa de missão e seu estado associado ao progresso.
        """
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cur:
                    # 1. Encontrar a área interativa a ser removida
                    cur.execute("""
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
                        LIMIT 1;
                    """, (id_area_origem, id_missao, x, y, largura, altura))

                    resultado = cur.fetchone()
                    if not resultado:
                        return {'sucesso': False, 'erro': 'Gatilho não encontrado'}

                    id_area_interativa = resultado[0]

                    # 2. Remover o estado associado ao progresso
                    cur.execute("""
                        DELETE FROM estado_area_interativa
                        WHERE identificador_area_interativa = %s AND identificador_progresso = %s;
                    """, (id_area_interativa, id_progresso))

                    # 3. Remover a própria área interativa
                    cur.execute("""
                        DELETE FROM area_interativa
                        WHERE identificador_area_interativa = %s;
                    """, (id_area_interativa,))

            return {'sucesso': True}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}
        


    def inserir_area_interativa_de_missao(self, id_area_origem, id_missao, x, y, largura, altura, id_progresso, metodo_ativacao, chave_imagem=None):
        """
        Insere uma nova área interativa de missão no banco de dados e seu estado associado ao progresso.
        Se a área interativa já estiver registrada no progresso atual, retorna seu identificador.
        """
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cur:
                    # 1. Verificar se já existe a área interativa COM estado no progresso atual
                    cur.execute("""
                        SELECT ai.identificador_area_interativa
                        FROM area_interativa ai
                        JOIN estado_area_interativa eai ON ai.identificador_area_interativa = eai.identificador_area_interativa
                        WHERE 
                            ai.identificador_area_origem = %s AND
                            ai.identificador_missao = %s AND
                            ai.x = %s AND ai.y = %s AND ai.largura = %s AND ai.altura = %s AND
                            ai.tipo_evento = 'missao' AND ai.metodo_ativacao = %s AND
                            eai.identificador_progresso = %s
                        LIMIT 1;
                    """, (id_area_origem, id_missao, x, y, largura, altura, metodo_ativacao, id_progresso))

                    resultado = cur.fetchone()

                    if resultado:
                        id_area_interativa = resultado[0]
                    else:
                        # 2. Inserir a nova área interativa
                        if chave_imagem:
                            cur.execute("""
                                INSERT INTO area_interativa
                                    (identificador_area_origem, identificador_missao, x, y, largura, altura, chave_imagem, tipo_evento, metodo_ativacao)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, 'missao', %s)
                                RETURNING identificador_area_interativa;
                            """, (id_area_origem, id_missao, x, y, largura, altura, chave_imagem, metodo_ativacao))
                        else:
                            cur.execute("""
                                INSERT INTO area_interativa
                                    (identificador_area_origem, identificador_missao, x, y, largura, altura, tipo_evento, metodo_ativacao)
                                VALUES (%s, %s, %s, %s, %s, %s, 'missao', %s)
                                RETURNING identificador_area_interativa;
                            """, (id_area_origem, id_missao, x, y, largura, altura, metodo_ativacao))
                        
                        id_area_interativa = cur.fetchone()[0]

                        # 3. Inserir o estado da área interativa no progresso atual
                        cur.execute("""
                            INSERT INTO estado_area_interativa (identificador_progresso, identificador_area_interativa)
                            VALUES (%s, %s);
                        """, (id_progresso, id_area_interativa))

            return {'sucesso': True, 'id_area_interativa': id_area_interativa}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}



    def remover_area_interativa(self, identificador_area_interativa, identificador_progresso):
        """
        Remove o estado de uma área interativa para um progresso específico.
        Se não houver mais nenhum estado vinculado, remove também a área interativa.
        """
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cur:
                    # 1. Remover o estado da área interativa apenas para o progresso informado
                    cur.execute("""
                        DELETE FROM estado_area_interativa
                        WHERE identificador_area_interativa = %s
                        AND identificador_progresso = %s;
                    """, (identificador_area_interativa, identificador_progresso))

                    # 2. Verificar se ainda existem estados associados a essa área
                    cur.execute("""
                        SELECT 1 FROM estado_area_interativa
                        WHERE identificador_area_interativa = %s
                        LIMIT 1;
                    """, (identificador_area_interativa,))
                    
                    if not cur.fetchone():
                        # 3. Se não houver mais estados, remover a área interativa
                        cur.execute("""
                            DELETE FROM area_interativa
                            WHERE identificador_area_interativa = %s;
                        """, (identificador_area_interativa,))
            
            return {'sucesso': True}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}



    def desativar_area_interativa(self, identificador_area_interativa, id_progresso):
        """
        Desativa uma área interativa no progresso informado.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    UPDATE estado_area_interativa
                    SET ativa = FALSE
                    WHERE identificador_area_interativa = %s
                    AND identificador_progresso = %s;
                """, (identificador_area_interativa, id_progresso))

            return {'sucesso': True}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}



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
                if "precisa esperar 15 minutos" in str(e):
                    self.conn.commit()
                    return {'sucesso': False, 'mensagem': "Erro: você precisa esperar 15 minutos para interagir novamente."}
                self.conn.rollback()
                print("[ERRO] Falha ao inserir em recompensa_de_exploracao:", str(e))
                return {'sucesso': False, 'mensagem': "Erro ao registrar tentativa de recompensa."}
            
            # Busca a área atual do jogador
            jogador = self.buscar_jogador(id_jogador)
            if not jogador:
                return {'sucesso': False, 'mensagem': "Erro: jogador não encontrado."}

            id_area_atual = jogador.identificador_area
            id_ilha = self.buscar_info_area(id_area_atual, jogador.identificador_progresso).identificador_ilha


            # Busca chance de sucesso da área interativa
            self.cursor.execute("""
                SELECT chance_sucesso
                FROM area_interativa
                WHERE identificador_area_interativa = %s;
            """, (id_area_interativa,))
            resultado = self.cursor.fetchone()
            if not resultado:
                return {'sucesso': False, 'mensagem': "Erro: área interativa não encontrada."}

            chance_sucesso = float(resultado.chance_sucesso)
            if random.random() > chance_sucesso:
                self.conn.commit()
                return {'sucesso': False, 'mensagem': "Tentativa registrada, mas nenhum item foi encontrado."}

            # Busca todos os itens possíveis da ilha atual
            consumiveis = self.buscar_itens_na_ilha(id_ilha, tipo="consumivel")
            nao_consumiveis = self.buscar_itens_na_ilha(id_ilha, tipo="nao_consumivel")
            todos_itens = consumiveis + nao_consumiveis

            if not todos_itens:
                return {'sucesso': False, 'mensagem': "Nenhum item disponível para ser recebido nesta ilha."}

            # Escolhe item aleatório
            item_escolhido = random.choice(todos_itens)
            id_item = item_escolhido.identificador_item

            # Pega ID da mochila do jogador
            mochila = self.buscar_inventario(id_jogador, tipo_inventario='moc', identificador_progresso=jogador.identificador_progresso)
            if not mochila:
                return {'sucesso': False, 'mensagem': "Erro: mochila do jogador não encontrada."}

            id_inventario = mochila[0].identificador_inventario

            # Adiciona o item
            sucesso = self.adicionar_item_ao_inventario(id_inventario, id_item)
            if sucesso:
                notificador.adicionar_item(item_escolhido.nome_item, 1)
                self.conn.commit()
                return {'sucesso': True, 'mensagem': f"Item '{item_escolhido.nome_item}' adicionado à mochila!"}
            else:
                return {'sucesso': False, 'mensagem': "Erro ao adicionar o item à mochila."}
        except Exception as e:
            self.conn.rollback()
            print(f"[ERRO] executar_recompensa_exploracao: {e}")
            return {'sucesso': False, 'mensagem': "Erro inesperado ao tentar coletar recompensa."}



    def buscar_arma_atributos(self, id_arma):
         consulta = """
            SELECT
                a.nome,
                a.raridade,
                a.preco_de_compra,
                a.preco_de_venda,
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
            SELECT identificador_consumivel, nome, descricao, raridade, local_encontrado, preco_de_compra, preco_de_venda, e_fabricavel, e_coletado
            FROM consumivel
            WHERE identificador_consumivel = %s;
        """
        return self.executar_query(consulta, (id_consumivel,), fetchone=True)



    def buscar_acessorio_atributos(self, id_acessorio):
        """
        Ver os atributos de um medicamento específico. (Adaptado para Acessorio)
        """
        consulta = """
            SELECT nome, tipo, raridade, preco_de_compra, preco_de_venda
            FROM acessorio
            WHERE identificador_acessorio = %s;
        """
        return self.executar_query(consulta, (id_acessorio,), fetchone=True)



    def buscar_nao_consumivel_atributos(self, id_nao_consumivel):
        """
        Ver os atributos de um utilizável específico. (Adaptado para Não-Consumível geral)
        """
        consulta = """
            SELECT nome, tipo, raridade, quantidade, preco_de_compra, preco_de_venda
            FROM nao_consumivel
            WHERE identificador_nao_consumivel = %s;
        """
        return self.executar_query(consulta, (id_nao_consumivel,), fetchone=True)



    def buscar_fruta_atributos(self, id_fruta):
        """
        Ver os atributos de uma fruta específica.
        """
        consulta = """
            SELECT f.nome, f.tipo, f.raridade, f.preco_de_compra, f.preco_de_venda, e.nome AS habilidade_nome, e.bravura
            FROM fruta f
            LEFT JOIN efeito e ON f.identificador_habilidade = e.identificador_efeito
            WHERE f.identificador_fruta = %s;
        """
        return self.executar_query(consulta, (id_fruta,), fetchone=True)



    def adquirir_novo_barco(self, identificador_progresso, tipo_barco):
        """
        Marca um barco como adquirido em um progresso específico
        """
        consulta = """
            UPDATE barco
            SET estado = 'adquirido'
            WHERE identificador_progresso = %s
                AND tipo_barco = %s;
        """
        self.executar_query(consulta, (identificador_progresso, tipo_barco))



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



    # ===============================================
    # Métodos de Operações com Inventário e Itens
    # ===============================================


    def buscar_inventario_vendedor(self, id_vendedor, id_progresso):
        """Busca o inventário de um vendedor específico."""
        query = """
            SELECT
                ii.identificador_item,
                ii.quantidade,
                ti.tipo as tipo_item,
                CASE
                    WHEN ti.tipo = 'con' THEN TRIM(c.nome)
                    WHEN ti.tipo = 'ncn' THEN TRIM(nc.nome)
                    WHEN ti.tipo = 'arm' THEN TRIM(a.nome)
                    WHEN ti.tipo = 'ace' THEN TRIM(ac.nome)
                    WHEN ti.tipo = 'fru' THEN TRIM(f.nome)
                END as nome_item,
                CASE
                    WHEN ti.tipo = 'con' THEN TRIM(c.descricao)
                    WHEN ti.tipo = 'ncn' THEN TRIM(nc.descricao)
                    WHEN ti.tipo = 'arm' THEN TRIM(a.descricao)
                    WHEN ti.tipo = 'ace' THEN TRIM(ac.descricao)
                    WHEN ti.tipo = 'fru' THEN TRIM(f.descricao)
                END as descricao,
                CASE
                    -- Prioriza o preço de compra original, se existir
                    WHEN ti.tipo = 'con' AND c.preco_de_compra IS NOT NULL THEN c.preco_de_compra
                    WHEN ti.tipo = 'ncn' AND nc.preco_de_compra IS NOT NULL THEN nc.preco_de_compra
                    WHEN ti.tipo = 'arm' THEN a.preco_de_compra
                    WHEN ti.tipo = 'ace' THEN ac.preco_de_compra
                    
                    -- AQUI ESTÁ A MÁGICA:
                    -- Se não houver preço de compra, crie um com base no preço de venda.
                    -- Vamos definir que a loja revende pelo dobro do preço que pagou.
                    WHEN ti.tipo = 'con' AND c.preco_de_venda IS NOT NULL THEN c.preco_de_venda * 2
                    WHEN ti.tipo = 'ncn' AND nc.preco_de_venda IS NOT NULL THEN nc.preco_de_venda * 2
                    WHEN ti.tipo = 'fru' AND f.preco_de_venda IS NOT NULL THEN f.preco_de_venda * 2
                    
                    -- Se o item realmente não tiver preço algum, ele não pode ser comprado.
                    ELSE NULL 
                END as preco_de_compra,
                CASE
                    WHEN ti.tipo = 'con' THEN c.preco_de_venda
                    WHEN ti.tipo = 'ncn' THEN nc.preco_de_venda
                    WHEN ti.tipo = 'arm' THEN NULL
                    WHEN ti.tipo = 'ace' THEN NULL
                    WHEN ti.tipo = 'fru' THEN f.preco_de_venda
                END as preco_de_venda
            FROM inventario inv
            JOIN item_inventario ii ON inv.identificador_inventario = ii.identificador_inventario
            JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item
            LEFT JOIN consumivel c ON ii.identificador_item = c.identificador_consumivel AND ti.tipo = 'con'
            LEFT JOIN nao_consumivel nc ON ii.identificador_item = nc.identificador_nao_consumivel AND ti.tipo = 'ncn'
            LEFT JOIN arma a ON ii.identificador_item = a.identificador_arma AND ti.tipo = 'arm'
            LEFT JOIN acessorio ac ON ii.identificador_item = ac.identificador_acessorio AND ti.tipo = 'ace'
            LEFT JOIN fruta f ON ii.identificador_item = f.identificador_fruta AND ti.tipo = 'fru'
            WHERE inv.identificador_personagem = %s
            AND inv.identificador_progresso = %s
            AND inv.tipo_inventario = 'moc'
            AND ii.quantidade > 0
        """
        return self.executar_query(query, (id_vendedor, id_progresso), fetchall=True)


        
    def realizar_compra(self, id_jogador, id_vendedor, id_inventario_jogador, id_inventario_vendedor, id_item, quantidade, preco_total, id_progresso):
        """
        Realiza uma transação de compra, movendo item do vendedor para o jogador
        e dinheiro do jogador para o vendedor.
        """
        if not self.conn:
            return {'sucesso': False, 'erro': 'Sem conexão com o banco.'}
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cur:
                    # 1. Debitar dinheiro do jogador
                    cur.execute(
                        "UPDATE jogador SET moedas_totais = moedas_totais - %s WHERE identificador_jogador = %s AND moedas_totais >= %s",
                        (preco_total, id_jogador, preco_total)
                    )
                    if cur.rowcount == 0:
                        raise Exception("Moedas insuficientes.")

                    # --- INÍCIO DA CORREÇÃO ---
                    # 2. Creditar dinheiro ao vendedor, limitando o total a 999.
                    # A função LEAST() garante que o valor nunca ultrapassará o limite da carteira.
                    cur.execute(
                        "UPDATE estado_habitante SET moedas_totais = LEAST(999, moedas_totais + %s) WHERE identificador_habitante = %s AND identificador_progresso = %s",
                        (preco_total, id_vendedor, id_progresso)
                    )
                    # --- FIM DA CORREÇÃO ---

                    # 3. Diminuir item do inventário do vendedor
                    cur.execute(
                        "UPDATE item_inventario SET quantidade = quantidade - %s WHERE identificador_inventario = %s AND identificador_item = %s AND quantidade >= %s",
                        (quantidade, id_inventario_vendedor, id_item, quantidade)
                    )
                    if cur.rowcount == 0:
                        raise Exception("Vendedor sem estoque suficiente.")

                    # 4. Adicionar item ao inventário do jogador
                    cur.execute(
                        "INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade) VALUES (%s, %s, %s) ON CONFLICT (identificador_inventario, identificador_item) DO UPDATE SET quantidade = item_inventario.quantidade + %s",
                        (id_inventario_jogador, id_item, quantidade, quantidade)
                    )

                    # 5. Registrar negociação
                    cur.execute(
                        "INSERT INTO negociacao (identificador_item, identificador_jogador, identificador_vendedor, quantidade, preco_final, tipo_negociacao) VALUES (%s, %s, %s, %s, %s, 'compra')",
                        (id_item, id_jogador, id_vendedor, quantidade, preco_total)
                    )
            return {'sucesso': True}
        except Exception as e:
            print(f"ERRO na transação de compra: {e}")
            return {'sucesso': False, 'erro': str(e)}



    def limpar_inventario_jogador(self, id_jogador):
            """
            Apaga todos os itens do inventário 'ger' de um jogador específico.
            """
            # Primeiro, encontra o ID do inventário do jogador
            id_inventario = self.buscar_id_inventario_por_personagem(id_jogador)
            if not id_inventario:
                print(f"Nenhum inventário encontrado para o jogador {id_jogador}, nada a limpar.")
                return True # Considera sucesso, pois não há o que limpar

            # Query para deletar todos os itens daquele inventário
            query = "DELETE FROM item_inventario WHERE identificador_inventario = %s"
            print(f"Limpando itens do inventário {id_inventario} para o jogador {id_jogador}.")
            
            # Usa uma transação para garantir a operação
            try:
                with self.conn.transaction():
                    with self.conn.cursor() as cur:
                        cur.execute(query, (id_inventario,))
                return True
            except psycopg.Error as e:
                print(f"DBManager ERRO ao limpar inventário do jogador '{id_jogador}': {e}")
                return False



    def adicionar_itens_iniciais_jogador(self, id_jogador):
        """
        Adiciona um conjunto pré-definido de itens ao inventário de um jogador.
        Ideal para ser usado ao iniciar um "Novo Jogo".
        """
        # Define os itens iniciais aqui (ID do item, quantidade)
        itens_iniciais = [
            ('con001', 3),  # 3x Fruta do Mar Azul
            ('con002', 2),  # 2x Fruta do Mar Vermelha
            ('ncn001', 1)   # 1x Abóbora Redonduda
        ]

        # Busca o ID do inventário do jogador
        id_inventario = self.buscar_id_inventario_por_personagem(id_jogador)
        if not id_inventario:
            print(f"ERRO: Não foi possível encontrar o inventário para {id_jogador} ao adicionar itens iniciais.")
            return False

        print(f"Adicionando itens iniciais ao inventário {id_inventario}...")
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cur:
                    for id_item, quantidade in itens_iniciais:
                        # Query que insere o item ou atualiza a quantidade se ele já existir
                        cur.execute("""
                            INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (identificador_inventario, identificador_item)
                            DO UPDATE SET quantidade = item_inventario.quantidade + EXCLUDED.quantidade;
                        """, (id_inventario, id_item, quantidade))
            print("Itens iniciais adicionados com sucesso.")
            return True
        except psycopg.Error as e:
            print(f"DBManager ERRO ao adicionar itens iniciais: {e}")
            return False

    

    def _resetar_inventarios_vendedores(self, cursor):
        """
        [PRIVADO] Limpa e repopula os inventários de todos os vendedores.
        Este método deve ser chamado DENTRO de uma transação existente.
        """
        print("-> Resetando inventários de vendedores...")
        inventarios_iniciais = {
            'ven001': [('arm001', 3), ('arm010', 2), ('ace001', 1)],
            'ven002': [('ncn001', 10), ('ncn002', 8), ('con012', 5)],
            'ven003': [('arm002', 2), ('ace002', 1)],
            'ven004': [('con020', 3), ('con021', 2)],
            'ven005': [('arm001', 5), ('con023', 10)]
        }
        
        cursor.execute("SELECT identificador_personagem, identificador_inventario FROM inventario WHERE identificador_personagem LIKE 'ven%%'")
        inventarios_vendedores = {row.identificador_personagem: row.identificador_inventario for row in cursor.fetchall()}
        
        if not inventarios_vendedores:
            print("-> Nenhum inventário de vendedor encontrado.")
            return

        # --- INÍCIO DA MODIFICAÇÃO ---
        # Limpa o inventário de cada vendedor individualmente para evitar o erro de sintaxe com 'IN'
        print("-> Limpando inventários antigos dos vendedores...")
        for id_inventario in inventarios_vendedores.values():
            cursor.execute("DELETE FROM item_inventario WHERE identificador_inventario = %s", (id_inventario,))
        # --- FIM DA MODIFICAÇÃO ---
        
        # Repopula os inventários
        for id_vendedor, itens in inventarios_iniciais.items():
            id_inventario = inventarios_vendedores.get(id_vendedor)
            if id_inventario:
                for id_item, quantidade in itens:
                    cursor.execute("""
                        INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
                        VALUES (%s, %s, %s)
                    """, (id_inventario, id_item, quantidade))
        print("-> Inventários dos vendedores preparados para o reset.")



    def _resetar_inventario_jogador(self, cursor, id_jogador):
        """
        [PRIVADO] Limpa o inventário do jogador e adiciona os itens iniciais.
        Este método deve ser chamado DENTRO de uma transação existente.
        """
        print(f"-> Resetando inventário do jogador {id_jogador}...")
        itens_iniciais = [
            ('con001', 3),
            ('con002', 2),
            ('ncn001', 1)
        ]
        
        id_inventario = self.buscar_id_inventario_por_personagem(id_jogador)
        if not id_inventario:
            print(f"-> Nenhum inventário para o jogador {id_jogador}, nada a fazer.")
            return

        cursor.execute("DELETE FROM item_inventario WHERE identificador_inventario = %s", (id_inventario,))
        
        for id_item, quantidade in itens_iniciais:
            # --- INÍCIO DA CORREÇÃO ---
            # Remova os comentários de dentro desta string
            cursor.execute("""
                INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
                VALUES (%s, %s, %s)
            """, (id_inventario, id_item, quantidade))
            # --- FIM DA CORREÇÃO ---
        print("-> Inventário do jogador preparado para o reset.")
        
        
        
    def equipar_arma(self, id_jogador, id_arma):
        """
        Equipa uma arma para um jogador, inserindo ou atualizando o registro
        na tabela jogador_equipamento. Usa a sintaxe ON CONFLICT (UPSERT).
        """
        print(f"Tentando equipar a arma {id_arma} para o jogador {id_jogador}...")
        query = """
            INSERT INTO jogador_equipamento (identificador_jogador, identificador_arma)
            VALUES (%s, %s)
            ON CONFLICT (identificador_jogador) 
            DO UPDATE SET identificador_arma = EXCLUDED.identificador_arma;
        """
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (id_jogador, id_arma))
            print(f"Arma {id_arma} equipada com sucesso para o jogador {id_jogador}.")
            return True
        except psycopg.Error as e:
            print(f"DBManager ERRO ao equipar arma: {e}")
            return False



    def usar_consumivel(self, id_jogador, id_item_consumivel):
        """
        Usa um item consumível, aplicando seus efeitos ao jogador e removendo
        uma unidade do inventário. A operação é feita em uma única transação.
        """
        print(f"Jogador {id_jogador} tentando usar o item {id_item_consumivel}...")
        
        # 1. Buscar os efeitos do consumível
        efeitos_query = """
            SELECT e.nome, e.valor
            FROM efeito_consumivel ec
            JOIN efeito e ON ec.identificador_efeito = e.identificador_efeito
            WHERE ec.identificador_consumivel = %s;
        """
        
        # 2. Buscar o ID do inventário do jogador
        id_inventario = self.buscar_id_inventario_por_personagem(id_jogador)
        if not id_inventario:
            print("ERRO: Inventário do jogador não encontrado.")
            return False

        try:
            with self.conn.transaction():
                with self.conn.cursor() as cursor:
                    # Verifica se o jogador possui o item
                    cursor.execute("""
                        SELECT quantidade FROM item_inventario 
                        WHERE identificador_inventario = %s AND identificador_item = %s AND quantidade > 0
                    """, (id_inventario, id_item_consumivel))
                    
                    if cursor.rowcount == 0:
                        print("ERRO: Jogador não possui o item para consumir.")
                        return False # A transação será desfeita (rollback)

                    # Busca os efeitos e o estado atual do jogador
                    cursor.execute(efeitos_query, (id_item_consumivel,))
                    efeitos = cursor.fetchall()
                    
                    cursor.execute("SELECT vida, vida_atual, energia FROM jogador WHERE identificador_jogador = %s", (id_jogador,))
                    jogador_stats = cursor.fetchone()

                    updates = []
                    for efeito in efeitos:
                        nome_efeito = efeito.nome.strip()
                        if nome_efeito == 'Cura':
                            # Garante que a vida atual não ultrapasse a vida máxima
                            nova_vida = min(jogador_stats.vida, jogador_stats.vida_atual + efeito.valor)
                            updates.append(f"vida_atual = {nova_vida}")
                        elif nome_efeito == 'Energia':
                            # Assumindo que o campo 'energia' representa tanto a energia atual quanto a máxima.
                            # Se você adicionar um campo 'energia_maxima', a lógica seria min(jogador_stats.energia_maxima, ...)
                            nova_energia = min(jogador_stats.energia, jogador_stats.energia + efeito.valor) # Usa jogador_stats.energia
                            updates.append(f"energia = {nova_energia}") # Atualiza o campo 'energia'
                    # Aplica os efeitos no jogador, se houver algum
                    if updates:
                        update_jogador_query = f"UPDATE jogador SET {', '.join(updates)} WHERE identificador_jogador = %s"
                        cursor.execute(update_jogador_query, (id_jogador,))
                        print(f"Efeitos aplicados ao jogador {id_jogador}.")

                    # Remove uma unidade do item do inventário
                    cursor.execute("""
                        UPDATE item_inventario 
                        SET quantidade = quantidade - 1 
                        WHERE identificador_inventario = %s AND identificador_item = %s
                    """, (id_inventario, id_item_consumivel))

                    # Opcional: Remove o item se a quantidade chegar a zero
                    cursor.execute("""
                        DELETE FROM item_inventario 
                        WHERE identificador_inventario = %s AND identificador_item = %s AND quantidade = 0
                    """, (id_inventario, id_item_consumivel))
            
            print(f"Item {id_item_consumivel} consumido com sucesso.")
            return True

        except psycopg.Error as e:
            print(f"DBManager ERRO ao usar consumível: {e}")
            return False



    def realizar_venda(self,
                  jogador_id,
                  vendedor_id,
                  id_inventario_jogador,
                  id_inventario_vendedor,
                  identificador_item,
                  quantidade,
                  preco_total,
                  id_progresso):
        """
        Realiza a venda de um item do jogador para o vendedor
        """
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cur:
                    # Remova esta consulta que está causando o erro - não precisamos obter o preço de compra
                    # já que ele não é usado no restante do método
                    
                    # 1. Remover do inventário do jogador
                    cur.execute(
                        """UPDATE item_inventario 
                        SET quantidade = quantidade - %s 
                        WHERE identificador_inventario = %s AND identificador_item = %s""", 
                        (quantidade, id_inventario_jogador, identificador_item))

                    # 2. Adicionar ao inventário do vendedor
                    cur.execute(
                        """INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (identificador_inventario, identificador_item)
                        DO UPDATE SET quantidade = item_inventario.quantidade + %s""", 
                        (id_inventario_vendedor, identificador_item, quantidade, quantidade))
                    
                    # 3. Atualizar moedas do jogador
                    cur.execute(
                        """UPDATE jogador 
                        SET moedas_totais = moedas_totais + %s 
                        WHERE identificador_jogador = %s""", 
                        (preco_total, jogador_id))

                    # 4. Atualizar moedas do vendedor
                    cur.execute(
                        """UPDATE estado_habitante 
                        SET moedas_totais = moedas_totais - %s 
                        WHERE identificador_habitante = %s AND identificador_progresso = %s""", 
                        (preco_total, vendedor_id, id_progresso))

                    # 5. Remove itens com quantidade 0
                    cur.execute(
                        "DELETE FROM item_inventario WHERE quantidade <= 0")
                    
                    # 6. Registrar negociação
                    cur.execute(
                        """
                        INSERT INTO negociacao
                            (identificador_item, identificador_jogador, identificador_vendedor, quantidade, preco_final, tipo_negociacao)
                        VALUES
                            (%s, %s, %s, %s, %s, 'venda')
                        """, 
                        (identificador_item, jogador_id, vendedor_id, quantidade, preco_total))


            return {'sucesso': True}
        except Exception as e:
            return {'sucesso': False, 'erro': str(e)}
        


    def buscar_arma_equipada(self, id_jogador):
        """
        Busca a arma atualmente equipada por um jogador.
        Retorna um objeto com os detalhes da arma ou None se nenhuma estiver equipada.
        """
        query = """
            SELECT
                je.identificador_arma AS identificador_item,
                'arm' AS tipo_item,
                TRIM(a.nome) AS nome_item,
                TRIM(a.descricao) AS descricao,
                a.raridade,
                a.preco_de_compra
            FROM jogador_equipamento je
            JOIN arma a ON je.identificador_arma = a.identificador_arma
            WHERE je.identificador_jogador = %s;
        """
        return self.executar_query(query, (id_jogador,), fetchone=True)


        
    def equipar_acessorio(self, id_jogador, id_acessorio):
        """
        Equipa um acessório para um jogador, inserindo ou atualizando o registro
        na tabela jogador_equipamento. Usa a sintaxe ON CONFLICT (UPSERT).
        """
        print(f"Tentando equipar o acessório {id_acessorio} para o jogador {id_jogador}...")
        query = """
            INSERT INTO jogador_equipamento (identificador_jogador, identificador_acessorio)
            VALUES (%s, %s)
            ON CONFLICT (identificador_jogador) 
            DO UPDATE SET identificador_acessorio = EXCLUDED.identificador_acessorio;
        """
        try:
            with self.conn.transaction():
                with self.conn.cursor() as cursor:
                    cursor.execute(query, (id_jogador, id_acessorio))
            print(f"Acessório {id_acessorio} equipado com sucesso para o jogador {id_jogador}.")
            return True
        except psycopg.Error as e:
            print(f"DBManager ERRO ao equipar acessório: {e}")
            return False
        

        
    def desequipar_arma(self, id_jogador):
            """
            Desequipa a arma de um jogador, definindo o identificador_arma como NULL
            na tabela jogador_equipamento.
            """
            print(f"Tentando desequipar arma para o jogador {id_jogador}...")
            query = """
                UPDATE jogador_equipamento
                SET identificador_arma = NULL
                WHERE identificador_jogador = %s;
            """
            try:
                with self.conn.transaction():
                    with self.conn.cursor() as cursor:
                        cursor.execute(query, (id_jogador,))
                print(f"Arma desequipada com sucesso para o jogador {id_jogador}.")
                return True
            except psycopg.Error as e:
                print(f"DBManager ERRO ao desequipar arma: {e}")
                return False



    # ===============================================
    # Métodos de Operações com Habilidades
    # ===============================================

    def buscar_habilidades_por_arma(self, id_arma):
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
            FROM habilidade_arma
                JOIN habilidade   ON  habilidade.identificador_habilidade = habilidade_arma.identificador_habilidade
            	LEFT JOIN efeito  ON  efeito.identificador_efeito = habilidade.identificador_efeito
            WHERE habilidade_arma.identificador_arma = %s;
        """
        return self.executar_query(consulta, (id_arma,), fetchall=True)



    def buscar_habilidades_por_fruta(self, id_arma):
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
            FROM habilidade_fruta
                JOIN habilidade   ON  habilidade.identificador_habilidade = habilidade_fruta.identificador_habilidade
            	LEFT JOIN efeito  ON  efeito.identificador_efeito = habilidade.identificador_efeito
            WHERE habilidade_fruta.identificador_fruta = %s;
        """
        return self.executar_query(consulta, (id_arma,), fetchall=True)
