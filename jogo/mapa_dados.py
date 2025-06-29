# mapa_dados.py

from utilidades.constantes import *

def get_ilha_por_mapa_id(mapa_id):
    """
    Retorna o ID da ilha à qual um determinado mapa pertence.
    :param mapa_id: O ID (string) do mapa.
    :return: O ID da ilha (string), ou None se o mapa não for encontrado em nenhuma ilha.
    """
    for ilha_id, dados_ilha in dados_das_ilhas.items():
        if 'areas' in dados_ilha and mapa_id in dados_ilha['areas']:
            return ilha_id
    return None

def get_ilhas_vizinhas(id_mapa_atual):
    """
    Retorna uma lista dos nomes das ilhas vizinhas à ilha do mapa atual.
    :param id_mapa_atual: O ID (string) do mapa atual.
    :return: Uma lista de strings com os nomes das ilhas vizinhas, ou uma lista vazia se não encontrado.
    """
    ilha_atual_id = get_ilha_por_mapa_id(id_mapa_atual)
    if ilha_atual_id and ilha_atual_id in dados_das_ilhas:
        return dados_das_ilhas[ilha_atual_id].get('ilhas_vizinhas', [])
    return []

# Dicionário para armazenar os dados de configuração de cada mapa do jogo.
# Cada chave é o ID único do mapa.
dados_das_ilhas = {
    'Ilha de Borabóia': {
        'nome': 'Ilha de Borabóia',
        'visitada': False,
        'ilhas_vizinhas': ['Cidade de Lurien', 'Cactuaraquara'],
        'areas':  [
            ID_MAPA_CAMPO_COSTA_OESTE,
            ID_MAPA_CAMPO_VILA,
            ID_MAPA_CAMPO_LOJA,
            ID_MAPA_CAMPO_COSTA_LESTE
        ],
        'pier': ID_MAPA_CAMPO_COSTA_LESTE,
    },
    'Cidade de Lurien': {
        'nome': 'Cidade de Lurien',
        'visitada': False,
        'ilhas_vizinhas': ['Ilha de Borabóia', 'Ilha Glacial de Frimora', 'Quartel Naval D-57'],
        'areas': [
            ID_MAPA_CIDADE_PORTO,
            ID_MAPA_CIDADE_CENTRO,
            ID_MAPA_CIDADE_SUBURBIO,
            ID_MAPA_CIDADE_PRACA,
            ID_MAPA_CIDADE_LOJA,
        ],
        'pier': ID_MAPA_CIDADE_PORTO,
    },
    'Ilha Glacial de Frimora': {
        'nome': 'Ilha Glacial de Frimora',
        'visitada': False,
        'ilhas_vizinhas': ['Cidade de Lurien', 'Cactuaraquara', 'Nublária'],
        'areas': [
            #ID_MAPA_NEVE_COSTA_OESTE,
            ID_MAPA_NEVE_VILA,
            ID_MAPA_NEVE_COZINHA,
        ],
        'pier': ID_MAPA_NEVE_VILA,
    },
    'Cactuaraquara': {
        'nome': 'Cactuaraquara',
        'visitada': False,
        'ilhas_vizinhas': ['Ilha de Borabóia', 'Ilha Glacial de Frimora'],
        'areas': [
            ID_MAPA_DESERTO_COSTA_OESTE,
            ID_MAPA_DESERTO_VILA,
            ID_MAPA_DESERTO_LOJA,
            ID_MAPA_DESERTO_COSTA_LESTE
        ],
        'pier': ID_MAPA_DESERTO_COSTA_LESTE,
    },
    'Nublária': {
        'nome': 'Nublária',
        'visitada': False,
        'ilhas_vizinhas': ['Ilha Glacial de Frimora', 'Quartel Naval D-57'],
        'areas': [
            ID_MAPA_ASSOMBRADA_COSTA_OESTE,
            ID_MAPA_ASSOMBRADA_VILA,
            ID_MAPA_ASSOMBRADA_LOJA,
        ],
        'pier': ID_MAPA_ASSOMBRADA_COSTA_OESTE,
    },
    'Quartel Naval D-57': {
        'nome': 'Quartel Naval D-57',
        'visitada': False,
        'ilhas_vizinhas': ['Cidade de Lurien', 'Nublária'],
        'areas': [
            ID_MAPA_FORTALEZA_PORTO,
            ID_MAPA_FORTALEZA_INTERIOR,
            ID_MAPA_FORTALEZA_LOJA,
        ],
        'pier': ID_MAPA_FORTALEZA_PORTO,
    },
}

