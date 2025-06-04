# utilidades/camera.py

import pygame

class Camera:
    def __init__(self, largura_janela, altura_janela, tamanho_mundo):
        """
        Inicializa a câmera.

        :param largura_janela: Largura da janela do jogo (tela).
        :param altura_janela: Altura da janela do jogo (tela).
        :param tamanho_mundo: Uma tupla (largura_mundo, altura_mundo) representando
                              as dimensões totais do mapa do jogo.
        """
        self.largura_janela = largura_janela
        self.altura_janela = altura_janela
        self.largura_mundo, self.altura_mundo = tamanho_mundo

        # O 'rect' da câmera representa a área visível do mundo.
        # Começa no canto superior esquerdo do mundo.
        self.rect = pygame.Rect(0, 0, largura_janela, altura_janela)

        # offset_x é o valor que precisa ser subtraído das coordenadas
        # do mundo para desenhar na tela (perspectiva da câmera).
        self.offset_x = 0

    def update(self, target_rect):
        """
        Atualiza a posição da câmera para seguir um alvo (target_rect),
        geralmente o jogador.

        :param target_rect: O pygame.Rect do objeto que a câmera deve seguir.
        """
        # Centraliza a câmera no alvo
        self.rect.centerx = target_rect.centerx
        self.rect.centery = target_rect.centery

        # Garante que a câmera não saia dos limites do mundo
        # Limite Esquerdo
        if self.rect.left < 0:
            self.rect.left = 0
        # Limite Direito
        if self.rect.right > self.largura_mundo:
            self.rect.right = self.largura_mundo
        # Limite Superior
        if self.rect.top < 0:
            self.rect.top = 0
        # Limite Inferior
        if self.rect.bottom > self.altura_mundo:
            self.rect.bottom = self.altura_mundo

        # Calcula o offset de x para desenhar os elementos do mundo.
        # Se o jogador está na posição mundo_x, ele deve ser desenhado em (mundo_x - offset_x) na tela.
        self.offset_x = self.rect.x

    def apply(self, entity_rect):
        """
        Aplica o offset da câmera a um pygame.Rect de uma entidade,
        retornando a posição na tela.

        Este método não é estritamente necessário se você fizer a subtração
        diretamente no draw de cada entidade, como no código atualizado.
        Ele seria mais útil se você quisesse que a própria câmera retornasse
        a posição transformada.

        :param entity_rect: O pygame.Rect da entidade na coordenada do mundo.
        :return: Um novo pygame.Rect representando a posição da entidade na tela.
        """
        return entity_rect.move(-self.rect.x, -self.rect.y)

    def apply_point(self, point_x, point_y):
        """
        Aplica o offset da câmera a um ponto (x, y) do mundo,
        retornando a posição na tela.

        :param point_x: Coordenada X do mundo.
        :param point_y: Coordenada Y do mundo.
        :return: Uma tupla (x_tela, y_tela) com a posição na tela.
        """
        return point_x - self.rect.x, point_y - self.rect.y