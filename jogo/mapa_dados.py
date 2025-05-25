# mapa_dados.py

from utilidades.constantes import *

# Dicionário para armazenar os dados de configuração de cada mapa do jogo.
# Cada chave é o ID único do mapa.
mapas_data = {
    ID_MAPA_CAMPO_COSTA_OESTE: { # ID do primeiro mapa
        'chave_cenario': CHAVE_CENARIO_CAMPO_COSTA_OESTE, # Chave do gerenciador de recursos para a imagem de fundo deste mapa
        'obstaculos': [ # Lista de obstáculos para este mapa. Cada item é um dicionário com as propriedades do obstáculo.
            # Limite superior do caminho (particionado em segmentos)
            {'x': 0, 'y': -20, 'largura': 3540, 'altura': 20},
            # Limite inferior do caminho (segmento único)
            {'x': 0, 'y': 600, 'largura': 3540, 'altura': 20},
            {'x': -20, 'y': 0, 'largura': 20, 'altura': 600},
            {'x': 900, 'y': 0, 'largura': 20, 'altura': 600},
        ],
        'npcs': [
            # Lista de NPCs para este mapa.
            # Ex: {'tipo': 'npc_aldeao', 'x': 500, 'y': 400, 'dialogo_id': 'ilha_inicial_intro'}
        ],
        'inimigos': [
            {
                'tipo': INIMIGO_LOBO,
                'x': 500, 'y': 350,
                'velocidade_caminhada': 150, # Exemplo: 1.5 pixels/frame
                'velocidade_corrida': 300,   # Exemplo: 3.5 pixels/frame
                'alcance_visao': 200,
                'angulo_visao_graus': 90,
                'tempo_reacao_ms': 750,      # 0.75 segundos para reagir
                'imagem_chave': INIMIGO_LOBO
            },
            {
                'tipo': INIMIGO_CORVO,
                'x': 720, 'y': 320,
                'velocidade_caminhada': 150,
                'velocidade_corrida': 300,
                'alcance_visao': 200,
                'angulo_visao_graus': 120,
                'tempo_reacao_ms': 1200,     # 1.2 segundos para reagir (mais lento)
                'imagem_chave': INIMIGO_CORVO
            }
        ],
        'pontos_de_entrada_no_mapa': {
            # Ponto de entrada padrão (usado se nenhum ponto específico for dado ao criar a TelaJogo)
            'entrada_padrao': {'x': 100, 'y': 370, 'olhando_direita': True},
            'entrada_esquerda': {'x': 3361, 'y': 370, 'olhando_direita': False},
        },
        'areas_interacao': [
            # Entrada direita
            {
                'x': 850, 'y': 360, 'largura': 50, 'altura': 150, # Ex: Perto do final do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_VILA, # O ID da próxima área
                    'ponto_de_destino': 'entrada_padrao'
                }
            },
        ]
    },
    ID_MAPA_CAMPO_VILA: { # ID do primeiro mapa
        'chave_cenario': CHAVE_CENARIO_CAMPO_VILA, # Chave do gerenciador de recursos para a imagem de fundo deste mapa
        'obstaculos': [ # Lista de obstáculos para este mapa. Cada item é um dicionário com as propriedades do obstáculo.
            # Limite superior do caminho (particionado em segmentos)
            {'x': 0, 'y': 323, 'largura': 1715, 'altura': 20},
            {'x': 1716, 'y': 290, 'largura': 200, 'altura': 20}, # Exemplo de segmento inclinado/variado
            {'x': 1916, 'y': 323, 'largura': 3540 - 1915, 'altura': 20}, # Continuação do limite superior
            # Limite inferior do caminho (segmento único)
            {'x': 0, 'y': 530, 'largura': 3540, 'altura': 20},
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
            'entrada_padrao': {'x': 100, 'y': 370, 'olhando_direita': True},
            # Ponto onde o jogador começa em um novo jogo
            'entrada_leste': {'x': 3361, 'y': 370, 'olhando_direita': False},
            # Ponto onde aparece na ilha inicial ao SAIR da loja principal
            'saida_loja_principal': {'x': 1777, 'y': 312, 'olhando_direita': True}, # Ajuste as coordenadas para a frente da loja
            # Adicione outros pontos conforme necessário (entradas/saídas para outras áreas na ilha)
        },
        'areas_interacao': [
            # Entrada esquerda
            {
                'x': 0, 'y': 360, 'largura': 50, 'altura': 150, # Perto do início do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_COSTA_OESTE,  # O ID da área anterior
                    'ponto_de_destino': 'entrada_padrao'
                }
            },
            # Entrada da loja
            {
                'x': 1716, 'y': 300, 'largura': 200, 'altura': 40, # Perto da entrada da loja
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_LOJA, # O ID do interior da loja
                    'ponto_de_destino': 'entrada_padrao'
                }
            },
            # Entrada direita
            {
                'x': 3490, 'y': 360, 'largura': 50, 'altura': 150, # Ex: Perto do final do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_NEVE_VILA, # O ID da próxima área
                    'ponto_de_destino': 'entrada_padrao'
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
    # Adicione dados para outros mapas aqui
    # 'outra_ilha': {
    #     'chave_cenario': 'background_outra_ilha',
    #     'player_start_x': 50,
    #     'player_start_y': 200,
    #      'obstaculos': [
    #         # Obstáculos específicos de outra_ilha
    #         {'x': 0, 'y': 150, 'largura': 1000, 'altura': 20},
    #         {'x': 0, 'y': 300, 'largura': 1000, 'altura': 20},
    #     ],
    #     'npcs': [],
    #     'inimigos': [],
    #     'areas_interacao': [
    #          # Áreas de interação específicas para outra_ilha
    #           {
    #             'x': 50, 'y': 180, 'largura': 50, 'altura': 50, # Ex: Perto de um portal para voltar
    #             'tipo_evento': 'mudar_mapa',
    #             'dados_evento': {'id_proximo_mapa': 'ilha_inicial'} # Volta para a ilha inicial
    #         },
    #     ]
    # },
    ID_MAPA_CAMPO_LOJA: {
        'chave_cenario': CHAVE_LOJA_INTERIOR,
        'escala': 2.5,
        'obstaculos': [
            # Limite superior do caminho
            {'x': 0, 'y': 245, 'largura': 900, 'altura': 20},
            # Limite inferior do caminho
            {'x': 0, 'y': 600, 'largura': 900, 'altura': 20},
        ],
        'npcs': [],
        'inimigos': [],
        'pontos_de_entrada_no_mapa': {
            # Ponto de entrada padrão
            'entrada_padrao': {'x': 100, 'y': 275, 'olhando_direita': True},
        },
        'areas_interacao': [
              {
                'x': 0, 'y': 300, 'largura': 50, 'altura': 270, # Perto da saída da loja
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_VILA, # Volta para a ilha inicial
                    'ponto_de_destino': 'saida_loja_principal'
                }
            },
        ]
    },
    ID_MAPA_NEVE_VILA: { # ID do primeiro mapa
        'chave_cenario': CHAVE_CENARIO_NEVE_VILA, # Chave do gerenciador de recursos para a imagem de fundo deste mapa
        'obstaculos': [ # Lista de obstáculos para este mapa. Cada item é um dicionário com as propriedades do obstáculo.
            # Limite superior do caminho (particionado em segmentos)
            {'x': 0, 'y': 300, 'largura': 678, 'altura': 20},
            {'x': 679, 'y': 252, 'largura': 116, 'altura': 20}, # Exemplo de segmento inclinado/variado
            {'x': 795, 'y': 300, 'largura': 3540 - 795, 'altura': 20}, # Continuação do limite superior
            # Limite inferior do caminho (segmento único)
            {'x': 0, 'y': 570, 'largura': 3540, 'altura': 20},
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
            'entrada_padrao': {'x': 100, 'y': 415, 'olhando_direita': True},
            # Ponto onde o jogador começa em um novo jogo
            'entrada_leste': {'x': 3361, 'y': 415, 'olhando_direita': False},
            # Ponto onde aparece na ilha inicial ao SAIR da loja principal
            'saida_cozinha': {'x': 705, 'y': 325, 'olhando_direita': True}, # Ajuste as coordenadas para a frente da loja
            # Adicione outros pontos conforme necessário (entradas/saídas para outras áreas na ilha)
        },
        'areas_interacao': [
            # Entrada esquerda
            {
                'x': 0, 'y': 360, 'largura': 50, 'altura': 150, # Perto do início do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_CAMPO_VILA,  # O ID da área anterior
                    'ponto_de_destino': 'entrada_leste'
                }
            },
            # Entrada da cozinha
            {
                'x': 679, 'y': 270, 'largura': 116, 'altura': 40, # Perto da entrada da cozinha
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_NEVE_COZINHA, # O ID do interior da cozinha
                    'ponto_de_destino': 'entrada_padrao'
                }
            },
            # Entrada direita
            {
                'x': 3490, 'y': 360, 'largura': 50, 'altura': 150, # Ex: Perto do final do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_NEVE_VILA, # O ID da próxima área
                    'ponto_de_destino': 'entrada_leste'
                }
            },
        ]
    },
    ID_MAPA_NEVE_COZINHA: {
        'chave_cenario': CHAVE_COZINHA_INTERIOR,
        'escala': 2.5,
        'obstaculos': [
            # Limite superior do caminho
            {'x': 0, 'y': 213, 'largura': 900, 'altura': 20},
            # Limite inferior do caminho
            {'x': 0, 'y': 600, 'largura': 900, 'altura': 20},
        ],
        'npcs': [],
        'inimigos': [],
        'pontos_de_entrada_no_mapa': {
            # Ponto de entrada padrão
            'entrada_padrao': {'x': 100, 'y': 260, 'olhando_direita': True},
        },
        'areas_interacao': [
              {
                'x': 0, 'y': 280, 'largura': 50, 'altura': 270, # Perto da saída da cozinha
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {
                    'id_proximo_mapa': ID_MAPA_NEVE_VILA,
                    'ponto_de_destino': 'saida_cozinha'
                }
            },
        ]
    },
    # Adicione quantos mapas forem necessários
}

def get_mapa_data(id_mapa):
    """
    Retorna os dados de configuração para um mapa específico pelo seu ID.
    :param id_mapa: O ID (string) do mapa desejado.
    :return: Um dicionário contendo os dados do mapa, ou None se o ID do mapa não for encontrado.
    """
    return mapas_data.get(id_mapa) # O método .get() retorna None se a chave não existe