dados_das_salas = {
    ID_MAPA_CAMPO_COSTA_OESTE: {
        'nome': 'Costa Oeste',
        'chave_cenario': CHAVE_CENARIO_CAMPO_COSTA_OESTE, # Chave do gerenciador de recursos para a imagem de fundo deste mapa
        'chave_camada_superior': CHAVE_CENARIO_CAMPO_COSTA_OESTE_CAMADA_SUPERIOR, # Chave do gerenciador de recursos para a camada superior deste mapa
        'obstaculos': [],
        'caminhos': [
            {'x': 3329, 'y': 0, 'largura': 1144, 'altura': 600, 'tipo_terreno': 'arena'},
            {'x': 4473, 'y': 197, 'largura': 36, 'altura': 180, 'tipo_terreno': 'normal'},
            {'x': 826, 'y': 216, 'largura': 2503, 'altura': 154, 'tipo_terreno': 'normal'},
            {'x': 826, 'y': 370, 'largura': 150, 'altura': 230, 'tipo_terreno': 'normal'},
            {'x': 339, 'y': 438, 'largura': 487, 'altura': 162, 'tipo_terreno': 'normal'},

        ],
        'npcs': [
            # Lista de NPCs para este mapa.
            # Ex: {'tipo': 'npc_aldeao', 'x': 500, 'y': 400, 'dialogo_id': 'ilha_inicial_intro'}
        ],
        'inimigos': [
            {
                'tipo': INIMIGO_LOBO,
                'x': 3600, 'y': 427,
                'velocidade_caminhada': 150, # Exemplo: 1.5 pixels/frame
                'velocidade_corrida': 300,   # Exemplo: 3.5 pixels/frame
                'alcance_visao': 200,
                'angulo_visao_graus': 90,
                'tempo_reacao_ms': 750,      # 0.75 segundos para reagir
                'imagem_chave': INIMIGO_LOBO
            },
            {
                'tipo': INIMIGO_LOBO,
                'x': 3935, 'y': 208,
                'velocidade_caminhada': 150, # Exemplo: 1.5 pixels/frame
                'velocidade_corrida': 300,   # Exemplo: 3.5 pixels/frame
                'alcance_visao': 200,
                'angulo_visao_graus': 90,
                'tempo_reacao_ms': 750,      # 0.75 segundos para reagir
                'imagem_chave': INIMIGO_LOBO
            },
            {
                'tipo': INIMIGO_CORVO,
                'x': 3430, 'y': 55,
                'velocidade_caminhada': 150,
                'velocidade_corrida': 300,
                'alcance_visao': 200,
                'angulo_visao_graus': 120,
                'tempo_reacao_ms': 1200,     # 1.2 segundos para reagir (mais lento)
                'imagem_chave': INIMIGO_CORVO
            },
            {
                'tipo': INIMIGO_CORVO,
                'x': 4273, 'y': 412,
                'velocidade_caminhada': 150,
                'velocidade_corrida': 300,
                'alcance_visao': 200,
                'angulo_visao_graus': 120,
                'tempo_reacao_ms': 1200,     # 1.2 segundos para reagir (mais lento)
                'imagem_chave': INIMIGO_CORVO
            },
        ],
        'pontos_de_entrada_no_mapa': {
            'praia': {'x': 400, 'y': 430, 'olhando_direita': True},
            'novo_jogo': {'x': 1950, 'y': 140, 'olhando_direita': True},
            'vila': {'x': 4373, 'y': 174, 'olhando_direita': False},
        },
        'areas_interacao': [
            # Entrada direita
            {
                'x': 4473, 'y': 197, 'largura': 20, 'altura': 180,
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_VILA, # O ID da próxima área
                    'ponto_de_destino': 'oeste'
                }
            },
        ]
    },
    ID_MAPA_CAMPO_VILA: {
        'nome': 'Vila',
        'chave_cenario': CHAVE_CENARIO_CAMPO_VILA,
        'obstaculos': [],
        'caminhos': [
            {'x': 0, 'y': 445, 'largura': 3540, 'altura': 155, 'tipo_terreno': 'normal'},
            {'x': 1728, 'y': 412, 'largura': 174, 'altura': 33, 'tipo_terreno': 'normal'},
        ],
        'npcs': [
            # Lista de NPCs para este mapa.
            # Ex: {'tipo': 'npc_aldeao', 'x': 500, 'y': 400, 'dialogo_id': 'ilha_inicial_intro'}
        ],
        'inimigos': [
            # Lista de inimigos para este mapa.
            # Ex: {'tipo': 'inimigo_goblin', 'x': 800, 'y': 450, 'patrulha': [800, 1000]}
        ],
        'pontos_de_entrada_no_mapa': {
            # Ponto de entrada padrão (usado se nenhum ponto específico for dado ao criar a TelaJogo)
            'oeste': {'x': 100, 'y': 370, 'olhando_direita': True},
            # Ponto onde o jogador começa em um novo jogo
            'leste': {'x': 3361, 'y': 370, 'olhando_direita': False},
            # Ponto onde aparece na ilha inicial ao SAIR da loja principal
            'loja': {'x': 1777, 'y': 312, 'olhando_direita': True}, # Ajuste as coordenadas para a frente da loja
            # Adicione outros pontos conforme necessário (entradas/saídas para outras áreas na ilha)
        },
        'areas_interacao': [
            # Entrada esquerda
            {
                'x': 0, 'y': 360, 'largura': 50, 'altura': 150, # Perto do início do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_COSTA_OESTE,  # O ID da área anterior
                    'ponto_de_destino': 'vila'
                }
            },
            # Entrada da loja
            {
                'x': 1716, 'y': 300, 'largura': 200, 'altura': 40, # Perto da entrada da loja
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_LOJA, # O ID do interior da loja
                    'ponto_de_destino': 'porta'
                }
            },
            # Entrada direita
            {
                'x': 3490, 'y': 360, 'largura': 50, 'altura': 150, # Ex: Perto do final do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_COSTA_LESTE, # O ID da próxima área
                    'ponto_de_destino': 'vila'
                }
            },
            # {
            #     'x': 500, 'y': 400, 'largura': 50, 'altura': 50, # Ex: Perto de uma prateleira
            #     'tipo_evento': 'comprar_item',
            #     'dados_evento': {'item_id': 'pocao_vida', 'preco': 50}
            # },
            # {
            #     'x': 300, 'y': 300, 'largura': 80, 'altura': 80, # Ex: Perto de um NPC
            #     'tipo_evento': 'dialogo',
            #     'dados_evento': {'dialogo_key': 'npc_aldeao_intro'}
            # }
        ]
        # Adicione outros dados específicos do mapa (ex: pontos de spawn de itens, triggers de eventos)
    },
    ID_MAPA_CAMPO_COSTA_LESTE: {
        'nome': 'Costa Leste',
        'chave_cenario': CHAVE_CENARIO_CAMPO_COSTA_LESTE,
        'chave_camada_superior': CHAVE_CENARIO_CAMPO_COSTA_LESTE_CAMADA_SUPERIOR,
        'obstaculos': [
            {'x': 3717, 'y': 471, 'largura': 250, 'altura': 24},
        ],
        'caminhos': [
            {'x': 0, 'y': 236, 'largura': 1360, 'altura': 156, 'tipo_terreno': 'normal'},
            {'x': 1360, 'y': 33, 'largura': 1226, 'altura': 567, 'tipo_terreno': 'arena'},
            {'x': 2586, 'y': 230, 'largura': 827, 'altura': 145, 'tipo_terreno': 'normal'},
            {'x': 3413, 'y': 230, 'largura': 481, 'altura': 370, 'tipo_terreno': 'normal'},
            {'x': 3894, 'y': 313, 'largura': 361, 'altura': 158, 'tipo_terreno': 'normal'},
        ],
        'npcs': [],
        'inimigos': [
            {
                'tipo': INIMIGO_LOBO,
                'x': 1500, 'y': 125,
                'velocidade_caminhada': 150, # Exemplo: 1.5 pixels/frame
                'velocidade_corrida': 300,   # Exemplo: 3.5 pixels/frame
                'alcance_visao': 200,
                'angulo_visao_graus': 90,
                'tempo_reacao_ms': 750,      # 0.75 segundos para reagir
                'imagem_chave': INIMIGO_LOBO
            },
            {
                'tipo': INIMIGO_LOBO,
                'x': 1900, 'y': 400,
                'velocidade_caminhada': 150, # Exemplo: 1.5 pixels/frame
                'velocidade_corrida': 300,   # Exemplo: 3.5 pixels/frame
                'alcance_visao': 200,
                'angulo_visao_graus': 90,
                'tempo_reacao_ms': 750,      # 0.75 segundos para reagir
                'imagem_chave': INIMIGO_LOBO
            },
            {
                'tipo': INIMIGO_LOBO,
                'x': 2360, 'y': 210,
                'velocidade_caminhada': 150, # Exemplo: 1.5 pixels/frame
                'velocidade_corrida': 300,   # Exemplo: 3.5 pixels/frame
                'alcance_visao': 200,
                'angulo_visao_graus': 90,
                'tempo_reacao_ms': 750,      # 0.75 segundos para reagir
                'imagem_chave': INIMIGO_LOBO
            },
        ],
        'pontos_de_entrada_no_mapa': {
            'vila': {'x': 50, 'y': 190, 'olhando_direita': True},
            'pier': {'x': 4160, 'y': 280, 'olhando_direita': False},
        },
        'areas_interacao': [
            {
                'x': 0, 'y': 200, 'largura': 50, 'altura': 150, # Perto do início do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_VILA,  # O ID da área anterior
                    'ponto_de_destino': 'leste'
                }
            },
            {
                'x': 4205, 'y': 313, 'largura': 50, 'altura': 158,
                'tipo_evento': 'embarcar',
                'dados_evento': {}
            },
        ]
    },
    ID_MAPA_CAMPO_LOJA: {
        'nome': 'Loja',
        'chave_cenario': CHAVE_LOJA_INTERIOR,
        'escala': 2.5,
        'obstaculos': [
            # Limite superior do caminho
            {'x': 0, 'y': 245, 'largura': 900, 'altura': 20},
            # Limite inferior do caminho
        ],
        'npcs': [],
        'inimigos': [],
        'pontos_de_entrada_no_mapa': {
            # Ponto de entrada padrão
            'porta': {'x': 100, 'y': 275, 'olhando_direita': True},
        },
        'areas_interacao': [
              {
                'x': 0, 'y': 300, 'largura': 50, 'altura': 270, # Perto da saída da loja
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_VILA, # Volta para a ilha inicial
                    'ponto_de_destino': 'loja'
                }
            },
        ]
    },
    ID_MAPA_CIDADE_PORTO: {
        'nome': 'Porto',
        'chave_cenario': CHAVE_CENARIO_CIDADE_PORTO,
        'chave_camada_superior': CHAVE_CENARIO_CIDADE_PORTO_CAMADA_SUPERIOR,
        'obstaculos': [
            {'x': 354, 'y': 390, 'largura': 93, 'altura': 22},
            {'x': 1413, 'y': 390, 'largura': 93, 'altura': 22},
            {'x': 2472, 'y': 390, 'largura': 93, 'altura': 22},
        ],
        'caminhos': [
            {'x': 111, 'y': 309, 'largura': 2589, 'altura': 107, 'tipo_terreno': 'normal'},
            {'x': 580, 'y': 270, 'largura': 290, 'altura': 39, 'tipo_terreno': 'normal'},
        ],
        'npcs': [],
        'inimigos': [],
        'pontos_de_entrada_no_mapa': {
            'pier': {'x': 2470, 'y': 265, 'olhando_direita': False},
            'centro': {'x': 680, 'y': 175, 'olhando_direita': True},
        },
        'areas_interacao': [
            {
                'x': 2472, 'y': 375, 'largura': 93, 'altura': 67,
                'tipo_evento': 'embarcar',
                'dados_evento': {}
            },
            {
                'x': 610, 'y': 185, 'largura': 250, 'altura': 20,
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CIDADE_CENTRO,
                    'ponto_de_destino': 'porto'
                }
            },
        ]
    },
    ID_MAPA_CIDADE_CENTRO: {
        'nome': 'Centro',
        'chave_cenario': CHAVE_CENARIO_CIDADE_CENTRO,
        'obstaculos': [
            {'x': 1539, 'y': 418, 'largura': 102, 'altura': 17},
            {'x': 1641, 'y': 435, 'largura': 41, 'altura': 25},
        ],
        'npcs': [],
        'inimigos': [],
        'pontos_de_entrada_no_mapa': {
            'porto': {'x': 100, 'y': 415, 'olhando_direita': True},
            'praca': {'x': 1570, 'y': 460, 'olhando_direita': False},
        },
        'caminhos': [
            {'x': 0, 'y': 498, 'largura': 1682, 'altura': 102, 'tipo_terreno': 'normal'},
            {'x': 1539, 'y': 403, 'largura': 143, 'altura': 95, 'tipo_terreno': 'normal'},
        ],
        'areas_interacao': [
            {
                'x': 0, 'y': 480, 'largura': 50, 'altura': 150,
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CIDADE_PORTO,
                    'ponto_de_destino': 'centro'
                }
            },
            {
                'x': 1656, 'y': 484, 'largura': 50, 'altura': 150,
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CIDADE_PRACA,
                    'ponto_de_destino': 'centro'
                }
            },
        ]
    },
    ID_MAPA_CIDADE_PRACA: {
        'nome': 'Praça',
        'chave_cenario': CHAVE_CENARIO_CIDADE_PRACA,
        'obstaculos': [],
        'caminhos': [
            {'x': 0, 'y': 483, 'largura': 764, 'altura': 117, 'tipo_terreno': 'normal'},
            {'x': 764, 'y': 203, 'largura': 1036, 'altura': 397, 'tipo_terreno': 'arena'},
        ],
        'npcs': [],
        'inimigos': [],
        'pontos_de_entrada_no_mapa': {
            'centro': {'x': 100, 'y': 415, 'olhando_direita': True},
        },
        'areas_interacao': [
            {
                'x': 0, 'y': 500, 'largura': 50, 'altura': 85,
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CIDADE_CENTRO,
                    'ponto_de_destino': 'praca'
                }
            },
        ]
    },
    ID_MAPA_NEVE_VILA: {
        'nome': 'Vila',
        'chave_cenario': CHAVE_CENARIO_NEVE_VILA,
        'obstaculos': [],
        'caminhos': [
            {'x': 0, 'y': 407, 'largura': 3540, 'altura': 193, 'tipo_terreno': 'normal'},
            {'x': 0, 'y': 407, 'largura': 3540, 'altura': 74, 'tipo_terreno': 'neve'},
            {'x': 0, 'y': 571, 'largura': 3540, 'altura': 29, 'tipo_terreno': 'neve'},
        ],
        'npcs': [],
        'inimigos': [],
        'pontos_de_entrada_no_mapa': {
            'pier': {'x': 100, 'y': 415, 'olhando_direita': True},
            'leste': {'x': 3361, 'y': 415, 'olhando_direita': False},
            'cozinha': {'x': 705, 'y': 325, 'olhando_direita': True}, # Ajuste as coordenadas para a frente da loja
        },
        'areas_interacao': [
            # Entrada esquerda
            {
                'x': 0, 'y': 360, 'largura': 50, 'altura': 150, # Perto do início do mapa
                'tipo_evento': 'embarcar',
                'dados_evento': {
                    #'id_proximo_mapa': ID_MAPA_CAMPO_VILA,  # O ID da área anterior
                    #'ponto_de_destino': 'oeste'
                }
            },
            # Entrada da cozinha
            {
                'x': 679, 'y': 270, 'largura': 116, 'altura': 40, # Perto da entrada da cozinha
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_NEVE_COZINHA, # O ID do interior da cozinha
                    'ponto_de_destino': 'porta'
                }
            },
            # Entrada direita
            {
                'x': 3490, 'y': 360, 'largura': 50, 'altura': 150, # Ex: Perto do final do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_NEVE_VILA, # O ID da próxima área
                    'ponto_de_destino': 'leste'
                }
            },
        ]
    },
    ID_MAPA_NEVE_COZINHA: {
        'nome': 'Cozinha',
        'chave_cenario': CHAVE_COZINHA_INTERIOR,
        'escala': 2.5,
        'obstaculos': [
            # Limite superior do caminho
            {'x': 0, 'y': 213, 'largura': 900, 'altura': 20},
        ],
        'npcs': [],
        'inimigos': [],
        'pontos_de_entrada_no_mapa': {
            # Ponto de entrada padrão
            'porta': {'x': 100, 'y': 260, 'olhando_direita': True},
        },
        'areas_interacao': [
              {
                'x': 0, 'y': 280, 'largura': 50, 'altura': 270, # Perto da saída da cozinha
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_NEVE_VILA,
                    'ponto_de_destino': 'cozinha'
                }
            },
        ]
    },
    # Adicione quantos mapas forem necessários
}

def obter_dados_da_sala(id_mapa):
    """
    Retorna os dados de configuração para um mapa específico pelo seu ID.
    :param id_mapa: O ID (string) do mapa desejado.
    :return: Um dicionário contendo os dados do mapa, ou None se o ID do mapa não for encontrado.
    """
    return dados_das_salas.get(id_mapa) # O método .get() retorna None se a chave não existe

def obter_dados_da_ilha(id_ilha):
    """
    Retorna os dados de configuração para uma ilha específica pelo seu ID.
    :param id_ilha: O ID (string) da ilha desejada.
    :return: Um dicionário contendo os dados da ilha, ou None se o ID da ilha não for encontrado.
    """
    return dados_das_ilhas.get(id_ilha) # O método .get() retorna None se a chave não existe