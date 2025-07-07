# main.py
# No topo de gerenciador_de_recursos.py

import pygame
import sys
from utilidades.constantes import *
from recursos import GerenciadorDeRecursos
from utilidades import DBManager
from telas import GerenciadorDeTelas, TelaJogo

# Inicializa o Pygame (DEVE VIR ANTES DE CARREGAR FONTES/IMAGENS)
pygame.init()
# Inicializa apenas o módulo de fonte explicitamente
pygame.font.init()

# Configurações da tela principal
# Usar DOUBLEBUF e HWSURFACE pode melhorar o desempenho em algumas máquinas
# vsync=1 tenta sincronizar com a taxa de atualização do monitor para evitar "tearing"
tela_principal = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), pygame.DOUBLEBUF | pygame.HWSURFACE, vsync=1)
pygame.display.set_caption("Marventura") # Título da janela do jogo

# --- Gerenciadores Principais ---
# Cria as instâncias únicas dos gerenciadores
gerenciador_recursos = GerenciadorDeRecursos()
gerenciador_banco_de_dados = DBManager()

# Carrega todos os assets (imagens, fontes) para a memória
gerenciador_recursos.carregar_recursos()

# --- Função Principal do Jogo ---
def executar_jogo():
    """Função que contém o loop principal do jogo."""
    relogio = pygame.time.Clock()

    # Cria uma instância do GerenciadorDeTelas, passando os outros gerenciadores.
    # Ele será responsável por inicializar a primeira tela (menu principal).
    gerenciador_telas = GerenciadorDeTelas(tela_principal, gerenciador_recursos, gerenciador_banco_de_dados)

    rodando = True
    while rodando:
        # Delta time (dt) é o tempo em segundos desde o último frame.
        # É crucial para um movimento e animação independentes da taxa de quadros.
        dt = relogio.tick(FPS) / 1000.0
        eventos_pygame = pygame.event.get()

        for evento in eventos_pygame:
            # A verificação de QUIT deve estar no loop principal para garantir o encerramento adequado.
            if evento.type == pygame.QUIT:
                rodando = False
                continue # Pula o resto do loop para este evento
            # O gerenciador de telas lida com os eventos e a transição de telas
            gerenciador_telas.handle_input(evento)

        # --- Atualização do Estado dos Elementos ---
        # O gerenciador de telas atualiza a tela ativa, que por sua vez atualiza suas entidades.
        gerenciador_telas.update(dt)

        # --- Desenho ---
        # Limpa a tela com uma cor de fundo antes de desenhar a nova cena
        tela_principal.fill(PRETO)
        # O gerenciador de telas sabe qual tela desenhar
        gerenciador_telas.draw()

        # --- Atualização da Tela ---
        # pygame.display.flip() atualiza toda a superfície da tela para o que foi desenhado.
        pygame.display.flip()

    # --- Lógica de Encerramento ---
    # Antes de fechar, verifica se o jogador estava na tela de jogo para salvar o progresso.
    if isinstance(gerenciador_telas.tela_atual, TelaJogo):
        gerenciador_telas.tela_atual.salvar_progresso()
    else:
        # Se a tela atual NÃO for a de jogo, ainda assim tentamos salvar se a anterior foi.
        # Esta é uma segurança extra graças à sua outra modificação.
        print("Não estava na tela de jogo no momento de fechar. O progresso deve ter sido salvo na última transição.")

    # --- INÍCIO DA MODIFICAÇÃO ---
    # Garante que a conexão seja fechada antes de o Pygame encerrar.
    gerenciador_banco_de_dados.fechar_conexao()
    
    pygame.quit()
    # sys.exit() # <-- COMENTE OU REMOVA ESTA LINHA
    # --- FIM DA MODIFICAÇÃO ---


# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    executar_jogo()
