# tela_inicial.py

import pygame
import sys
from .tela_modelo import TelaModelo
from utilidades.constantes import *

class TelaInicial(TelaModelo):
    """
    Representa a tela inicial (menu principal) do jogo.
    Contém a logo do jogo e botões para "Novo Jogo" e "Fechar".
    Acessa recursos visuais e fontes via gerenciador de recursos.
    """
    # Recebe o gerenciador de recursos no construtor
    def __init__(self, gerenciador_recursos):
        # Chama o construtor da classe base, passando o gerenciador
        super().__init__(gerenciador_recursos)

        # --- Obtém os recursos necessários do gerenciador ---
        # Obtém a imagem da logo e as fontes para os botões e títulos
        self.imagem_logo = self.gerenciador_recursos.get_image(CHAVE_LOGO)
        self.fonte_botoes = self.gerenciador_recursos.get_font(CHAVE_FONTE_BOTAO)
        self.fonte_grande = self.gerenciador_recursos.get_font(CHAVE_FONTE_TITULO)

        # Nota: O carregamento e redimensionamento da logo são feitos no GerenciadorDeRecursos

        # --- Elementos específicos da tela inicial (posições, tamanhos, textos) ---
        # Estes são definidos localmente para esta tela.

        # Posições e dimensões dos botões
        _largura_botao = 300
        _altura_botao = 45
        # Centraliza horizontalmente
        _x_botao = (LARGURA_TELA - _largura_botao) // 2
        # Posição vertical inicial mais embaixo na tela
        _y_inicio_botao = ALTURA_TELA - 150
        _espacamento_botao = 60 # Espaçamento entre os botões

        # Cria os retângulos de colisão/posicionamento para os botões
        self._rect_botao_iniciar = pygame.Rect(_x_botao, _y_inicio_botao, _largura_botao, _altura_botao)
        self._rect_botao_sair = pygame.Rect(_x_botao, _y_inicio_botao + _espacamento_botao, _largura_botao, _altura_botao)

        # Textos dos botões
        self._texto_botao_iniciar = "Novo jogo"
        self._texto_botao_sair = "Fechar"

        # Grossura da borda do texto para os botões
        self._grossura_borda = 2


    def handle_event(self, event):
        """
        Processa um evento para a tela inicial (menu principal).
        Verifica cliques nos botões "Novo Jogo" e "Fechar".
        Retorna o ID do próximo estado (ESTADO_MENU_SALVAR) ou sys.exit para sair.
        Retorna None para continuar na mesma tela.
        """
        # Chama o manipulador de eventos da classe base (para eventos comuns, ex: ESC para menu de pausa)
        proximo_estado = super().handle_event(event)

        # Se a classe base já tratou o evento e retornou um próximo estado (diferente de None), retorna esse estado imediatamente
        if proximo_estado is not None:
             return proximo_estado

        # --- Lógica específica da Tela Inicial ---
        # Verifica se o evento foi um clique do botão do mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica se o botão clicado foi o botão esquerdo (botão 1)
            if event.button == 1:
                posicao_mouse = event.pos
                # Verifica se a posição do clique colide com o retângulo do botão "Novo Jogo"
                if self._rect_botao_iniciar.collidepoint(posicao_mouse):
                    print("Clicou em Novo Jogo -> Mudando para Tela de Saves") # Print de debug
                    # Sinaliza para o loop principal mudar para o estado da tela de salvar/carregar
                    return ESTADO_MENU_SALVAR
                # Verifica se a posição do clique colide com o retângulo do botão "Fechar"
                elif self._rect_botao_sair.collidepoint(posicao_mouse):
                    print("Clicou em Fechar -> Saindo") # Print de debug
                    # Sinaliza para o loop principal sair completamente do jogo
                    return sys.exit() # Retorna sys.exit para sair

        # Se nenhum evento específico da tela inicial foi tratado que cause uma mudança de estado, retorna None
        return None # Continua na mesma tela (TelaInicial)


    def draw(self, tela):
        """
        Desenha todos os elementos da tela inicial na superfície da tela.
        Desenha o fundo, a logo e os botões.
        :param tela: A superfície principal (tela) onde desenhar.
        """
        # Desenha o fundo comum usando o método da classe base (que obtém o fundo do gerenciador)
        super().draw(tela) # <-- Chama o método draw da base

        # Desenha a logo centralizada em cima (imagem obtida do gerenciador)
        if self.imagem_logo:
            # Obtém o retângulo da logo e o centraliza horizontalmente na posição vertical 1/4 da tela
            rect_logo = self.imagem_logo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 4))
            # Desenha a logo na tela
            tela.blit(self.imagem_logo, rect_logo)

        # Desenha os textos dos botões com borda, usando o método auxiliar da classe base
        # Usa os textos, a fonte dos botões e as cores BRANCO/PRETO (obtidas das constantes)
        # Passa o centro dos retângulos dos botões para posicionar o texto
        self._desenhar_texto_com_borda( # <-- Chama o método auxiliar
            tela, # Superfície onde desenhar
            self._texto_botao_iniciar, # Texto
            self.fonte_botoes, # Fonte
            BRANCO, PRETO, # Cores
            self._grossura_borda, # Grossura da borda
            self._rect_botao_iniciar.center # Posição central
        )
        self._desenhar_texto_com_borda( # <-- Chama o método auxiliar
            tela, # Superfície onde desenhar
            self._texto_botao_sair, # Texto
            self.fonte_botoes, # Fonte
            BRANCO, PRETO, # Cores
            self._grossura_borda, # Grossura da borda
            self._rect_botao_sair.center # Posição central
        )

        # Opcional: desenhar retângulos de colisão para debug
        # Verifica se a flag de debug de colisão está ativa (obtida das constantes)
        # if DEBUG_DESENHAR_CAIXAS_COLISAO:
        #    pygame.draw.rect(tela, VERMELHO, self._rect_botao_iniciar, 1) # Desenha o contorno do rect
        #    pygame.draw.rect(tela, VERMELHO, self._rect_botao_sair, 1)   # Desenha o contorno do rect