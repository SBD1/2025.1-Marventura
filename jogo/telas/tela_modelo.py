# tela_modelo.py

import pygame
import sys # Para sys.exit()
from utilidades.constantes import *

class TelaModelo:
    """
    Classe base para todas as telas do jogo.
    Define a interface comum (contrato) para as telas, incluindo gerenciadores
    e métodos essenciais como processar_eventos, update e draw.
    """
    def __init__(self, gerenciador_telas, gerenciador_recursos):
        """
        Construtor da TelaModelo.
        :param gerenciador_telas: Referência ao gerenciador de telas para transições.
        :param gerenciador_recursos: Referência ao gerenciador de recursos para assets.
        """
        self.gerenciador_telas = gerenciador_telas
        self.gerenciador_recursos = gerenciador_recursos


    def processar_eventos(self, evento):
        """
        Processa um evento de entrada.
        Deve ser sobrescrito pelas subclasses para lidar com a lógica específica da tela.
        Retorna um dicionário de transição (com a chave 'estado' e kwargs) ou None.
        Um retorno de 'sys.exit' ou similar pode sinalizar a saída do jogo.
        """
        if evento.type == pygame.QUIT:
            sys.exit() # Evento de fechar a janela, saída imediata

        # Lógica de eventos comum a todas as telas (ex: pressionar ESC para menu de pausa)
        # if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
        #     # Exemplo de como uma TelaModelo pode solicitar uma transição via gerenciador
        #     # self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MENU_PAUSA)
        #     return None # Ou um dicionário de transição, se a TelaModelo decidir a transição

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MENU_PRINCIPAL)
            return None # Ou um dicionário de transição, se a TelaModelo decidir a transição

        return None # Por padrão, não faz nada e não solicita transição

    def atualizar(self, dt):
        """
        Atualiza a lógica interna da tela (movimento de entidades, timers, etc.).
        Deve ser sobrescrito pelas classes filhas.
        :param dt: Delta time (tempo desde o último frame) em segundos.
        Retorna um dicionário de transição (com a chave 'estado' e kwargs) ou None.
        """
        return None # Implementação padrão não faz nada

    def desenhar(self, tela):
        """
        Desenha os elementos da tela na superfície principal do Pygame.
        Deve ser sobrescrito pelas classes filhas.
        :param tela: A superfície de exibição do Pygame onde desenhar.
        """
        # A lógica de desenho de fundo comum, se aplicável a TODAS as telas, viria aqui.
        # Se o fundo comum é apenas para algumas telas (menu, salvar),
        # então as subclasses deverão implementá-lo no seu próprio método draw.
        pass # Por padrão, não desenha nada

    def _desenhar_texto_com_borda(self, superficie, texto, fonte, cor, cor_borda, grossura_borda, posicao_centro):
        """
        Método auxiliar para desenhar um texto em uma superfície com uma borda simples.
        Pode ser reutilizado por qualquer tela que herde desta base.
        """
        print(f"Desenhando texto com borda: '{texto}' na posição {posicao_centro} com cor {cor} e borda {cor_borda}")
        # Renderiza a superfície da borda do texto
        superficie_borda = fonte.render(texto, True, cor_borda)
        rect_borda = superficie_borda.get_rect(center=posicao_centro)

        # Desenha a borda movendo a superfície da borda ligeiramente
        for dx in [-grossura_borda, 0, grossura_borda]:
            for dy in [-grossura_borda, 0, grossura_borda]:
                 if dx != 0 or dy != 0: # Desenha apenas as 8 direções em volta do centro
                    superficie.blit(superficie_borda, (rect_borda.x + dx, rect_borda.y + dy))

        # Renderiza a superfície principal do texto
        superficie_principal = fonte.render(texto, True, cor)
        rect_principal = superficie_principal.get_rect(center=posicao_centro)
        superficie.blit(superficie_principal, rect_principal)