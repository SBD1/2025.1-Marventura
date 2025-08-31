# telas/tela_transicao_ilha.py

import pygame
from utilidades.constantes import *
from .tela_modelo import TelaModelo
from entidades.barco import Canoa, Veleiro, Navio

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import GerenciadorDeTelas, GerenciadorDeRecursos, GerenciadorDeEntidades, DBManager

class TelaTransicaoIlha(TelaModelo):
    """
    Uma tela intermediária que mostra o jogador em um barco
    viajando da esquerda para a direita, simulando a viagem entre ilhas.
    """
    def __init__(self, gerenciador_telas: 'GerenciadorDeTelas', gerenciador_recursos: 'GerenciadorDeRecursos', gerenciador_banco_de_dados: 'DBManager', gerenciador_entidades: 'GerenciadorDeEntidades', dados_destino: dict):
        super().__init__(gerenciador_telas, gerenciador_recursos)
        
        self.entidades = gerenciador_entidades
        self.banco_de_dados = gerenciador_banco_de_dados
        self.jogador = self.entidades.jogador
        self.dados_destino = dados_destino # Dicionário com informações para a próxima tela

        # Carrega a imagem de fundo do oceano
        self.fundo_oceano = self.gerenciador_recursos.obter_imagem(CHAVE_CENARIO_OCEANO)
        if not self.fundo_oceano:
            self.fundo_oceano = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.fundo_oceano.fill(AZUL) # Cor de fallback

        # Cria o barco fora da tela, à esquerda
        self.barco = Navio(self.gerenciador_recursos)

        # --- LÓGICA DE POSICIONAMENTO REFEITA USANDO A ÂNCORA ---

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
        
        # --- FIM DA NOVA LÓGICA ---
        
        # Bloqueia o movimento do jogador controlado por script, mas não pelo teclado
        self.jogador.movimento_bloqueado = False

        self.todos_os_sprites = pygame.sprite.Group(self.barco, self.jogador)



    def atualizar(self, dt):
        """Atualiza a posição do barco e do jogador, garantindo que o jogador acompanhe o barco."""
        
        # Guarda a posição COMPLETA do barco antes do movimento
        posicao_anterior_barco = self.barco.rect.topleft

        # Atualiza o barco (que agora se move em X e Y)
        self.barco.atualizar(dt)
        
        # Calcula o deslocamento em AMBOS os eixos
        deslocamento_x = self.barco.rect.x - posicao_anterior_barco[0]
        deslocamento_y = self.barco.rect.y - posicao_anterior_barco[1]

        # Aplica o mesmo deslocamento ao jogador
        self.jogador.coordenada_x += deslocamento_x
        self.jogador.coordenada_y += deslocamento_y
        
        # Atualiza o jogador, desativando o limite de mundo
        self.jogador.atualizar(dt, obstaculos=[], lista_de_caminhos=[self.barco.caminho_rect_absoluto], largura_mundo=LARGURA_TELA, altura_mundo=ALTURA_TELA, limitar_posicao_no_mundo=False)

        # Verifica a condição de término da transição (sem alterações aqui)
        if self.barco.rect.left > LARGURA_TELA:
            print("Viagem concluída. Transicionando para o destino...")

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
        tela.blit(self.fundo_oceano, (0, 0))
        
        self.barco.desenhar_plano_fundo(tela)

        self.jogador.desenhar(tela, camera_x=0, camera_y=0)
        
        self.barco.desenhar(tela)


    def processar_eventos(self, evento):
        """Processa eventos, principalmente para permitir que o jogador se mova no barco."""
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Não é necessário processar outros eventos, mas a estrutura está aqui
        return None