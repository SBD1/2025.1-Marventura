import pygame
from utilidades.constantes import *



class BarraDeEstado:
    def __init__(self, gerenciador_recursos, jogador):
        self.gerenciador_recursos = gerenciador_recursos
        self.jogador = jogador
        
        self.imagem_barra = self.gerenciador_recursos.obter_imagem(CHAVE_BARRA_DE_ESTADO)
        self.rect_barra = self.imagem_barra.get_rect(topleft=(0, 0))
        
        self.titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TITULO)
        self.texto = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)

        self.texto_nivel = self.texto.render(f"Nv. {self.jogador.nivel}", True, BRANCO_CLARO)
        self.rect_texto_nivel = self.texto_nivel.get_rect(topleft=(10, 80))

        # Verifica se a imagem foi carregada corretamente
        if not self.imagem_barra:
            print("AVISO: Imagem 'barra_de_estado' não encontrada. Usando fundo cinza.")
            self.imagem_barra = pygame.Surface((800, 100))
            self.imagem_barra.fill((50, 50, 50))  # Cor cinza escuro como fallback

        self.coracao = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_CORACAO)
        if not self.coracao:
            print("AVISO: Ícone de coração não encontrado. Usando ícone padrão.")
            self.coracao = pygame.Surface((20, 20))
            self.coracao.fill(VERMELHO)

        self.energia = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_ENERGIA)
        if not self.energia:
            print("AVISO: Ícone de energia não encontrado. Usando ícone padrão.")
            self.energia = pygame.Surface((20, 20))
            self.energia.fill(AZUL)

        self.moeda = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_MOEDA)
        if not self.moeda:
            print("AVISO: Ícone de moeda não encontrado. Usando ícone padrão.")
            self.moeda = pygame.Surface((20, 20))
            self.moeda.fill(AMARELO)



    # Método para desenhar texto com ícone ao lado
    def desenhar_texto_com_icone(self, tela, texto_fixo, icone_surface, texto_estado, fonte, cor_texto, pos_x, pos_y, espaçamento=5):
        # Renderiza o texto
        texto_fixo_renderizado = fonte.render(texto_fixo, True, cor_texto)
        texto_estado_renderizado = fonte.render(texto_estado, True, cor_texto)

        # Desenha o texto
        if texto_fixo_renderizado:
            tela.blit(texto_fixo_renderizado, (pos_x, pos_y))

        # Desenha o ícone ao lado do texto
        if icone_surface:
            icone_x = pos_x + texto_fixo_renderizado.get_width() + espaçamento
            tela.blit(icone_surface, (icone_x, pos_y+15))

        # Desenha o texto do estado atual ao lado do ícone
        tela.blit(texto_estado_renderizado, (icone_x + icone_surface.get_width() + espaçamento, pos_y))

        # Retorna a largura total (pode ser usado para posicionar o próximo item)
        largura_total = texto_fixo_renderizado.get_width() + espaçamento + icone_surface.get_width() + texto_estado_renderizado.get_width() + espaçamento
        return largura_total
    


    # Método para desenhar a barra de estado na tela
    def desenhar(self, tela):
        tela.blit(self.imagem_barra, self.rect_barra)

        x = 10
        y = 0

        # Desenha PV ❤️
        largura_pv = self.desenhar_texto_com_icone(
            tela,
            "PV",                                                       # Texto
            self.coracao,                                               # Ícone
            f"{self.jogador.vida_atual}/{self.jogador.vida_maxima}",    # Estado atual
            self.titulo,                                                # Fonte
            BRANCO_CLARO,                                               # Cor do texto
            x,                                                          # X inicial
            y                                                           # Y
        )

        # Próxima linha
        x += largura_pv + 100

        # Desenha PE ⚡
        largura_pe = self.desenhar_texto_com_icone(
            tela,
            "PE",
            self.energia,
            f"{self.jogador.energia_atual}/{self.jogador.energia_maxima}",
            self.titulo,
            BRANCO_CLARO,
            x,
            y
        )

        # Próxima linha
        x += largura_pe + 150

        # Desenha moedas 🪙
        largura_moeda = self.desenhar_texto_com_icone(
            tela,
            "x",
            self.moeda,
            f"{self.jogador.moedas}",
            self.titulo,
            BRANCO_CLARO,
            x,
            y
        )

        # Desenha o texto do nível
        tela.blit(self.texto_nivel, self.rect_texto_nivel)

        # Desenha a barra de XP ao lado do texto
        largura_barra_total = 200
        altura_barra = 10
        x_barra = self.rect_texto_nivel.right + 10
        y_barra = self.rect_texto_nivel.top + (self.texto_nivel.get_height() - altura_barra) // 2

        # Calcula o preenchimento
        proporcao = self.jogador.experiencia_atual / self.jogador.experiencia_por_nivel
        largura_preenchida = int(largura_barra_total * proporcao)

        # Fundo da barra
        pygame.draw.rect(tela, BRANCO_CLARO, (x_barra, y_barra, largura_barra_total, altura_barra), border_radius=5)

        # Parte preenchida
        pygame.draw.rect(tela, VERDE_CLARO, (x_barra, y_barra, largura_preenchida, altura_barra), border_radius=5)
