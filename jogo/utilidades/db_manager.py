
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
        if self.cursor:
            self.cursor.close()
        if self.conn:
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
    def buscar_jogador(self, id_jogador):
        """Busca os dados de um jogador pelo ID."""
        query = """
            SELECT
                identificador_jogador,
                identificador_area,
                nome,
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
    
    # ===============================================
    # Métodos de Operações com Inventário e Itens
    # ===============================================

    def buscar_inventario_jogador(self, id_jogador):
        """Acessa o inventário de um jogador e seus atributos."""
        query = """
            SELECT id_inventario, nome, id_jogador
            FROM inventario
            WHERE id_jogador = %s;
        """
        return self.executar_query(query, (id_jogador,), fetchone=True)

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
            SELECT  il.identificador_instancia_lacaio,
                    il.coordenada_x AS x,
                    il.coordenada_y AS y,
                    il.vida_atual,

                    l.identificador_lacaio,
                    TRIM(l.nome) AS nome_lacaio,
                    TRIM(l.descricao) AS descricao_lacaio,
                    l.vida AS vida_total,
                    l.nivel,
                    l.experiencia,
                    l.tempo_reacao,

                    h.nome AS nome_habilidade,
                    h.dano,
                    h.tipo_de_habilidade,
                    h.tipo_de_ataque,

                    ti.identificador_item,
                    ti.tipo AS tipo_item,

                    consumivel.nome AS nome_consumivel,
                    nao_consumivel.nome AS nome_nao_consumivel

                FROM instancia_lacaio il
                JOIN lacaio l ON il.identificador_lacaio = l.identificador_lacaio
                LEFT JOIN habilidade h ON l.identificador_habilidade = h.identificador_habilidade

                LEFT JOIN inventario inv ON inv.identificador_personagem = l.identificador_lacaio
                LEFT JOIN item_inventario ii ON ii.identificador_inventario = inv.identificador_inventario
                LEFT JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item

                -- subtipos possíveis do item
                LEFT JOIN consumivel ON consumivel.identificador_consumivel = ti.identificador_item
                LEFT JOIN nao_consumivel ON nao_consumivel.identificador_nao_consumivel = ti.identificador_item

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
    
    def buscar_areas_interativas_da_area(self, id_area):
        """
        Busca todos os elementos espaciaias do tipo "Área interativa" na área atual.
        """
        consulta = """
            SELECT *
            FROM area_interativa
            WHERE identificador_area = %s;
        """
        return self.executar_query(consulta, (id_area,), fetchall=True)

    def buscar_conexoes_ilha(self, id_ilha_origem):
        """
        Ver todas as conexões de um lugar X. (Adaptado para Ilhas via corredor_maritimo)
        """
        query = """
            SELECT i.identificador_ilha, TRIM(i.nome) AS nome_ilha, i.visitada
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

