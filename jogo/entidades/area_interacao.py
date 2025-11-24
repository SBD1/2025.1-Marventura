# area_interacao.py

import pygame
from utilidades.constantes import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import GerenciadorDeRecursos

class AreaInteracao(pygame.sprite.Sprite):
    """
    Representa uma área no mundo do jogo que ativa um evento quando o jogador a sobrepõe
    e interage (ex: pressiona uma tecla). Não é um obstáculo sólido.
    """
    def __init__(self, identificador, x, y, largura, altura, tipo_evento, metodo_ativacao,
                ativa, chance_sucesso=1.0, area_destino=None, chave_imagem=None, identificador_missao=None, gererenciador_recursos:'GerenciadorDeRecursos'=None):
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

        self.tipo_evento = tipo_evento
        self.chance_sucesso = chance_sucesso
        self.area_destino = area_destino
        self.metodo_ativacao = metodo_ativacao
        self.ativa = ativa
        self.identificador_missao = identificador_missao
        self.chave_imagem = chave_imagem
        self.gerenciador_recursos = gererenciador_recursos
        self.identificador = identificador

        # Animação de chacoalhar horizontal
        self.animando = False
        self.ciclos_restantes = 0
        self.amplitude_chacoalho = 4  # pixels de deslocamento lateral
        self.contador_ciclo = 0

        self._imagem_alternativa = None

        # Se for usar imagem
        if chave_imagem:
            if not self.gerenciador_recursos:
                raise ValueError("gerenciador_recursos é obrigatório se chave_imagem for usada.")

            if chave_imagem == 'cerca':
                self._imagem_alternativa = self.gerenciador_recursos.obter_imagem(f"{chave_imagem}_danificada")

            imagem = self.gerenciador_recursos.obter_imagem(chave_imagem)
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
            
            print(f"Largura: {largura}, Altura: {altura}")
            self.imagem = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.imagem.fill((0, 0, 0, 0))  # transparente

        # Define a área de colisão
        self.rect = self.imagem.get_rect(topleft=(x, y))



    def iniciar_animacao_chacoalhar(self, ciclos=6):
        self.animando = True
        self.ciclos_restantes = ciclos  # Total de frames que vai oscilar
        self.contador_ciclo = 0



    def atualizar(self):
        if self.animando:
            self.contador_ciclo += 1
            if self.contador_ciclo >= self.ciclos_restantes:
                self.animando = False



    def desenhar(self, superficie, camera_x, camera_y=0):
        """
        Desenha a imagem da área de interação (se houver),
        ou o retângulo de colisão para debug.
        """
        pos_x = self.rect.x - camera_x
        pos_y = self.rect.y - camera_y

        if self.animando:
            deslocamento = self.amplitude_chacoalho if self.contador_ciclo % 2 == 0 else -self.amplitude_chacoalho
            pos_x += deslocamento

        if self._imagem_alternativa and self.ativa:
            superficie.blit(self._imagem_alternativa, (pos_x, pos_y))
        else:
            superficie.blit(self.imagem, (pos_x, pos_y))

        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            pygame.draw.rect(
                superficie,
                COR_CAIXA_COLISAO,
                pygame.Rect(pos_x, pos_y, self.rect.width, self.rect.height),
                1
            )
