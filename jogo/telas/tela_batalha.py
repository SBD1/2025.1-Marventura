# telas/tela_batalha.py

import pygame
from utilidades.constantes import *
from .tela_modelo import TelaModelo

class TelaBatalha(TelaModelo):
    def __init__(self, gerenciador_telas, gerenciador_recursos, personagem, inimigo_tipo, jogador_x, jogador_y, jogador_olhando_direita, mapa_retorno_id):
        super().__init__(gerenciador_telas, gerenciador_recursos) # Já chamava corretamente
        self.inimigo_tipo = inimigo_tipo
        self.personagem = personagem
        
        # Dados do jogador para retornar ao mapa
        self.jogador_x_retorno = jogador_x
        self.jogador_y_retorno = jogador_y
        self.jogador_olhando_direita_retorno = jogador_olhando_direita
        self.mapa_retorno_id = mapa_retorno_id

        self.fundo_batalha = self.gerenciador_recursos.obter_imagem('batalha_fundo_padrao')
        if not self.fundo_batalha:
            self.fundo_batalha = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.fundo_batalha.fill(CINZA_ESCURO)
            print("AVISO: Imagem 'batalha_fundo_padrao' não encontrada. Usando fundo cinza.")

        self.imagem_inimigo = self.gerenciador_recursos.obter_imagem(f'batalha_inimigo_{inimigo_tipo}')
        if not self.imagem_inimigo:
             print(f"AVISO: Imagem de batalha para '{inimigo_tipo}' não encontrada. Usando cor fallback.")
             self.imagem_inimigo = pygame.Surface((150, 150))
             self.imagem_inimigo.fill(VERMELHO)

        self.fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_TITULO)
        self.fonte_botao = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_BOTAO)

        self.texto_batalha = f"Uma batalha contra um {self.inimigo_tipo}!"
        self.texto_botao = "Fugir (Voltar ao Mapa)"

        self.rect_botao = pygame.Rect(LARGURA_TELA // 2 - 150, ALTURA_TELA - 100, 300, 70)

    def handle_input(self, evento):
        # Chama o handle_input da base para eventos comuns (ex: QUIT)
        super().handle_input(evento)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect_botao.collidepoint(evento.pos):
                print("Fugindo da batalha...")
                # Usa o gerenciador de telas para solicitar a transição de volta
                self.gerenciador_telas.mudar_tela(
                    CHAVE_TRANSICAO_MAPA,
                    id_mapa=self.mapa_retorno_id, # Usar 'id_proximo_mapa' para o TelaJogo
                    personagem=self.personagem, # Você pode passar o tipo de personagem de volta se for relevante
                    coordenada_x=self.jogador_x_retorno,
                    coordenada_y=self.jogador_y_retorno,
                    olhando_para_direita=self.jogador_olhando_direita_retorno
                )
                return # Nenhuma transição de tela a ser reportada diretamente
        return None

    def update(self, dt):
        return None

    def draw(self, tela):
        tela.blit(self.fundo_batalha, (0, 0))

        if self.imagem_inimigo:
            inimigo_rect = self.imagem_inimigo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 100))
            tela.blit(self.imagem_inimigo, inimigo_rect)

        if self.fonte_titulo:
            self._desenhar_texto_com_borda(tela, self.texto_batalha, self.fonte_titulo, BRANCO, PRETO, 2, (LARGURA_TELA // 2, 50))

        pygame.draw.rect(tela, VERMELHO, self.rect_botao, border_radius=10)
        if self.fonte_botao:
            self._desenhar_texto_com_borda(tela, self.texto_botao, self.fonte_botao, BRANCO, PRETO, 1, self.rect_botao.center)