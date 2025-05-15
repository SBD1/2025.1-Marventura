# tela_modelo.py

from utilidades.constantes import *

class TelaModelo:
    """
    Classe base para as telas do jogo.
    Recebe e armazena o gerenciador de recursos para acesso comum.
    Lida com elementos comuns como fundo (acessado via gerenciador).
    Inclui um método auxiliar para desenhar texto com borda.
    """
    # Recebe o gerenciador de recursos no construtor
    def __init__(self, gerenciador_recursos):
        # Armazena a referência ao gerenciador de recursos
        self.gerenciador_recursos = gerenciador_recursos

        # A imagem de fundo comum não é mais passada diretamente, é obtida do gerenciador
        # self.imagem_fundo = self.gerenciador_recursos.get_image('background_common')
        # É melhor obter o fundo no método draw, pois pode variar entre subclasses ou ser None

    def handle_event(self, event):
        """
        Processa um evento. Deve ser sobrescrito pelas subclasses para lidar com a lógica específica da tela.
        Eventos comuns a todas as telas podem ser tratados aqui (ex: menu de pausa com ESC).
        Retorna o ID do próximo estado do jogo (um int da constante) ou None (continua na mesma tela).
        Retorna sys.exit para sinalizar a saída completa do jogo.
        """
        # Lógica de eventos comum a todas as telas (ex: pressionar ESC para menu de pausa)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        #     print("ESC pressionado na tela base")
        #     # Retornaria o ID do estado de pausa, por exemplo
        #     # return ESTADO_PAUSA # Assumindo que ESTADO_PAUSA está em constantes.py
        pass # Implementação base não faz nada com eventos específicos

        return None # Retorna None por padrão (continua na mesma tela atual)

    def draw(self, tela):
        """
        Desenha o conteúdo da tela. Deve ser sobrescrito pelas subclasses para desenhar seus elementos específicos.
        Desenha o fundo comum (obtido do gerenciador de recursos).
        :param tela: A superfície principal (tela) onde desenhar.
        """
        # Obtém a imagem de fundo comum do gerenciador para desenhar
        imagem_fundo = self.gerenciador_recursos.get_image('fundo_inicial')
        if imagem_fundo:
            tela.blit(imagem_fundo, (0, 0))
        else:
            tela.fill(PRETO)

    # Método auxiliar de desenho de texto com borda (útil para as subclasses)
    # Este método já recebe a fonte como parâmetro, o que é bom.
    # Poderíamos modificá-lo para obter a fonte pelo nome do gerenciador, mas passá-la é mais flexível.
    def _desenhar_texto_com_borda(self, superficie, texto, fonte, cor, cor_borda, grossura_borda, posicao_centro):
        """
        Desenha um texto em uma superfície com uma borda simples.
        :param superficie: A superfície onde desenhar (ex: a tela do jogo).
        :param texto: O texto a ser desenhado.
        :param fonte: O objeto pygame.font.Font a ser usado.
        :param cor: A cor principal do texto.
        :param cor_borda: A cor da borda do texto.
        :param grossura_borda: A espessura da borda em pixels.
        :param posicao_centro: Uma tupla (x, y) para o centro onde o texto deve ser posicionado.
        """
        # Renderiza a superfície da borda do texto
        superficie_borda = fonte.render(texto, True, cor_borda)
        rect_borda = superficie_borda.get_rect(center=posicao_centro)

        # Desenha a borda movendo a superfície da borda ligeiramente
        for dx in [-grossura_borda, 0, grossura_borda]:
            for dy in [-grossura_borda, 0, grossura_borda]:
                 if dx != 0 or dy != 0:
                    superficie.blit(superficie_borda, (rect_borda.x + dx, rect_borda.y + dy))

        # Renderiza a superfície principal do texto
        superficie_principal = fonte.render(texto, True, cor)
        rect_principal = superficie_principal.get_rect(center=posicao_centro)

        # Desenha a superfície principal do texto por cima da borda
        superficie.blit(superficie_principal, rect_principal)