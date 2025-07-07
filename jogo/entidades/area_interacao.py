# area_interacao.py

import pygame
from utilidades.constantes import *

class AreaInteracao(pygame.sprite.Sprite):
    """
    Representa uma área no mundo do jogo que ativa um evento quando o jogador a sobrepõe
    e interage (ex: pressiona uma tecla). Não é um obstáculo sólido.
    """
    def __init__(self, x, y, largura, altura, tipo_evento,
        mudar_area = None, navegar_para = None, investigar = None, ):
        """
        Inicializa uma Área de Interação.
        :param x: Posição X no mundo do jogo (canto superior esquerdo).
        :param y: Posição Y no mundo do jogo (canto superior esquerdo).
        :param largura: Largura da área.
        :param altura: Altura da área.
        :param tipo_evento: Uma string que define o tipo de evento (ex: 'mudar_mapa', 'dialogo').
        :param dados_evento: Um dicionário ou objeto contendo dados específicos para o evento (ex: {'mapa_id': 'outra_ilha'}).
        :param resource_manager: O gerenciador de recursos (opcional, pode ser necessário para carregar ícones).
        """
        super().__init__()

        # Definir o retângulo da área de interação no mundo
        self.rect = pygame.Rect(x, y, largura, altura)

        # Informações sobre o evento a ser ativado
        self.tipo_evento = tipo_evento
        self.ir_para_area = mudar_area
        self.navegar_para = navegar_para
        self.investigar = investigar

        # A área de interação não precisa de uma imagem visível por padrão,
        # mas podemos desenhar seu contorno para debug.
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA) # Cria uma superfície transparente
        self.image.fill((0, 0, 0, 0)) # Totalmente transparente

        # O ícone de interação (ex: balão de fala) será desenhado na GameScreen

    def update(self):
        # Áreas de interação estáticas geralmente não precisam de um método update
        pass

    def draw(self, superficie, camera_x):
        """
        Desenha a caixa de colisão da área de interação para debug, se ativado.
        :param superficie: A superfície onde desenhar (a tela principal do jogo).
        :param camera_x: A posição X da câmera para ajustar as coordenadas de desenho.
        """
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            # Ajusta a posição do retângulo para a tela
            screen_rect = pygame.Rect(
                self.rect.x - camera_x,
                self.rect.y,
                self.rect.width,
                self.rect.height
            )
            # Desenha o contorno do retângulo de colisão para debug
            # Usa a cor de debug definida em constantes.py
            pygame.draw.rect(superficie, COR_CAIXA_COLISAO, screen_rect, 1) # Desenha apenas o contorno
            
            