# utilidades/camera.py

import pygame
import math # Para funções de interpolação se necessário
from utilidades.constantes import *

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
        self.rect = pygame.Rect(0, 0, largura_janela, altura_janela)

        # offset_x é o valor que precisa ser subtraído das coordenadas
        # do mundo para desenhar na tela (perspectiva da câmera).
        self.offset_x = 0
        self.offset_y = 0 # Adicionado offset_y para rolagem vertical

        # --- NOVOS ATRIBUTOS PARA CONTROLE AVANÇADO DA CÂMERA ---
        # Modos de operação da câmera
        self.modo = 'seguir_jogador' # 'seguir_jogador', 'foco_fixo', 'movimento_suave'

        # Para modo 'foco_fixo'
        self.ponto_foco_x = 0
        self.ponto_foco_y = 0

        # Para modo 'movimento_suave'
        self.destino_x = 0
        self.destino_y = 0
        self.velocidade_movimento_suave = 0 # Pixels por segundo
        self.tempo_inicio_movimento = 0
        self.duracao_movimento = 0 # Em milissegundos
        self.ponto_inicial_movimento_x = 0
        self.ponto_inicial_movimento_y = 0
        self.movimento_completo = True # Flag para saber se o movimento suave terminou

        # Para zoom (abordagem mais simples, apenas para demonstração)
        self.zoom_level = 1.0 # 1.0 = zoom normal. Valores maiores aproximam (menos do mapa visível).
        # Nota: O zoom afetaria o tamanho real do rect da câmera ou a escala dos elementos desenhados.
        # Para um zoom real que redimensiona a área visível da câmera, precisaríamos recalcular o rect
        # e ajustar as coordenadas de desenho. Por enquanto, foco no movimento.

    def _aplicar_limites_mundo(self):
        """Garra que a câmera não saia dos limites do mundo."""
        if self.rect.left < 0:
            self.rect.left = 0
        if not self.largura_mundo == INFINITO and self.rect.right > self.largura_mundo:
            self.rect.right = self.largura_mundo
        if self.rect.top < 0:
            self.rect.top = 0
        if not self.altura_mundo == INFINITO and self.rect.bottom > self.altura_mundo:
            self.rect.bottom = self.altura_mundo

        # Atualiza os offsets com base na posição final do rect
        self.offset_x = self.rect.x
        self.offset_y = self.rect.y

    def atualizar(self, dt_ms, target_rect=None): # dt_ms é delta time em milissegundos
        """
        Atualiza a posição da câmera com base no modo atual.
        :param dt_ms: Delta time em milissegundos (pygame.time.get_ticks() - último_tick).
        :param target_rect: O pygame.Rect do objeto que a câmera deve seguir (apenas no modo 'seguir_jogador').
        """
        if self.modo == 'seguir_jogador' and target_rect:
            self.rect.centerx = target_rect.centerx
            self.rect.centery = target_rect.centery
            self.movimento_completo = True # Reseta flag se mudar para seguir jogador

        elif self.modo == 'foco_fixo':
            self.rect.centerx = self.ponto_foco_x
            self.rect.centery = self.ponto_foco_y
            self.movimento_completo = True # Reseta flag

        elif self.modo == 'movimento_suave':
            if not self.movimento_completo:
                tempo_decorrido = pygame.time.get_ticks() - self.tempo_inicio_movimento

                if tempo_decorrido < self.duracao_movimento:
                    # Interpolação linear (LERP)
                    t = tempo_decorrido / self.duracao_movimento
                    self.rect.centerx = self.ponto_inicial_movimento_x + (self.destino_x - self.ponto_inicial_movimento_x) * t
                    self.rect.centery = self.ponto_inicial_movimento_y + (self.destino_y - self.ponto_inicial_movimento_y) * t
                else:
                    self.rect.centerx = self.destino_x
                    self.rect.centery = self.destino_y
                    self.movimento_completo = True
                    self.modo = 'foco_fixo' # Ou pode voltar para 'seguir_jogador' automaticamente aqui

        self._aplicar_limites_mundo() # Garante que a câmera não saia dos limites

    def focar_em_ponto(self, x_mundo, y_mundo):
        """
        Define a câmera para focar instantaneamente em um ponto específico do mundo.
        :param x_mundo: Coordenada X do mundo para focar.
        :param y_mundo: Coordenada Y do mundo para focar.
        """
        self.ponto_foco_x = x_mundo
        self.ponto_foco_y = y_mundo
        self.modo = 'foco_fixo'
        self.movimento_completo = True # Garante que qualquer movimento suave anterior seja parado.

    def iniciar_movimento_suave(self, inicio_x, inicio_y, fim_x, fim_y, duracao_ms):
        """
        Inicia um movimento suave da câmera de um ponto a outro.
        :param inicio_x: Coordenada X inicial do movimento.
        :param inicio_y: Coordenada Y inicial do movimento.
        :param fim_x: Coordenada X final do movimento.
        :param fim_y: Coordenada Y final do movimento.
        :param duracao_ms: Duração total do movimento em milissegundos.
        """
        self.ponto_inicial_movimento_x = inicio_x
        self.ponto_inicial_movimento_y = inicio_y
        self.destino_x = fim_x
        self.destino_y = fim_y
        self.duracao_movimento = duracao_ms
        self.tempo_inicio_movimento = pygame.time.get_ticks()
        self.modo = 'movimento_suave'
        self.movimento_completo = False

    def movimento_suave_completo(self):
        """Retorna True se o movimento suave da câmera terminou."""
        return self.movimento_completo

    def retornar_para_jogador(self):
        """Define o modo da câmera de volta para seguir o jogador."""
        self.modo = 'seguir_jogador'
        self.movimento_completo = True # Reseta flag


    def aplicar_deslocamento_da_camera(self, retangulo_da_entidade):
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
        return retangulo_da_entidade.move(-self.rect.x, -self.rect.y)

    def aplicar_deslocamento_por_ponto(self, ponto_x, ponto_y):
        """
        Aplica o offset da câmera a um ponto (x, y) do mundo,
        retornando a posição na tela.

        :param point_x: Coordenada X do mundo.
        :param point_y: Coordenada Y do mundo.
        :return: Uma tupla (x_tela, y_tela) com a posição na tela.
        """
        return ponto_x - self.rect.x, ponto_y - self.rect.y