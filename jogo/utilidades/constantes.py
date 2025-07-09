# constantes.py

import pygame


# --- Dimensões da tela ---
LARGURA_TELA = 900
ALTURA_TELA = 600
LARGURA_MUNDO_MAPA_TESTE = 3450
ALTURA_MUNDO_MAPA_TESTE = 600

# --- Cores ---
BRANCO = (202, 169, 122)
PRETO = (53, 38, 16)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AZUL_CLARO = (0, 191, 255)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
CINZA = (150, 150, 150)
CINZA_ESCURO = (100, 100, 100)
COR_TEXTO_SALVAR = (53, 38, 16) # Cor específica para texto de salvar

# --- Animação do Jogador ---
VELOCIDADE_ANIMACAO_CAMINHADA = 0.15 # Segundos por frame na animação de caminhada (ajuste conforme quiser)
FPS = 60 # Quadros por segundo

# --- Animação do Inimigo ---
VELOCIDADE_ANIMACAO_INIMIGO = 0.2

# --- Constantes do Jogador ---
VELOCIDADE_JOGADOR = 5 # Exemplo de velocidade padrão para o jogador
LARGURA_JOGADOR = 80
ALTURA_JOGADOR = 120

# --- Constantes do Inimigo ---
ANGULO_VISAO = 120
ALCANCE_VISAO = 200
VELOCIDADE_CORRIDA_INIMIGO = 300
VELOCIDADE_CAMINHADA_INIMIGO = 150
TEMPO_REACAO_INIMIGO = 750
TEMPO_RECARGA_ATAQUE_INIMIGO_MS = 1500 # Tempo entre ataques do inimigo
DURACAO_ATAQUE_INIMIGO_MS = 300      # Duração da animação/fase de ataque do inimigo
DISTANCIA_ATAQUE_INIMIGO = 40        # Distância que o inimigo considera "alvo ao alcance" para atacar

# --- Chaves de Transição de Tela ---
CHAVE_TRANSICAO_BATALHA = 'batalha'
CHAVE_TRANSICAO_MAPA = 'mapa'
CHAVE_TRANSICAO_MENU_PRINCIPAL = 'menu_principal'
CHAVE_TRANSICAO_SALVAMENTO = 'salvamento'
CHAVE_TRANSICAO_SELECAO_PERSONAGEM = 'selecao_personagem'
CHAVE_TRANSICAO_NOVO_JOGO = 'novo_jogo'
CHAVE_TRANSICAO_CARREGAR_JOGO = 'carregar_jogo'

# --- Estados do Inimigo ---
ESTADO_INIMIGO_PARADO = 'parado'
ESTADO_INIMIGO_MOVENDO = 'movendo'
ESTADO_INIMIGO_ATACANDO = 'atacando'
ESTADO_INIMIGO_RECARGA = 'recarregando'

# --- Estados do jogo (para gerenciamento de telas) ---
ESTADO_MENU_INICIAL = 0
ESTADO_MENU_SALVAR = 1
ESTADO_JOGO = 2
ESTADO_SELECAO_PERSONAGEM = 3
# Adicione outros estados conforme necessário

# --- Interação ---
OFFSET_ICONE_INTERACAO_Y = 40

# --- Jogador ---
SILVIE = 'Silvie'
SHUAN = 'Shuan'

# --- Inimigos ---
INIMIGO_LOBO = 'Lobo'
INIMIGO_CORVO = 'Corvo'

# --- Habitantes ---
BIGODINI = 'campones_b'
TIAO_PALHA = 'campones_a'
LINA_PANELA = 'camponesa_a'
TIA_COTINHA = 'camponesa_b'
SR_LEE = 'lee'
SR_LEE_LOGISTA = 'lee_busto'


# --- Identificadores de Mapas ---
ID_MAPA_OCEANO = 'oceano'

ID_MAPA_CAMPO_COSTA_OESTE = 'ilha_campo_costa_oeste'
ID_MAPA_CAMPO_COSTA_LESTE = 'ilha_campo_costa_leste'
ID_MAPA_CAMPO_VILA = 'ilha_campo_vila'
ID_MAPA_CAMPO_LOJA = 'ilha_campo_loja'

ID_MAPA_CIDADE_PORTO = 'ilha_cidade_porto'
ID_MAPA_CIDADE_CENTRO = 'ilha_cidade_centro'
ID_MAPA_CIDADE_PRACA = 'ilha_cidade_praca'
ID_MAPA_CIDADE_LOJA = 'ilha_cidade_loja'
ID_MAPA_CIDADE_SUBURBIO = 'ilha_cidade_suburbio'

ID_MAPA_NEVE_COSTA = 'ilha_neve_costa'
ID_MAPA_NEVE_VILA = 'ilha_neve_vila'
ID_MAPA_NEVE_MONTANHA = 'ilha_neve_montanha'
ID_MAPA_NEVE_COZINHA = 'ilha_neve_cozinha'

ID_MAPA_DESERTO_COSTA_OESTE = 'ilha_deserto_costa_oeste'
ID_MAPA_DESERTO_VILA = 'ilha_deserto_vila'
ID_MAPA_DESERTO_LOJA = 'ilha_deserto_loja'
ID_MAPA_DESERTO_COSTA_LESTE = 'ilha_deserto_costa_leste'

