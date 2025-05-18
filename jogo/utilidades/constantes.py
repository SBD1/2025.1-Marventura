# constantes.py

import pygame


# --- Dimensões da tela ---
LARGURA_TELA = 900
ALTURA_TELA = 600

# --- Cores ---
BRANCO = (202, 169, 122)
PRETO = (53, 38, 16)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (150, 150, 150)
CINZA_ESCURO = (100, 100, 100)
COR_TEXTO_SALVAR = (53, 38, 16) # Cor específica para texto de salvar

# --- Animação do Jogador ---
VELOCIDADE_ANIMACAO_CAMINHADA = 0.15 # Segundos por frame na animação de caminhada (ajuste conforme quiser)
FPS = 60 # Quadros por segundo

# --- Estados do jogo (para gerenciamento de telas) ---
ESTADO_MENU_INICIAL = 0
ESTADO_MENU_SALVAR = 1
ESTADO_JOGO = 2
ESTADO_SELECAO_PERSONAGEM = 3
# Adicione outros estados conforme necessário

# --- Interação ---
TECLA_INTERACAO = pygame.K_e # Tecla para interagir (Ex: tecla 'E')

# --- Debugging ---
DEBUG_DESENHAR_CAIXAS_COLISAO = True # (True para exibir, False para ocultar)
COR_CAIXA_COLISAO = VERMELHO # Vermelho (para visível)

# --- Jogador ---
PERSONAGEM_MENINA = 'menina'
PERSONAGEM_MENINO = 'menino'

# --- Identificadores de Mapas ---
ID_MAPA_CAMPO_VILA = 'ilha_campo_vila'
ID_MAPA_CAMPO_LOJA = 'ilha_campo_loja'
ID_MAPA_NEVE_VILA = 'ilha_neve_vila'
ID_MAPA_NEVE_COZINHA = 'ilha_neve_cozinha'

# --- Chaves de recursos ---
CHAVE_LOGO = 'logo'
CHAVE_TELA_INICIAL = 'tela_inicial'
CHAVE_FONTE_TITULO = 'titulo'
CHAVE_FONTE_BOTAO = 'botao'
CHAVE_FONTE_NOME_CARTAZ = 'nome_cartaz'
CHAVE_FONTE_DATA_CARTAZ = 'data_cartaz'
CHAVE_CARTAZ_PROCURADA = 'cartaz_de_procurada'
CHAVE_CARTAZ_PROCURADO = 'cartaz_de_procurado'
CHAVE_CARTAZ_VAZIO = 'cartaz_vazio'
CHAVE_ICONE_INTERACAO = 'icone_interacao'

CHAVE_LOJA_INTERIOR = 'loja_interior'
CHAVE_COZINHA_INTERIOR = 'cozinha_interior'

CHAVE_CENARIO_CAMPO_COSTA_OESTE = 'cenario_ilha_1_parte_1'
CHAVE_CENARIO_CAMPO_VILA = 'cenario_ilha_1_parte_2'
CHAVE_CENARIO_CAMPO_COSTA_LESTE = 'cenario_ilha_1_parte_3'

CHAVE_CENARIO_ILHA_2_PARTE_1 = 'cenario_ilha_2_parte_1'
CHAVE_CENARIO_ILHA_2_PARTE_2 = 'cenario_ilha_2_parte_2'
CHAVE_CENARIO_ILHA_2_PARTE_3 = 'cenario_ilha_2_parte_3'

CHAVE_CENARIO_NEVE_COSTA_OESTE = 'cenario_ilha_3_parte_1'
CHAVE_CENARIO_NEVE_VILA = 'cenario_ilha_3_parte_2'
CHAVE_CENARIO_NEVE_COSTA_LESTE = 'cenario_ilha_3_parte_3'

CHAVE_CENARIO_ILHA_4_PARTE_1 = 'cenario_ilha_4_parte_1'
CHAVE_CENARIO_ILHA_4_PARTE_2 = 'cenario_ilha_4_parte_2'
CHAVE_CENARIO_ILHA_4_PARTE_3 = 'cenario_ilha_4_parte_3'

CHAVE_CENARIO_ILHA_5_PARTE_1 = 'cenario_ilha_5_parte_1'
CHAVE_CENARIO_ILHA_5_PARTE_2 = 'cenario_ilha_5_parte_2'
CHAVE_CENARIO_ILHA_5_PARTE_3 = 'cenario_ilha_5_parte_3'

CHAVE_CENARIO_ILHA_6_PARTE_1 = 'cenario_ilha_6_parte_1'
CHAVE_CENARIO_ILHA_6_PARTE_2 = 'cenario_ilha_6_parte_2'
CHAVE_CENARIO_ILHA_6_PARTE_3 = 'cenario_ilha_6_parte_3'
