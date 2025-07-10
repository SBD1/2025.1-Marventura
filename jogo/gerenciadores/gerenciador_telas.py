# telas/gerenciador_telas.py

import pygame
import sys
from telas import TelaInicial
from telas import TelaSalvamento
from telas import TelaSelecaoPersonagem
from telas import TelaJogo
from telas import TelaBatalha
from gerenciadores import GerenciadorDeEntidades
from utilidades.constantes import *

class GerenciadorDeTelas:
    """
    Gerencia as diferentes telas (estados) do jogo.
    Responsável por criar, armazenar e transitar entre as telas.
    """
    def __init__(self, tela_principal_surface, gerenciador_recursos, gerenciador_banco_de_dados):
        self.tela_principal_surface = tela_principal_surface
        self.gerenciador_recursos = gerenciador_recursos
        self.gerenciador_banco_de_dados = gerenciador_banco_de_dados
        self.gerenciador_entidades = GerenciadorDeEntidades()
        self.tela_atual = None
        self.telas_carregadas = {} # Cache de telas já criadas, se aplicável (ex: para não recriar a tela inicial)

        # Estado inicial do jogo
        self.mudar_tela(CHAVE_TRANSICAO_MENU_PRINCIPAL) # Começa com o menu principal

    def _criar_instancia_tela(self, estado_desejado, **kwargs):
        """
        Cria uma nova instância de tela com base no estado desejado e nos argumentos.
        Esta função é a 'fábrica' de telas.
        """
        if estado_desejado == CHAVE_TRANSICAO_MENU_PRINCIPAL:
            # A TelaInicial não precisa de 'gerenciador_telas' no seu __init__
            # A não ser que você queira que ela chame diretamente self.gerenciador_telas.mudar_tela
            # Se ela chamar `self.gerenciador_telas.mudar_tela`, então passe `self` para ela
            return TelaInicial(self, self.gerenciador_recursos)
        elif estado_desejado == CHAVE_TRANSICAO_SALVAMENTO:
            return TelaSalvamento(self, self.gerenciador_recursos,
                                  self.gerenciador_banco_de_dados)
        elif estado_desejado == CHAVE_TRANSICAO_SELECAO_PERSONAGEM:
            return TelaSelecaoPersonagem(self, self.gerenciador_recursos,
                                         self.gerenciador_banco_de_dados,)
        elif estado_desejado == CHAVE_TRANSICAO_NOVO_JOGO:
            return TelaJogo(self, self.gerenciador_recursos,
                            self.gerenciador_banco_de_dados)
        elif estado_desejado == CHAVE_TRANSICAO_CARREGAR_JOGO:
            return TelaJogo(self, self.gerenciador_recursos,
                            self.gerenciador_banco_de_dados)

        elif estado_desejado == CHAVE_TRANSICAO_MAPA:
            print(f"Tela: {kwargs.get('ponto_geracao_jogador')}")
            
            return TelaJogo(self, self.gerenciador_recursos,
                            self.gerenciador_banco_de_dados)
        elif estado_desejado == CHAVE_TRANSICAO_BATALHA:
            return TelaBatalha(self, self.gerenciador_recursos, # Passa self aqui
                               self.gerenciador_banco_de_dados,
                               inimigos_na_batalha=kwargs.get('inimigos_na_batalha'),
                               jogador_iniciou= kwargs.get('jogador_iniciou', False))
        else:
            print(f"ERRO: Estado de tela desconhecido: {estado_desejado}")
            return None

    def mudar_tela(self, novo_estado, **kwargs):
        """
        Define a tela atualmente ativa do jogo.
        Qualquer tela pode chamar este método no gerenciador.
        """
        nova_tela = self._criar_instancia_tela(novo_estado, **kwargs)
        if nova_tela:
            self.tela_atual = nova_tela
        else:
            print(f"Não foi possível mudar para a tela {novo_estado}. Permanece na tela atual.")

    def handle_input(self, evento):
        """
        Encaminha os eventos de entrada para a tela atual.
        Se a tela atual retornar uma transição, a muda.
        """
        if self.tela_atual:
            # A tela pode retornar um dicionário de transição ou None
            transicao_info = self.tela_atual.processar_eventos(evento)
            if transicao_info and 'estado' in transicao_info:
                estado_desejado = transicao_info['estado']
                del transicao_info['estado']
                self.mudar_tela(estado_desejado, **transicao_info)
        
        # Lidar com o evento de sair do Pygame aqui também, para garantir
        if evento.type == pygame.QUIT:
            sys.exit()

    def update(self, dt):
        """
        Atualiza a tela atualmente ativa.
        Se a tela atual retornar uma transição, a muda.
        """
        if self.tela_atual:
            # A tela pode retornar um dicionário de transição ou None
            transicao_info = self.tela_atual.atualizar(dt)
            if transicao_info and 'estado' in transicao_info:
                estado_desejado = transicao_info['estado']
                del transicao_info['estado']
                self.mudar_tela(estado_desejado, **transicao_info)


    def draw(self):
        """
        Desenha a tela atualmente ativa na superfície principal do Pygame.
        """
        if self.tela_atual:
            self.tela_atual.desenhar(self.tela_principal_surface)