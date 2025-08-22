# telas/tela_cozinha.py

import pygame
from utilidades.constantes import *
from .tela_modelo import TelaModelo
from dataclasses import dataclass
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import DBManager
    from gerenciadores import GerenciadorDeRecursos
    from gerenciadores import GerenciadorDeTelas
    from gerenciadores import GerenciadorDeEntidades



@dataclass
class Receita:
    identificador_receita: str
    identificador_produto: int
    nome_produto: str
    efeitos: list # Lista de namedtuple_row (efeito_nome, efeito_valor)
    ingredientes: list  # Lista de namedtuple_row (identificador_ingrediente, nome_ingrediente)



class TelaCozinha(TelaModelo):
    """
    Representa a tela de cozinha do jogo, onde o jogador pode combinar dois ingredientes para criar novos itens.
    Também é possível visualizar as receitas conhecidas.
    """
    def __init__(self, gerenciador_telas: 'GerenciadorDeTelas', gerenciador_recursos: 'GerenciadorDeRecursos', gerenciador_banco_de_dados: 'DBManager', gerenciador_entidades: 'GerenciadorDeEntidades'):
        super().__init__(gerenciador_telas, gerenciador_recursos)
        self.banco_de_dados = gerenciador_banco_de_dados
        self.entidades = gerenciador_entidades

        # Imagens de UI
        self.painel_de_fundo = None # Será carregado em _carregar_recursos

        # Dados do inventário
        self.mochila = []
        self.lista_itens = []
        self.lista_ingredientes = []
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
        self.deslocamento_de_rolagem_receitas = 0
        self.scroll_detalhes_receita = 0 # <--- NOVO: Rolagem dos detalhes (direita)
        self.altura_conteudo_detalhes = 0 # <--- NOVO: Altura total do conteúdo do painel direito
    
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
        self.aba_atual = "cozinhar" # 'cozinhar', 'receitas'

        self.receita_selecionada = None
        self.imagem_receita_selecionada = None # Imagem da receita selecionada

        # Estado do menu de informações do item
        self.showing_item_details_popup = False
        self.item_details_to_show = None
        self.fundo_menu_selecao = None
        self.rect_menu_selecao = None
        self.botao_fechar_menu_info = None
        self.rect_botao_fechar_menu_selecao_ingrediente = None
        self.botao_usar_item = None
        self.rect_botao_usar_item = None

        # --- NOVO: Estado da aba Cozinhar ---
        self.slot1_ingrediente = None
        self.slot2_ingrediente = None
        self.imagem_ingrediente_1 = None
        self.imagem_ingrediente_2 = None

        self.rect_slot1 = None
        self.rect_slot2 = None
        self.rect_botao_cozinhar = None
        
        # Estado do menu de seleção de ingredientes
        self.exibindo_menu_ingredientes = False
        self.slot_ativo_para_selecao = None # Vai guardar 1 ou 2
        self.scroll_menu_ingredientes = 0
        self.lista_ingredientes_disponiveis = []

         # --- NOVO: Mensagem de feedback de cozimento ---
        self.mensagem_resultado = None # Guarda o texto da mensagem
        self.tempo_exibicao_mensagem = 0 # Timer para a mensagem desaparecer
        self.DURACAO_MENSAGEM = 3 # Duração em segundos

        # Carrega os recursos e dados iniciais
        self._carregar_recursos()



    def _carregar_recursos(self):
        """
        Carrega os recursos necessários para a tela de inventário, incluindo imagens dos botões e seus retângulos.
        """
        self.painel_de_fundo = self.gerenciador_recursos.obter_imagem(INV_PAINEL_FUNDO)
        if not self.painel_de_fundo:
            print("[ERRO] Imagem de fundo do inventário INV_PAINEL_FUNDO não encontrada.")
            self.painel_de_fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.painel_de_fundo.fill(CINZA_ESCURO)

        # Novas imagens para os painéis de itens
        self.painel_itens = self.gerenciador_recursos.obter_imagem(INV_PAINEL_ITENS)
        if not self.painel_itens:
            print("[ERRO] Imagem INV_PAINEL_ITENS não encontrada. Usando fundo cinza.")
            self.painel_itens = pygame.Surface((self.largura_painel_central, self.altura_painel_central))
            self.painel_itens.fill(CINZA)

        self.painel_receitas = self.gerenciador_recursos.obter_imagem(PAINEL_RECEITAS)
        if not self.painel_receitas:
            print("[ERRO] Imagem PAINEL_RECEITAS não encontrada. Usando fundo cinza.")
            self.painel_receitas = pygame.Surface((self.largura_painel_central, self.altura_painel_central))
            self.painel_receitas.fill(CINZA)

        self.painel_vazio = self.gerenciador_recursos.obter_imagem(INV_VAZIO)
        if not self.painel_vazio:
            print("[ERRO] Imagem INV_VAZIO não encontrada. Usando fundo cinza.")
            self.painel_vazio = pygame.Surface((self.largura_painel_central, self.altura_painel_central))
            self.painel_vazio.fill(CINZA_ESCURO)

        # Imagem do menu de informações do item
        self.fundo_menu_selecao = self.gerenciador_recursos.obter_imagem(MENU_INFO)
        if self.fundo_menu_selecao:
            self.rect_menu_selecao = self.fundo_menu_selecao.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
        else:
            print("[AVISO] Imagem MENU_INFO não encontrada. O menu de informações do item não será exibido.")
            self.rect_menu_selecao = pygame.Rect(0, 0, 400, 300) # Fallback rect
            self.fundo_menu_selecao = pygame.Surface(self.rect_menu_selecao.size)
            self.fundo_menu_selecao.fill(PRETO) # Fallback color

        # Botão de fechar para o menu de informações do item (reutiliza a imagem existente)
        self.botao_fechar_menu_info = self.gerenciador_recursos.obter_imagem(INV_BOTAO_FECHAR)
        if self.botao_fechar_menu_info and self.rect_menu_selecao:
            self.rect_botao_fechar_menu_selecao_ingrediente = self.botao_fechar_menu_info.get_rect(topright=(self.rect_menu_selecao.right + self.botao_fechar_menu_info.get_width()-1, self.rect_menu_selecao.top + 10))
        else:
            print("[AVISO] Imagem INV_BOTAO_FECHAR não encontrada para o menu de informações do item.")
            self.rect_botao_fechar_menu_selecao_ingrediente = pygame.Rect(0,0,0,0) # Fallback rect

        # Botão "Usar" para o menu de informações do item
        self.botao_usar_item = self.gerenciador_recursos.obter_imagem(INV_BOTAO_USAR) # Assumindo que esta imagem existe
        if self.botao_usar_item and self.rect_menu_selecao:
            self.rect_botao_usar_item = self.botao_usar_item.get_rect(center=(self.rect_menu_selecao.centerx, self.rect_menu_selecao.bottom))
        else:
            print("[AVISO] Imagem INV_BOTAO_USAR não encontrada. O botão 'Usar' não será exibido.")
            # Fallback: criar uma superfície simples para o botão
            self.botao_usar_item = pygame.Surface((100, 40))
            self.botao_usar_item.fill(AZUL)
            self.rect_botao_usar_item = self.botao_usar_item.get_rect(center=(self.rect_menu_selecao.centerx, self.rect_menu_selecao.bottom - 30))


        # Carrega as fontes com os tamanhos definidos
        # Certifique-se de que GerenciadorDeRecursos.obter_fonte pode aceitar um argumento 'size'
        self.fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
        self.fonte_texto = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
        self.fonte_texto_hover = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
        self.fonte_raridade = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_HACHI_MARU_TEXTO)

        altura_fonte_maior = self.fonte_texto_hover.get_linesize()
        self.altura_linha_item = altura_fonte_maior + 10


        # Botão de fechar principal do inventário
        self.botao_fechar = self.gerenciador_recursos.obter_imagem(INV_BOTAO_FECHAR)
        self.rect_botao_fechar = self.botao_fechar.get_rect(topright=(self.x_painel_central + self.painel_de_fundo.get_width(), 97))

        # Botões laterais e seus retângulos
        self.botoes_laterais = {}
        y_inicial_botoes = 94 # Posição Y inicial para os botões laterais
        x_inicial_botoes = self.x_painel_central # Posição X inicial para os botões laterais

        # Botão Cozinhar
        img_cozinhar_normal = self.gerenciador_recursos.obter_imagem(ABA_LATERAL_COZINHAR)
        img_cozinhar_ativo = self.gerenciador_recursos.obter_imagem(ABA_LATERAL_COZINHAR_ATIVO)
        rect_cozinhar = img_cozinhar_normal.get_rect(topleft=(x_inicial_botoes, y_inicial_botoes))
        self.botoes_laterais['cozinhar'] = {
            'normal': img_cozinhar_normal,
            'ativo': img_cozinhar_ativo,
            'rect': rect_cozinhar
        }

        # Botão Receitas
        img_receitas_normal = self.gerenciador_recursos.obter_imagem(ABA_LATERAL_RECEITAS)
        img_receitas_ativo = self.gerenciador_recursos.obter_imagem(ABA_LATERAL_RECEITAS_ATIVO)
        rect_receitas = img_receitas_normal.get_rect(topleft=(x_inicial_botoes, y_inicial_botoes + 83)) # Ajuste o espaçamento
        self.botoes_laterais['receitas'] = {
            'normal': img_receitas_normal,
            'ativo': img_receitas_ativo,
            'rect': rect_receitas
        }

        self.img_slot_vazio = self.gerenciador_recursos.obter_imagem(SLOT_INGREDIENTE_VAZIO)
        self.img_botao_cozinhar_ativo = self.gerenciador_recursos.obter_imagem(BOTAO_COZINHAR_ATIVO)
        self.img_botao_cozinhar_inativo = self.gerenciador_recursos.obter_imagem(BOTAO_COZINHAR_INATIVO)


        # Carrega os dados do inventário e do jogador
        self._carregar_dados_inventario()

        self._carregar_receitas_conhecidas()



    def _carregar_dados_inventario(self):
        """
        Carrega os dados do inventário e do jogador do banco de dados.
        Atualiza também os dados de vida e energia do jogador a partir da entidade do jogador.
        """
        if not self.entidades.jogador or not self.entidades.progresso_do_jogo:
            print("[ERRO] Jogador ou progresso do jogo não disponíveis para carregar inventário.")
            return

        self.mochila = self.entidades.jogador.mochila

        # Filtra o inventário em listas separadas
        # Consumíveis agora inclui 'con' e 'ncn' para permitir filtragem
        self.lista_ingredientes = [item for item in self.mochila.itens if item.tipo in ['con', 'ncn'] and not item.item_de_missao]

        # Ordena as listas por nome para facilitar a visualização
        self.lista_ingredientes.sort(key=lambda item: item.nome)



    def _carregar_receitas_conhecidas(self):
        """
        Carrega as receitas conhecidas do banco de dados.
        """
        receitas_conhecidas = self.banco_de_dados.buscar_livro_de_receitas(self.entidades.jogador.identificador)

        if not receitas_conhecidas:
            return # Sai se o jogador não conhece nenhuma receita

        self.receitas_conhecidas: list[Receita] = []
        for receita in receitas_conhecidas:

            efeitos = self.banco_de_dados.buscar_efeitos_por_item(receita.identificador_consumivel)

            ingredientes = self.banco_de_dados.buscar_ingredientes_da_receita(receita.identificador_receita)

            self.receitas_conhecidas.append(Receita(
                identificador_receita=receita.identificador_receita,
                identificador_produto=receita.identificador_consumivel,
                nome_produto=receita.nome,
                efeitos=efeitos,
                ingredientes=ingredientes
            ))

        # Filtra a lista, mantendo apenas as receitas cujo nome do produto NÃO é 'Frankenprato'
        self.receitas_conhecidas = [receita for receita in self.receitas_conhecidas if receita.nome_produto != 'Frankenprato']



    def processar_eventos(self, evento):
        """
        Processa eventos específicos da tela de inventário.
        """
        super().processar_eventos(evento) # Permite eventos base (ex: ESC para sair)

        # Se o menu de seleção estiver aberto, ele tem prioridade sobre todos os outros eventos
        if self.exibindo_menu_ingredientes:
            
            # Calcula o retângulo do menu para verificar colisões
            rect_viewport = self.rect_menu_selecao.inflate(0, -30)

            # --- Lógica de Rolagem (MOUSEWHEEL) ---
            if evento.type == pygame.MOUSEWHEEL:
                mouse_pos = pygame.mouse.get_pos()
                # O scroll só funciona se o mouse estiver sobre o menu
                if self.rect_menu_selecao.collidepoint(mouse_pos):
                    max_itens_visiveis = rect_viewport.height // self.altura_linha_item
                    max_offset = max(0, (len(self.lista_ingredientes_disponiveis) - max_itens_visiveis) * self.altura_linha_item)
                    self.scroll_menu_ingredientes = self._aplicar_scroll(self.scroll_menu_ingredientes, evento.y, max_offset)
                return # Finaliza o processamento de evento

            # --- Lógica de Clique (MOUSEBUTTONDOWN) ---
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.rect_botao_fechar_menu_selecao_ingrediente and self.rect_botao_fechar_menu_selecao_ingrediente.collidepoint(evento.pos):
                    self.exibindo_menu_ingredientes = False
                    self.slot_ativo_para_selecao = None
                    return

                item_clicado = None
                
                # Verifica se o clique foi DENTRO da área da lista (viewport)
                if rect_viewport.collidepoint(evento.pos):
                    y_coluna_inicial = rect_viewport.y
                    
                    for i, item in enumerate(self.lista_ingredientes_disponiveis):
                        y_item_top = y_coluna_inicial + (i * self.altura_linha_item) - self.scroll_menu_ingredientes
                        rect_item = pygame.Rect(rect_viewport.x, y_item_top, rect_viewport.width, self.altura_linha_item)

                        if rect_item.collidepoint(evento.pos):
                            item_clicado = item
                            break # Encontrou o item, pode parar o loop
                
                # Se um item foi clicado, preenche o slot e fecha o menu
                if item_clicado:
                    if self.slot_ativo_para_selecao == 1:
                        self.slot1_ingrediente = item_clicado
                        self.imagem_ingrediente_1 = self.gerenciador_recursos.obter_imagem(item_clicado.nome)
                        if not self.imagem_ingrediente_1:
                            self.imagem_ingrediente_1 = self.gerenciador_recursos.obter_imagem(ITEM_GENERICO) # Fallback para uma imagem padrão
                    elif self.slot_ativo_para_selecao == 2:
                        self.slot2_ingrediente = item_clicado
                        self.imagem_ingrediente_2 = self.gerenciador_recursos.obter_imagem(item_clicado.nome)
                        if not self.imagem_ingrediente_2:
                            self.imagem_ingrediente_2 = self.gerenciador_recursos.obter_imagem(ITEM_GENERICO) # Fallback para uma imagem padrão
                
                # Fecha o menu (seja por selecionar um item ou clicar fora)
                self.exibindo_menu_ingredientes = False
                self.slot_ativo_para_selecao = None
            
            return # Impede que eventos do menu afetem a tela de trás


        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Clique esquerdo
                # Lógica para o botão de fechar
                if self.rect_botao_fechar.collidepoint(evento.pos):
                    #self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MAPA) # Ou a tela anterior, se houver um histórico
                    self.gerenciador_telas.tela_atual.menu_cozinha = None
                    self.gerenciador_telas.tela_atual.menu_cozinha_ativo = False
                    return

                # Lógica para os botões laterais (abas)
                for nome_da_aba, botao in self.botoes_laterais.items():
                    if botao['rect'].collidepoint(evento.pos):
                        self.aba_atual = nome_da_aba
                        print(f"[DEBUG] Aba alterada para: {self.aba_atual}")
                        self.item_em_foco = None # Limpa o item em foco ao mudar de aba
                        return
                

                # Lógica para selecionar item (se houver)
                # Esta lógica só deve ser ativada se uma aba de itens estiver ativa
                if self.aba_atual == 'receitas':
                    # Calcula o retângulo do painel esquerdo (exatamente como na rolagem)
                    largura_total_visivel = self.painel_de_fundo.get_width() - 77 - 49
                    largura_painel_receita = self.painel_receitas.get_width()
                    altura_painel_receita = self.painel_receitas.get_height()
                    espacamento = 20
                    x_inicial = self.x_painel_central + 77 + (largura_total_visivel - 2 * largura_painel_receita - espacamento) // 2
                    y_inicial = self.y_painel_central + (self.painel_de_fundo.get_height() - altura_painel_receita) // 2
                    rect_painel_esquerdo = pygame.Rect(x_inicial, y_inicial, largura_painel_receita, altura_painel_receita)

                    # Verifica se o clique foi dentro do painel esquerdo
                    if rect_painel_esquerdo.collidepoint(evento.pos):
                        # Posição inicial da coluna de texto
                        x_coluna = rect_painel_esquerdo.x + 10
                        y_coluna_inicial = rect_painel_esquerdo.y + 10

                        # Itera sobre TODAS as receitas para encontrar a clicada
                        for i, receita in enumerate(self.receitas_conhecidas):
                            # Calcula a posição Y do item na tela (mesma fórmula do desenho)
                            y_item_top = y_coluna_inicial + (i * self.altura_linha_item) - self.deslocamento_de_rolagem_receitas
                            
                            # Cria o retângulo de colisão para este item
                            rect_item = pygame.Rect(x_coluna, y_item_top, rect_painel_esquerdo.width - 20, self.altura_linha_item)

                            # Verifica a colisão APENAS se o item estiver visível dentro do painel
                            if rect_painel_esquerdo.colliderect(rect_item) and rect_item.collidepoint(evento.pos):
                                self.receita_selecionada = receita
                                self.imagem_receita_selecionada = self.gerenciador_recursos.obter_imagem(receita.nome_produto)
                                if not self.imagem_receita_selecionada:
                                    self.imagem_receita_selecionada = self.gerenciador_recursos.obter_imagem(ITEM_GENERICO)
                                self.scroll_detalhes_receita = 0 # Reseta a rolagem do painel direito
                                print(f"[DEBUG] Receita selecionada: {receita.nome_produto}.")
                                return # Sai do loop de eventos após o clique
                        
                if self.aba_atual == 'cozinhar':

                    if self.rect_slot1 and self.rect_slot1.collidepoint(evento.pos):
                        print("[DEBUG] Clicou no slot 1. Abrindo menu de seleção.")
                        
                        # --- LÓGICA DE FILTRAGEM ---
                        self.lista_ingredientes_disponiveis = []
                        item_no_slot2 = self.slot2_ingrediente
                        
                        for item_no_inventario in self.lista_ingredientes:
                            # Se o item do inventário é o mesmo que está no outro slot...
                            if item_no_slot2 and item_no_inventario.identificador_item == item_no_slot2.identificador_item:
                                # ...só o adiciona na lista se a quantidade for maior que 1.
                                if item_no_inventario.quantidade > 1:
                                    self.lista_ingredientes_disponiveis.append(item_no_inventario)
                            else:
                                # Se for um item diferente, pode adicionar.
                                self.lista_ingredientes_disponiveis.append(item_no_inventario)

                        self.exibindo_menu_ingredientes = True
                        self.slot_ativo_para_selecao = 1
                        self.scroll_menu_ingredientes = 0
                    
                    elif self.rect_slot2 and self.rect_slot2.collidepoint(evento.pos):
                        print("[DEBUG] Clicou no slot 2. Abrindo menu de seleção.")

                        # --- LÓGICA DE FILTRAGEM (para o slot 2) ---
                        self.lista_ingredientes_disponiveis = []
                        item_no_slot1 = self.slot1_ingrediente

                        for item_no_inventario in self.lista_ingredientes:
                            if item_no_slot1 and item_no_inventario.identificador_item == item_no_slot1.identificador_item:
                                if item_no_inventario.quantidade > 1:
                                    self.lista_ingredientes_disponiveis.append(item_no_inventario)
                            else:
                                self.lista_ingredientes_disponiveis.append(item_no_inventario)

                        self.exibindo_menu_ingredientes = True
                        self.slot_ativo_para_selecao = 2
                        self.scroll_menu_ingredientes = 0 # Reseta a rolagem do menu

                    elif self.rect_botao_cozinhar and self.rect_botao_cozinhar.collidepoint(evento.pos):
                        if self.slot1_ingrediente or self.slot2_ingrediente:
                            print("[DEBUG] Clicou em Cozinhar!")
                            self._executar_cozimento()
                        else:
                            print("[DEBUG] Faltam ingredientes para cozinhar.")
                            # (Opcional: tocar um som de "erro")
        
        elif evento.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            
            # Só processa a rolagem se a aba de receitas estiver ativa
            if self.aba_atual == 'receitas':
                # --- Lógica para calcular a posição dos painéis ---
                largura_total_visivel = self.painel_de_fundo.get_width() - 77 - 49
                largura_painel_receita = self.painel_receitas.get_width()
                altura_painel_receita = self.painel_receitas.get_height()
                espacamento = 20
                x_inicial = self.x_painel_central + 77 + (largura_total_visivel - 2 * largura_painel_receita - espacamento) // 2
                y_inicial = self.y_painel_central + (self.painel_de_fundo.get_height() - altura_painel_receita) // 2

                rect_painel_esquerdo = pygame.Rect(x_inicial, y_inicial, largura_painel_receita, altura_painel_receita)
                rect_painel_direito = pygame.Rect(x_inicial + largura_painel_receita + espacamento, y_inicial, largura_painel_receita, altura_painel_receita)

                # --- Verifica em qual painel o mouse está ---
                if rect_painel_esquerdo.collidepoint(mouse_pos):
                    # ROLAGEM DO PAINEL ESQUERDO (LISTA DE RECEITAS)
                    max_itens_visiveis = altura_painel_receita // self.altura_linha_item
                    max_offset_lista = max(0, (len(self.receitas_conhecidas) - max_itens_visiveis) * self.altura_linha_item)
                    self.deslocamento_de_rolagem_receitas = self._aplicar_scroll(self.deslocamento_de_rolagem_receitas, evento.y, max_offset_lista)

                elif rect_painel_direito.collidepoint(mouse_pos) and self.receita_selecionada:
                    # ROLAGEM DO PAINEL DIREITO (DETALHES DA RECEITA)
                    max_offset_detalhes = max(0, self.altura_conteudo_detalhes - rect_painel_direito.height)
                    self.scroll_detalhes_receita = self._aplicar_scroll(self.scroll_detalhes_receita, evento.y, max_offset_detalhes)



    def _esta_sobre_area_painel_central(self, mouse_pos):
        """Verifica se a posição do mouse está dentro da área do painel central de itens."""
        # Ajusta o retângulo para a área onde os itens são realmente listados, abaixo dos filtros
        rect_painel_central = pygame.Rect(self.pos_lista_itens[0], self.pos_lista_itens[1], self.largura_painel_central, self.altura_painel_central - 40)
        return rect_painel_central.collidepoint(mouse_pos)



    def _aplicar_scroll(self, current_offset, scroll_delta, max_offset):
        """Aplica o scroll a um offset específico, respeitando os limites."""
        incremento = self.altura_linha_item 
        new_offset = current_offset - (scroll_delta * incremento)
        
        return max(0, min(new_offset, max_offset))



    def _obter_scroll_offset_ativo(self):
        """Retorna o offset de scroll da aba ativa."""
        if self.aba_atual == 'receitas':
            return self.deslocamento_de_rolagem_receitas
        return 0



    def atualizar(self, dt):
        """
        Atualiza a lógica interna da tela de cozinha.
        Recarrega os dados do inventário e do jogador para garantir que estejam sempre atualizados.
        """
        self._carregar_dados_inventario() # Garante que HP/PE e itens estejam atualizados

        # --- NOVO: Lógica do timer da mensagem ---
        if self.tempo_exibicao_mensagem > 0:
            self.tempo_exibicao_mensagem -= dt # Subtrai o tempo passado
            if self.tempo_exibicao_mensagem <= 0:
                self.mensagem_resultado = None # Esconde a mensagem quando o tempo acaba



    def desenhar(self, tela):
        """
        Desenha os elementos da tela de inventário.
        """
        # Posiciona o fundo_inventario em (144, 88)
        tela.blit(self.painel_de_fundo, (self.x_painel_central, self.y_painel_central))

        mouse_pos = pygame.mouse.get_pos()
        self.item_em_foco = None # Reseta o item em foco a cada frame

        # Desenha o botão de fechar
        tela.blit(self.botao_fechar, self.rect_botao_fechar)

        # Desenha os botões laterais
        for tab_name, button_data in self.botoes_laterais.items():
            image_to_draw = button_data['ativo'] if self.aba_atual == tab_name else button_data['normal']
            tela.blit(image_to_draw, button_data['rect'])

        # Desenha o conteúdo da aba ativa
        if self.aba_atual == 'cozinhar':
            self._desenhar_aba_cozinhar(tela, mouse_pos)
        elif self.aba_atual == 'receitas':
            self._desenhar_aba_receitas(tela, mouse_pos)



    def _desenhar_aba_cozinhar(self, tela, mouse_pos):
        """
        Desenha a aba de cozinhar, com os slots de ingredientes e o botão de cozinhar.
        """
        # Desenha o painel de fundo da aba
        tela.blit(self.painel_de_fundo, (self.x_painel_central, self.y_painel_central))

        # --- POSICIONAMENTO DOS ELEMENTOS ---
        painel_rect = self.painel_de_fundo.get_rect(topleft=(self.x_painel_central, self.y_painel_central))
        espacamento = 20
        largura_total_visivel = self.painel_de_fundo.get_width() - 77 - 49  # Largura visível do painel de fundo

        # Slots de ingredientes (superiores)
        largura_total_slots = self.img_slot_vazio.get_width() * 2 + espacamento
        x_inicial_slots = painel_rect.centerx - (largura_total_slots / 2)
        y_slots = painel_rect.y + 80 # Posição vertical dos slots

        self.rect_slot1 = self.img_slot_vazio.get_rect(topleft=(x_inicial_slots, y_slots))
        self.rect_slot2 = self.img_slot_vazio.get_rect(topleft=(x_inicial_slots + self.img_slot_vazio.get_width() + espacamento, y_slots))

        # Botão Cozinhar (inferior)
        self.rect_botao_cozinhar = self.img_botao_cozinhar_ativo.get_rect(centerx=painel_rect.centerx, bottom=painel_rect.bottom - 80)

        # --- DESENHO DOS SLOTS ---
        # Slot 1
        if self.slot1_ingrediente and self.imagem_ingrediente_1:
            tela.blit(self.imagem_ingrediente_1, self.rect_slot1)
        else:
            tela.blit(self.img_slot_vazio, self.rect_slot1)

        # Slot 2
        if self.slot2_ingrediente and self.imagem_ingrediente_2:
            tela.blit(self.imagem_ingrediente_2, self.rect_slot2)
        else:
            tela.blit(self.img_slot_vazio, self.rect_slot2)

        # --- DESENHO DO BOTÃO COZINHAR ---
        if self.slot1_ingrediente or self.slot2_ingrediente:
            tela.blit(self.img_botao_cozinhar_ativo, self.rect_botao_cozinhar)
        else:
            tela.blit(self.img_botao_cozinhar_inativo, self.rect_botao_cozinhar)

        # --- NOVO: DESENHO DA MENSAGEM DE RESULTADO ---
        if self.mensagem_resultado:
            # Posição do texto, abaixo do botão de cozinhar
            pos_y_mensagem = self.rect_botao_cozinhar.bottom + 20

            # Cor do texto baseada no sucesso ou falha
            cor_texto = AMARELO_CLARO if "Frankenprato" in self.mensagem_resultado else VERDE_CLARO

            mensagem = self.quebrar_texto(self.mensagem_resultado, self.fonte_texto, largura_total_visivel - 15)

            for i, linha in enumerate(mensagem):
                # Calcula a posição Y para cada linha de texto
                pos_y_mensagem += i * (self.fonte_texto.get_linesize() + 5)

                self._desenhar_texto_com_borda(
                    tela,
                    linha,
                    self.fonte_texto,
                    cor_texto,
                    PRETO,
                    1,
                    (self.rect_botao_cozinhar.centerx, pos_y_mensagem),
                    align='center'
                )

        # --- DESENHO DO MENU DE SELEÇÃO (SE ESTIVER ATIVO) ---
        if self.exibindo_menu_ingredientes:
            # Cria uma superfície semi-transparente preta para escurecer o fundo
            s = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            tela.blit(s, (0, 0))
            
            # Chama a nova função de desenho da lista
            self._desenhar_menu_selecao_ingredientes(tela, mouse_pos)



    def _desenhar_aba_receitas(self, tela, mouse_pos):
        """
        Desenha a aba de receitas, onde o jogador pode ver as receitas conhecidas.
        """
        # Desenha o painel de fundo
        tela.blit(self.painel_de_fundo, (self.x_painel_central, self.y_painel_central))

        # Calcula as posições para centralizar os painéis de receitas
        largura_total_visivel = self.painel_de_fundo.get_width() - 77 - 49  # Largura visível do painel de fundo
        largura_painel_receita = self.painel_receitas.get_width()
        espacamento = 20  # Espaçamento entre os painéis de receitas

        # Calcula a posição inicial para centralizar os dois painéis
        x_inicial = self.x_painel_central + 77 + (largura_total_visivel - 2 * largura_painel_receita - espacamento) // 2
        y_inicial = self.y_painel_central + (self.painel_de_fundo.get_height() - largura_painel_receita) // 2

        # Desenha o painel da esquerda para a lista
        tela.blit(self.painel_receitas, (x_inicial, y_inicial))
        
        # Define a posição do painel da direita
        x_painel_direito = x_inicial + largura_painel_receita + espacamento
        y_painel_direito = y_inicial
        tela.blit(self.painel_receitas, (x_painel_direito, y_painel_direito))


        # Título da aba
        titulo = "Receitas"
        self._desenhar_texto_com_borda(
            tela,
            titulo,
            self.fonte_titulo,
            VERDE_CLARO,
            PRETO,
            1,
            (self.x_painel_central + self.largura_painel_central // 2, self.y_painel_central + 20),
            align='center'
        )

        # Desenha as receitas conhecidas
        # Restringe a área de desenho para a largura do painel de receitas da esquerda
        largura_painel_receita
        
        # Crie o rect do painel esquerdo
        rect_painel_esquerdo = pygame.Rect(x_inicial, y_inicial, largura_painel_receita, self.painel_receitas.get_height())
        
        # Desenha as receitas conhecidas
        self._desenhar_receitas_conhecidas(tela, mouse_pos, rect_painel_esquerdo)

        if self.receita_selecionada:
            rect_painel_direito = pygame.Rect(x_painel_direito, y_painel_direito, largura_painel_receita, self.painel_receitas.get_height())
            self._desenhar_detalhes_da_receita(tela, self.receita_selecionada, rect_painel_direito)



    def _desenhar_receitas_conhecidas(self, tela, mouse_pos, rect_painel_esquerdo):
        """Desenha a lista de receitas conhecidas (versão corrigida e robusta)."""
        # --- Coordenadas agora são calculadas aqui dentro para garantir sincronia ---
        x_coluna = rect_painel_esquerdo.x + 10
        y_coluna_inicial = rect_painel_esquerdo.y + 10
        largura_maxima_texto = rect_painel_esquerdo.width - 20

        tela.set_clip(rect_painel_esquerdo)

        for i, receita in enumerate(self.receitas_conhecidas):

            y_item_top = y_coluna_inicial + (i * self.altura_linha_item) - self.deslocamento_de_rolagem_receitas

            if y_item_top + self.altura_linha_item > rect_painel_esquerdo.top and y_item_top < rect_painel_esquerdo.bottom:
                rect_item = pygame.Rect(x_coluna, y_item_top, largura_maxima_texto, self.altura_linha_item)
                mouse_sobre = rect_item.collidepoint(mouse_pos)

                current_font = self.fonte_texto_hover if mouse_sobre else self.fonte_texto
                
                texto_limitado = self.renderizar_texto_limitado(current_font, receita.nome_produto, BRANCO_CLARO, largura_maxima_texto)
                texto_renderizado = current_font.render(texto_limitado, True, BRANCO_CLARO)
                
                text_rect = texto_renderizado.get_rect()
                text_y_centered = y_item_top + (self.altura_linha_item - text_rect.height) // 2

                self._desenhar_texto_com_borda(
                    tela, texto_limitado, current_font, BRANCO_CLARO, PRETO, 1,
                    (x_coluna, text_y_centered), align='left'
                )
        
        tela.set_clip(None)
        


    def _desenhar_detalhes_da_receita(self, tela, receita_selecionada: Receita, rect_painel):
        """
        Desenha os detalhes de uma Receita (produto, efeitos e ingredientes)
        dentro do painel fornecido, usando o novo dataclass.
        """
        painel = rect_painel.inflate(0, -30)
        tela.set_clip(painel)

        # Posições base, considerando o deslocamento da rolagem
        x_base = rect_painel.x + 15
        # O conteúdo começa "acima" e a rolagem o move para baixo
        y_inicial_conteudo = painel.y - self.scroll_detalhes_receita
        y_atual = y_inicial_conteudo + 15

        # 1. Nome do Produto (com quebra de linha)
        # Primeiro, pegue a lista de linhas
        largura_max_nome = painel.width - 30 # Deixa uma margem de 15px de cada lado
        nome_produto = self.quebrar_texto(receita_selecionada.nome_produto, self.fonte_titulo, largura_max_nome)

        for linha in nome_produto:
            self._desenhar_texto_com_borda(
                tela,
                linha,  # <--- Desenha uma linha por vez
                self.fonte_titulo, BRANCO, PRETO, 1,
                (painel.centerx, y_atual), 
                align='center'
            )
            y_atual += self.fonte_titulo.get_linesize() # <--- Move o Y para a próxima linha


        # 2. Imagem do Produto (a chave é o nome)

        if self.imagem_receita_selecionada:
            img_rect = self.imagem_receita_selecionada.get_rect(centerx=rect_painel.centerx, top=y_atual)
            tela.blit(self.imagem_receita_selecionada, img_rect)
            y_atual += self.imagem_receita_selecionada.get_height() + 15

        # 3. Efeitos
        if receita_selecionada.efeitos:
            y_atual += 25
            
            # Carrega a imagem de fundo para os efeitos
            img_fundo_efeito = self.gerenciador_recursos.obter_imagem(ETIQUETA)

            for efeito in receita_selecionada.efeitos:
                # Monta o texto do efeito
                if efeito.efeito_valor:
                    texto_efeito = f"{efeito.efeito_nome} +{efeito.efeito_valor}"
                else:
                    texto_efeito = f"{efeito.efeito_nome}"

                # --- LÓGICA DE DESENHO EM CAMADAS ---
                if img_fundo_efeito:
                    # Pega o retângulo da imagem para saber onde posicioná-la e centralizar o texto
                    efeito_rect = img_fundo_efeito.get_rect(center=(rect_painel.x + rect_painel.width // 2, y_atual))

                    # 1. Desenha a imagem de fundo primeiro
                    tela.blit(img_fundo_efeito, efeito_rect)

                    # 2. Desenha o texto do efeito centralizado sobre a imagem
                    self._desenhar_texto_com_borda(
                        tela,
                        texto_efeito,
                        self.fonte_texto,
                        BRANCO_CLARO, PRETO, 1,
                        (efeito_rect.centerx, efeito_rect.centery -6), # <--- Posição central da imagem
                        align='center'      # <--- Alinhamento central
                    )
                    
                    # Move o cursor Y para o próximo efeito, com base na altura da imagem
                    y_atual += efeito_rect.height + 5 # 5 pixels de espaçamento

                else:
                    # Fallback: se a imagem não for encontrada, desenha como texto simples
                    self._desenhar_texto_com_borda(tela, texto_efeito, self.fonte_texto, VERDE_CLARO, PRETO, 1, (x_base + 10, y_atual), align='left')
                    y_atual += 25
        y_atual += 10

        # 4. Ingredientes (com quebra de texto)
        self._desenhar_texto_com_borda(tela, "Ingredientes:", self.fonte_texto, BRANCO, PRETO, 1, (x_base, y_atual), align='left')
        y_atual += 25

        if receita_selecionada.ingredientes:
            # Define a largura máxima que o texto do ingrediente pode ocupar
            largura_max_ingrediente = rect_painel.width - (x_base - rect_painel.x) - 20 # Largura do painel - margens

            for ingrediente in receita_selecionada.ingredientes:
                # Monta a string completa do ingrediente
                nome_ingrediente = ingrediente.nome_ingrediente
                id_ingrediente = ingrediente.identificador_ingrediente
                
                item_no_inventario = self.mochila.encontrar_item_por_id(id_ingrediente)
                qtd_possuida = item_no_inventario.quantidade if item_no_inventario else 0
                
                cor_texto = BRANCO_CLARO if qtd_possuida >= 1 else VERMELHO
                
                texto_completo = f"- {nome_ingrediente} ({qtd_possuida}/1)"
                
                # <--- APLICA A QUEBRA DE TEXTO ---
                # Quebra a string completa em uma lista de linhas
                linhas_ingrediente = self.quebrar_texto(texto_completo, self.fonte_texto, largura_max_ingrediente)
                
                # <--- DESENHA CADA LINHA SEPARADAMENTE ---
                # Itera sobre as linhas geradas e desenha uma por uma
                for linha in linhas_ingrediente:
                    self._desenhar_texto_com_borda(
                        tela, 
                        linha, # Desenha a linha atual
                        self.fonte_texto, 
                        cor_texto, 
                        PRETO, 1,
                        (x_base + 10, y_atual), 
                        align='left'
                    )
                    # Move o Y para a próxima linha, usando o tamanho da fonte
                    y_atual += self.fonte_texto.get_linesize()
                
                # Adiciona um pequeno espaço entre os ingredientes, se houver mais de uma linha
                if len(linhas_ingrediente) > 1:
                    y_atual += 5
        
        y_atual += 10 # Espaço extra após os ingredientes

        self.altura_conteudo_detalhes = y_atual - y_inicial_conteudo
        
        tela.set_clip(None)



    def _desenhar_menu_selecao_ingredientes(self, tela, mouse_pos):
        """
        Desenha um menu rolável para o jogador escolher um ingrediente da mochila.
        """
        # Usa a imagem de fundo do menu de informações como painel
        rect_menu = self.fundo_menu_selecao.get_rect(center=tela.get_rect().center)
        tela.blit(self.fundo_menu_selecao, rect_menu)

        if self.botao_fechar_menu_info and self.rect_botao_fechar_menu_selecao_ingrediente:
            tela.blit(self.botao_fechar_menu_info, self.rect_botao_fechar_menu_selecao_ingrediente)


        # --- Lógica de Lista Rolável ---
        # Define a área interna do menu para a lista (viewport)
        rect_viewport = rect_menu.inflate(0, -30) # Reduz o retângulo para criar margens
        tela.set_clip(rect_viewport)

        x_coluna = rect_viewport.x
        y_coluna_inicial = rect_viewport.y
        largura_texto = rect_viewport.width

        for i, item in enumerate(self.lista_ingredientes_disponiveis):
            # Calcula a posição Y do item, deslocada pela rolagem
            y_item_top = y_coluna_inicial + (i * self.altura_linha_item) - self.scroll_menu_ingredientes

            # Desenha apenas os itens visíveis
            if y_item_top + self.altura_linha_item > rect_viewport.top and y_item_top < rect_viewport.bottom:
                rect_item = pygame.Rect(x_coluna, y_item_top, largura_texto, self.altura_linha_item)
                mouse_sobre = rect_item.collidepoint(mouse_pos)

                fonte = self.fonte_texto_hover if mouse_sobre else self.fonte_texto
                cor = BRANCO if mouse_sobre else BRANCO_CLARO
                
                texto_item = f"{item.nome} x{item.quantidade}"
                
                self._desenhar_texto_com_borda(tela, texto_item, fonte, cor, PRETO, 1, (rect_item.x + 10, rect_item.centery - fonte.get_height() // 2), 'left')
        
        # Limpa a área de recorte
        tela.set_clip(None)



    def _executar_cozimento(self):
        """
        Executa o processo de cozimento, verificando os ingredientes e atualizando o inventário.
        """

        resultado = self.banco_de_dados.tentar_cozinhar_item(self.entidades.jogador.id_mochila, self.slot1_ingrediente.identificador_item if self.slot1_ingrediente else None, self.slot2_ingrediente.identificador_item if self.slot2_ingrediente else None)

        print(resultado['mensagem'])

        self.slot1_ingrediente = None
        self.slot2_ingrediente = None
        self.imagem_ingrediente_1 = None
        self.imagem_ingrediente_2 = None

        if resultado['sucesso']:
            self.banco_de_dados.aprender_receita(resultado['receita'], self.entidades.jogador.identificador)
            self.gerenciador_recursos.obter_som(SOM_COMPRA_SUCESSO).play()
            self._carregar_receitas_conhecidas()

            self.mensagem_resultado = f"Você obteve {resultado['item_produzido']['nome']}!"
        else:
            self.banco_de_dados.adicionar_item_ao_inventario(
                self.entidades.jogador.id_mochila,
                'con067', # Frankenprato
            )
            self.gerenciador_recursos.obter_som(SOM_COMPRA_FALHA).play()

            self.mensagem_resultado = "Cozimento falhou! Você obteve um Frankenprato."

        self.tempo_exibicao_mensagem = self.DURACAO_MENSAGEM # Inicia o timer

        self.entidades.jogador.mochila = self.banco_de_dados.carregar_mochila_do_jogador(self.entidades.jogador.identificador, self.entidades.progresso_do_jogo.identificador_progresso)


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
