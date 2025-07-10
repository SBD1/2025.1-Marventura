
import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import namedtuple_row

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
        # --- INÍCIO DA MODIFICAÇÃO ---
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
        
        DBManager._instance = None # Reseta a instância Singleton

    def executar_query(self, query, params=None, fetchone=False, fetchall=False):
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
            self.conn.rollback()
            print(f"DBManager ERRO ao executar query '{query}': {e}")
            return False

    # ===============================================
    # Métodos de Operações com Jogador
    # ===============================================
    def carregar_dados_do_progresso(self, id_jogador):
        """
        Retorna uma tupla com os dados do jogador, da área atual e dos inimigos na área (se houver arena).
        :return: (jogador, area, inimigos ou None)
        """
        #print(f"\n--- Carregando dados do jogador '{id_jogador}' ---\n")

        jogador = self.buscar_jogador(id_jogador)
        if not jogador:
            #print(f"Jogador com ID '{id_jogador}' não encontrado.")
            return None, None, None

        #print(f"Jogador encontrado: {jogador}")

        area = self.buscar_info_area(jogador.identificador_area)
        #print(f"\nInformações da área atual: {area}")

        ilha = self.buscar_info_ilha(area.identificador_ilha)

        return jogador, ilha, area

    def buscar_jogador(self, id_jogador):
        """Busca os dados de um jogador pelo ID."""
        query = """
            SELECT
                identificador_jogador,
                identificador_area,
                TRIM(nome) AS nome, -- ADICIONE O TRIM() AQUI
                TRIM(descricao) AS descricao,
                coordenada_x,
                coordenada_y,
                TRIM(orientacao) AS orientacao,
                energia,
                vida,
                nivel,
                sorte,
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

    def salvar_novo_jogador(self, nome, id_personagem, id_habilidade, id_mapa, energia, vida, nivel, sorte, vida_atual, dano_base, experiencia_atual, coord_x, coord_y):
        """Insere um novo jogador no banco de dados e retorna o ID gerado."""
        query = """
            INSERT INTO jogador (
                nome, id_personagem, id_habilidade, id_mapa, energia, vida, nivel, sorte,
                vida_atual, dano_base, experiencia_atual, coordenada_x, coordenada_y
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_jogador;
        """
        params = (nome, id_personagem, id_habilidade, id_mapa, energia, vida, nivel, sorte, vida_atual, dano_base, experiencia_atual, coord_x, coord_y)
        result = self.executar_query(query, params, fetchone=True)
        return result[0] if result else None
    
    def salvar_progresso_jogador(self, id_jogador, vida_atual, experiencia_atual, nivel, moedas_totais, coordenada_x, coordenada_y, orientacao, identificador_area):
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
                vida_atual = %s,
                experiencia_atual = %s,
                nivel = %s,
                moedas_totais = %s,
                coordenada_x = %s,
                coordenada_y = %s,
                orientacao = %s,
                identificador_area = %s
            WHERE identificador_jogador = %s;
        """
        params = (vida_atual, experiencia_atual, nivel, moedas_totais, coordenada_x, coordenada_y, orientacao, identificador_area, id_jogador)
        
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

    # ===============================================
    # Métodos de Operações com Inventário e Itens
    # ===============================================

    def buscar_inventario_jogador(self, id_jogador):
        """Busca os itens no inventário de um jogador específico."""
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
                    WHEN ti.tipo = 'con' THEN c.preco_de_compra
                    WHEN ti.tipo = 'ncn' THEN nc.preco_de_compra
                    WHEN ti.tipo = 'arm' THEN a.preco_de_compra
                    WHEN ti.tipo = 'ace' THEN ac.preco_de_compra
                    WHEN ti.tipo = 'fru' THEN NULL
                END as preco_compra,
                CASE
                    WHEN ti.tipo = 'con' THEN c.preco_de_venda
                    WHEN ti.tipo = 'ncn' THEN nc.preco_de_venda
                    WHEN ti.tipo = 'arm' THEN NULL
                    WHEN ti.tipo = 'ace' THEN NULL
                    WHEN ti.tipo = 'fru' THEN f.preco_de_venda
                END as preco_venda
            FROM inventario inv
            JOIN item_inventario ii ON inv.identificador_inventario = ii.identificador_inventario
            JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item
            LEFT JOIN consumivel c ON ii.identificador_item = c.identificador_consumivel AND ti.tipo = 'con'
            LEFT JOIN nao_consumivel nc ON ii.identificador_item = nc.identificador_nao_consumivel AND ti.tipo = 'ncn'
            LEFT JOIN arma a ON ii.identificador_item = a.identificador_arma AND ti.tipo = 'arm'
            LEFT JOIN acessorio ac ON ii.identificador_item = ac.identificador_acessorio AND ti.tipo = 'ace'
            LEFT JOIN fruta f ON ii.identificador_item = f.identificador_fruta AND ti.tipo = 'fru'
            WHERE inv.identificador_personagem = %s
            AND inv.tipo_inventario = 'ger'
            AND ii.quantidade > 0
        """
        return self.executar_query(query, (id_jogador,), fetchall=True)

    def buscar_id_inventario_por_personagem(self, id_personagem):
        """Busca o ID do inventário 'ger' de um personagem específico."""
        query = "SELECT identificador_inventario FROM inventario WHERE identificador_personagem = %s AND tipo_inventario = 'ger'"
        resultado = self.executar_query(query, (id_personagem,), fetchone=True)
        return resultado.identificador_inventario if resultado else None

    def criar_inventario(self, id_jogador, nome_inventario="Inventário Padrão"):
        """Cria um novo inventário para um jogador e retorna o ID do inventário."""
        query = """
            INSERT INTO inventario (id_jogador, nome)
            VALUES (%s, %s)
            RETURNING id_inventario;
        """
        result = self.executar_query(query, (id_jogador, nome_inventario), fetchone=True)
        return result[0] if result else None

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

    def adicionar_item_ao_inventario(self, id_inventario, identificador_item_tipo):
        """Adiciona um tipo de item ao inventário."""
        query = """
            INSERT INTO iteminventario (id_inventario, identificador_item)
            VALUES (%s, %s);
        """
        return self.executar_query(query, (id_inventario, identificador_item_tipo))

    def remover_item_do_inventario(self, id_inventario, identificador_item_tipo):
        """Remove um tipo de item específico do inventário."""
        query = """
            DELETE FROM iteminventario
            WHERE id_inventario = %s AND identificador_item = %s;
        """
        return self.executar_query(query, (id_inventario, identificador_item_tipo))
    
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
    
    def buscar_lacaios_por_area(self, identificador_area):
        """
        Busca todos os lacaios em uma área específica.
        """
        consulta = """
            SELECT 
                il.identificador_instancia_lacaio,
                il.coordenada_x AS x,
                il.coordenada_y AS y,
                il.vida_atual,
                il.moedas_totais,

                l.identificador_lacaio,
                TRIM(l.nome) AS nome_lacaio,
                TRIM(l.descricao) AS descricao_lacaio,
                l.vida AS vida_total,
                l.nivel,
                l.experiencia,

                h.identificador_habilidade,
                h.nome AS nome_habilidade,
                h.dano,
                h.tipo_de_ataque,
                h.tipo_de_alvo,

                ti.identificador_item,
                ti.tipo AS tipo_item,

                consumivel.nome AS consumivel_saqueavel,
                nao_consumivel.nome AS nao_consumivel_saqueavel

            FROM instancia_lacaio il
            JOIN lacaio l ON il.identificador_lacaio = l.identificador_lacaio

            -- Habilidades do lacaio (1 ou mais)
            LEFT JOIN habilidade_personagem hp ON hp.identificador_personagem = l.identificador_lacaio
            LEFT JOIN habilidade h ON h.identificador_habilidade = hp.identificador_habilidade

            -- Inventário geral do lacaio
            LEFT JOIN inventario inv ON inv.identificador_personagem = l.identificador_lacaio AND inv.tipo_inventario = 'ger'
            LEFT JOIN item_inventario ii ON ii.identificador_inventario = inv.identificador_inventario
            LEFT JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item

            -- Subtipos possíveis do item
            LEFT JOIN consumivel ON consumivel.identificador_consumivel = ti.identificador_item
            LEFT JOIN nao_consumivel ON nao_consumivel.identificador_nao_consumivel = ti.identificador_item

            -- Restrição pela área atual do jogador
            WHERE il.identificador_area = %s;
        """
        return self.executar_query(consulta, (identificador_area,), fetchall=True)
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

    # ===============================================
    # Métodos de Operações com Locais (Mapas, Ilhas, Salas)
    # ===============================================

    def buscar_info_ilha(self, id_ilha):
        """
        Ver (nome, descrição, motim) de uma prisão X. (Adaptado para Mapa)
        """
        query = """
            SELECT
                identificador_ilha,
                TRIM(nome) AS nome,
                visitada
            FROM ilha WHERE identificador_ilha = %s;
            """
        return self.executar_query(query, (id_ilha,), fetchone=True)
    
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
    
    def buscar_info_area(self, id_area):
        """
        Busca informações de uma sala específica
        """
        query = """
            SELECT
                identificador_area,
                identificador_ilha,
                TRIM(nome) AS nome,
                TRIM(tipo_area) AS tipo_area,
                TRIM(chave_imagem_fundo) AS chave_imagem_fundo,
                TRIM(chave_imagem_frente) AS chave_imagem_frente,
                visitada
            FROM area
            WHERE identificador_area = %s;
        """
        return self.executar_query(query, (id_area,), fetchone=True)
    
    def buscar_porto_por_ilha(self, id_ilha):
        """
        Busca informações de uma sala específica que é o porto da ilha
        """
        query = """
            SELECT
                identificador_area,
                identificador_ilha,
                TRIM(nome) AS nome,
                TRIM(tipo_area) AS tipo_area,
                TRIM(chave_imagem_fundo) AS chave_imagem_fundo,
                TRIM(chave_imagem_frente) AS chave_imagem_frente,
                visitada
            FROM area
            WHERE identificador_ilha = %s AND tipo_area = 'Porto';
        """
        return self.executar_query(query, (id_ilha,), fetchone=True)
    
    def buscar_areas_interativas_da_area(self, id_area):
        """
        Busca todos os elementos espaciaias do tipo "Área interativa" na área atual.
        """
        consulta = """
            SELECT
                identificador_area_interativa,
                identificador_area,
                TRIM(chave_imagem) AS chave_imagem,
                x,
                y,
                largura,
                altura,
                TRIM(tipo_evento) AS tipo_evento
            FROM area_interativa
            WHERE identificador_area = %s;
        """
        return self.executar_query(consulta, (id_area,), fetchall=True)
    
    def buscar_eventos_embarcar(self, id_area_interativa):
        """
        Busca todos os eventos embarcar acionados por uma área interativa específica.
        """
        consulta = """
            SELECT
                e.identificador_evento,
                TRIM(e.tipo_evento) AS tipo_evento,

                -- Campos para embarcar
                e.identificador_porto_destino,

                -- Campos comuns
                e.ponto_geracao_x,
                e.ponto_geracao_y,
                TRIM(e.orientacao) AS orientacao


            FROM area_interativa_evento aie
            JOIN evento e ON e.identificador_evento = aie.identificador_evento
            WHERE aie.identificador_area_interativa = %s;
        """
        return self.executar_query(consulta, (id_area_interativa,), fetchall=True)
    
    def buscar_eventos_mudar_area(self, id_area_interativa):
        """
        Busca o evento mudar_area acionado por uma área interativa específica.
        """
        consulta = """
            SELECT
                e.identificador_evento,
                TRIM(e.tipo_evento) AS tipo_evento,
                e.ponto_geracao_x,
                e.ponto_geracao_y,
                TRIM(e.orientacao) AS orientacao,

                a_dest.identificador_area AS area_destino

            FROM area_interativa_evento aie
            JOIN evento e ON e.identificador_evento = aie.identificador_evento
            JOIN area_interativa ai ON ai.identificador_area_interativa = aie.identificador_area_interativa

            -- Detecta a área de destino real com base na área da área_interativa
            JOIN area a_dest ON a_dest.identificador_area = 
                CASE
                    WHEN e.identificador_area_a = ai.identificador_area THEN e.identificador_area_b
                    ELSE e.identificador_area_a
                END

            WHERE aie.identificador_area_interativa = %s;
        """
        return self.executar_query(consulta, (id_area_interativa,), fetchone=True)

    def buscar_conexoes_ilha(self, id_ilha_origem):
        """
        Ver todas as conexões de um lugar X. (Adaptado para Ilhas via corredor_maritimo)
        """
        query = """
            SELECT i.identificador_ilha, TRIM(i.nome) AS nome, i.visitada
                FROM conexao_entre_ilhas c
                JOIN ilha i ON i.identificador_ilha = 
                    CASE
                        WHEN c.identificador_ilha_a = %s THEN c.identificador_ilha_b
                        ELSE c.identificador_ilha_a
                    END
                WHERE %s IN (c.identificador_ilha_a, c.identificador_ilha_b);

        """
        return self.executar_query(query, (id_ilha_origem, id_ilha_origem), fetchall=True)

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


# Dentro da classe DBManager em utilidades/db_manager.py

    def buscar_vendedor_por_area(self, id_area):
        """Busca vendedores em uma área específica."""
        query = """
            SELECT
                h.identificador_habitante,
                TRIM(h.nome) as nome,
                TRIM(h.descricao) as descricao,
                h.coordenada_x,
                h.coordenada_y,
                h.moedas_totais
            FROM habitante h
            WHERE h.identificador_area = %s
            AND h.tipo_habitante = 'ven'
        """
        return self.executar_query(query, (id_area,), fetchall=True)

    def buscar_inventario_vendedor(self, id_vendedor):
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
                END as preco_compra,
                CASE
                    WHEN ti.tipo = 'con' THEN c.preco_de_venda
                    WHEN ti.tipo = 'ncn' THEN nc.preco_de_venda
                    WHEN ti.tipo = 'arm' THEN NULL
                    WHEN ti.tipo = 'ace' THEN NULL
                    WHEN ti.tipo = 'fru' THEN f.preco_de_venda
                END as preco_venda
            FROM inventario inv
            JOIN item_inventario ii ON inv.identificador_inventario = ii.identificador_inventario
            JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item
            LEFT JOIN consumivel c ON ii.identificador_item = c.identificador_consumivel AND ti.tipo = 'con'
            LEFT JOIN nao_consumivel nc ON ii.identificador_item = nc.identificador_nao_consumivel AND ti.tipo = 'ncn'
            LEFT JOIN arma a ON ii.identificador_item = a.identificador_arma AND ti.tipo = 'arm'
            LEFT JOIN acessorio ac ON ii.identificador_item = ac.identificador_acessorio AND ti.tipo = 'ace'
            LEFT JOIN fruta f ON ii.identificador_item = f.identificador_fruta AND ti.tipo = 'fru'
            WHERE inv.identificador_personagem = %s
            AND inv.tipo_inventario = 'ger'
            AND ii.quantidade > 0
        """
        return self.executar_query(query, (id_vendedor,), fetchall=True)

    def realizar_compra(self, id_jogador, id_vendedor, id_inventario_jogador, id_inventario_vendedor, id_item, quantidade, preco_total):
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

                    # 2. Creditar dinheiro ao vendedor
                    cur.execute(
                        "UPDATE habitante SET moedas_totais = moedas_totais + %s WHERE identificador_habitante = %s",
                        (preco_total, id_vendedor)
                    )

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
        
    def realizar_compra(self, id_jogador, id_vendedor, id_inventario_jogador, id_inventario_vendedor, id_item, quantidade, preco_total):
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
                        "UPDATE habitante SET moedas_totais = LEAST(999, moedas_totais + %s) WHERE identificador_habitante = %s",
                        (preco_total, id_vendedor)
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

    # ===============================================
    # Métodos de Operações com Inventário e Itens
    # ===============================================
    
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

    def _carregar_dados_inventario(self):
        inventario_completo = self.db_manager.buscar_inventario_jogador(self.jogador_id)
        self.dados_jogador = self.db_manager.buscar_jogador(self.jogador_id)

        # Filtra o inventário em listas separadas
        self.lista_armas = [item for item in inventario_completo if item.tipo_item == 'arm']
        self.lista_acessorios = [item for item in inventario_completo if item.tipo_item == 'ace']
        self.lista_consumiveis = [item for item in inventario_completo if item.tipo_item == 'con']
        self.lista_outros = [item for item in inventario_completo if item.tipo_item == 'ncn']

        self._resetar_selecao()
        
        
        
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
                  preco_total):
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
                        """UPDATE habitante 
                        SET moedas_totais = moedas_totais - %s 
                        WHERE identificador_habitante = %s""", 
                        (preco_total, vendedor_id))

                    # 5. Remove itens com quantidade 0
                    cur.execute(
                        "DELETE FROM item_inventario WHERE quantidade <= 0")

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
