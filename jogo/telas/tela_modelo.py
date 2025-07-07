# tela_modelo.py

import pygame
import sys # Para sys.exit()
from utilidades.constantes import *

class TelaModelo:
    """
    Classe base para todas as telas do jogo.
    Define a interface comum (contrato) para as telas, incluindo gerenciadores
    e métodos essenciais como handle_input, update e draw.
    """
    def __init__(self, gerenciador_telas, gerenciador_recursos):
        """
        Construtor da TelaModelo.
        :param gerenciador_telas: Referência ao gerenciador de telas para transições.
        :param gerenciador_recursos: Referência ao gerenciador de recursos para assets.
        """
        self.gerenciador_telas = gerenciador_telas
        self.gerenciador_recursos = gerenciador_recursos


    def handle_input(self, evento):
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

    def update(self, dt):
        """
        Atualiza a lógica interna da tela (movimento de entidades, timers, etc.).
        Deve ser sobrescrito pelas classes filhas.
        :param dt: Delta time (tempo desde o último frame) em segundos.
        Retorna um dicionário de transição (com a chave 'estado' e kwargs) ou None.
        """
        return None # Implementação padrão não faz nada

    def draw(self, tela):
        """
        Desenha os elementos da tela na superfície principal do Pygame.
        Deve ser sobrescrito pelas classes filhas.
        :param tela: A superfície de exibição do Pygame onde desenhar.
        """
        # A lógica de desenho de fundo comum, se aplicável a TODAS as telas, viria aqui.
        # Se o fundo comum é apenas para algumas telas (menu, salvar),
        # então as subclasses deverão implementá-lo no seu próprio método draw.
        pass # Por padrão, não desenha nada

    def _desenhar_texto_com_borda(self, superficie, texto, fonte, cor, cor_borda, grossura_borda, pos, align='center'):
        """
        Método auxiliar para desenhar texto com borda, com suporte a alinhamento.
        """
        # Renderiza a superfície principal e a da borda
        superficie_texto = fonte.render(texto, True, cor)
        superficie_borda = fonte.render(texto, True, cor_borda)
        
        # Define o retângulo do texto com base no alinhamento desejado
        if align == 'center':
            rect_texto = superficie_texto.get_rect(center=pos)
        elif align == 'left':
            rect_texto = superficie_texto.get_rect(midleft=pos)
        elif align == 'right':
            rect_texto = superficie_texto.get_rect(midright=pos)
        else: # Padrão para o centro se o alinhamento for desconhecido
            rect_texto = superficie_texto.get_rect(center=pos)

        # Desenha a borda em 8 direções
        for dx in range(-grossura_borda, grossura_borda + 1):
            for dy in range(-grossura_borda, grossura_borda + 1):
                if dx != 0 or dy != 0:
                    superficie.blit(superficie_borda, (rect_texto.x + dx, rect_texto.y + dy))
        
        # Desenha o texto principal por cima da borda
        superficie.blit(superficie_texto, rect_texto)
        
    def _draw_text_wrapped(self, surface, text, font, color, rect):
        """Desenha o texto com quebra de linha automática dentro de um retângulo."""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            # Adiciona uma pequena margem interna ao retângulo
            if font.size(test_line)[0] < rect.width - 20:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        # Ajusta a posição inicial Y para descer um pouco
        y = rect.top + 70 
        for line in lines:
            line_surface = font.render(line, True, color)
            # Adiciona uma margem à esquerda
            surface.blit(line_surface, (rect.left + 10, y))
            y += font.get_linesize()