# entidades/caminho.py

import pygame
from utilidades.constantes import *

class Caminho(pygame.Rect):
    """
    Representa um caminho no mundo do jogo.
    Um caminho é uma área onde o jogador pode se mover livremente, sem obstáculos.
    """
    def __init__(self, x, y, largura, altura, tipo_terreno):
        """
        Inicializa um caminho.
        :param x: Posição X no mundo do jogo (canto superior esquerdo).
        :param y: Posição Y no mundo do jogo (canto superior esquerdo).
        :param largura: Largura do caminho.
        :param altura: Altura do caminho.
        """
        super().__init__(x, y, largura, altura)
        self.tipo_terreno = tipo_terreno

    def desenhar(self, tela, camera_x):
        """
        Desenha o caminho na tela.
        :param tela: A superfície onde desenhar (a tela principal do jogo).
        :param camera_x: A posição X da câmera para ajustar as coordenadas de desenho para a tela.
        """
        # Ajusta a posição do retângulo do caminho para a tela, baseada na câmera
        posicao_tela_x = self.x - camera_x
        posicao_tela_y = self.y

        # Desenha o caminho como um retângulo preenchido
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            superficie = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            if self.tipo_terreno == 'arena':
                superficie.fill((255, 0, 0, 50))
            elif self.tipo_terreno == 'normal':
                superficie.fill((0, 255, 0, 50))
            elif self.tipo_terreno == 'neve':
                superficie.fill((0, 0, 255, 50))

            tela.blit(superficie, (posicao_tela_x, posicao_tela_y))