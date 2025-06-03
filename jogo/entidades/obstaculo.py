# obstaculo.py

import pygame
from utilidades.constantes import *

class Obstaculo(pygame.sprite.Sprite):
    """
    Representa um obstáculo no mundo do jogo.
    Pode ser uma parede, um limite de caminho, ou qualquer objeto sólido que colide com o jogador.
    """
    def __init__(self, gerenciador_recursos, x, y, largura, altura, chave_imagem=None):
        """
        Inicializa um obstáculo.
        :param gerenciador_recursos: O gerenciador de recursos do jogo.
        :param x: Posição X no mundo do jogo (canto superior esquerdo).
        :param y: Posição Y no mundo do jogo (canto superior esquerdo).
        :param largura: Largura do obstáculo.
        :param altura: Altura do obstáculo.
        :param chave_imagem: Chave da imagem no gerenciador de recursos (opcional, se o obstáculo tiver uma imagem visível).
        """
        super().__init__()
        # Armazena a referência ao gerenciador de recursos
        self.gerenciador_recursos = gerenciador_recursos

        # Definir o retângulo de colisão do obstáculo no mundo
        # Mantemos 'rect' pois é um atributo padrão de Sprite
        self.rect = pygame.Rect(x, y, largura, altura)

        # Imagem do obstáculo (opcional, para visualização se não for apenas um limite invisível)
        self.imagem = None
        if chave_imagem:
            self.imagem = self.gerenciador_recursos.obter_imagem(chave_imagem)
            # Nota: Se o obstáculo tiver uma imagem visível, o self.rect
            # normalmente seria o rect da imagem, posicionado em (x, y).
            # Ou a imagem seria redimensionada para self.rect.
            # Como este obstáculo é focado na colisão, o rect é a prioridade.
            # Se for desenhar a imagem, precisa ajustar o desenho relativo ao self.rect.

    def draw(self, superficie, camera_x):
        """
        Desenha o obstáculo na tela.
        Desenha a imagem visível (se existir) ou a caixa de colisão de debug.
        :param superficie: A superfície onde desenhar (a tela principal do jogo).
        :param camera_x: A posição X da câmera para ajustar as coordenadas de desenho para a tela.
        """
        # Ajusta a posição do retângulo do obstáculo para a tela, baseada na câmera
        posicao_tela_x = self.rect.x - camera_x
        posicao_tela_y = self.rect.y # Assumindo câmera apenas horizontal

        # Se o obstáculo tiver uma imagem visível, desenha-a primeiro
        if self.imagem:
            superficie.blit(self.imagem, (posicao_tela_x, posicao_tela_y))

        # Desenha a caixa de colisão para debug, se a flag estiver ativada
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            # Cria um retângulo para desenhar na tela
            retangulo_tela_debug = pygame.Rect(
                posicao_tela_x,
                posicao_tela_y,
                self.rect.width, # Usa largura e altura do rect original
                self.rect.height
            )
            # Desenha o contorno do retângulo de colisão na superfície da tela
            pygame.draw.rect(superficie, COR_CAIXA_COLISAO, retangulo_tela_debug, 1) # 1 para desenhar apenas o contorno

    def update(self):
        """
        Atualiza o estado do obstáculo.
        Obstáculos estáticos (como limites de caminho) geralmente não precisam de lógica de atualização.
        """
        # Lógica de atualização para obstáculos dinâmicos (movendo, etc.) viria aqui.
        pass # Obstáculos estáticos não fazem nada no update