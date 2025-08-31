# entidades/barco.py

import pygame
import math
from utilidades.constantes import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import GerenciadorDeRecursos

class _Barco(pygame.sprite.Sprite):
    """
    Representa o barco usado na transição entre ilhas.
    Move-se horizontalmente e contém uma área onde o jogador pode andar.
    """
    def __init__(self, gerenciador_recursos: 'GerenciadorDeRecursos', chave_imagem, velocidade, caminho_relativo: pygame.Rect, ponto_ancoragem: tuple[int, int], amplitude_onda=5, frequencia_onda=1.5):
        super().__init__()
        
        self.imagem = gerenciador_recursos.obter_imagem(chave_imagem)
        if not self.imagem:
            self.imagem = pygame.Surface((100, 50))
            self.imagem.fill(COR_CAIXA_COLISAO)
        
        self.plano_fundo = gerenciador_recursos.obter_imagem(f"{chave_imagem}_fundo")
        if not self.plano_fundo:
            self.plano_fundo = pygame.Surface((100, 50))
            self.plano_fundo.fill(COR_CAIXA_COLISAO)

        comprimento_barco = self.imagem.get_width()
        altura_barco = self.imagem.get_height()

        self.posicao_y_base = 500 - altura_barco  # Guarda a posição Y do centro da oscilação

        self.rect = self.imagem.get_rect(topleft=(-comprimento_barco, self.posicao_y_base))
        self.velocidade = velocidade
        self.ponto_ancoragem = ponto_ancoragem
        self.caminho_relativo = caminho_relativo
        self.caminho_rect_absoluto = self.caminho_relativo.move(self.rect.topleft)

        self.amplitude_onda = amplitude_onda  # O quão "alto" a onda é (em pixels)
        self.frequencia_onda = frequencia_onda # O quão "rápido" o barco balança



    def atualizar(self, dt):
        """Move o barco para a direita e atualiza sua área caminhável."""
        # Movimento horizontal (X) continua o mesmo
        self.rect.x += self.velocidade * dt

        # --- CÁLCULO DO MOVIMENTO VERTICAL (Y) COM SENO ---
        # Pegamos o tempo de jogo em segundos para ter uma base contínua para a onda
        tempo_atual_segundos = pygame.time.get_ticks() / 1000.0
        
        # Calculamos o deslocamento vertical usando a função seno
        # offset_y irá variar suavemente entre -amplitude_onda e +amplitude_onda
        offset_y = self.amplitude_onda * math.sin(tempo_atual_segundos * self.frequencia_onda)

        # Aplicamos o deslocamento à posição Y base original do barco
        self.rect.y = self.posicao_y_base + offset_y
        
        # O caminho caminhável acompanha a posição total do barco (X e Y)
        self.caminho_rect_absoluto.topleft = (self.rect.x + self.caminho_relativo.x, self.rect.y + self.caminho_relativo.y)



    def desenhar(self, tela):
        """Desenha o barco na tela."""
        tela.blit(self.imagem, self.rect)
        
        # DEBUG: Desenha a área caminhável para visualização
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            pygame.draw.rect(tela, VERDE, self.caminho_rect_absoluto, 2)
            pygame.draw.rect(tela, VERMELHO, self.rect, 2)



    def desenhar_plano_fundo(self, tela):
        """Desenha o plano de fundo do barco na tela."""
        tela.blit(self.plano_fundo, self.rect)



class Canoa(_Barco):
    """
    Representa uma canoa pequena usada para a transição entre ilhas.
    Move-se horizontalmente e contém uma área onde o jogador pode andar.
    """
    def __init__(self, gerenciador_recursos):
        # Define os dados específicos da Canoa
        dados_canoa = {
            'chave_imagem': CANOA,
            'velocidade': 80, # Canoa é um pouco mais lenta
            'caminho_relativo': pygame.Rect(10, 15, 80, 20),
            'ponto_ancoragem': (105, 55),
            'amplitude_onda': 4,   # Balanço curto
            'frequencia_onda': 2.0 # Balanço rápido
        }

        # Chama o construtor da classe pai com esses dados
        super().__init__(gerenciador_recursos, **dados_canoa)



class Veleiro(_Barco):
    """
    Representa um veleiro usado para a transição entre ilhas.
    Move-se horizontalmente e contém uma área onde o jogador pode andar.
    """
    def __init__(self, gerenciador_recursos):
        # Define os dados específicos do Veleiro
        dados_veleiro = {
            'chave_imagem': VELEIRO,
            'velocidade': 100, # Veleiro é mais rápido
            'caminho_relativo': pygame.Rect(42, 621, 587, 20),
            'ponto_ancoragem': (251, 630),
            'amplitude_onda': 8,   # Balanço mais amplo
            'frequencia_onda': 1.2 # Balanço mais lento e pesado
        }

        # Chama o construtor da classe pai com esses dados
        super().__init__(gerenciador_recursos, **dados_veleiro)



class Navio(_Barco):
    """
    Representa um navio usado para a transição entre ilhas.
    Move-se horizontalmente e contém uma área onde o jogador pode andar.
    """
    def __init__(self, gerenciador_recursos):
        # Define os dados específicos do Navio
        dados_navio = {
            'chave_imagem': NAVIO,
            'velocidade': 90, # Navio é mais lento
            'caminho_relativo': pygame.Rect(30, 50, 200, 50),
            'ponto_ancoragem': (130, 70),
            'amplitude_onda': 6,   # Balanço moderado
            'frequencia_onda': 1.0 # Balanço mais lento
        }

        # Chama o construtor da classe pai com esses dados
        super().__init__(gerenciador_recursos, **dados_navio)