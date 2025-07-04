import pygame
from utilidades.constantes import *

class CaixaDeDialogo:
    def __init__(self, gerenciador_recursos):
        self.retangulo = pygame.Rect(50, ALTURA_TELA - 150, LARGURA_TELA - 100, 100)
        self.cor_fundo = (50, 50, 50)
        self.cor_borda = (0, 0, 0)
        self.cor_texto = (255, 255, 255)
        self.fonte = gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO)
        self.altura_linha = 30

        self.texto_completo = ""
        self.texto_exibido = ""
        self.indice_texto = 0
        self.tempo_exibicao_caractere = 50 # Tempo em ms para cada caractere aparecer
        self.tempo_ultimo_caractere = 0
        self.esta_digitando = False
        self.aguardando_input = False # Para esperar por input do usuário para avançar
        self.nome_personagem = None # Novo atributo para o nome do personagem
        self.fonte_nome_personagem = gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO) # Nova fonte para o nome, um pouco menor


    def definir_texto(self, texto, nome_personagem=None):
        self.texto_completo = texto
        self.texto_exibido = ""
        self.indice_texto = 0
        self.tempo_ultimo_caractere = pygame.time.get_ticks()
        self.esta_digitando = True
        self.aguardando_input = False
        self.nome_personagem = nome_personagem

    def atualizar(self):
        if self.esta_digitando:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ultimo_caractere > self.tempo_exibicao_caractere:
                if self.indice_texto < len(self.texto_completo):
                    self.texto_exibido += self.texto_completo[self.indice_texto]
                    self.indice_texto += 1
                    self.tempo_ultimo_caractere = tempo_atual
                else:
                    self.esta_digitando = False
                    self.aguardando_input = True

    def desenhar(self, superficie):
        if not self.texto_completo and not self.nome_personagem: # Não desenha se não houver texto nem nome
            return

        # Desenha o fundo e a borda da caixa de diálogo
        pygame.draw.rect(superficie, self.cor_fundo, self.retangulo, border_radius=10)
        pygame.draw.rect(superficie, self.cor_borda, self.retangulo, 3, border_radius=10)

        # Desenha o nome do personagem, se houver
        y_texto_offset = 10 # Padding superior inicial
        if self.nome_personagem:
            # Renderiza o nome do personagem
            superficie_nome = self.fonte_nome_personagem.render(self.nome_personagem, True, (255, 255, 255))
            # Calcula a posição para o nome (canto superior esquerdo, com padding)
            pos_x_nome = self.retangulo.left + 15 # Um pouco mais de padding
            pos_y_nome = self.retangulo.top - superficie_nome.get_height() - 5 # Acima da caixa, com pequeno espaçamento
            
            # Opcional: desenhar um pequeno fundo para o nome para destacá-lo
            padding_x = 12  # aumenta o padding horizontal
            padding_y = 2   # aumenta o padding vertical
            fundo_nome_rect = pygame.Rect(
                pos_x_nome - padding_x,
                pos_y_nome - padding_y,
                superficie_nome.get_width() + 2 * padding_x,
                superficie_nome.get_height() + 2 * padding_y
            )
            pygame.draw.rect(superficie, CINZA, fundo_nome_rect, border_radius=5) # Fundo cinza para o nome
            pygame.draw.rect(superficie, PRETO, fundo_nome_rect, 2, border_radius=5) # Borda para o fundo do nome

            superficie.blit(superficie_nome, (pos_x_nome, pos_y_nome))
            y_texto_offset = superficie_nome.get_height() + 20 # Ajusta o offset do texto do diálogo para baixo

        # Renderiza e blita o texto exibido
        palavras = self.texto_exibido.split(' ')
        linhas_renderizadas = []
        linha_atual = ""

        # A largura disponível para o texto é a largura do retângulo menos o padding horizontal (20)
        largura_disponivel_texto = self.retangulo.width - 20 

        for palavra in palavras:
            linha_teste = linha_atual + (" " if linha_atual else "") + palavra
            largura_texto, _ = self.fonte.size(linha_teste)

            if largura_texto > largura_disponivel_texto:
                linhas_renderizadas.append(linha_atual)
                linha_atual = palavra
            else:
                linha_atual = linha_teste
        
        if linha_atual:
            linhas_renderizadas.append(linha_atual)

        y_texto = self.retangulo.top + y_texto_offset # Começa com o padding superior ajustado
        for linha in linhas_renderizadas:
            superficie_texto = self.fonte.render(linha, True, self.cor_texto)
            superficie.blit(superficie_texto, (self.retangulo.left + 10, y_texto))
            y_texto += self.altura_linha

        if not self.esta_digitando and self.aguardando_input:
            texto_indicador = self.fonte.render("Pressione ESPAÇO para continuar...", True, CINZA)
            retangulo_indicador = texto_indicador.get_rect(center=(self.retangulo.centerx, self.retangulo.bottom - 20))
            superficie.blit(texto_indicador, retangulo_indicador)

    def pular_digitacao(self):
        if self.esta_digitando:
            self.texto_exibido = self.texto_completo
            self.indice_texto = len(self.texto_completo)
            self.esta_digitando = False
            self.aguardando_input = True

    def esta_finalizado(self):
        return not self.esta_digitando and self.aguardando_input

    def limpar_dialogo(self):
        self.texto_completo = ""
        self.texto_exibido = ""
        self.esta_digitando = False
        self.aguardando_input = False
        self.nome_personagem = None # Limpa o nome do personagem também
