# telas/gerenciador_telas.py

import pygame
import sys
from telas import TelaInicial
from telas import TelaSalvamento
from telas import TelaSelecaoPersonagem
from telas import TelaJogo
from telas import TelaBatalha
from utilidades.constantes import *
from utilidades import carregar_dados_do_progresso

class GerenciadorDeTelas:
    """
    Gerencia as diferentes telas (estados) do jogo.
    Responsável por criar, armazenar e transitar entre as telas.
    """
    def __init__(self, tela_principal_surface, gerenciador_recursos, gerenciador_banco_de_dados):
        self.tela_principal_surface = tela_principal_surface
        self.gerenciador_recursos = gerenciador_recursos
        self.gerenciador_banco_de_dados = gerenciador_banco_de_dados
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
            return TelaSalvamento(self, self.gerenciador_recursos)
        elif estado_desejado == CHAVE_TRANSICAO_SELECAO_PERSONAGEM:
            return TelaSelecaoPersonagem(self, self.gerenciador_recursos)
        elif estado_desejado == CHAVE_TRANSICAO_NOVO_JOGO:
            return TelaJogo(self, self.gerenciador_recursos,
                            id_mapa_atual=ID_MAPA_CAMPO_COSTA_OESTE, # Mapa inicial padrão
                            personagem=kwargs.get('personagem'),
                            ponto_de_destino='novo_jogo')
        elif estado_desejado == CHAVE_TRANSICAO_CARREGAR_JOGO:
            jogador, ilha, area = carregar_dados_do_progresso('jog001', self.gerenciador_banco_de_dados)

                    
            posicao_jogador = (
                jogador.coordenada_x,
                jogador.coordenada_y,
                'direita'
            )

            return TelaJogo(self, self.gerenciador_recursos,
                            gerenciador_banco_de_dados=self.gerenciador_banco_de_dados,
                            id_mapa_atual=kwargs.get('id_mapa'),
                            dados_da_area=area,
                            dados_da_ilha=ilha,
                            jogador=jogador,
                            ponto_geracao_jogador=posicao_jogador)
        elif estado_desejado == CHAVE_TRANSICAO_MAPA:
            return TelaJogo(self, self.gerenciador_recursos,
                            gerenciador_banco_de_dados=self.gerenciador_banco_de_dados,
                            id_mapa_atual=kwargs.get('id_mapa'),
                            dados_da_area=kwargs.get('dados_da_area'),
                            dados_da_ilha=kwargs.get('dados_da_ilha'),
                            jogador=kwargs.get('jogador'),
                            ponto_geracao_jogador=kwargs.get('ponto_geracao_jogador'))
        elif estado_desejado == CHAVE_TRANSICAO_BATALHA:
            return TelaBatalha(self, self.gerenciador_recursos, # Passa self aqui
                               inimigo_tipo=kwargs.get('inimigo_batalha'),
                               personagem=kwargs.get('personagem'),
                               jogador_x=kwargs.get('jogador_atual_x'),
                               jogador_y=kwargs.get('jogador_atual_y'),
                               jogador_olhando_direita=kwargs.get('jogador_olhando_direita'),
                               mapa_retorno_id=kwargs.get('mapa_atual_id'))
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
            transicao_info = self.tela_atual.handle_input(evento)
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
            transicao_info = self.tela_atual.update(dt)
            if transicao_info and 'estado' in transicao_info:
                estado_desejado = transicao_info['estado']
                del transicao_info['estado']
                self.mudar_tela(estado_desejado, **transicao_info)


    def draw(self):
        """
        Desenha a tela atualmente ativa na superfície principal do Pygame.
        """
        if self.tela_atual:
            self.tela_atual.draw(self.tela_principal_surface)