# area_interacao.py

import pygame
from utilidades.constantes import *

class AreaInteracao(pygame.sprite.Sprite):
    """
    Representa uma área no mundo do jogo que ativa um evento quando o jogador a sobrepõe
    e interage (ex: pressiona uma tecla). Não é um obstáculo sólido.
    """
    def __init__(self, identificador, x, y, largura=None, altura=None, tipo_evento=None,
                 chance_sucesso=1.0, area_destino=None,
                 chave_imagem=None, gerenciador_recursos=None):
        super().__init__()

        self.identificador = identificador
        self.tipo_evento = tipo_evento
        self.chance_sucesso = chance_sucesso
        self.area_destino = area_destino
        self.chave_imagem = chave_imagem

        # Animação de chacoalhar horizontal
        self.animando = False
        self.ciclos_restantes = 0
        self.amplitude_chacoalho = 4  # pixels de deslocamento lateral
        self.contador_ciclo = 0


        # Se for usar imagem
        if chave_imagem:
            if not gerenciador_recursos:
                raise ValueError("gerenciador_recursos é obrigatório se chave_imagem for usada.")

            imagem = gerenciador_recursos.obter_imagem(chave_imagem)
            if imagem:
                self.imagem = imagem.convert_alpha()
                largura = imagem.get_width()
                altura = imagem.get_height()
            else:
                print(f"[AreaInteracao] ERRO: Imagem '{chave_imagem}' não encontrada.")
                self.imagem = pygame.Surface((1, 1), pygame.SRCALPHA)
                largura, altura = 1, 1
        else:
            if largura is None or altura is None:
                raise ValueError("largura e altura são obrigatórios se nenhuma imagem for usada.")
            self.imagem = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.imagem.fill((0, 0, 0, 0))  # transparente

        # Define a área de colisão
        self.rect = self.imagem.get_rect(topleft=(x, y))



    def iniciar_animacao_chacoalhar(self, ciclos=6):
        self.animando = True
        self.ciclos_restantes = ciclos  # Total de frames que vai oscilar
        self.contador_ciclo = 0



    def update(self):
        if self.animando:
            self.contador_ciclo += 1
            if self.contador_ciclo >= self.ciclos_restantes:
                self.animando = False



    def desenhar(self, superficie, camera_x):
        """
        Desenha a imagem da área de interação (se houver),
        ou o retângulo de colisão para debug.
        """
        pos_x = self.rect.x - camera_x
        pos_y = self.rect.y

        if self.animando:
            deslocamento = self.amplitude_chacoalho if self.contador_ciclo % 2 == 0 else -self.amplitude_chacoalho
            pos_x += deslocamento

        if self.imagem:
            superficie.blit(self.imagem, (pos_x, pos_y))

        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            pygame.draw.rect(
                superficie,
                COR_CAIXA_COLISAO,
                pygame.Rect(pos_x, pos_y, self.rect.width, self.rect.height),
                1
            )
