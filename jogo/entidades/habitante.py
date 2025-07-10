# entidades/habitante.py

import pygame
from utilidades.constantes import * # Certifique-se que suas constantes estão aqui

class Habitante(pygame.sprite.Sprite):
    """
    Representa um habitante (NPC) no jogo.
    Ele não se move, mas pode interagir com o jogador e iniciar diálogos.
    Seu sprite se vira para a direção do jogador.
    """

    def __init__(self, gerenciador_recursos, identificador, area, x_inicial, y_inicial, nome, descricao, tipo, moedas, especialidade = None, chave_imagem = None, dialogos = [], missoes = []):
        super().__init__()
        self.gerenciador_recursos = gerenciador_recursos
        self.identificador = identificador
        self.area = area
        self.nome = nome
        self.descricao = descricao
        self.tipo = tipo
        self.moedas = moedas
        self.especialidade = especialidade
        self.chave_imagem = chave_imagem
        self.coordenada_x = float(x_inicial)
        self.coordenada_y = float(y_inicial)
        self.dialogos = dialogos # Lista de strings para os diálogos
        self.missoes_pendentes = missoes # Lista de missões associadas ao NPC
        self.mostrar_icone_interacao = False # Flag para controlar a visibilidade do ícone
        self.icone_interacao = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_INTERACAO) # Carrega a imagem do ícone

        # Carregar a imagem base e configurar o sprite inicial
        self.imagem_original = self.gerenciador_recursos.obter_imagem(self.chave_imagem)
        
        if self.imagem_original:
            self.imagem = self.imagem_original
        else:
            print(f"AVISO: Imagem '{self.chave_imagem}' não encontrada para o habitante '{self.nome}'. Usando fallback padrão.")
            self.imagem = pygame.Surface((LARGURA_JOGADOR, ALTURA_JOGADOR), pygame.SRCALPHA) # Usa tamanho similar ao jogador como fallback
            self.imagem.fill(CINZA) # Cor para indicar um NPC sem imagem

        self.rect = self.imagem.get_rect(topleft=(int(self.coordenada_x), int(self.coordenada_y)))

        self.orientacao_atual = 'direita' # Orientação inicial do habitante



    def _atualizar_icone_interacao(self):
            """
            Verifica se há missões ativas associadas a este habitante
            e atualiza a flag para mostrar ou esconder o ícone de interação.
            """
            self.mostrar_icone_interacao = bool(self.missoes_pendentes) # True se a lista de missões não estiver vazia



    def atualizar(self, dt, jogador_rect):
        """
        Atualiza o estado do habitante.
        Neste caso, apenas ajusta sua orientação para encarar o jogador.
        :param dt: Delta time (tempo em segundos desde o último frame).
        :param jogador_rect: O retângulo de colisão do jogador.
        """
        # Ajusta a orientação do habitante para encarar o jogador
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

        self._atualizar_icone_interacao()


    def desenhar(self, tela, camera_x, camera_y):
        """
        Desenha o habitante na tela, ajustando pela posição da câmera.
        :param tela: A superfície do Pygame onde desenhar.
        :param camera_x: A posição X da câmera.
        :param camera_y: A posição Y da câmera (se o jogo rolar verticalmente).
        """
        posicao_tela_x = self.coordenada_x - camera_x
        posicao_tela_y = self.coordenada_y - camera_y
        
        tela.blit(self.imagem, (int(posicao_tela_x), int(posicao_tela_y)))

        # Desenha o ícone de interação se aplicável
        if self.mostrar_icone_interacao and self.icone_interacao:
            # Posição do ícone acima do habitante
            icone_x = posicao_tela_x + self.rect.width // 2 - self.icone_interacao.get_width() // 2
            icone_y = posicao_tela_y - self.icone_interacao.get_height() + 10 # Ajuste o +10 conforme necessário para o espaçamento
            tela.blit(self.icone_interacao, (int(icone_x), int(icone_y)))

        # DEBUG: Desenha o retângulo de colisão do habitante
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            debug_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height)
            pygame.draw.rect(tela, AZUL_CLARO, debug_rect, 1) # Usando uma cor diferente para NPCs