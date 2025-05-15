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
ICONE_INTERACAO_KEY = 'icone_interacao' # Chave do gerenciador de recursos para o ícone de interação (balão de fala, etc.)

# --- Debugging ---
DEBUG_DESENHAR_CAIXAS_COLISAO = False # (True para exibir, False para ocultar)
COR_CAIXA_COLISAO = VERMELHO # Vermelho (para visível)

# --- Jogador ---
PERSONAGEM_MENINA = 'menina'
PERSONAGEM_MENINO = 'menino'

# --- Mapa Inicial ---
MAPA_INICIAL_ID = 'ilha_inicial'