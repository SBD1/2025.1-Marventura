# main.py

import pygame
import sys
from utilidades.constantes import *
from recursos import GerenciadorDeRecursos
from telas import GerenciadorDeTelas

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

# --- Carregar Recursos usando o gerenciador ---
# Carregar Fontes usando o gerenciador
caminho_arquivo_fonte = 'recursos/fontes/Tagesschrift-Regular.ttf'
gerenciador_recursos.load_font(CHAVE_FONTE_TITULO, caminho_arquivo_fonte, 70)       # Fonte para títulos grandes
gerenciador_recursos.load_font(CHAVE_FONTE_BOTAO, caminho_arquivo_fonte, 48)     # Fonte para botões
gerenciador_recursos.load_font(CHAVE_FONTE_NOME_CARTAZ, caminho_arquivo_fonte, 20)  # Fonte para nome no cartaz
gerenciador_recursos.load_font(CHAVE_FONTE_DATA_CARTAZ, caminho_arquivo_fonte, 12)   # Fonte para data/dados no cartaz

# --- Carregar Imagens usando o gerenciador ---
# Imagem de fundo comum (para menu inicial e tela de arquivos de progresso salvos)
gerenciador_recursos.load_image(CHAVE_TELA_INICIAL, 'recursos/imagens/cenario/tela_inicial.png', escalar_para_tamanho=(LARGURA_TELA, ALTURA_TELA))
# Imagem do logo (para a tela inicial)
gerenciador_recursos.load_image(CHAVE_LOGO, 'recursos/imagens/interface/logo.png')

# --- Carregar Imagens dos Cartazes de Procurado para Slots de Save (Por Tipo de Personagem) ---
gerenciador_recursos.load_image(CHAVE_CARTAZ_PROCURADA, 'recursos/imagens/interface/cartaz_de_procurado_menina.png')
gerenciador_recursos.load_image(CHAVE_CARTAZ_PROCURADO, 'recursos/imagens/interface/cartaz_de_procurado_menino.png')
gerenciador_recursos.load_image(CHAVE_CARTAZ_VAZIO, 'recursos/imagens/interface/cartaz_de_procurado_vazio.png')

# Carregar backgrounds para os mapas do jogo
# Use as chaves que você definiu para os backgrounds dos mapas em mapa_dados.py
gerenciador_recursos.load_image(CHAVE_CENARIO_CAMPO_COSTA_OESTE, 'recursos/imagens/cenario/ilha_campo_costa_oeste.png', escalar_para_altura=ALTURA_TELA)
gerenciador_recursos.load_image(CHAVE_CENARIO_CAMPO_VILA, 'recursos/imagens/cenario/ilha_campo_vila.png', escalar_para_altura=ALTURA_TELA)
gerenciador_recursos.load_image(CHAVE_CENARIO_NEVE_VILA, 'recursos/imagens/cenario/ilha_neve_vila.png', escalar_para_altura=ALTURA_TELA)
gerenciador_recursos.load_image(CHAVE_LOJA_INTERIOR, 'recursos/imagens/cenario/loja_interior.png')
gerenciador_recursos.load_image(CHAVE_COZINHA_INTERIOR, 'recursos/imagens/cenario/cozinha_interior.png')
# Certifique-se de carregar os fundos de TODOS os mapas que você definiu em mapa_dados.py aqui.


# --- Carregar Imagens do Jogador para Animação (Para Ambos os Tipos) ---
gerenciador_recursos.load_image(PERSONAGEM_MENINO, 'recursos/imagens/jogador/jogador_parado.png', escalar_para_altura=300)
gerenciador_recursos.load_image(PERSONAGEM_MENINA, 'recursos/imagens/jogador/jogadora_parada.png', escalar_para_altura=300)

gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINO}_em_repouso', 'recursos/imagens/jogador/jogador_parado.png', escalar_para_altura=120)
gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINO}_caminhando_1', 'recursos/imagens/jogador/jogador_caminhando_1.png', escalar_para_altura=120)
gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINO}_caminhando_2', 'recursos/imagens/jogador/jogador_caminhando_2.png', escalar_para_altura=120)

gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINA}_em_repouso', 'recursos/imagens/jogador/jogadora_parada.png', escalar_para_altura=120)
gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINA}_caminhando_1', 'recursos/imagens/jogador/jogadora_caminhando_1.png', escalar_para_altura=120)
gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINA}_caminhando_2', 'recursos/imagens/jogador/jogadora_caminhando_2.png', escalar_para_altura=120)

# --- Carregar Imagens dos Inimigos ---
gerenciador_recursos.load_image('inimigo_goblin', 'recursos/imagens/inimigos/goblin.png', escalar_para_altura=120) # Exemplo
gerenciador_recursos.load_image('inimigo_esqueleto', 'recursos/imagens/inimigos/esqueleto.png', escalar_para_altura=120) # Exemplo

# --- Carregar Ícone de Interação ---
gerenciador_recursos.load_image(CHAVE_ICONE_INTERACAO, 'recursos/imagens/icones/icone_interacao.png', escalar_para_altura=48)
gerenciador_recursos.load_image('icone_alerta_inimigo', 'recursos/imagens/icones/alerta.png', escalar_para_altura=48)
gerenciador_recursos.load_image('icone_interrogacao_inimigo', 'recursos/imagens/icones/interrogacao.png', escalar_para_altura=48) # Novo!


# Verifica se todos os recursos críticos foram carregados com sucesso
# Em um jogo real, você poderia exibir uma tela de erro e sair graciosamente.
if not gerenciador_recursos.all_loaded_successfully():
    print("Recursos críticos falharam ao carregar. Saindo.") # Print traduzido
    pygame.quit() # Sai do Pygame
    sys.exit() # Sai do script Python


# --- Função Principal do Jogo ---
def executar_jogo():
    relogio = pygame.time.Clock()

    # Cria uma instância do GerenciadorDeTelas.
    # Ele será responsável por inicializar a primeira tela (menu principal).
    gerenciador_telas = GerenciadorDeTelas(tela_principal, gerenciador_recursos)

    rodando = True
    while rodando:
        dt = relogio.tick(FPS) / 1000.0 # Delta time em segundos

        # --- Processamento de Eventos ---
        eventos_pygame = pygame.event.get()
        for evento in eventos_pygame:
            # O gerenciador de telas agora lida com os eventos e a transição de telas
            gerenciador_telas.handle_input(evento)

        # --- Atualização do Estado dos Elementos ---
        # O gerenciador de telas agora lida com a atualização e a transição de telas
        gerenciador_telas.update(dt)

        # --- Desenho ---
        tela_principal.fill(PRETO) # Limpa a tela antes de desenhar
        gerenciador_telas.draw() # O gerenciador de telas sabe qual tela desenhar

        # --- Atualização da Tela e Controle de FPS ---
        pygame.display.flip()

    # --- Fim do Jogo ---
    pygame.quit()
    sys.exit()

# Inicia o jogo chamando a função principal (se o script for executado diretamente)
if __name__ == "__main__":
    executar_jogo() # <-- Chama a função principal do jogo