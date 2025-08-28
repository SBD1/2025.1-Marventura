# entidades/chefe.py

import pygame
from .personagem import Personagem
from utilidades.constantes import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entidades.habilidades import Habilidade



class Chefe(Personagem):
    """
    Representa um chefe no jogo.
    Herda de Personagem e pode ter comportamentos específicos de chefes.
    """

    def __init__(self, gerenciador_recursos, identificador, area, coordenada_x, coordenada_y, nome, descricao, vida_total, vida_atual, nivel, experiencia, habilidade: list['Habilidade'], inventario):
        super().__init__(gerenciador_recursos, identificador, coordenada_x, coordenada_y, nome, descricao, area)
        # Atributos específicos do chefe podem ser adicionados aqui
        self.vida_total = vida_total
        self.vida_atual = vida_atual
        self.nivel = nivel
        self.experiencia = experiencia
        self.habilidade = habilidade
        self.inventario = inventario

        # Carregar a imagem base e configurar o sprite inicial
        self.imagem_original = self.gerenciador_recursos.obter_imagem(self.nome)
        
        if self.imagem_original:
            self.imagem = self.imagem_original
        else:
            print(f"AVISO: Imagem '{self.nome}.png' não encontrada para o chefe '{self.nome}'. Usando fallback padrão.")
            self.imagem = pygame.Surface((LARGURA_JOGADOR, ALTURA_JOGADOR), pygame.SRCALPHA) # Usa tamanho similar ao jogador como fallback
            self.imagem.fill(CINZA)

        self.rect = self.imagem.get_rect(topleft=(int(self.coordenada_x), int(self.coordenada_y)))

        self.orientacao_atual = 'direita'



    def atualizar(self, dt, jogador_rect):
        """
        Atualiza o estado do chefe.
        Este método pode ser sobrescrito para adicionar lógica específica do chefe.
        :param dt: Delta time (tempo em segundos desde o último frame).
        """
        # Ajusta a orientação do chefe para encarar o jogador
        if jogador_rect.centerx < self.rect.centerx:
            self.orientacao_atual = 'direita'
        else:
            self.orientacao_atual = 'esquerda'
        
        # Aplica o flip na imagem se necessário
        imagem_para_desenhar = self.imagem_original
        if imagem_para_desenhar:
            if self.orientacao_atual == 'esquerda':
                self.imagem = pygame.transform.flip(imagem_para_desenhar, True, False)
            else:
                self.imagem = imagem_para_desenhar
        else: # Fallback se a imagem original não foi carregada
            # Mantém a imagem de fallback (cinza) ou cria uma nova, sem flip
            self.imagem = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            self.imagem.fill(CINZA)



    def desenhar(self, tela, camera_x=0, camera_y=0):
        """
        Desenha o chefe na tela, considerando a posição da câmera.
        :param tela: A superfície onde o chefe será desenhado.
        :param camera_x: A posição x da câmera.
        :param camera_y: A posição y da câmera.
        """
        pos_x = int(self.coordenada_x - camera_x)
        pos_y = int(self.coordenada_y - camera_y)
        tela.blit(self.imagem, (pos_x, pos_y))

        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            debug_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height)
            pygame.draw.rect(tela, AZUL_CLARO, debug_rect, 1)