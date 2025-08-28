import pygame
from utilidades.constantes import * # Importa as constantes

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import GerenciadorDeRecursos

class Personagem(pygame.sprite.Sprite):
    def __init__(self, gerenciador_recursos: 'GerenciadorDeRecursos', identificador, coordenada_x, coordenada_y, nome, descricao, area = None):
        """ Inicializa o personagem.
        :param gerenciador_recursos: Gerenciador de recursos do jogo.
        :param identificador: Identificador único do personagem.
        :param coordenada_x: Posição X inicial do personagem.
        :param coordenada_y: Posição Y inicial do personagem.
        :param nome: Nome do personagem.
        :param descricao: Descrição do personagem.
        :param area: Área onde o personagem está localizado (opcional)."""
        super().__init__()
        self.gerenciador_recursos = gerenciador_recursos
        self.identificador: str = identificador
        self.area: str = area
        self.nome: str = nome
        self.descricao: str = descricao
        self.coordenada_x = float(coordenada_x)
        self.coordenada_y = float(coordenada_y)



    def atualizar(self, dt):
        """
        Atualiza o estado do personagem.
        Este método pode ser sobrescrito por subclasses para adicionar lógica específica.
        """
        pass



    def desenhar(self, tela: pygame.surface.Surface, camera_x=0, camera_y=0):
        """
        Desenha o personagem na tela, considerando a posição da câmera.
        """
        pass