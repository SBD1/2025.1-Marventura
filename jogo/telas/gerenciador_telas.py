# telas/gerenciador_telas.py

from collections import namedtuple
import pygame
import sys
from .tela_inicial import TelaInicial
from .tela_salvamento import TelaSalvamento
from .tela_selecao_personagem import TelaSelecaoPersonagem
from .tela_de_jogo import TelaJogo
from .tela_batalha import TelaBatalha
from .tela_loja import TelaLoja
from .tela_inventario import TelaInventario # Garanta que esta linha exista
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
            # --- Lógica para iniciar um novo jogo ---
            id_area_inicial = ID_MAPA_CAMPO_COSTA_OESTE
            nome_personagem = kwargs.get('personagem')

            # Busca os dados da área e da ilha inicial no banco de dados
            dados_area_inicial = self.gerenciador_banco_de_dados.buscar_info_area(id_area_inicial)
            dados_ilha_inicial = self.gerenciador_banco_de_dados.buscar_info_ilha(dados_area_inicial.identificador_ilha)

            # Define o ponto de geração inicial para um novo jogo
            ponto_geracao_inicial = (1950, 140, 'direita')

            # Cria um objeto temporário para o jogador com status iniciais.
            # A estrutura (campos) deve ser a mesma retornada por `buscar_jogador`.
            JogadorInfo = namedtuple('JogadorInfo', [
                'identificador_jogador', 'identificador_area', 'nome', 'descricao',
                'coordenada_x', 'coordenada_y', 'orientacao', 'energia', 'vida', 'nivel', 'sorte',
                'vida_atual', 'experiencia_atual', 'moedas_totais'
            ])
            jogador_inicial = JogadorInfo(
                identificador_jogador='jog001',
                identificador_area=id_area_inicial,
                nome=nome_personagem,
                descricao=f"Um(a) jovem aventureiro(a) chamado(a) {nome_personagem}.",
                coordenada_x=ponto_geracao_inicial[0], coordenada_y=ponto_geracao_inicial[1],
                orientacao=ponto_geracao_inicial[2],
                energia=35, vida=70, nivel=1, sorte=5,
                vida_atual=70, experiencia_atual=0, moedas_totais=900
            )

            # Salva/Reseta o estado inicial do jogador no banco de dados IMEDIATAMENTE
            self.gerenciador_banco_de_dados.resetar_ou_criar_jogador(jogador_inicial)

            # Cria a TelaJogo com os dados em memória
            return TelaJogo(
                self, self.gerenciador_recursos,
                dados_da_ilha=dados_ilha_inicial,
                dados_da_area=dados_area_inicial,
                gerenciador_banco_de_dados=self.gerenciador_banco_de_dados,
                jogador=jogador_inicial,
                ponto_geracao_jogador=ponto_geracao_inicial
            )
        elif estado_desejado == CHAVE_TRANSICAO_CARREGAR_JOGO:
            jogador, ilha, area = self.gerenciador_banco_de_dados.carregar_dados_do_progresso('jog001')

                    
            posicao_jogador = (
                jogador.coordenada_x,
                jogador.coordenada_y,
                jogador.orientacao
            )

            return TelaJogo(self, self.gerenciador_recursos,
                            gerenciador_banco_de_dados=self.gerenciador_banco_de_dados,
                            dados_da_area=area,
                            dados_da_ilha=ilha,
                            jogador=jogador,
                            ponto_geracao_jogador=posicao_jogador)
        elif estado_desejado == CHAVE_TRANSICAO_MAPA:
            return TelaJogo(self, self.gerenciador_recursos,
                            gerenciador_banco_de_dados=self.gerenciador_banco_de_dados,
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
        elif estado_desejado == CHAVE_TRANSICAO_LOJA:
         return TelaLoja(self, self.gerenciador_recursos,
                        self.gerenciador_banco_de_dados,
                        kwargs.get('jogador_id'),
                        kwargs.get('vendedor_id'),
                        kwargs.get('nome_vendedor'),
                        kwargs.get('dados_retorno_ilha'),
                        kwargs.get('dados_retorno_area'),
                        kwargs.get('ponto_retorno_jogador'))
        elif estado_desejado == CHAVE_TRANSICAO_INVENTARIO:
            return TelaInventario(self, self.gerenciador_recursos,
                                  self.gerenciador_banco_de_dados,
                                  kwargs.get('jogador_id'),
                                  kwargs.get('dados_retorno_ilha'),
                                  kwargs.get('dados_retorno_area'),
                                  kwargs.get('ponto_retorno_jogador'),
                                  snapshot_fundo=kwargs.get('snapshot_fundo'))
        else:
            print(f"ERRO: Estado de tela desconhecido: {estado_desejado}")
            return None

    def mudar_tela(self, novo_estado, **kwargs):
        """
        Define a tela atualmente ativa do jogo.
        Qualquer tela pode chamar este método no gerenciador.
        """
        if isinstance(self.tela_atual, TelaJogo):
            self.tela_atual.salvar_progresso()
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
            
