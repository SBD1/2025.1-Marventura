# telas/tela_mapa.py

import pygame
from utilidades.constantes import *
from .tela_modelo import TelaModelo
from typing import TYPE_CHECKING, Literal, Optional
if TYPE_CHECKING:
    from gerenciadores import DBManager
    from gerenciadores import GerenciadorDeRecursos
    from gerenciadores import GerenciadorDeTelas
    from gerenciadores import GerenciadorDeEntidades

class Mapa(TelaModelo):
    def __init__(self, gerenciador_telas: 'GerenciadorDeTelas', gerenciador_recursos: 'GerenciadorDeRecursos', gerenciador_banco_de_dados: 'DBManager', gerenciador_entidades: 'GerenciadorDeEntidades', modo: Literal['Exibir', 'Navegar'], opcoes_destino: Optional[list] = None):
        super().__init__(gerenciador_telas, gerenciador_recursos)

        self.banco_de_dados = gerenciador_banco_de_dados
        self.entidades = gerenciador_entidades
        self.modo = modo
        self.opcoes_destino = opcoes_destino if opcoes_destino else []

        # Dicionário para mapear nomes de ilhas para seus dados
        self.dados_das_ilhas = {ilha.nome: ilha for ilha in self.banco_de_dados.buscar_ilhas(self.entidades.progresso_do_jogo.identificador_progresso)}

        # Busca o barco atual para saber se possui um barco que possa ser navegado
        self.barco = self.banco_de_dados.buscar_barco_atual(self.entidades.progresso_do_jogo.identificador_progresso)

        if modo == 'Navegar':
            if not self.barco:
                print("Você não possui um barco para navegar")
                self._carregar_recursos_minimos()
                return None
            
            if not self.opcoes_destino or all(destino.bloqueada for destino in self.opcoes_destino):
                print("Não é possível navegar agora.")
                self._carregar_recursos_minimos()
                return None
            

        # Carrega todas as imagens e fontes necessárias
        self._carregar_recursos()

        # Define as áreas clicáveis (retângulos) para cada ilha
        self.rects_das_ilhas = self._definir_posicoes_ilhas()
        
        # Centraliza a imagem de fundo na tela
        self.fundo_rect = self.imagem_fundo.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2))

        # Encontra a ilha atual para posicionar o marcador
        self.ilha_atual_nome = self.entidades.ilha_atual.nome
        self.posicao_marcador = self._calcular_posicao_marcador()



    def _carregar_recursos(self):
        """Carrega imagens e outros recursos necessários para o mapa."""
        self.imagem_fundo = self.gerenciador_recursos.obter_imagem(CHAVE_IMAGEM_MAPA_FUNDO)
        
        # Marcador do jogador (Silvie ou Shuan)
        self.imagem_marcador = self.gerenciador_recursos.obter_imagem(CHAVE_MARCADOR_MAPA_SILVIE if self.entidades.jogador.nome == 'Silvie' else CHAVE_MARCADOR_MAPA_SHUAN)

        # Dicionários que associam o nome da ilha à sua imagem de ícone e nuvem
        self.icones_das_ilhas = {
            "Ilha de Borabóia": self.gerenciador_recursos.obter_imagem(ICONE_ILHA_CAMPOS),
            "Cidade de Lurien": self.gerenciador_recursos.obter_imagem(ICONE_ILHA_CIDADE),
            "Ilha Glacial de Frimora": self.gerenciador_recursos.obter_imagem(ICONE_ILHA_NEVE),
            "Cactuaraquara": self.gerenciador_recursos.obter_imagem(ICONE_ILHA_DESERTO),
            "Nublária": self.gerenciador_recursos.obter_imagem(ICONE_ILHA_ASSOMBRADA),
            "Quartel Naval D-57": self.gerenciador_recursos.obter_imagem(ICONE_ILHA_FORTALEZA)
        }
        self.icones_das_nuvens = {
            "Cidade de Lurien": self.gerenciador_recursos.obter_imagem(ICONE_NUVEM_CIDADE),
            "Ilha Glacial de Frimora": self.gerenciador_recursos.obter_imagem(ICONE_NUVEM_NEVE),
            "Cactuaraquara": self.gerenciador_recursos.obter_imagem(ICONE_NUVEM_DESERTO),
            "Nublária": self.gerenciador_recursos.obter_imagem(ICONE_NUVEM_ASSOMBRADA),
            "Quartel Naval D-57": self.gerenciador_recursos.obter_imagem(ICONE_NUVEM_FORTALEZA)
        }
        
        # Cores para o feedback visual no modo 'Navegar'
        self.cor_borda_hover = (255, 255, 0)  # Amarelo para destacar



    def _carregar_recursos_minimos(self):
        self.imagem_fundo = self.gerenciador_recursos.obter_imagem(CHAVE_CAIXA_DE_TEXTO)

        # Centraliza a imagem de fundo na tela
        self.fundo_rect = self.imagem_fundo.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2))

        self.fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)

        self.mensagem = "Você não possui um barco para navegar." if not self.barco else "Não há destinos disponíveis para navegar agora."

        self.mensagem_superficie = self.fonte.render(self.mensagem, True, BRANCO_CLARO)
        self.mensagem_rect = self.mensagem_superficie.get_rect(center=(self.fundo_rect.centerx, self.fundo_rect.centery))



    def _definir_posicoes_ilhas(self) -> dict[str, pygame.Rect]:
        """
        Define manualmente as coordenadas e o tamanho das áreas clicáveis para cada ilha.
        """
        # A posição (x,y) é relativa à janela do jogo.
        # A largura/altura deve ser aproximada ao tamanho do ícone da ilha.
        return {
            "Ilha de Borabóia": pygame.Rect(253, 379, 125, 115),
            "Cidade de Lurien": pygame.Rect(385, 287, 117, 112),
            "Ilha Glacial de Frimora": pygame.Rect(419, 89, 127, 110),
            "Cactuaraquara": pygame.Rect(240, 176, 114, 112),
            "Nublária": pygame.Rect(559, 169, 122, 123),
            "Quartel Naval D-57": pygame.Rect(516, 392, 125, 126)
        }



    def _calcular_posicao_marcador(self) -> tuple[int, int]:
        """Calcula a posição do marcador do jogador sobre a ilha atual."""
        if self.ilha_atual_nome in self.rects_das_ilhas:
            rect_ilha_atual = self.rects_das_ilhas[self.ilha_atual_nome]
            # Posiciona o marcador um pouco acima e centralizado no rect da ilha
            marcador_x = rect_ilha_atual.centerx - self.imagem_marcador.get_width() / 2
            marcador_y = rect_ilha_atual.top - self.imagem_marcador.get_height() + 15 
            return (marcador_x, marcador_y)
        return (0, 0) # Posição padrão caso algo dê errado



    def processar_eventos(self, evento: pygame.event.Event):
        """Processa os eventos de input (mouse e teclado), apenas no modo 'Navegar'."""
        super().processar_eventos(evento)

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "cancelar"
            
        if self.modo != 'Navegar':
            return None
        
        # Se não houver barco ou destino disponíveis e o modo for 'Navegar', apenas permite fechar a tela
        if not self.barco or not self.opcoes_destino:
            return None

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botão esquerdo do mouse
                pos_mouse = pygame.mouse.get_pos()
                for nome_ilha, rect_ilha in self.rects_das_ilhas.items():
                    if rect_ilha.collidepoint(pos_mouse):
                        # Verifica se a ilha clicada é um destino válido e não está bloqueada
                        for destino in self.opcoes_destino:
                            if destino.nome == nome_ilha and not destino.bloqueada:
                                print(f"Ilha selecionada para viagem: {nome_ilha}")
                                return destino  # Retorna o objeto da ilha selecionada
        return None



    def desenhar_mensagem(self, tela: pygame.Surface):
        """"""
        # 1. Desenha a imagem de fundo
        tela.blit(self.imagem_fundo, self.fundo_rect)

        # 2. Desenha a mensagem centralizada
        self._desenhar_texto_com_borda(tela, self.mensagem, self.fonte, BRANCO_CLARO, PRETO, 1, self.mensagem_rect.center)

        



    def desenhar(self, tela: pygame.Surface):
        """Desenha todos os elementos visuais do mapa na tela."""
        if self.modo == 'Navegar':
            if not self.barco or not self.opcoes_destino or all(destino.bloqueada for destino in self.opcoes_destino):
                self.desenhar_mensagem(tela)
                return
            
        # 1. Desenha a imagem de fundo
        tela.blit(self.imagem_fundo, self.fundo_rect)
        
        # Posição atual do mouse para o efeito de hover
        pos_mouse = pygame.mouse.get_pos() if self.modo == 'Navegar' else None

        # 2. Desenha os ícones das ilhas e as nuvens
        for nome_ilha, rect_ilha in self.rects_das_ilhas.items():
            ilha_data = self.dados_das_ilhas.get(nome_ilha)
            if not ilha_data:
                continue

            # Desenha o ícone da ilha
            icone_ilha = self.icones_das_ilhas.get(nome_ilha)
            if icone_ilha:
                # Cria um rect para o ícone centralizado dentro da área clicável
                tela.blit(icone_ilha, self.fundo_rect)

            # Desenha a nuvem por cima se a ilha não foi visitada
            if not ilha_data.visitada:
                nuvem_ilha = self.icones_das_nuvens.get(nome_ilha)
                if nuvem_ilha:
                    tela.blit(nuvem_ilha, self.fundo_rect)

            # 3. Efeito de hover no modo 'Navegar'
            if self.modo == 'Navegar' and pos_mouse and rect_ilha.collidepoint(pos_mouse):
                # Verifica se a ilha sob o mouse é um destino válido
                eh_destino_valido = any(d.nome == nome_ilha and not d.bloqueada for d in self.opcoes_destino)
                if eh_destino_valido:
                    pygame.draw.rect(tela, self.cor_borda_hover, rect_ilha, 3, border_radius=10)


        # 4. Desenha o marcador do jogador
        tela.blit(self.imagem_marcador, self.posicao_marcador)