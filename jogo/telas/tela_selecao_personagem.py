# telas/tela_selecao_personagem.py

import pygame
import sys
from .tela_modelo import TelaModelo
from utilidades.constantes import *

class TelaSelecaoPersonagem(TelaModelo):
    """
    Tela onde o jogador escolhe entre Menino e Menina ao iniciar um novo jogo.
    Ao escolher, solicita ao GerenciadorDeTelas para iniciar o jogo no mapa inicial,
    com o personagem selecionado e o ponto de entrada de "novo jogo".
    """
    def __init__(self, gerenciador_telas, gerenciador_recursos): # Adiciona gerenciador_telas
        super().__init__(gerenciador_telas, gerenciador_recursos)

        # --- Recursos específicos da Tela de Seleção de Personagem ---
        self.fonte_botoes = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_BOTAO)
        self.fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_TITULO)
        
        # Imagem de fundo comum para telas de menu
        self.imagem_fundo = self.gerenciador_recursos.obter_imagem(CHAVE_TELA_INICIAL)
        if not self.imagem_fundo:
            self.imagem_fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.imagem_fundo.fill(CINZA_ESCURO) # Fallback

        # Carregue imagens dos personagens aqui se forem desenhadas na UI desta tela
        self.imagem_menino_ui = self.gerenciador_recursos.obter_imagem(SHUAN) # Exemplo: Usando sprite existente
        self.imagem_menina_ui = self.gerenciador_recursos.obter_imagem(SILVIE) # Exemplo: Usando sprite existente

        # --- Constantes de Layout da Tela de Seleção ---
        self._largura_opcao = 250 # Largura da área clicável da opção
        self._altura_opcao = 300  # Altura da área clicável da opção
        self._espacamento_horizontal = 250 # Espaçamento entre as opções
        self._grossura_borda = 2 # Espessura da borda para o texto

        # --- Elementos da Tela de Seleção ---
        # Opção Menino
        self._rect_opcao_menino = pygame.Rect(
            LARGURA_TELA // 2 - self._largura_opcao - self._espacamento_horizontal // 2,
            ALTURA_TELA - 30 - self._altura_opcao,
            self._largura_opcao,
            self._altura_opcao
        )
        self._texto_menino = SHUAN
        self._imagem_menino_offset_y = 0 # Ajuste vertical para a imagem

        # Opção Menina
        self._rect_opcao_menina = pygame.Rect(
            LARGURA_TELA // 2 + self._espacamento_horizontal // 2,
            ALTURA_TELA - 30 - self._altura_opcao,
            self._largura_opcao,
            self._altura_opcao
        )
        self._texto_menina = SILVIE
        self._imagem_menina_offset_y = 0 # Ajuste vertical para a imagem

        # Botão "Voltar"
        self._rect_botao_voltar = pygame.Rect(
            LARGURA_TELA // 2 - 100,
            ALTURA_TELA - 80,
            200, 50
        )
        self._texto_botao_voltar = "Voltar"

    def handle_input(self, evento):
        super().handle_input(evento) # Chama o handle_input da base para eventos comuns (ex: QUIT)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Clique com o botão esquerdo
                if self._rect_opcao_menino.collidepoint(evento.pos):
                    print(f"Selecionado {SHUAN}! Iniciando novo jogo...")
                    self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_NOVO_JOGO, personagem=SHUAN)
                elif self._rect_opcao_menina.collidepoint(evento.pos):
                    print(f"Selecionado {SILVIE}! Iniciando novo jogo...")
                    self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_NOVO_JOGO, personagem=SILVIE)
                elif self._rect_botao_voltar.collidepoint(evento.pos):
                    print("Voltando ao Menu Principal...")
                    self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MENU_PRINCIPAL)
        return None

    def update(self, dt):
        return None

    def draw(self, tela):
        # Desenha o fundo
        tela.blit(self.imagem_fundo, (0, 0))

        # Desenha o título
        if self.fonte_titulo:
            self._desenhar_texto_com_borda(
                tela, "Selecione seu Personagem", self.fonte_titulo, BRANCO, PRETO, self._grossura_borda, (LARGURA_TELA // 2, 80)
            )

        # Desenha as opções de personagem
        # Opção Menino
        if self.imagem_menino_ui:
            img_rect_menino = self.imagem_menino_ui.get_rect(center=(self._rect_opcao_menino.centerx, self._rect_opcao_menino.centery + self._imagem_menino_offset_y))
            tela.blit(self.imagem_menino_ui, img_rect_menino)
        
        if self.fonte_botoes:
            self._desenhar_texto_com_borda(
                tela, self._texto_menino, self.fonte_botoes, BRANCO, PRETO, self._grossura_borda, 
                (self._rect_opcao_menino.centerx, self._rect_opcao_menino.top) # Posição do texto na parte superior
            )

        # Opção Menina
        if self.imagem_menina_ui:
            img_rect_menina = self.imagem_menina_ui.get_rect(center=(self._rect_opcao_menina.centerx, self._rect_opcao_menina.centery + self._imagem_menina_offset_y))
            tela.blit(self.imagem_menina_ui, img_rect_menina)
        
        if self.fonte_botoes:
            self._desenhar_texto_com_borda(
                tela, self._texto_menina, self.fonte_botoes, BRANCO, PRETO, self._grossura_borda,
                (self._rect_opcao_menina.centerx, self._rect_opcao_menina.top) # Posição do texto na parte superior
            )

        # Desenha o botão "Voltar"
        if self.fonte_botoes:
            self._desenhar_texto_com_borda(
                tela, self._texto_botao_voltar, self.fonte_botoes, BRANCO, PRETO, self._grossura_borda, self._rect_botao_voltar.center
            )

        # Opcional: desenhar retângulos de colisão para debug
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            pygame.draw.rect(tela, COR_CAIXA_COLISAO, self._rect_opcao_menino, 1)
            pygame.draw.rect(tela, COR_CAIXA_COLISAO, self._rect_opcao_menina, 1)
            pygame.draw.rect(tela, COR_CAIXA_COLISAO, self._rect_botao_voltar, 1)