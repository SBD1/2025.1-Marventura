# mapa_dados.py

# Dicionário para armazenar os dados de configuração de cada mapa do jogo.
# Cada chave é o ID único do mapa.
mapas_data = {
    'ilha_inicial': { # ID do primeiro mapa
        'background_key': 'cenario_ilha_1', # Chave do gerenciador de recursos para a imagem de fundo deste mapa
        'player_start_x': 100, # Posição X inicial do jogador neste mapa (coordenada do mundo)
        'player_start_y': 370, # Posição Y inicial do jogador neste mapa (coordenada do mundo)
        'obstaculos': [ # Lista de obstáculos para este mapa. Cada item é um dicionário com as propriedades do obstáculo.
            # Limite superior do caminho (particionado em segmentos)
            {'x': 0, 'y': 323, 'largura': 1715, 'altura': 20},
            {'x': 1716, 'y': 290, 'largura': 200, 'altura': 20}, # Exemplo de segmento inclinado/variado
            {'x': 1916, 'y': 323, 'largura': 3540 - 1915, 'altura': 20}, # Continuação do limite superior
            # Limite inferior do caminho (segmento único)
            {'x': 0, 'y': 530, 'largura': 3540, 'altura': 20},
            # Adicione outros obstáculos aqui (paredes, limites verticais, etc.)
            # {'x': 500, 'y': 400, 'largura': 50, 'altura': 100}, # Exemplo de uma caixa
        ],
        'npcs': [
            # Lista de NPCs para este mapa.
            # Ex: {'tipo': 'npc_aldeao', 'x': 500, 'y': 400, 'dialogo_id': 'ilha_inicial_intro'}
        ],
        'inimigos': [
            # Lista de inimigos para este mapa.
            # Ex: {'tipo': 'inimigo_goblin', 'x': 800, 'y': 450, 'patrulha': [800, 1000]}
        ],
        'areas_interacao': [
            {
                'x': 0, 'y': 360, 'largura': 50, 'altura': 150, # Ex: Perto do início do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {'proximo_mapa_id': 'outra_ilha'} # O ID da área anterior
            },
            {
                'x': 1716, 'y': 300, 'largura': 200, 'altura': 40, # Ex: Perto da entrada da loja
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {'proximo_mapa_id': 'loja_comida_ilha_1'} # O ID do interior da loja
            },
            {
                'x': 3490, 'y': 360, 'largura': 50, 'altura': 150, # Ex: Perto do final do mapa
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {'proximo_mapa_id': 'outra_ilha'} # O ID do próximo mapa
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
    'outra_ilha': {
        'background_key': 'background_outra_ilha',
        'player_start_x': 50,
        'player_start_y': 200,
         'obstaculos': [
            # Obstáculos específicos de outra_ilha
            {'x': 0, 'y': 150, 'largura': 1000, 'altura': 20},
            {'x': 0, 'y': 300, 'largura': 1000, 'altura': 20},
        ],
        'npcs': [],
        'inimigos': [],
        'areas_interacao': [
             # Áreas de interação específicas para outra_ilha
              {
                'x': 50, 'y': 180, 'largura': 50, 'altura': 50, # Ex: Perto de um portal para voltar
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {'proximo_mapa_id': 'ilha_inicial'} # Volta para a ilha inicial
            },
        ]
    },
    'loja_comida_ilha_1': {
        'background_key': 'loja_interior',
        'player_start_x': 50,
        'player_start_y': 370,
         'obstaculos': [
            # Obstáculos específicos de outra_ilha
            {'x': 0, 'y': 150, 'largura': 900, 'altura': 20},
            {'x': 0, 'y': 500, 'largura': 900, 'altura': 20},
        ],
        'npcs': [],
        'inimigos': [],
        'areas_interacao': [
             # Áreas de interação específicas para outra_ilha
              {
                'x': 50, 'y': 180, 'largura': 50, 'altura': 50, # Ex: Perto de um portal para voltar
                'tipo_evento': 'mudar_mapa',
                'dados_evento': {'proximo_mapa_id': 'ilha_inicial'} # Volta para a ilha inicial
            },
        ]
    },
    # Adicione quantos mapas forem necessários
}

def get_mapa_data(map_id):
    """
    Retorna os dados de configuração para um mapa específico pelo seu ID.
    :param map_id: O ID (string) do mapa desejado.
    :return: Um dicionário contendo os dados do mapa, ou None se o ID do mapa não for encontrado.
    """
    return mapas_data.get(map_id) # O método .get() retorna None se a chave não existe