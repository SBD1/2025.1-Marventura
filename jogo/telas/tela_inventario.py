# telas/tela_inventario.py

import pygame
from utilidades.constantes import *
from .tela_modelo import TelaModelo
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import DBManager
    from gerenciadores import GerenciadorDeRecursos
    from gerenciadores import GerenciadorDeTelas
    from gerenciadores import GerenciadorDeEntidades

class TelaInventario(TelaModelo):
    """
    Representa a tela de inventário do jogo, onde o jogador pode visualizar seus itens.
    """
    def __init__(self, gerenciador_telas: 'GerenciadorDeTelas', gerenciador_recursos: 'GerenciadorDeRecursos', gerenciador_banco_de_dados: 'DBManager', gerenciador_entidades: 'GerenciadorDeEntidades'):
        super().__init__(gerenciador_telas, gerenciador_recursos)
        self.gerenciador_banco_de_dados = gerenciador_banco_de_dados
        self.entidades = gerenciador_entidades

        # Imagens de UI
        self.fundo_inventario = None # Será carregado em _carregar_recursos
        self.quadro_item_detalhes = self.gerenciador_recursos.obter_imagem(CHAVE_CAIXA_DE_TEXTO)
        self.largura_quadro_detalhes = self.quadro_item_detalhes.get_width()
        self.altura_quadro_detalhes = self.quadro_item_detalhes.get_height()
        self.x_quadro_detalhes = (LARGURA_TELA - self.largura_quadro_detalhes) // 2
        self.y_quadro_detalhes = ALTURA_TELA - self.altura_quadro_detalhes - 20 # Posição na parte inferior

        # Dados do inventário
        self.mochila = []
        self.dados_jogador = None
        self.lista_armas = []
        self.lista_acessorios = []
        self.lista_consumiveis = []
        self.lista_outros = []
        self.item_em_foco = None # Item atualmente sob o mouse

        # Fontes
        self.font_size_titulo = 30 # Tamanho base para títulos
        self.font_size_texto_normal = 20 # Tamanho base para texto de item
        self.font_size_texto_hover = 25 # Tamanho para texto de item em foco

        self.fonte_titulo = None
        self.fonte_texto = None
        self.fonte_texto_hover = None
        self.fonte_raridade = None # Nova fonte para a raridade

        # Scroll
        self.scroll_offset_armas = 0
        self.scroll_offset_acessorios = 0
        self.scroll_offset_consumiveis = 0
        self.scroll_offset_outros = 0
        self.itens_visiveis_por_coluna = 8 # Quantos itens visíveis por vez em cada categoria

        # Posições base para o conteúdo do painel central (dentro do fundo_inventario)
        self.x_painel_central = 114 # x do fundo_inventario + margem esquerda
        self.y_painel_central = 88  # y do fundo_inventario + margem superior
        self.largura_painel_central = 400 # Largura estimada do painel de itens
        self.altura_painel_central = 400 # Altura estimada do painel de itens

        # Posição para as listas de itens dentro do painel central
        # Ajustado para deixar espaço para os botões de filtro
        self.pos_lista_itens = (self.x_painel_central + 140, self.y_painel_central + 120) # 140, 120 pixels a partir do painel central
        self.largura_coluna = self.largura_painel_central # A lista de itens ocupará a largura do painel central
        self.altura_linha_item = 30

        # Estado da aba atual
        self.current_tab = "estado" # 'estado', 'armas', 'acessorios', 'consumiveis', 'especial'

        # Estados dos filtros - Agora iniciam com um dos tipos específicos
        self.current_filter_armas = 'espada' # 'espada', 'projetil'
        self.current_filter_consumiveis = 'consumivel' # 'consumivel', 'nao_consumivel'
        self.current_filter_acessorios = 'acessorio' # Apenas um tipo de filtro para esta aba
        self.current_filter_especial = 'especial' # Apenas um tipo de filtro para esta aba

        # Estado do menu de informações do item
        self.showing_item_details_popup = False
        self.item_details_to_show = None
        self.menu_info_image = None
        self.rect_menu_info = None
        self.botao_fechar_menu_info = None
        self.rect_botao_fechar_menu_info = None
        self.botao_usar_item = None
        self.rect_botao_usar_item = None


        # Carrega os recursos e dados iniciais
        self._carregar_recursos()


    def _carregar_recursos(self):
        """
        Carrega os recursos necessários para a tela de inventário, incluindo imagens dos botões e seus retângulos.
        """
        self.fundo_inventario = self.gerenciador_recursos.obter_imagem('inv_painel_fundo')
        if not self.fundo_inventario:
            print("[ERRO] Imagem de fundo do inventário 'inv_painel_fundo' não encontrada.")
            self.fundo_inventario = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.fundo_inventario.fill(CINZA_ESCURO)

        # Novas imagens para os painéis de itens
        self.painel_itens = self.gerenciador_recursos.obter_imagem('inv_painel_itens')
        if not self.painel_itens:
            print("[ERRO] Imagem 'inv_painel_itens' não encontrada. Usando fundo cinza.")
            self.painel_itens = pygame.Surface((self.largura_painel_central, self.altura_painel_central))
            self.painel_itens.fill(CINZA)

        self.painel_vazio = self.gerenciador_recursos.obter_imagem('inv_vazio')
        if not self.painel_vazio:
            print("[ERRO] Imagem 'inv_vazio' não encontrada. Usando fundo cinza.")
            self.painel_vazio = pygame.Surface((self.largura_painel_central, self.altura_painel_central))
            self.painel_vazio.fill(CINZA_ESCURO)

        # Novas imagens de estatísticas do jogador
        self.estatistica_shuan = self.gerenciador_recursos.obter_imagem('estatistica_shuan')
        if not self.estatistica_shuan:
            print("[AVISO] Imagem 'estatistica_shuan' não encontrada.")
        self.estatistica_silvie = self.gerenciador_recursos.obter_imagem('estatistica_silvie')
        if not self.estatistica_silvie:
            print("[AVISO] Imagem 'estatistica_silvie' não encontrada.")

        # Imagem do menu de informações do item
        self.menu_info_image = self.gerenciador_recursos.obter_imagem('menu_info')
        if self.menu_info_image:
            self.rect_menu_info = self.menu_info_image.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
        else:
            print("[AVISO] Imagem 'menu_info' não encontrada. O menu de informações do item não será exibido.")
            self.rect_menu_info = pygame.Rect(0, 0, 400, 300) # Fallback rect
            self.menu_info_image = pygame.Surface(self.rect_menu_info.size)
            self.menu_info_image.fill(PRETO) # Fallback color

        # Botão de fechar para o menu de informações do item (reutiliza a imagem existente)
        self.botao_fechar_menu_info = self.gerenciador_recursos.obter_imagem('inv_botao_fechar')
        if self.botao_fechar_menu_info and self.rect_menu_info:
            self.rect_botao_fechar_menu_info = self.botao_fechar_menu_info.get_rect(topright=(self.rect_menu_info.right + self.botao_fechar_menu_info.get_width()-1, self.rect_menu_info.top + 10))
        else:
            print("[AVISO] Imagem 'inv_botao_fechar' não encontrada para o menu de informações do item.")
            self.rect_botao_fechar_menu_info = pygame.Rect(0,0,0,0) # Fallback rect

        # Botão "Usar" para o menu de informações do item
        self.botao_usar_item = self.gerenciador_recursos.obter_imagem('inv_botao_usar') # Assumindo que esta imagem existe
        if self.botao_usar_item and self.rect_menu_info:
            self.rect_botao_usar_item = self.botao_usar_item.get_rect(center=(self.rect_menu_info.centerx, self.rect_menu_info.bottom))
        else:
            print("[AVISO] Imagem 'inv_botao_usar' não encontrada. O botão 'Usar' não será exibido.")
            # Fallback: criar uma superfície simples para o botão
            self.botao_usar_item = pygame.Surface((100, 40))
            self.botao_usar_item.fill(AZUL)
            self.rect_botao_usar_item = self.botao_usar_item.get_rect(center=(self.rect_menu_info.centerx, self.rect_menu_info.bottom - 30))


        # Carrega as fontes com os tamanhos definidos
        # Certifique-se de que GerenciadorDeRecursos.obter_fonte pode aceitar um argumento 'size'
        self.fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
        self.fonte_texto = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
        self.fonte_texto_hover = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
        self.fonte_raridade = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_HACHI_MARU_TEXTO)


        # Botão de fechar principal do inventário
        self.botao_fechar = self.gerenciador_recursos.obter_imagem('inv_botao_fechar')
        self.rect_botao_fechar = self.botao_fechar.get_rect(topright=(self.x_painel_central + self.fundo_inventario.get_width(), 97))

        # Botões laterais e seus retângulos
        self.botoes_laterais = {}
        y_inicial_botoes = 94 # Posição Y inicial para os botões laterais
        x_inicial_botoes = self.x_painel_central # Posição X inicial para os botões laterais

        # Botão Estado
        img_estado_normal = self.gerenciador_recursos.obter_imagem('inv_lateral_estado')
        img_estado_ativo = self.gerenciador_recursos.obter_imagem('inv_lateral_estado_ativo')
        rect_estado = img_estado_normal.get_rect(topleft=(x_inicial_botoes, y_inicial_botoes))
        self.botoes_laterais['estado'] = {
            'normal': img_estado_normal,
            'ativo': img_estado_ativo,
            'rect': rect_estado
        }

        # Botão Arma
        img_arma_normal = self.gerenciador_recursos.obter_imagem('inv_lateral_arma')
        img_arma_ativo = self.gerenciador_recursos.obter_imagem('inv_lateral_arma_ativo')
        rect_arma = img_arma_normal.get_rect(topleft=(x_inicial_botoes, y_inicial_botoes + 83)) # Ajuste o espaçamento
        self.botoes_laterais['armas'] = {
            'normal': img_arma_normal,
            'ativo': img_arma_ativo,
            'rect': rect_arma
        }

        # Botão Acessório
        img_acessorio_normal = self.gerenciador_recursos.obter_imagem('inv_lateral_acessorio')
        img_acessorio_ativo = self.gerenciador_recursos.obter_imagem('inv_lateral_acessorio_ativo')
        rect_acessorio = img_acessorio_normal.get_rect(topleft=(x_inicial_botoes, y_inicial_botoes + 166))
        self.botoes_laterais['acessorios'] = {
            'normal': img_acessorio_normal,
            'ativo': img_acessorio_ativo,
            'rect': rect_acessorio
        }

        # Botão Consumível
        img_consumivel_normal = self.gerenciador_recursos.obter_imagem('inv_lateral_consumivel')
        img_consumivel_ativo = self.gerenciador_recursos.obter_imagem('inv_lateral_consumivel_ativo')
        rect_consumivel = img_consumivel_normal.get_rect(topleft=(x_inicial_botoes, y_inicial_botoes + 249))
        self.botoes_laterais['consumiveis'] = {
            'normal': img_consumivel_normal,
            'ativo': img_consumivel_ativo,
            'rect': rect_consumivel
        }

        # Botão Especial (Outros)
        img_especial_normal = self.gerenciador_recursos.obter_imagem('inv_lateral_especial')
        img_especial_ativo = self.gerenciador_recursos.obter_imagem('inv_lateral_especial_ativo')
        rect_especial = img_especial_normal.get_rect(topleft=(x_inicial_botoes, y_inicial_botoes + 331))
        self.botoes_laterais['especial'] = {
            'normal': img_especial_normal,
            'ativo': img_especial_ativo,
            'rect': rect_especial
        }

        # Botões de filtro
        self.botoes_filtro = {}
        # Posição inicial para os botões de filtro dentro do painel central
        x_filtro_inicial = self.x_painel_central + 375 # Margem do painel
        y_filtro_inicial = self.y_painel_central + 33 # Margem do painel

        # Filtros de Armas (apenas espada e projetil)
        self.botoes_filtro['armas_espada'] = {
            'ativo': self.gerenciador_recursos.obter_imagem('filtro_espada'),
            'rect': self.gerenciador_recursos.obter_imagem('filtro_espada').get_rect(topleft=(x_filtro_inicial, y_filtro_inicial))
        }
        self.botoes_filtro['armas_projetil'] = {
            'ativo': self.gerenciador_recursos.obter_imagem('filtro_projetil'),
            'rect': self.gerenciador_recursos.obter_imagem('filtro_projetil').get_rect(topleft=(x_filtro_inicial, y_filtro_inicial))
        }

        # Filtros de Consumíveis (apenas consumivel e nao_consumivel)
        self.botoes_filtro['consumiveis_consumivel'] = {
            'ativo': self.gerenciador_recursos.obter_imagem('filtro_consumivel'),
            'rect': self.gerenciador_recursos.obter_imagem('filtro_consumivel').get_rect(topleft=(x_filtro_inicial, y_filtro_inicial))
        }
        self.botoes_filtro['consumiveis_nao_consumivel'] = {
            'ativo': self.gerenciador_recursos.obter_imagem('filtro_nao_consumivel'),
            'rect': self.gerenciador_recursos.obter_imagem('filtro_nao_consumivel').get_rect(topleft=(x_filtro_inicial, y_filtro_inicial))
        }

        # Filtro de Acessórios (único)
        self.botoes_filtro['acessorios_acessorio'] = {
            'ativo': self.gerenciador_recursos.obter_imagem('filtro_acessorio'),
            'rect': self.gerenciador_recursos.obter_imagem('filtro_acessorio').get_rect(topleft=(x_filtro_inicial, y_filtro_inicial))
        }

        # Filtro Especial (único)
        self.botoes_filtro['especial_especial'] = {
            'ativo': self.gerenciador_recursos.obter_imagem('filtro_especial'),
            'rect': self.gerenciador_recursos.obter_imagem('filtro_especial').get_rect(topleft=(x_filtro_inicial, y_filtro_inicial))
        }


        # Carrega os dados do inventário e do jogador
        self._carregar_dados_inventario()

    def _carregar_dados_inventario(self):
        """
        Carrega os dados do inventário e do jogador do banco de dados.
        Atualiza também os dados de vida e energia do jogador a partir da entidade do jogador.
        """
        if not self.entidades.jogador or not self.entidades.progresso_do_jogo:
            print("[ERRO] Jogador ou progresso do jogo não disponíveis para carregar inventário.")
            return

        self.mochila = self.entidades.jogador.mochila
        # print(f"[DEBUG] Mochila carregada: {len(self.mochila.itens)} itens")

        # Atualiza self.dados_jogador a partir da entidade do jogador para obter os valores mais recentes
        self.dados_jogador = self.entidades.jogador
        # print(f"[DEBUG] Dados do jogador carregados: {self.dados_jogador.nome if self.dados_jogador else 'Nenhum'}")


        # Filtra o inventário em listas separadas
        self.lista_armas = [item for item in self.mochila.itens if item.tipo == 'arm']
        self.lista_acessorios = [item for item in self.mochila.itens if item.tipo == 'ace']
        # Consumíveis agora inclui 'con' e 'ncn' para permitir filtragem
        self.lista_consumiveis = [item for item in self.mochila.itens if item.tipo in ['con', 'ncn']]
        # Outros agora só inclui 'fru'
        self.lista_outros = [item for item in self.mochila.itens if item.tipo == 'fru']

        # Ordena as listas por nome para facilitar a visualização
        self.lista_armas.sort(key=lambda item: item.nome)
        self.lista_acessorios.sort(key=lambda item: item.nome)
        self.lista_consumiveis.sort(key=lambda item: item.nome)
        self.lista_outros.sort(key=lambda item: item.nome)


    def processar_eventos(self, evento):
        """
        Processa eventos específicos da tela de inventário.
        """
        super().processar_eventos(evento) # Permite eventos base (ex: ESC para sair)

        if self.showing_item_details_popup:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Lógica para o botão de fechar do menu de informações
                if self.rect_botao_fechar_menu_info and self.rect_botao_fechar_menu_info.collidepoint(evento.pos):
                    self.showing_item_details_popup = False
                    self.item_details_to_show = None
                    print("[DEBUG] Fechou o menu de informações do item.")
                    return
                # Lógica para o botão "Usar" do menu de informações
                elif self.rect_botao_usar_item and self.rect_botao_usar_item.collidepoint(evento.pos):
                    if self.item_details_to_show:
                        print(f"[DEBUG] Usando item: {self.item_details_to_show.nome}")
                        # Chama a função para usar o item
                        self.entidades.jogador.usar_item_da_mochila(self.item_details_to_show)
                        # Fecha o popup e recarrega os dados do inventário para refletir a mudança
                        self.showing_item_details_popup = False
                        self.item_details_to_show = None
                        # A chamada para _carregar_dados_inventario() será feita no método 'atualizar'
                    return
            return # Não processa outros eventos enquanto o popup está aberto

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Clique esquerdo
                # Lógica para o botão de fechar
                if self.rect_botao_fechar.collidepoint(evento.pos):
                    #self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MAPA) # Ou a tela anterior, se houver um histórico
                    self.gerenciador_telas.tela_atual.menu_inventario = None
                    self.gerenciador_telas.tela_atual.menu_inventario_ativo = False
                    return

                # Lógica para os botões laterais (abas)
                for tab_name, button_data in self.botoes_laterais.items():
                    if button_data['rect'].collidepoint(evento.pos):
                        self.current_tab = tab_name
                        print(f"[DEBUG] Aba alterada para: {self.current_tab}")
                        self.item_em_foco = None # Limpa o item em foco ao mudar de aba
                        return
                
                # Lógica para os botões de filtro (dentro das abas de itens)
                if self.current_tab == 'armas':
                    if self.botoes_filtro['armas_espada']['rect'].collidepoint(evento.pos):
                        # Se o filtro atual é espada, alterna para projetil; caso contrário, define como espada
                        self.current_filter_armas = 'projetil' if self.current_filter_armas == 'espada' else 'espada'
                    elif self.botoes_filtro['armas_projetil']['rect'].collidepoint(evento.pos):
                        # Se o filtro atual é projetil, alterna para espada; caso contrário, define como projetil
                        self.current_filter_armas = 'espada' if self.current_filter_armas == 'projetil' else 'projetil'
                    print(f"[DEBUG] Filtro de Armas alterado para: {self.current_filter_armas}")
                
                elif self.current_tab == 'consumiveis':
                    if self.botoes_filtro['consumiveis_consumivel']['rect'].collidepoint(evento.pos):
                        # Se o filtro atual é consumivel, alterna para nao_consumivel; caso contrário, define como consumivel
                        self.current_filter_consumiveis = 'nao_consumivel' if self.current_filter_consumiveis == 'consumivel' else 'consumivel'
                    elif self.botoes_filtro['consumiveis_nao_consumivel']['rect'].collidepoint(evento.pos):
                        # Se o filtro atual é nao_consumivel, alterna para consumivel; caso contrário, define como nao_consumivel
                        self.current_filter_consumiveis = 'consumivel' if self.current_filter_consumiveis == 'nao_consumivel' else 'nao_consumivel'
                    print(f"[DEBUG] Filtro de Consumíveis alterado para: {self.current_filter_consumiveis}")
                
                # Acessórios e Especial não precisam de lógica de clique para filtro, pois têm apenas um filtro.

                # Lógica para selecionar item (se houver)
                # Esta lógica só deve ser ativada se uma aba de itens estiver ativa
                if self.current_tab in ['armas', 'acessorios', 'consumiveis', 'especial']:
                    # Determina qual lista de itens usar com base na aba atual E no filtro ativo
                    lista_itens_filtrada = self._obter_lista_itens_filtrada()

                    # Calcula a posição da coluna ativa - agora usa a posição do painel central
                    pos_coluna_ativa = self.pos_lista_itens


                    inicio = self._obter_scroll_offset_ativo()
                    fim = min(len(lista_itens_filtrada), inicio + self.itens_visiveis_por_coluna)
                    itens_visiveis = lista_itens_filtrada[inicio:fim]

                    for i, item in enumerate(itens_visiveis):
                        y_item = pos_coluna_ativa[1] + i * self.altura_linha_item
                        rect_item = pygame.Rect(pos_coluna_ativa[0], y_item, self.largura_coluna, self.altura_linha_item)

                        if rect_item.collidepoint(evento.pos):
                            # Lógica para exibir o menu de informações do item
                            self.item_details_to_show = item
                            self.showing_item_details_popup = True
                            print(f"[DEBUG] Clicou no item: {item.nome}. Exibindo detalhes.")
                            return # Não processa mais cliques após abrir o popup
        
        elif evento.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            
            # Determina qual coluna está sob o mouse para aplicar o scroll
            # A rolagem agora só afeta a aba ativa e verifica se o mouse está sobre a área do painel central
            if self._esta_sobre_area_painel_central(mouse_pos):
                if self.current_tab == 'armas':
                    self.scroll_offset_armas = self._aplicar_scroll(self.scroll_offset_armas, evento.y, self._obter_lista_itens_filtrada())
                elif self.current_tab == 'acessorios':
                    self.scroll_offset_acessorios = self._aplicar_scroll(self.scroll_offset_acessorios, evento.y, self._obter_lista_itens_filtrada())
                elif self.current_tab == 'consumiveis':
                    self.scroll_offset_consumiveis = self._aplicar_scroll(self.scroll_offset_consumiveis, evento.y, self._obter_lista_itens_filtrada())
                elif self.current_tab == 'especial':
                    self.scroll_offset_outros = self._aplicar_scroll(self.scroll_offset_outros, evento.y, self._obter_lista_itens_filtrada())

    def _esta_sobre_area_painel_central(self, mouse_pos):
        """Verifica se a posição do mouse está dentro da área do painel central de itens."""
        # Ajusta o retângulo para a área onde os itens são realmente listados, abaixo dos filtros
        rect_painel_central = pygame.Rect(self.pos_lista_itens[0], self.pos_lista_itens[1], self.largura_painel_central, self.altura_painel_central - 40)
        return rect_painel_central.collidepoint(mouse_pos)

    def _aplicar_scroll(self, current_offset, scroll_delta, lista_itens):
        """Aplica o scroll a um offset específico, respeitando os limites."""
        total_itens = len(lista_itens)
        max_offset = max(0, total_itens - self.itens_visiveis_por_coluna)
        new_offset = current_offset - scroll_delta
        return max(0, min(new_offset, max_offset))

    def _obter_lista_itens_filtrada(self):
        """Retorna a lista de itens filtrada com base na aba e filtro ativos."""
        lista_base = []
        current_filter = ''

        if self.current_tab == 'armas':
            lista_base = self.lista_armas
            current_filter = self.current_filter_armas
            if current_filter == 'espada':
                return [item for item in lista_base if item.tipo_arma == 'esp']
            elif current_filter == 'projetil':
                return [item for item in lista_base if item.tipo_arma in ['est', 'arco']] # Estilingue e Arco
        elif self.current_tab == 'acessorios':
            lista_base = self.lista_acessorios
            current_filter = self.current_filter_acessorios # Será 'acessorio'
            # Acessórios não precisam de sub-filtro complexo, já estão filtrados por tipo_item == 'ace'
        elif self.current_tab == 'consumiveis':
            lista_base = self.lista_consumiveis # Esta lista agora contém 'con' e 'ncn'
            current_filter = self.current_filter_consumiveis
            if current_filter == 'consumivel':
                return [item for item in lista_base if item.tipo == 'con']
            elif current_filter == 'nao_consumivel':
                return [item for item in lista_base if item.tipo == 'ncn']
        elif self.current_tab == 'especial':
            lista_base = self.lista_outros # Esta lista agora contém apenas 'fru'
            current_filter = self.current_filter_especial # Será 'especial'
            # Para a aba "especial", o filtro "especial" significa mostrar as frutas
            bolsa_de_moedas = self.entidades.jogador.moedas
            return [item for item in lista_base if item.tipo == 'ncn' and item.item_de_missao]

        return lista_base # Retorna a lista completa da aba se o filtro for 'todos' ou único

    def _obter_scroll_offset_ativo(self):
        """Retorna o offset de scroll da aba ativa."""
        if self.current_tab == 'armas':
            return self.scroll_offset_armas
        elif self.current_tab == 'acessorios':
            return self.scroll_offset_acessorios
        elif self.current_tab == 'consumiveis':
            return self.scroll_offset_consumiveis
        elif self.current_tab == 'especial':
            return self.scroll_offset_outros
        return 0


    def atualizar(self, dt):
        """
        Atualiza a lógica interna da tela de inventário.
        Recarrega os dados do inventário e do jogador para garantir que estejam sempre atualizados.
        """
        self._carregar_dados_inventario() # Garante que HP/PE e itens estejam atualizados
        pass # Não há muita lógica de atualização contínua aqui, a menos que haja animações.

    def desenhar(self, tela):
        """
        Desenha os elementos da tela de inventário.
        """
        # Posiciona o fundo_inventario em (144, 88)
        tela.blit(self.fundo_inventario, (self.x_painel_central, self.y_painel_central))

        mouse_pos = pygame.mouse.get_pos()
        self.item_em_foco = None # Reseta o item em foco a cada frame

        # Desenha o botão de fechar
        tela.blit(self.botao_fechar, self.rect_botao_fechar)

        # Desenha os botões laterais
        for tab_name, button_data in self.botoes_laterais.items():
            image_to_draw = button_data['ativo'] if self.current_tab == tab_name else button_data['normal']
            tela.blit(image_to_draw, button_data['rect'])

        # Desenha o conteúdo da aba ativa
        if self.current_tab == 'estado':
            self._desenhar_info_jogador(tela)
        elif self.current_tab == 'armas':
            # Sempre desenha o painel de itens, mesmo que vazio
            tela.blit(self.painel_itens, (self.x_painel_central, self.y_painel_central))
            self._desenhar_filtros_armas(tela) # Desenha os botões de filtro
            lista_filtrada = self._obter_lista_itens_filtrada()
            if lista_filtrada: # Só desenha a coluna de itens se houver itens para mostrar
                self._desenhar_coluna_itens(tela, "Armas", lista_filtrada, self.pos_lista_itens, self.scroll_offset_armas, mouse_pos)
            else:
                tela.blit(self.painel_vazio, (self.x_painel_central, self.y_painel_central))
        elif self.current_tab == 'acessorios':
            tela.blit(self.painel_itens, (self.x_painel_central, self.y_painel_central))
            self._desenhar_filtros_acessorios(tela) # Desenha o botão de filtro
            lista_filtrada = self._obter_lista_itens_filtrada()
            if lista_filtrada:
                self._desenhar_coluna_itens(tela, "Acessórios", lista_filtrada, self.pos_lista_itens, self.scroll_offset_acessorios, mouse_pos)
            else:
                tela.blit(self.painel_vazio, (self.x_painel_central, self.y_painel_central))
        elif self.current_tab == 'consumiveis':
            tela.blit(self.painel_itens, (self.x_painel_central, self.y_painel_central))
            self._desenhar_filtros_consumiveis(tela) # Desenha os botões de filtro
            lista_filtrada = self._obter_lista_itens_filtrada()
            if lista_filtrada:
                self._desenhar_coluna_itens(tela, "Consumíveis", lista_filtrada, self.pos_lista_itens, self.scroll_offset_consumiveis, mouse_pos)
            else:
                tela.blit(self.painel_vazio, (self.x_painel_central, self.y_painel_central))
        elif self.current_tab == 'especial': # Corresponde a 'outros'
            tela.blit(self.painel_itens, (self.x_painel_central, self.y_painel_central))
            self._desenhar_filtros_especial(tela) # Desenha o botão de filtro
            lista_filtrada = self._obter_lista_itens_filtrada()
            if lista_filtrada:
                self._desenhar_coluna_itens(tela, "Outros", lista_filtrada, self.pos_lista_itens, self.scroll_offset_outros, mouse_pos)
            else:
                tela.blit(self.painel_vazio, (self.x_painel_central, self.y_painel_central))


        # Desenha os detalhes do item em foco (sempre na mesma posição, independente da aba)
        #if self.item_em_foco: # Esta linha foi comentada pois o popup de detalhes agora lida com isso
        #    self._desenhar_detalhes_item(tela, self.item_em_foco)

        # Desenha o menu de informações do item por cima de tudo
        if self.showing_item_details_popup and self.item_details_to_show:
            # Cria uma superfície semi-transparente preta para escurecer o fundo
            s = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180)) # Cor preta com 180 de alpha (0-255)
            tela.blit(s, (0, 0))

            self._desenhar_menu_info_item(tela, self.item_details_to_show)

    def _desenhar_filtros_armas(self, tela):
        """Desenha os botões de filtro para a aba de armas."""
        # Desenha o filtro ativo
        if self.current_filter_armas == 'espada':
            tela.blit(self.botoes_filtro['armas_espada']['ativo'], self.botoes_filtro['armas_espada']['rect'])
        elif self.current_filter_armas == 'projetil':
            tela.blit(self.botoes_filtro['armas_projetil']['ativo'], self.botoes_filtro['armas_projetil']['rect'])


    def _desenhar_filtros_consumiveis(self, tela):
        """Desenha os botões de filtro para a aba de consumíveis."""
        # Desenha o filtro ativo
        if self.current_filter_consumiveis == 'consumivel':
            tela.blit(self.botoes_filtro['consumiveis_consumivel']['ativo'], self.botoes_filtro['consumiveis_consumivel']['rect'])
        elif self.current_filter_consumiveis == 'nao_consumivel':
            tela.blit(self.botoes_filtro['consumiveis_nao_consumivel']['ativo'], self.botoes_filtro['consumiveis_nao_consumivel']['rect'])


    def _desenhar_filtros_acessorios(self, tela):
        """Desenha o botão de filtro para a aba de acessórios (único)."""
        button_data = self.botoes_filtro['acessorios_acessorio']
        # Sempre ativo, pois é o único filtro
        tela.blit(button_data['ativo'], button_data['rect'])

    def _desenhar_filtros_especial(self, tela):
        """Desenha o botão de filtro para a aba especial (único)."""
        button_data = self.botoes_filtro['especial_especial']
        # Sempre ativo, pois é o único filtro
        tela.blit(button_data['ativo'], button_data['rect'])


    def _desenhar_coluna_itens(self, tela, titulo_coluna, lista_itens, pos_coluna, scroll_offset, mouse_pos):
        """Desenha uma coluna de itens com título e itens listados."""
        x_coluna, y_coluna = pos_coluna

        # Desenha os itens
        inicio = scroll_offset
        fim = min(len(lista_itens), inicio + self.itens_visiveis_por_coluna)
        itens_visiveis = lista_itens[inicio:fim]

        for i, item in enumerate(itens_visiveis):
            y_item_top = y_coluna + i * self.altura_linha_item # Topo da área da linha do item
            rect_item = pygame.Rect(x_coluna, y_item_top, self.largura_coluna, self.altura_linha_item)

            mouse_sobre = rect_item.collidepoint(mouse_pos)

            current_font = self.fonte_texto
            if mouse_sobre:
                self.item_em_foco = item # Define o item em foco
                current_font = self.fonte_texto_hover
            
            # Desenha o nome do item e quantidade
            texto_item = f"{item.nome} x{item.quantidade}"
            
            # Renderiza o texto com a fonte atual
            texto_renderizado = current_font.render(texto_item, True, BRANCO_CLARO) # Mantém a cor branca
            
            # Ajusta o texto se exceder a largura
            if texto_renderizado.get_width() > self.largura_coluna - 10: # Pequena margem
                texto_item = self.renderizar_texto_limitado(current_font, texto_item, BRANCO_CLARO, self.largura_coluna - 10)
                texto_renderizado = current_font.render(texto_item, True, BRANCO_CLARO) # Renderiza novamente após truncar

            # Calcula o centro vertical para o texto dentro da linha do item
            text_rect = texto_renderizado.get_rect()
            text_y_centered = y_item_top + (self.altura_linha_item - text_rect.height) // 2

            self._desenhar_texto_com_borda(
                tela,
                texto_item,
                current_font, # Passa a fonte atual (normal ou hover)
                BRANCO_CLARO, # Cor do texto
                PRETO, # Cor da borda
                1, # Grossura da borda
                (x_coluna + 5, text_y_centered), # Usa o y calculado para centralização
                align='left'
            )
            
            # Removido: Desenho do retângulo de destaque no hover


    def _desenhar_detalhes_item(self, tela, item):
        """Desenha os detalhes de um item na parte inferior da tela."""
        tela.blit(self.quadro_item_detalhes, (self.x_quadro_detalhes, self.y_quadro_detalhes))

        # Título do item
        self._desenhar_texto_com_borda(
            tela,
            item.nome,
            self.fonte_titulo,
            VERDE_CLARO,
            PRETO,
            1,
            (self.x_quadro_detalhes + self.largura_quadro_detalhes // 2, self.y_quadro_detalhes + 20),
            align='center'
        )

        # Descrição do item (com quebra de linha)
        largura_texto_detalhes = self.largura_quadro_detalhes - 40 # Margem
        linhas_desc = self.quebrar_texto(item.descricao, self.fonte_texto, largura_texto_detalhes)
        
        y_offset = self.y_quadro_detalhes + 60
        for linha in linhas_desc:
            texto_renderizado = self.fonte_texto.render(linha, True, PRETO)
            tela.blit(texto_renderizado, (self.x_quadro_detalhes + 20, y_offset))
            y_offset += self.fonte_texto.get_linesize()

        # Efeitos do item (se houver)
        efeitos = item.resumir_efeitos() # Assumindo que o item tem este método
        if efeitos:
            self._desenhar_texto_com_borda(
                tela,
                f"Efeitos: {efeitos}",
                self.fonte_texto,
                AZUL_CLARO,
                PRETO,
                1,
                (self.x_quadro_detalhes + 20, y_offset + 10),
                align='left'
            )

    def _desenhar_menu_info_item(self, tela, item):
        """Desenha o menu de informações detalhadas do item."""
        if not self.menu_info_image or not self.rect_menu_info:
            return # Não desenha se a imagem ou o rect não existirem

        tela.blit(self.menu_info_image, self.rect_menu_info)
        
        if self.botao_fechar_menu_info and self.rect_botao_fechar_menu_info:
            tela.blit(self.botao_fechar_menu_info, self.rect_botao_fechar_menu_info)

        # Desenha o botão "Usar"
        if self.current_tab == 'consumiveis' and item.tipo == 'con':
            if self.botao_usar_item and self.rect_botao_usar_item:
                tela.blit(self.botao_usar_item, self.rect_botao_usar_item)
                # Adiciona texto ao botão "Usar"
                self._desenhar_texto_com_borda(
                    tela,
                    "Usar",
                    self.fonte_titulo, # Pode ser uma fonte diferente para o botão
                    BRANCO_CLARO,
                    PRETO,
                    1,
                    self.rect_botao_usar_item.center,
                    align='center'
                )


        # Posições para o texto dentro do menu_info_image
        x_base = self.rect_menu_info.x + 50 # Margem interna
        y_base = self.rect_menu_info.y + 50 # Margem interna

        # Título do item
        self._desenhar_texto_com_borda(
            tela,
            item.nome,
            self.fonte_titulo,
            VERDE_CLARO,
            PRETO,
            1,
            (self.rect_menu_info.centerx, y_base),
            align='center'
        )

        # Descrição do item (com quebra de linha)
        largura_texto_detalhes = self.rect_menu_info.width - 100 # Largura do menu - margens
        linhas_desc = self.quebrar_texto(item.descricao, self.fonte_texto, largura_texto_detalhes)
        
        y_offset = y_base + self.fonte_titulo.get_height() + 20 # Abaixo do título
        for linha in linhas_desc:
            texto_renderizado = self.fonte_texto.render(linha, True, PRETO)
            # Centraliza o texto horizontalmente dentro da área de detalhes
            text_rect = texto_renderizado.get_rect(centerx=self.rect_menu_info.centerx)
            tela.blit(texto_renderizado, (text_rect.x, y_offset))
            y_offset += self.fonte_texto.get_linesize()

        # Efeitos do item (se houver)
        efeitos = item.resumir_efeitos() # Assumindo que o item tem este método
        if efeitos:
            self._desenhar_texto_com_borda(
                tela,
                f"Efeitos: {efeitos}",
                self.fonte_texto,
                AZUL_CLARO,
                PRETO,
                1,
                (self.rect_menu_info.centerx, y_offset + 10),
                align='center'
            )
        
        # Raridade (separado em duas partes)
        texto_raridade_fixo = "Raridade: "
        texto_raridade_valor = str(item.raridade)

        # Renderiza a primeira parte com fonte_texto
        render_raridade_fixo = self.fonte_texto.render(texto_raridade_fixo, True, AMARELO)
        
        # Renderiza a segunda parte com fonte_raridade
        render_raridade_valor = self.fonte_raridade.render(texto_raridade_valor, True, AMARELO)

        # Calcula a largura total combinada para centralizar
        largura_total_raridade = render_raridade_fixo.get_width() + render_raridade_valor.get_width()
        
        # Calcula a posição X inicial para centralizar o conjunto
        x_raridade_inicial = self.rect_menu_info.centerx - (largura_total_raridade // 2)
        y_raridade = y_offset + 40 # Posição Y abaixo dos efeitos

        # Desenha a primeira parte
        self._desenhar_texto_com_borda(
            tela,
            texto_raridade_fixo,
            self.fonte_texto,
            AMARELO,
            PRETO,
            1,
            (x_raridade_inicial, y_raridade),
            align='left' # Alinha à esquerda da posição inicial calculada
        )

        # Desenha a segunda parte imediatamente após a primeira
        self._desenhar_texto_com_borda(
            tela,
            texto_raridade_valor,
            self.fonte_raridade,
            AMARELO,
            PRETO,
            1,
            (x_raridade_inicial + render_raridade_fixo.get_width(), y_raridade),
            align='left' # Alinha à esquerda da posição final da primeira parte
        )


    def _desenhar_info_jogador(self, tela):
        """Desenha informações básicas do jogador (HP, PE, Moedas) na tela."""
        # Posição para as informações do jogador (centralizado no painel central)
        x_info = self.x_painel_central
        y_info = self.y_painel_central

        # Desenha a imagem do personagem baseado no nome
        imagem_personagem = None
        if self.dados_jogador.nome == "Shuan" and self.estatistica_shuan:
            imagem_personagem = self.estatistica_shuan
        elif self.dados_jogador.nome == "Silvie" and self.estatistica_silvie:
            imagem_personagem = self.estatistica_silvie
        
        if imagem_personagem:
            # Posição da imagem do personagem (ajuste conforme o layout desejado)
            # Exemplo: acima das informações de texto
            rect_imagem = imagem_personagem.get_rect(topleft=(x_info, y_info))
            tela.blit(imagem_personagem, rect_imagem)

        self._desenhar_texto_com_borda(
            tela,
            str(self.dados_jogador.nivel),
            self.fonte_titulo,
            (255, 255, 255),
            PRETO,
            1,
            (x_info + 533, y_info + 192),
            align='center'
        )
        self._desenhar_texto_com_borda(
            tela,
            f"{self.dados_jogador.vida_atual}/{self.dados_jogador.vida_maxima}",
            self.fonte_titulo,
            (255, 255, 255),
            PRETO,
            1,
            (x_info + 533, y_info + 274),
            align='center'
        )
        self._desenhar_texto_com_borda(
            tela,
            f"{self.dados_jogador.energia_atual}/{self.dados_jogador.energia_maxima}",
            self.fonte_titulo,
            (255, 255, 255),
            PRETO,
            1,
            (x_info + 533, y_info + 354),
            align='center'
        )

        # Adicione mais atributos do jogador aqui, se desejar

    # Métodos auxiliares copiados e adaptados da TelaModelo/TelaBatalha
    def renderizar_texto_limitado(self, fonte, texto, cor, largura_max):
        """Limita o texto para caber na largura máxima, adicionando '...' se necessário."""
        texto_final = texto
        while fonte.size(texto_final)[0] > largura_max and len(texto_final) > 0:
            texto_final = texto_final[:-1]
        if texto_final != texto: # Se o texto foi truncado
            if len(texto_final) > 3: # Garante que há espaço para "..."
                texto_final = texto_final[:-3] + "..."
            else: # Se o texto é muito curto, apenas trunca
                texto_final = "..."
        return texto_final

    def quebrar_texto(self, texto, fonte, largura_max):
        """Quebra um texto em múltiplas linhas para caber em uma largura máxima."""
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            test_linha = linha_atual + palavra + " "
            if fonte.size(test_linha)[0] <= largura_max:
                linha_atual = test_linha
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + " "

        if linha_atual:
            linhas.append(linha_atual.strip())

        return linhas
