# telas/tela_selecao_personagem.py

import pygame
import sys
from .tela_modelo import TelaModelo
from utilidades.constantes import *

class TelaSelecaoPersonagem(TelaModelo):
    """
    Tela onde o jogador escolhe entre Menino e Menina ao iniciar um novo jogo.
    """
    def __init__(self, gerenciador_recursos):
        super().__init__(gerenciador_recursos)

        # --- Recursos específicos da Tela de Seleção de Personagem ---
        # Obtém fontes e possibly imagens de ícones dos personagens (se existirem)
        self.fonte_botoes = self.gerenciador_recursos.get_font('botao')
        self.fonte_grande = self.gerenciador_recursos.get_font('titulo')
        # Carregue imagens dos personagens aqui, se necessário para a UI
        # self.imagem_menino_ui = self.gerenciador_recursos.get_image('personagem_menino_ui')
        # self.imagem_menina_ui = self.gerenciador_recursos.get_image('personagem_menina_ui')


        # --- Elementos da Tela de Seleção ---
        # Botões/Áreas clicáveis para selecionar
        _largura_opcao = 200 # Exemplo
        _altura_opcao = 60   # Exemplo
        _espacamento = 40    # Exemplo

        # Calcula posições para centralizar as opções horizontalmente
        _largura_total_opcoes = (2 * _largura_opcao) + _espacamento
        _inicio_x = (LARGURA_TELA - _largura_total_opcoes) // 2
        _y_opcoes = ALTURA_TELA // 2 # Centralizado verticalmente

        self._rect_opcao_menino = pygame.Rect(_inicio_x, _y_opcoes, _largura_opcao, _altura_opcao)
        self._rect_opcao_menina = pygame.Rect(_inicio_x + _largura_opcao + _espacamento, _y_opcoes, _largura_opcao, _altura_opcao)

        # Textos para as opções
        self._texto_menino = "Menino"
        self._texto_menina = "Menina"

        # Título da tela
        self._texto_titulo = "Escolha seu personagem"

        # Grossura da borda do texto para os botões
        self._grossura_borda = 2


    def handle_event(self, event):
        """
        Processa eventos para a tela de seleção de personagem.
        Verifica cliques nas opções Menino/Menina.
        Retorna um dicionário para iniciar o jogo com o personagem escolhido,
        ou None para continuar na mesma tela.
        """
        proximo_estado = super().handle_event(event)
        if proximo_estado is not None:
             return proximo_estado

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Botão esquerdo
                posicao_mouse = event.pos

                # Verifica clique na opção Menino
                if self._rect_opcao_menino.collidepoint(posicao_mouse):
                    print("Selecionou Menino. Iniciando novo jogo.")
                    # Retorna o estado para ir para o jogo, o mapa inicial e o tipo de personagem
                    return {'estado': ESTADO_JOGO, 'map_id': MAPA_INICIAL_ID, 'character_type': PERSONAGEM_MENINO}

                # Verifica clique na opção Menina
                elif self._rect_opcao_menina.collidepoint(posicao_mouse):
                    print("Selecionou Menina. Iniciando novo jogo.")
                    # Retorna o estado para ir para o jogo, o mapa inicial e o tipo de personagem
                    return {'estado': ESTADO_JOGO, 'map_id': MAPA_INICIAL_ID, 'character_type': PERSONAGEM_MENINA} # Note: era PERSONAGEM_MENINA

        return None

    def draw(self, tela):
        """
        Desenha todos os elementos da tela de seleção de personagem.
        Desenha o fundo, título e opções de personagem.
        """
        super().draw(tela) # Desenha o fundo comum

        # Desenha o título
        if self.fonte_grande:
            texto_titulo_surface = self.fonte_grande.render(self._texto_titulo, True, BRANCO)
            rect_titulo = texto_titulo_surface.get_rect(center=(LARGURA_TELA // 2, 100))
            tela.blit(texto_titulo_surface, rect_titulo)
        else:
             print("AVISO: Fonte grande não disponível para título da tela de seleção.")


        # Desenha as opções (textos e retângulos)
        if self.fonte_botoes:
             # Desenha opção Menino
             self._desenhar_texto_com_borda(
                 tela, self._texto_menino, self.fonte_botoes, BRANCO, PRETO, self._grossura_borda, self._rect_opcao_menino.center
             )
             # Desenha opção Menina
             self._desenhar_texto_com_borda(
                 tela, self._texto_menina, self.fonte_botoes, BRANCO, PRETO, self._grossura_borda, self._rect_opcao_menina.center
             )
        else:
             print("AVISO: Fonte de botões não disponível para tela de seleção.")

        # Opcional: desenhar imagens dos personagens ao lado dos textos
        # if self.imagem_menino_ui:
        #    rect_imagem_menino = self.imagem_menino_ui.get_rect(center=(self._rect_opcao_menino.center[0], self._rect_opcao_menino.center[1] - 50))
        #    tela.blit(self.imagem_menino_ui, rect_imagem_menino)
        # if self.imagem_menina_ui:
        #    rect_imagem_menina = self.imagem_menina_ui.get_rect(center=(self._rect_opcao_menina.center[0], self._rect_opcao_menina.center[1] - 50))
        #    tela.blit(self.imagem_menina_ui, rect_imagem_menina)


        # Opcional: desenhar retângulos de debug
        # if DEBUG_DESENHAR_CAIXAS_COLISAO:
        #    pygame.draw.rect(tela, VERMELHO, self._rect_opcao_menino, 1)
        #    pygame.draw.rect(tela, VERMELHO, self._rect_opcao_menina, 1)