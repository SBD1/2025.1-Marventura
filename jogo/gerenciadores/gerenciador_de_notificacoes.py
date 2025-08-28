import pygame
import time
from utilidades.constantes import *

class _NotificacaoItem:
    def __init__(self, nome_item, quantidade, tempo_vida=3.0, tempo_esvanecer=0.5, altura_linha=30):
        self.texto = f"{nome_item} x{quantidade}"
        self.tempo_criacao = time.time()
        self.tempo_vida = tempo_vida
        self.tempo_esvanecer = tempo_esvanecer
        self.altura_linha = altura_linha
        self.posicao_animada = 0  # deslocamento vertical interpolado



    def esvanecer(self):
        """Retorna a opacidade baseada no tempo restante."""
        tempo_passado = time.time() - self.tempo_criacao
        tempo_restante = self.tempo_vida - tempo_passado

        if tempo_restante > self.tempo_esvanecer:
            return 255
        else:
            fator = max(0.0, tempo_restante / self.tempo_esvanecer)
            return int(255 * fator)
        


    def expirou(self):
        return time.time() - self.tempo_criacao >= self.tempo_vida


class GerenciadorNotificacoesItem:
    def __init__(self, fonte, posicao_base, espaco_vertical=30, velocidade_anim=200):
        """
        :param fonte: pygame.font.Font
        :param posicao_base: (x, y) da primeira notificação (tipicamente canto superior direito)
        :param espaco_vertical: espaço entre linhas (em pixels)
        """
        self.fonte = fonte
        self.posicao_base = posicao_base
        self.espaco_vertical = espaco_vertical
        self.velocidade_anim = velocidade_anim
        self.notificacoes = []

    def adicionar_item(self, nome, quantidade):
        print(f"Adicionando notificação: {nome} x{quantidade}")
        nova = _NotificacaoItem(nome, quantidade, altura_linha=self.espaco_vertical)
        nova.posicao_animada = len(self.notificacoes) * self.espaco_vertical  # começa na base
        self.notificacoes.append(nova)

    def atualizar(self, dt):
        # Remove expiradas
        self.notificacoes = [n for n in self.notificacoes if not n.expirou()]

        # Anima a subida de cada item até sua posição alvo
        for i, n in enumerate(self.notificacoes):
            destino = i * self.espaco_vertical
            diferenca = destino - n.posicao_animada
            deslocamento = self.velocidade_anim * dt

            if abs(diferenca) < deslocamento:
                n.posicao_animada = destino
            else:
                n.posicao_animada += deslocamento if diferenca > 0 else -deslocamento

    def desenhar(self, superficie):
        base_y = int(ALTURA_TELA * 0.35)  # ~um pouco acima do centro vertical
        x_direita = LARGURA_TELA - 20

        for notificacao in self.notificacoes:
            alfa = notificacao.esvanecer()
            superficie_texto = self.fonte.render(notificacao.texto, True, (255, 255, 255))
            superficie_texto.set_alpha(alfa)

            y = base_y + notificacao.posicao_animada
            x = x_direita - superficie_texto.get_width()
            superficie.blit(superficie_texto, (x, y))
