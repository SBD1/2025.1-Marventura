# telas/tela_transicao_ilha.py

import pygame
import random
from utilidades.constantes import *
from utilidades import Camera
from .tela_modelo import TelaModelo
from entidades import Canoa, Veleiro, Navio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import GerenciadorDeTelas, GerenciadorDeRecursos, GerenciadorDeEntidades, DBManager, GerenciadorDeMissoes

class TelaTransicaoIlha(TelaModelo):
    """
    Uma tela intermediária que mostra o jogador em um barco
    viajando da esquerda para a direita, simulando a viagem entre ilhas.
    """
    def __init__(self, gerenciador_telas: 'GerenciadorDeTelas', gerenciador_recursos: 'GerenciadorDeRecursos', gerenciador_banco_de_dados: 'DBManager', gerenciador_entidades: 'GerenciadorDeEntidades', gerenciador_missoes: 'GerenciadorDeMissoes', dados_destino: dict):
        super().__init__(gerenciador_telas, gerenciador_recursos)
        
        self.entidades = gerenciador_entidades
        self.banco_de_dados = gerenciador_banco_de_dados
        self.missoes = gerenciador_missoes
        self.jogador = self.entidades.jogador
        self.dados_destino = dados_destino # Dicionário com informações para a próxima tela

        self.barco = self.banco_de_dados.buscar_barco_atual(self.entidades.progresso_do_jogo.identificador_progresso)
        self.tipo_barco = 'can' # Valor padrão
        if self.barco:
            self.tipo_barco = self.barco.tipo_barco
            
        self.DURACAO_VIAGEM = 12.0  # Duração da fase "VIAJANDO" em segundos
        self.tempo_decorrido = 0.0
        self.fase_viagem = 'VIAJANDO' # Controla o estado da transição
        self.missoes.notificar_mudanca_de_area('mar001')
        self.verificacao_evento_realizada = False
        self.missao_ativada = False
        self.evento_maritimo = None

        # Carrega a imagem de fundo do oceano
        self.fundo_oceano = self.gerenciador_recursos.obter_imagem(CHAVE_CENARIO_OCEANO)
        if not self.fundo_oceano:
            self.fundo_oceano = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.fundo_oceano.fill(AZUL) # Cor de fallback

        self.largura_fundo = self.fundo_oceano.get_width()


        # --- CONFIGURAÇÃO DO BARCO E JOGADOR ---
        # Cria o barco fora da tela, à esquerda
        if self.tipo_barco == 'can':
            self.barco = Canoa(self.gerenciador_recursos)
        elif self.tipo_barco == 'vel':
            self.barco = Veleiro(self.gerenciador_recursos)
        else:
            self.barco = Navio(self.gerenciador_recursos)

        # 1. Calcula a posição absoluta (no mundo) do ponto de ancoragem do barco.
        ponto_ancoragem_absoluto_x = self.barco.rect.x + self.barco.ponto_ancoragem[0]
        ponto_ancoragem_absoluto_y = self.barco.rect.y + self.barco.ponto_ancoragem[1]

        # 2. Define o centro dos PÉS do jogador (pes_rect) para ser exatamente nesse ponto.
        #    Isso posiciona a "base" do jogador corretamente.
        self.jogador.pes_rect.center = (ponto_ancoragem_absoluto_x, ponto_ancoragem_absoluto_y)

        # 3. Agora, ajusta o retângulo principal de desenho (self.jogador.rect) para que
        #    ele fique alinhado com a nova posição dos pés.
        #    A relação entre rect e pes_rect é: centerx é o mesmo e bottom é o mesmo.
        self.jogador.rect.centerx = self.jogador.pes_rect.centerx
        self.jogador.rect.bottom = self.jogador.pes_rect.bottom

        # 4. Finalmente, sincroniza as coordenadas de movimento (coordenada_x/y), que são o
        #    topleft do rect principal, com a posição que acabamos de calcular.
        self.jogador.coordenada_x = float(self.jogador.rect.x)
        self.jogador.coordenada_y = float(self.jogador.rect.y)

        self.jogador.orientacao = 'direita' # O jogador sempre olha para a direita durante a viagem
        self.jogador.mostrar_icone_interacao = False # Não mostra ícone de interação
        
        # Bloqueia o movimento do jogador controlado por script, mas não pelo teclado
        self.jogador.movimento_bloqueado = False

        self.todos_os_sprites = pygame.sprite.Group(self.barco, self.jogador)

        # --- CONFIGURAÇÃO DA CÂMERA ---
        largura_mundo_viagem = self.barco.velocidade * (self.DURACAO_VIAGEM + 5) # Distância + uma margem
        self.camera = Camera(
            largura_janela=LARGURA_TELA,
            altura_janela=ALTURA_TELA,
            tamanho_mundo=(INFINITO, ALTURA_TELA)
        )


    def sortear_evento(self):
        """Sorteia um evento aleatório com 25% de chance"""
        if 0.25 > random.random():
            self.evento_maritimo = random.choice(['Ataque de piratas', 'Ataque do Rei dos Mares'])



    def atualizar(self, dt):
        """Atualiza a posição do barco e do jogador, garantindo que o jogador acompanhe o barco."""

        # 1. ATUALIZAR ESTADO DA VIAGEM
        if self.fase_viagem == 'VIAJANDO':
            self.tempo_decorrido += dt

            # Verifica apenas uma vez após 6 segundos
            if self.tempo_decorrido >= 6.0 and not self.verificacao_evento_realizada:
                self.verificacao_evento_realizada = True  # Marca que já verificou

                # Tenta retomar missão
                self.missao_ativada = self.missoes.notificar_mudanca_de_tela(self.__class__.__name__)

                if not self.missao_ativada:
                    self.sortear_evento()

                if self.evento_maritimo:
                    print(f"O evento marítimo '{self.evento_maritimo}' está prestes a acontecer")
            
            esta_em_evento_controlado = self.missoes.esta_em_evento_controlado()
           # print(f"[VIAGEM] Está em evento controlado: {self.tempo_decorrido >= self.DURACAO_VIAGEM and not esta_em_evento_controlado}")
            if self.tempo_decorrido >= self.DURACAO_VIAGEM and not esta_em_evento_controlado:
                self.fase_viagem = 'FINALIZANDO'
                print("FINALIZANDO")
                # Trava a câmera na posição atual
                self.camera.focar_em_ponto(self.camera.rect.centerx, self.camera.rect.centery)

        # 2. ATUALIZAR BARCO E JOGADOR (acontece em ambas as fases)
        # Guarda a posição COMPLETA do barco antes do movimento
        posicao_anterior_barco = self.barco.rect.topleft

        # Atualiza o barco (que agora se move em X e Y)
        self.barco.atualizar(dt)
        self.missoes.atualizar(dt * 1000)

        # Calcula o deslocamento em AMBOS os eixos
        deslocamento_x = self.barco.rect.x - posicao_anterior_barco[0]
        deslocamento_y = self.barco.rect.y - posicao_anterior_barco[1]

        # Aplica o mesmo deslocamento ao jogador
        self.jogador.coordenada_x += deslocamento_x
        self.jogador.coordenada_y += deslocamento_y
        
        # Atualiza o jogador, desativando o limite de mundo
        self.jogador.atualizar(dt, obstaculos=[], lista_de_caminhos=[self.barco.caminho_rect_absoluto], largura_mundo=LARGURA_TELA, altura_mundo=ALTURA_TELA, limitar_posicao_no_mundo=False)

        # 3. ATUALIZAR A CÂMERA
        # O método atualizar da câmera já sabe se deve seguir ou ficar parada
        self.camera.atualizar(dt, self.jogador.rect)

        # 4. VERIFICAR CONDIÇÃO DE TÉRMINO
        if self.fase_viagem == 'FINALIZANDO':
            # A transição termina quando o barco sai da VISÃO DA CÂMERA
            if self.barco.rect.left > self.camera.rect.right:
                self.entidades.jogador.atualizar_posicao_jogador(
                    self.dados_destino['coordenada_x'],
                    self.dados_destino['coordenada_y'],
                    self.dados_destino['orientacao']
                )
                
                self.banco_de_dados.atualizar_posicao_jogador(
                    self.entidades.jogador.identificador,
                    self.entidades.area_atual.identificador_area,
                    self.dados_destino['coordenada_x'],
                    self.dados_destino['coordenada_y']
                )

                self.gerenciador_telas.mudar_tela(
                    CHAVE_TRANSICAO_MAPA
                )



    def desenhar(self, tela):
        """Desenha o oceano, o barco e o jogador."""
        tela.fill(AZUL_OCEANO)

        # --- LÓGICA DO FUNDO INFINITO ---
        # Usa o operador módulo (%) para fazer o fundo "resetar" a posição
        x_desenho = -(self.camera.rect.x % self.largura_fundo)
        tela.blit(self.fundo_oceano, (x_desenho, 0))
        # Desenha uma segunda cópia do fundo logo em seguida para não haver espaços vazios
        tela.blit(self.fundo_oceano, (x_desenho + self.largura_fundo, 0))

        self.barco.desenhar_plano_fundo(tela, self.camera.rect.x, self.camera.rect.y)

        self.jogador.desenhar(tela, self.camera.rect.x, self.camera.rect.y)
        
        self.barco.desenhar(tela, self.camera.rect.x, self.camera.rect.y)

        if self.missoes.dialogo_controlado_ativo and self.missoes.caixa_dialogo:
            self.missoes.caixa_dialogo.desenhar(tela)


    def processar_eventos(self, evento):
        """Processa eventos, principalmente para permitir que o jogador se mova no barco."""
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if self.missao_ativada:
            if self.missoes.esta_em_evento_controlado():
                self.missoes.processar_eventos(evento)
                return None # Consome o evento para evitar que o jogador se mova ou faça outra coisa