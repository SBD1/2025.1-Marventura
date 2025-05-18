# telas/tela_selecao_personagem.py

import pygame
import sys
from .tela_modelo import TelaModelo
from utilidades.constantes import *

class TelaSelecaoPersonagem(TelaModelo):
    """
    Tela onde o jogador escolhe entre Menino e Menina ao iniciar um novo jogo.
    Ao escolher, retorna um dicionário para iniciar o jogo no mapa inicial,
    com o personagem selecionado e o ponto de entrada de "novo jogo".
    """
    def __init__(self, gerenciador_recursos):
        super().__init__(gerenciador_recursos)

        # --- Recursos específicos da Tela de Seleção de Personagem ---
        # Obtém fontes do gerenciador de recursos, usando as chaves que você definiu
        self.fonte_botoes = self.gerenciador_recursos.get_font(CHAVE_FONTE_BOTAO)
        self.fonte_grande = self.gerenciador_recursos.get_font(CHAVE_FONTE_TITULO)
        # Carregue imagens dos personagens aqui se forem desenhadas na UI desta tela
        # self.imagem_menino_ui = self.gerenciador_recursos.get_image('personagem_menino_ui')
        # self.imagem_menina_ui = self.gerenciador_recursos.get_image('personagem_menina_ui')


        # --- Elementos da Tela de Seleção ---
        # Botões/Áreas clicáveis para selecionar Menino ou Menina
        _largura_opcao = 200 # Exemplo
        _altura_opcao = 60   # Exemplo
        _espacamento = 40    # Exemplo

        # Calcula posições para centralizar as opções horizontalmente
        _largura_total_opcoes = (2 * _largura_opcao) + _espacamento
        _inicio_x = (LARGURA_TELA - _largura_total_opcoes) // 2
        _y_opcoes = ALTURA_TELA // 2 # Centralizado verticalmente

        self._rect_opcao_menino = pygame.Rect(_inicio_x, _y_opcoes, _largura_opcao, _altura_opcao)
        self._rect_opcao_menina = pygame.Rect(_inicio_x + _largura_opcao + _espacamento, _y_opcoes, _largura_opcao, _altura_opcao)

        # Textos para as opções
        self._texto_menino = "Menino"
        self._texto_menina = "Menina"

        # Título da tela
        self._texto_titulo = "Escolha seu personagem"

        # Grossura da borda do texto para os botões
        self._grossura_borda = 2


    def handle_event(self, event):
        """
        Processa eventos para a tela de seleção de personagem.
        Verifica cliques nas opções Menino/Menina.
        Ao selecionar, retorna um dicionário com todos os dados necessários
        para iniciar um novo jogo (estado, mapa inicial, personagem, ponto de entrada).
        Retorna None para continuar na mesma tela.
        """
        # Chama o manipulador de eventos da classe base (para eventos comuns, ex: ESC)
        proximo_estado = super().handle_event(event)
        # Se a base já tratou o evento e retornou um estado, retorna-o imediatamente
        if proximo_estado is not None:
             return proximo_estado

        # Lógica específica da Tela de Seleção de Personagem
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Botão esquerdo do mouse
                posicao_mouse = event.pos

                # Verifica clique na opção Menino
                if self._rect_opcao_menino.collidepoint(posicao_mouse):
                    print("Selecionou Menino. Iniciando novo jogo.")
                    # Retorna um dicionário contendo todos os dados para iniciar o jogo:
                    # 'estado': Para onde ir (o estado de jogo)
                    # 'id_mapa': O ID do mapa para carregar (o mapa inicial do jogo)
                    # 'tipo_personagem': O tipo de personagem escolhido
                    # 'ponto_entrada_destino_id': O ID do ponto de entrada NO MAPA INICIAL
                    # para um novo jogo (definido em mapa_dados.py).
                    return {
                        'estado': ESTADO_JOGO,
                        'id_mapa': ID_MAPA_CAMPO_VILA,
                        'tipo_personagem': PERSONAGEM_MENINO,
                        'ponto_entrada_destino_id': 'entrada_padrao' # <-- Inclui o ID do ponto de entrada inicial
                    }

                # Verifica clique na opção Menina
                elif self._rect_opcao_menina.collidepoint(posicao_mouse):
                    print("Selecionou Menina. Iniciando novo jogo.")
                     # Retorna um dicionário contendo todos os dados para iniciar o jogo:
                     # (mesma estrutura do Menino, mas com PERSONAGEM_MENINA)
                    return {
                        'estado': ESTADO_JOGO,
                        'id_mapa': ID_MAPA_CAMPO_VILA,
                        'tipo_personagem': PERSONAGEM_MENINA,
                        'ponto_entrada_destino_id': 'entrada_padrao' # <-- Inclui o ID do ponto de entrada inicial
                    }

        # Se nenhum clique tratado causou uma mudança de estado, retorna None
        return None

    def draw(self, tela):
        """
        Desenha todos os elementos da tela de seleção de personagem na superfície da tela.
        Desenha o fundo, título e opções de personagem (textos).
        :param tela: A superfície principal (tela) onde desenhar.
        """
        super().draw(tela) # Desenha o fundo comum usando o método da base

        # Desenha o título da tela de seleção
        if self.fonte_grande: # Verifica se a fonte foi carregada (usando a chave 'titulo')
            texto_titulo_surface = self.fonte_grande.render(self._texto_titulo, True, BRANCO) # Renderiza o texto do título
            rect_titulo = texto_titulo_surface.get_rect(center=(LARGURA_TELA // 2, 100)) # Centraliza o retângulo do título
            tela.blit(texto_titulo_surface, rect_titulo) # Desenha o título na tela
        else:
             print("AVISO: Fonte grande (chave 'titulo') não disponível para título da tela de seleção.") # Print de aviso

        # --- Desenha as opções de personagem (textos dos botões) ---
        # Desenha os textos das opções "Menino" e "Menina" com borda
        if self.fonte_botoes: # Verifica se a fonte foi carregada (usando a chave 'botao')
             # Desenha a opção Menino usando o método auxiliar da base
             self._desenhar_texto_com_borda(
                 tela,                     # Superfície onde desenhar
                 self._texto_menino,       # Texto ("Menino")
                 self.fonte_botoes,        # Fonte para botões
                 BRANCO, PRETO,            # Cores do texto e borda (constantes traduzidas)
                 self._grossura_borda,     # Grossura da borda
                 self._rect_opcao_menino.center # Posição central do retângulo da opção Menino
             )
             # Desenha a opção Menina usando o método auxiliar da base
             self._desenhar_texto_com_borda(
                 tela,                     # Superfície onde desenhar
                 self._texto_menina,       # Texto ("Menina")
                 self.fonte_botoes,        # Fonte para botões
                 BRANCO, PRETO,            # Cores do texto e borda
                 self._grossura_borda,     # Grossura da borda
                 self._rect_opcao_menina.center # Posição central do retângulo da opção Menina
             )
        else:
             print("AVISO: Fonte de botões (chave 'botao') não disponível para tela de seleção.") # Print de aviso


        # Opcional: desenhar imagens dos personagens ao lado ou acima dos textos
        # if self.imagem_menino_ui: ...
        # if self.imagem_menina_ui: ...


        # Opcional: desenhar retângulos de colisão para debug
        # Verifica se a flag de debug de colisão está ativa
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            pygame.draw.rect(tela, VERMELHO, self._rect_opcao_menino, 1) # Desenha o contorno do retângulo Menino
            pygame.draw.rect(tela, VERMELHO, self._rect_opcao_menina, 1) # Desenha o contorno do retângulo Menina