ID_MAPA_ASSOMBRADA_COSTA_OESTE = 'ilha_assombrada_costa_oeste'
ID_MAPA_ASSOMBRADA_VILA = 'ilha_assombrada_vila'
ID_MAPA_ASSOMBRADA_LOJA = 'ilha_assombrada_loja'

ID_MAPA_FORTALEZA_PORTO = 'ilha_fortaleza_porto'
ID_MAPA_FORTALEZA_INTERIOR = 'ilha_fortaleza_interior'
ID_MAPA_FORTALEZA_LOJA = 'ilha_fortaleza_loja'

# --- Chaves de recursos ---
CHAVE_LOGO = 'logo'
CHAVE_TELA_INICIAL = 'tela_inicial'
CHAVE_FONTE_COLINER_TITULO = 'fonte_coliner_titulo'
CHAVE_FONTE_COLINER_BOTAO = 'fonte_coliner_botao'
CHAVE_FONTE_COLINER_TEXTO = 'fonte_coliner_texto'
CHAVE_FONTE_PAYFAIR_TEXTO = 'fonte_payfair_texto'
CHAVE_FONTE_HEART_TEXTO = 'fonte_heart_texto'
CHAVE_CARTAZ_PROCURADA = 'cartaz_de_procurada'
CHAVE_CARTAZ_PROCURADO = 'cartaz_de_procurado'
CHAVE_CARTAZ_VAZIO = 'cartaz_vazio'
CHAVE_ICONE_INTERACAO = 'icone_interacao'
CHAVE_ICONE_ALERTA = 'icone_alerta'
CHAVE_ICONE_INTERROGACAO = 'icone_interrogacao'
CHAVE_MARCADOR_MAPA_SILVIE = 'marcador_mapa_silvie'
CHAVE_MARCADOR_MAPA_SHUAN = 'marcador_mapa_shuan'
CHAVE_CAIXA_DIALOGO = 'caixa_dialogo'

CHAVE_LOJA_INTERIOR = 'loja_interior'
CHAVE_COZINHA_INTERIOR = 'cozinha_interior'

CHAVE_CENARIO_OCEANO = 'cenario_oceano'

CHAVE_CENARIO_CAMPO_COSTA_OESTE = 'cenario_boraboia_pastos'
CHAVE_CENARIO_CAMPO_COSTA_OESTE_CAMADA_SUPERIOR = 'cenario_boraboia_pastos_camada_superior'
CHAVE_CENARIO_CAMPO_VILA = 'cenario_boraboia_vila'
CHAVE_CENARIO_CAMPO_COSTA_LESTE = 'cenario_boraboia_vale'
CHAVE_CENARIO_CAMPO_COSTA_LESTE_CAMADA_SUPERIOR = 'cenario_boraboia_vale_camada_superior'

CHAVE_CENARIO_CIDADE_PORTO = 'cenario_lurien_porto'
CHAVE_CENARIO_CIDADE_PORTO_CAMADA_SUPERIOR = 'cenario_lurien_porto_camada_superior'
CHAVE_CENARIO_CIDADE_CENTRO = 'cenario_lurien_centro'
CHAVE_CENARIO_CIDADE_PRACA = 'cenario_lurien_praca'
CHAVE_CENARIO_CIDADE_PRACA_CAMADA_SUPERIOR = 'cenario_lurien_praca_camada_superior'

CHAVE_CENARIO_NEVE_COSTA = 'cenario_frimora_costa'
CHAVE_CENARIO_NEVE_VILA = 'cenario_frimora_vila'
CHAVE_CENARIO_NEVE_FLORESTA = 'cenario_frimora_floresta'
CHAVE_CENARIO_NEVE_FLORESTA_CAMADA_SUPERIOR = 'cenario_frimora_floresta_camada_superior'
CHAVE_CENARIO_NEVE_MONTANHA = 'cenario_frimora_montanha'

CHAVE_CENARIO_ILHA_4_PARTE_1 = 'cenario_cactuaraquara_duna'
CHAVE_CENARIO_ILHA_4_PARTE_2 = 'cenario_cactuaraquara_cidadela'
CHAVE_CENARIO_ILHA_4_PARTE_3 = 'cenario_cactuaraquara_oasis'

CHAVE_CENARIO_ILHA_5_PARTE_1 = 'cenario_nublaria_penumbra'
CHAVE_CENARIO_ILHA_5_PARTE_2 = 'cenario_nublaria_acampamento'
CHAVE_CENARIO_ILHA_5_PARTE_3 = 'cenario_nublaria_floresta'

CHAVE_CENARIO_ILHA_6_PARTE_1 = 'cenario_quartel_porto'
CHAVE_CENARIO_ILHA_6_PARTE_2 = 'cenario_quartel_interior'
CHAVE_CENARIO_ILHA_6_PARTE_3 = 'cenario_quartel_escritorio'


CENA_SILVIE_NO_CAMPO = 'cena_silvie_no_campo'
CENA_SHUAN_NO_CAMPO = 'cena_shuan_no_campo'

# --- Debugging ---
DEBUG_DESENHAR_CAIXAS_COLISAO = False # (True para exibir, False para ocultar)
COR_CAIXA_COLISAO = (255, 0, 255) # Magenta para caixas de colisão