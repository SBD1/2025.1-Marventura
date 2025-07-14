import pygame
from utilidades.constantes import * # Presumindo que ALTURA_TELA e LARGURA_TELA ainda são relevantes

class CaixaDeDialogo:
    def __init__(self, gerenciador_recursos):
        # Dimensões da imagem da caixa de diálogo
        LARGURA_IMAGEM_CAIXA = 700
        ALTURA_IMAGEM_CAIXA = 151

        # Posição da caixa de diálogo (centralizada horizontalmente na parte inferior)
        pos_x_caixa = (LARGURA_TELA - LARGURA_IMAGEM_CAIXA) // 2
        pos_y_caixa = ALTURA_TELA - ALTURA_IMAGEM_CAIXA - 10 # Um pequeno padding da borda inferior

        self.retangulo = pygame.Rect(pos_x_caixa, pos_y_caixa, LARGURA_IMAGEM_CAIXA, ALTURA_IMAGEM_CAIXA)
        self.imagem = gerenciador_recursos.obter_imagem(CHAVE_CAIXA_DIALOGO)
        
        self.cor_texto = PRETO # Cor do texto do diálogo
        self.fonte = gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO)
        self.altura_linha = 30 # Altura de cada linha de texto

        self.texto_completo = ""
        self.texto_exibido = ""
        self.indice_texto = 0
        self.tempo_exibicao_caractere = 50
        self.tempo_ultimo_caractere = 0
        self.esta_digitando = False
        self.aguardando_input = False
        self.nome_personagem = None
        self.fonte_nome_personagem = gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO) # Fonte para o nome do personagem

        # Definição das bordas da imagem
        self.borda_superior = 39
        self.borda_lateral = 11
        self.borda_inferior = 11

        # Padding interno para o texto
        self.padding_texto = 20

        # Atributos para rolagem
        self.offset_rolagem = 0 # Quanto o texto rolou para cima (positivo) ou para baixo (negativo)
        self.max_offset_rolagem = 0 # O valor máximo que o offset pode atingir (quando todo o texto está visível)
        
        # Área visível para o texto (onde a rolagem acontece)
        self.area_visivel_texto = pygame.Rect(
            self.retangulo.left + self.borda_lateral + self.padding_texto,
            self.retangulo.top + self.borda_superior + self.padding_texto,
            self.retangulo.width - (2 * self.borda_lateral) - (2 * self.padding_texto),
            self.retangulo.height - self.borda_superior - self.borda_inferior - (2 * self.padding_texto)
        )
        
        # Armazenará as linhas quebradas do texto *exibido* para rolagem durante a digitação
        self._linhas_atuais_exibidas = []


    def definir_texto(self, texto, nome_personagem=None):
        self.texto_completo = texto
        self.texto_exibido = ""
        self.indice_texto = 0
        self.tempo_ultimo_caractere = pygame.time.get_ticks()
        self.esta_digitando = True
        self.aguardando_input = False
        self.nome_personagem = nome_personagem
        self.offset_rolagem = 0 # Resetar rolagem ao definir novo texto
        self._linhas_atuais_exibidas = [] # Resetar linhas exibidas

    def _quebrar_texto_em_linhas(self, texto_para_quebrar):
        """Função auxiliar para quebrar um texto em linhas com base na largura disponível."""
        linhas = []
        palavras = texto_para_quebrar.split(' ')
        linha_atual = ""
        largura_disponivel = self.area_visivel_texto.width

        for palavra in palavras:
            linha_teste = linha_atual + (" " if linha_atual else "") + palavra
            largura_texto, _ = self.fonte.size(linha_teste)

            if largura_texto > largura_disponivel:
                linhas.append(linha_atual)
                linha_atual = palavra
            else:
                linha_atual = linha_teste
        
        if linha_atual:
            linhas.append(linha_atual)
        return linhas


    def atualizar(self):
        if self.esta_digitando:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ultimo_caractere > self.tempo_exibicao_caractere:
                if self.indice_texto < len(self.texto_completo):
                    self.texto_exibido += self.texto_completo[self.indice_texto]
                    self.indice_texto += 1
                    self.tempo_ultimo_caractere = tempo_atual
                    
                    # Recalcular as linhas exibidas e ajustar rolagem após adicionar caractere
                    self._linhas_atuais_exibidas = self._quebrar_texto_em_linhas(self.texto_exibido)
                    self._ajustar_rolagem_dinamicamente()

                else:
                    self.esta_digitando = False
                    self.aguardando_input = True
                    # Quando a digitação termina, garante que o final do texto esteja visível
                    self._ajustar_rolagem_para_final()
        # Se não está digitando, mas está aguardando input e há texto longo,
        # o jogador pode rolar manualmente. A rolagem manual será tratada nos eventos.

    def _ajustar_rolagem_dinamicamente(self):
        """Ajusta o offset de rolagem para manter a última linha visível durante a digitação."""
        altura_texto_atual = len(self._linhas_atuais_exibidas) * self.altura_linha
        
        if altura_texto_atual > self.area_visivel_texto.height:
            # Se o texto atual exceder a altura visível, role para que a última linha esteja visível
            self.offset_rolagem = altura_texto_atual - self.area_visivel_texto.height
        else:
            self.offset_rolagem = 0 # Não há necessidade de rolar se cabe tudo


    def _ajustar_rolagem_para_final(self):
        """Ajusta o offset para mostrar o final do texto completo."""
        todas_as_linhas = self._quebrar_texto_em_linhas(self.texto_completo)
        altura_total_texto = len(todas_as_linhas) * self.altura_linha
        if altura_total_texto > self.area_visivel_texto.height:
            self.max_offset_rolagem = altura_total_texto - self.area_visivel_texto.height
            self.offset_rolagem = self.max_offset_rolagem
        else:
            self.max_offset_rolagem = 0
            self.offset_rolagem = 0

    def desenhar(self, superficie):
        if not self.texto_completo and not self.nome_personagem:
            return

        # Desenha a imagem da caixa de diálogo
        superficie.blit(self.imagem, (self.retangulo.x, self.retangulo.y))

        # Desenha o nome do personagem, se houver
        if self.nome_personagem:
            superficie_nome = self.fonte_nome_personagem.render(self.nome_personagem, True, (255, 255, 255))
            pos_x_nome = self.retangulo.left + self.borda_lateral
            pos_y_nome = self.retangulo.top + (self.borda_superior - superficie_nome.get_height()) // 2
            
            #padding_x_nome = 8
            #padding_y_nome = 2
            #fundo_nome_rect = pygame.Rect(
            #    pos_x_nome - padding_x_nome,
            #    pos_y_nome - padding_y_nome,
            #    superficie_nome.get_width() + 2 * padding_x_nome,
            #    superficie_nome.get_height() + 2 * padding_y_nome
            #)
            #pygame.draw.rect(superficie, CINZA, fundo_nome_rect, border_radius=5)
            #pygame.draw.rect(superficie, PRETO, fundo_nome_rect, 2, border_radius=5)

            superficie.blit(superficie_nome, (pos_x_nome, pos_y_nome))

        # Cria uma superfície temporária para o texto, que será blitada com um clip
        superficie_texto_renderizado = pygame.Surface(self.area_visivel_texto.size, pygame.SRCALPHA)
        superficie_texto_renderizado.fill((0,0,0,0)) # Transparente

        # Pega as linhas a serem desenhadas (do texto digitado ou do texto completo para rolagem manual)
        linhas_para_desenhar = self._linhas_atuais_exibidas if self.esta_digitando else self._quebrar_texto_em_linhas(self.texto_completo)

        y_offset_interno = 0 - self.offset_rolagem # O offset de rolagem afeta a posição Y

        for linha in linhas_para_desenhar:
            texto_surface = self.fonte.render(linha, True, self.cor_texto)
            superficie_texto_renderizado.blit(texto_surface, (0, y_offset_interno))
            y_offset_interno += self.altura_linha

        # Blita a superfície temporária para a superfície principal, na posição correta
        superficie.blit(superficie_texto_renderizado, self.area_visivel_texto.topleft)

        # Indicador para continuar/rolar
        if not self.esta_digitando and self.aguardando_input:
            # Recalcula max_offset_rolagem para o texto completo aqui também, para garantir precisão
            # (Pode ser redundante se _ajustar_rolagem_para_final foi chamado, mas garante)
            temp_linhas_completas = self._quebrar_texto_em_linhas(self.texto_completo)
            altura_total_completa = len(temp_linhas_completas) * self.altura_linha
            temp_max_offset = max(0, altura_total_completa - self.area_visivel_texto.height)

            texto_indicador = self.fonte.render("Pressione ESPAÇO para continuar...", True, CINZA)
            
            retangulo_indicador = texto_indicador.get_rect(center=(self.retangulo.centerx, self.retangulo.bottom - (self.borda_inferior + texto_indicador.get_height() // 2)))
            superficie.blit(texto_indicador, retangulo_indicador)

    def rolar(self, direcao): # direcao: 1 para baixo, -1 para cima
        if not self.esta_digitando and self.aguardando_input: # Só permite rolagem manual se não está digitando
            # Recalcula max_offset_rolagem para o texto completo, caso não tenha sido feito ainda
            todas_as_linhas = self._quebrar_texto_em_linhas(self.texto_completo)
            altura_total_texto = len(todas_as_linhas) * self.altura_linha
            self.max_offset_rolagem = max(0, altura_total_texto - self.area_visivel_texto.height)

            self.offset_rolagem += direcao * self.altura_linha # Rola uma linha por vez
            self.offset_rolagem = max(0, min(self.offset_rolagem, self.max_offset_rolagem))


    def pular_digitacao(self):
        if self.esta_digitando:
            self.texto_exibido = self.texto_completo
            self.indice_texto = len(self.texto_completo)
            self.esta_digitando = False
            self.aguardando_input = True
            self._ajustar_rolagem_para_final() # Ajusta para mostrar o final

    def esta_finalizado(self):
        # A caixa está finalizada se não está digitando E o offset de rolagem está no máximo
        # E está aguardando input do usuário
        # E todo o texto está visível ou já foi rolado até o final
        todas_as_linhas = self._quebrar_texto_em_linhas(self.texto_completo)
        altura_total_texto = len(todas_as_linhas) * self.altura_linha
        current_max_offset = max(0, altura_total_texto - self.area_visivel_texto.height)
        
        return (not self.esta_digitando and 
                self.aguardando_input and 
                self.offset_rolagem >= current_max_offset)

    def limpar_dialogo(self):
        self.texto_completo = ""
        self.texto_exibido = ""
        self.esta_digitando = False
        self.aguardando_input = False
        self.nome_personagem = None
        self.offset_rolagem = 0
        self.max_offset_rolagem = 0
        self._linhas_atuais_exibidas = []