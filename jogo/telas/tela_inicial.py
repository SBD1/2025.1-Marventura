# telas/tela_inicial.py

import pygame
import sys
from .tela_modelo import TelaModelo
from utilidades.constantes import *

class TelaInicial(TelaModelo): # Herda de TelaModelo
    def __init__(self, gerenciador_telas, gerenciador_recursos): # Adiciona gerenciador_telas
        super().__init__(gerenciador_telas, gerenciador_recursos) # Chama o construtor da TelaModelo

        self.imagem_logo = self.gerenciador_recursos.obter_imagem(CHAVE_LOGO)
        self.fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TITULO)
        self.fonte_botao = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_BOTAO)

        # A imagem de fundo comum pode ser carregada e mantida aqui
        self.imagem_fundo = self.gerenciador_recursos.obter_imagem(CHAVE_TELA_INICIAL) # Se tiver um background comum para menus
        if not self.imagem_fundo:
            # Fallback se a imagem não for encontrada
            self.imagem_fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.imagem_fundo.fill(CINZA_ESCURO)

        # Verifica se existe um progresso salvo para decidir quais botões mostrar
        db_manager = self.gerenciador_telas.gerenciador_banco_de_dados
        progresso_existe = db_manager.verificar_progresso_existente('jog001')

        self.botoes = []
        self._criar_botoes(progresso_existe)

    def _criar_botoes(self, progresso_existe):

        # Posições e dimensões dos botões
        _largura_botao = 300
        _altura_botao = 45
        _x_botao = (LARGURA_TELA - _largura_botao) // 2
        _espacamento_botao = 60

        if progresso_existe:
            # Layout para 3 botões
            _y_inicio_botao = ALTURA_TELA - 210
            self.botoes.append({
                'rect': pygame.Rect(_x_botao, _y_inicio_botao, _largura_botao, _altura_botao),
                'texto': "Continuar",
                'acao': lambda: self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_CARREGAR_JOGO)
            })
            self.botoes.append({
                'rect': pygame.Rect(_x_botao, _y_inicio_botao + _espacamento_botao, _largura_botao, _altura_botao),
                'texto': "Novo Jogo",
                'acao': lambda: self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_SELECAO_PERSONAGEM)
            })
            self.botoes.append({
                'rect': pygame.Rect(_x_botao, _y_inicio_botao + 2 * _espacamento_botao, _largura_botao, _altura_botao),
                'texto': "Fechar",
                'acao': lambda: sys.exit()
            })
        else:
            # Layout para 2 botões
            _y_inicio_botao = ALTURA_TELA - 150
            self.botoes.append({
                'rect': pygame.Rect(_x_botao, _y_inicio_botao, _largura_botao, _altura_botao),
                'texto': "Iniciar Jogo",
                'acao': lambda: self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_SELECAO_PERSONAGEM)
            })
            self.botoes.append({
                'rect': pygame.Rect(_x_botao, _y_inicio_botao + _espacamento_botao, _largura_botao, _altura_botao),
                'texto': "Fechar",
                'acao': lambda: sys.exit()
            })


    def handle_input(self, evento):
        # Chama o handle_input da base para eventos comuns (ex: QUIT)
        super().handle_input(evento)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            for botao in self.botoes:
                if botao['rect'].collidepoint(evento.pos):
                    botao['acao']() # Executa a ação associada ao botão
                    return # Não retorna transição de tela aqui, a ação já a lida
        return None # Nenhuma transição de tela a ser reportada ao main.py

    def update(self, dt):
        # Nenhuma lógica de atualização contínua para a tela inicial
        return None

    def draw(self, tela):
        # Desenha o fundo
        tela.blit(self.imagem_fundo, (0, 0))

        # Desenha a logo centralizada em cima (imagem obtida do gerenciador)
        if self.imagem_logo:
            # Obtém o retângulo da logo e o centraliza horizontalmente na posição vertical 1/4 da tela
            rect_logo = self.imagem_logo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 4))
            tela.blit(self.imagem_logo, rect_logo)

        # Desenha os botões
        for botao in self.botoes:
            if self.fonte_botao:
                self._desenhar_texto_com_borda(tela, botao['texto'], self.fonte_botao, BRANCO, PRETO, 2, botao['rect'].center)