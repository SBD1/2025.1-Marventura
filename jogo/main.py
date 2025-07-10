# main.py

import pygame
import sys
from utilidades.constantes import *
from gerenciadores import GerenciadorDeRecursos
from gerenciadores import DBManager
from gerenciadores import GerenciadorDeTelas

# Inicializa o Pygame (DEVE VIR ANTES DE CARREGAR FONTES/IMAGENS)
pygame.init()
# Inicializa apenas o módulo de fonte explicitamente (importante para o carregamento de fontes no gerenciador)
pygame.font.init()

# Configurações da tela principal
tela_principal = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.DOUBLEBUF | pygame.HWSURFACE, vsync=1)
pygame.display.set_caption("Marventura") # Título da janela do jogo

# --- Gerenciador de Recursos ---
# Cria uma única instância do gerenciador de recursos
gerenciador_recursos = GerenciadorDeRecursos()
gerenciador_banco_de_dados = DBManager()

gerenciador_recursos.carregar_recursos()

# --- Função Principal do Jogo ---
def executar_jogo():
    relogio = pygame.time.Clock()

    # Cria uma instância do GerenciadorDeTelas.
    # Ele será responsável por inicializar a primeira tela (menu principal).
    gerenciador_telas = GerenciadorDeTelas(tela_principal, gerenciador_recursos, gerenciador_banco_de_dados)

    rodando = True
    while rodando:
        dt = relogio.tick(FPS) / 1000.0 # Delta time em segundos

        # --- Processamento de Eventos ---
        eventos_pygame = pygame.event.get()
        for evento in eventos_pygame:
            # O gerenciador de telas agora lida com os eventos e a transição de telas
            gerenciador_telas.processar_eventos(evento)

        # --- Atualização do Estado dos Elementos ---
        # O gerenciador de telas agora lida com a atualização e a transição de telas
        gerenciador_telas.atualizar(dt)

        # --- Desenho ---
        tela_principal.fill(PRETO) # Limpa a tela antes de desenhar
        gerenciador_telas.desenhar() # O gerenciador de telas sabe qual tela desenhar

        # --- Atualização da Tela e Controle de FPS ---
        pygame.display.flip()

    # --- Fim do Jogo ---
    pygame.quit()
    sys.exit()

# Inicia o jogo chamando a função principal (se o script for executado diretamente)
if __name__ == "__main__":
    executar_jogo() # <-- Chama a função principal do jogo