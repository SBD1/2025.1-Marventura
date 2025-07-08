# ARQUIVO CORRIGIDO E COMPLETO: jogo/telas/tela_inventario.py

import pygame
from .tela_modelo import TelaModelo
from utilidades.constantes import *

class TelaInventario(TelaModelo):
    """
    Representa a interface do inventário do jogador, com abas para status,
    equipamentos e itens.
    """
    def __init__(self, gerenciador_telas, gerenciador_recursos, db_manager, jogador_id,
                 dados_retorno_ilha, dados_retorno_area, ponto_retorno_jogador, snapshot_fundo=None):
        super().__init__(gerenciador_telas, gerenciador_recursos)
        # --- Atributos essenciais ---
        self.db_manager = db_manager
        self.jogador_id = jogador_id
        self.dados_retorno_ilha = dados_retorno_ilha
        self.dados_retorno_area = dados_retorno_area
        self.ponto_retorno_jogador = ponto_retorno_jogador
        self.snapshot_fundo = snapshot_fundo  # Armazena a imagem de fundo que veio da tela de jogo
        
        # --- Estado da UI ---
        self.aba_ativa_index = 0
        self.item_selecionado = None
        self.indice_item_selecionado = -1
        self.scroll_offset = 0
        
        # --- Feedback de interface ---
        self.feedback_message = ""
        self.feedback_timer = 0
        self.feedback_duration = 3 # Segundos

        # --- NOVO: Estado do painel de informações do item ---
        self.showing_item_info = False
        self.item_details_to_show = None # Dicionário ou objeto com os detalhes do item

        # --- Carregamento e Configuração ---
        self._carregar_recursos()
        self._carregar_dados() # Já chama _resetar_selecao()
        self._definir_layout() 

        # --- Carregamento e Configuração ---
        self._carregar_recursos()
        self._carregar_dados() # Já chama _resetar_selecao()
        self._definir_layout()

    def _carregar_recursos(self):
        """Carrega todas as fontes e imagens da UI de uma vez."""
        self.fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_BOTAO)
        self.fonte_stats = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO)
        self.fonte_texto = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO)
        self.fonte_botao = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_BOTAO) # Adicionado se estava faltando

        dados_jogador_temp = self.db_manager.buscar_jogador(self.jogador_id)
        self.img_jogador_sprite = self.gerenciador_recursos.obter_imagem(f'{dados_jogador_temp.nome.strip()}_inventario')
        
        self.imagens_ui = {
            'painel_fundo': self.gerenciador_recursos.obter_imagem('inv_painel_fundo'),
            'botao_fechar': self.gerenciador_recursos.obter_imagem('inv_botao_fechar'),
            'label_equip': self.gerenciador_recursos.obter_imagem('inv_label_equip'),
            'label_estat': self.gerenciador_recursos.obter_imagem('inv_label_estat'),
            'fundo_personagem': self.gerenciador_recursos.obter_imagem('inv_fundo_personagem'),
            'inv_slot_item': self.gerenciador_recursos.obter_imagem('inv_slot_item'),
            'inv_nada_aqui': self.gerenciador_recursos.obter_imagem('inv_nada_aqui'),
            'inv_slot_arma_equipada': self.gerenciador_recursos.obter_imagem('inv_slot_arma_equipada'),
            # NOVO: Imagem padrão para itens se não encontrada
            'item_padrao': pygame.Surface((64, 64), pygame.SRCALPHA), # Um quadrado cinza transparente como fallback
        }
        # Preenche o item_padrao
        self.imagens_ui['item_padrao'].fill((100, 100, 100, 150))

        self.icones_abas = { i: self.gerenciador_recursos.obter_imagem(k) for i, k in enumerate(['inv_tab_status', 'inv_tab_arma', 'inv_tab_acessorio', 'inv_tab_consumivel', 'inv_tab_outros'])}
        self.icones_slots = {k: self.gerenciador_recursos.obter_imagem(f'inv_slot_{k}') for k in ['camisa', 'fruta', 'arma_especial']}
        self.imagens_itens = {}
        
    def _obter_imagem_item(self, item):
        """Obtém a imagem de um item, com cache para performance."""
        if item.identificador_item not in self.imagens_itens:
            # Tenta carregar a imagem do item usando o identificador
            try:
                self.imagens_itens[item.identificador_item] = self.gerenciador_recursos.obter_imagem(f'item_{item.identificador_item}')
            except:
                # Se não encontrar, usa uma imagem padrão (certifique-se de que 'item_padrao' exista ou crie uma Surface)
                self.imagens_itens[item.identificador_item] = pygame.Surface((64, 64), pygame.SRCALPHA) # Fallback simples
                self.imagens_itens[item.identificador_item].fill((100, 100, 100, 150)) # Cor cinza semi-transparente
                print(f"AVISO: Imagem para item '{item.identificador_item}' não encontrada. Usando fallback.")
        
        return self.imagens_itens[item.identificador_item]

    def _resetar_selecao(self):
        """Reseta a seleção de item para evitar bugs entre abas."""
        self.item_selecionado = None
        self.indice_item_selecionado = -1
        self.scroll_offset = 0

    def _carregar_dados(self):
        """Carrega e filtra os dados do inventário e do jogador."""
        inventario_completo = self.db_manager.buscar_inventario_jogador(self.jogador_id)
        self.dados_jogador = self.db_manager.buscar_jogador(self.jogador_id)
        # NOVO: Carregar item equipado do jogador
        self.arma_equipada = self.db_manager.buscar_arma_equipada(self.jogador_id) # Objeto (row) da arma equipada

        # Filtra o inventário em listas separadas
        self.lista_armas = [item for item in inventario_completo if item.tipo_item == 'arm']
        self.lista_acessorios = [item for item in inventario_completo if item.tipo_item == 'ace']
        self.lista_consumiveis = [item for item in inventario_completo if item.tipo_item == 'con']
        self.lista_outros = [item for item in inventario_completo if item.tipo_item in ['ncn', 'fru']]

        # Reinicia a seleção para evitar bugs
        self._resetar_selecao()

    def _definir_layout(self):
        """Define o retângulo principal do painel e os retângulos dos botões."""
        painel_img = self.imagens_ui.get('inv_painel_fundo')
        if painel_img:
            self.rect_painel = painel_img.get_rect(center=(LARGURA_TELA // 2 - 50, ALTURA_TELA // 2-50))
        else: 
            self.rect_painel = pygame.Rect(0, 0, 800, 500)
            self.rect_painel.center = (LARGURA_TELA // 2-50, ALTURA_TELA // 2-40)

        icone_fechar = self.imagens_ui.get('botao_fechar')
        if icone_fechar:
            pos_x_fechar = self.rect_painel.right - (icone_fechar.get_width() / 2) - 12
            pos_y_fechar = self.rect_painel.top + 125
            self.rect_botao_fechar = icone_fechar.get_rect(center=(pos_x_fechar, pos_y_fechar))
        else:
            self.rect_botao_fechar = pygame.Rect(0,0,0,0)

        self.rects_abas = []
        
        base_x_aba = self.rect_painel.left + 190
        base_y_aba = self.rect_painel.top + 132

        # Aba 0: Status
        if self.icones_abas.get(0):
            icone = self.icones_abas[0]
            pos_x = base_x_aba - (icone.get_width() / 2)
            pos_y = base_y_aba + (0 * 85) # Espaçamento original
            self.rects_abas.append(icone.get_rect(center=(pos_x, pos_y)))

        # Aba 1: Arma
        if self.icones_abas.get(1):
            icone = self.icones_abas[1]
            pos_x = base_x_aba - (icone.get_width() / 2)
            pos_y = base_y_aba + (1 * 86) # Espaçamento original
            self.rects_abas.append(icone.get_rect(center=(pos_x, pos_y - 3)))

        # Aba 2: Acessório
        if self.icones_abas.get(2):
            icone = self.icones_abas[2]
            pos_x = base_x_aba - (icone.get_width() / 2)
            pos_y = base_y_aba + (2 * 87) # Espaçamento original
            self.rects_abas.append(icone.get_rect(center=(pos_x, pos_y - 6)))

        # Aba 3: Consumível
        if self.icones_abas.get(3):
            icone = self.icones_abas[3]
            pos_x = base_x_aba - (icone.get_width() / 2)
            pos_y = base_y_aba + (3 * 88) # Espaçamento original
            self.rects_abas.append(icone.get_rect(center=(pos_x, pos_y - 12)))

        # Aba 4: Outros
        if self.icones_abas.get(4):
            icone = self.icones_abas[4]
            pos_x = base_x_aba - (icone.get_width() / 2)
            pos_y = base_y_aba + (4 * 89) # Espaçamento original
            self.rects_abas.append(icone.get_rect(center=(pos_x, pos_y - 24)))

        button_width = 180
        button_height = 40
        spacing = 10

        # Posição central para o grupo de botões
        center_x_group = self.rect_painel.centerx + 50 # Ajuste conforme necessário
        bottom_y_group = self.rect_painel.bottom - 60

        # Botão de Ação (Equipar/Usar/Desequipar) - à esquerda do centro do grupo
        self.rect_botao_acao = pygame.Rect(
            center_x_group - (button_width + 35 + spacing / 2),
            bottom_y_group,
            button_width,
            button_height
        )

        # Botão de Informação - à direita do centro do grupo
        self.rect_botao_informacao = pygame.Rect(
            center_x_group + 50 + spacing / 2,
            bottom_y_group,
            button_width,
            button_height
        )

        # NOVO: Painel de Informações do Item
        self.rect_info_panel = pygame.Rect(
            self.rect_painel.centerx - 200, # Ajuste a posição X e Y
            self.rect_painel.centery - 150,
            400, 300 # Largura e altura do painel
        )
        self.rect_info_panel_close_button = pygame.Rect(
            self.rect_info_panel.right - 30, self.rect_info_panel.top + 10, 20, 20
        )
        
    def handle_input(self, evento):
        """Gerencia cliques do mouse e teclas."""
        if evento.type == pygame.KEYDOWN and (evento.key == pygame.K_ESCAPE or evento.key == pygame.K_i):
            if self.showing_item_info: # Se o painel de info está aberto, ESC o fecha
                self.showing_item_info = False
                return
            self._voltar_ao_jogo()
            return

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos

            # NOVO: Se o painel de informações está aberto, só interage com ele
            if self.showing_item_info:
                if self.rect_info_panel_close_button.collidepoint(pos):
                    self.showing_item_info = False
                    return
                return # Consome o clique, não processa o resto

            # Lógica para fechar o inventário
            if self.rect_botao_fechar.collidepoint(pos):
                self._voltar_ao_jogo()
                return

            # Lógica para mudar de aba
            for i, rect_aba in enumerate(self.rects_abas):
                if rect_aba.collidepoint(pos):
                    self.aba_ativa_index = i
                    self._resetar_selecao() # Reseta a seleção ao mudar de aba
                    return
            
            # Lógica para cliques nos itens do inventário
            # ATENÇÃO: Esta chamada deve vir ANTES da lógica dos botões de ação/informação
            self._handle_item_click(pos)

            # NOVO: Lógica para clique no botão de ação
            if self.item_selecionado: # Só verifica se há um item selecionado
                if self.rect_botao_acao.collidepoint(pos):
                    self._executar_acao_item_selecionado()
                elif self.rect_botao_informacao.collidepoint(pos): # NOVO: Clique no botão Informação
                    self.showing_item_info = True
                    self.item_details_to_show = self.item_selecionado # Define o item para o painel de detalhes
                    print(f"Mostrando informações de: {self.item_details_to_show.nome_item.strip()}")
    
    def _executar_acao_item_selecionado(self):
        """Executa a ação (usar/equipar/desequipar) para o item atualmente selecionado."""
        if not self.item_selecionado:
            return

        if self.item_selecionado.tipo_item == 'con': # Consumível
            self._usar_consumivel(self.item_selecionado)
        elif self.item_selecionado.tipo_item == 'arm': # Arma
            # NOVO: Lógica Equipar/Desequipar para armas
            is_equipped = (self.arma_equipada and 
                           self.arma_equipada.identificador_item == self.item_selecionado.identificador_item)
            if is_equipped:
                self._desequipar_arma(self.item_selecionado)
            else:
                self._equipar_arma(self.item_selecionado)
        elif self.item_selecionado.tipo_item == 'ace': # Acessório
            self._equipar_acessorio(self.item_selecionado) # Por enquanto, acessório apenas equipa
        elif self.item_selecionado.tipo_item == 'fru': # Fruta
            pass # Adicione a lógica para frutas aqui
        else:
            self.feedback_message = "Este item não pode ser usado/equipado."
            self.feedback_timer = self.feedback_duration


    def _handle_item_click(self, pos):
        """
        Detecta qual item foi clicado na visualização atual (Armas, Acessórios, etc.)
        e o marca como selecionado.
        """
        current_list = []
        if self.aba_ativa_index == 1: # Armas
            current_list = self.lista_armas
        elif self.aba_ativa_index == 2: # Acessórios
            current_list = self.lista_acessorios
        elif self.aba_ativa_index == 3: # Consumíveis
            current_list = self.lista_consumiveis
        elif self.aba_ativa_index == 4: # Outros (não consumíveis e frutas)
            current_list = self.lista_outros

        if not current_list:
            self._resetar_selecao()
            return

        # Configurações da grade (copiadas de _draw_item_view para calcular a posição do clique)
        slot_img = self.imagens_ui.get('inv_slot_item')
        if not slot_img: return

        x_inicial_grelha = self.rect_painel.left + 80
        y_inicial_grelha = self.rect_painel.top + 120
        colunas = 4
        padding_grelha = 20
        largura_slot = slot_img.get_width()
        altura_slot = slot_img.get_height()

        for i, item in enumerate(current_list):
            coluna_atual = i % colunas
            linha_atual = i // colunas
            
            pos_x_slot = x_inicial_grelha + coluna_atual * (largura_slot + padding_grelha) + 34
            pos_y_slot = y_inicial_grelha + linha_atual * (altura_slot + padding_grelha) - 34
            
            item_rect = pygame.Rect(pos_x_slot, pos_y_slot, largura_slot, altura_slot)

            if item_rect.collidepoint(pos):
                self.item_selecionado = item
                self.indice_item_selecionado = i
                print(f"Item selecionado: {item.nome_item.strip()} (ID: {item.identificador_item})")
                self.feedback_message = "" # Limpa feedback anterior ao selecionar novo item
                return # Item clicado, não precisa verificar outros
        
        # Se clicou fora de qualquer item, deseleciona
        self._resetar_selecao()


    def _usar_consumivel(self, item_consumivel):
        """Lógica para usar um item consumível."""
        print(f"Tentando usar consumível: {item_consumivel.nome_item.strip()}")
        sucesso = self.db_manager.usar_consumivel(self.jogador_id, item_consumivel.identificador_item)
        if sucesso:
            print(f"Consumível {item_consumivel.nome_item.strip()} usado com sucesso!")
            self.feedback_message = f"{item_consumivel.nome_item.strip()} usado!"
            self.feedback_timer = self.feedback_duration
            self._carregar_dados() # Recarrega dados para atualizar contagem do item e stats do jogador
        else:
            print(f"Não foi possível usar o consumível {item_consumivel.nome_item.strip()}.")
            self.feedback_message = f"Não pode usar {item_consumivel.nome_item.strip()}."
            self.feedback_timer = self.feedback_duration

    def _equipar_arma(self, item_arma):
        """Lógica para equipar uma arma."""
        print(f"Tentando equipar arma: {item_arma.nome_item.strip()}")
        sucesso = self.db_manager.equipar_arma(self.jogador_id, item_arma.identificador_item)
        if sucesso:
            print(f"Arma {item_arma.nome_item.strip()} equipada com sucesso!")
            self.feedback_message = f"{item_arma.nome_item.strip()} equipado!"
            self.feedback_timer = self.feedback_duration
            self._carregar_dados() # Recarrega dados para atualizar status de equipamento do jogador
        else:
            print(f"Não foi possível equipar a arma {item_arma.nome_item.strip()}.")
            self.feedback_message = f"Não pode equipar {item_arma.nome_item.strip()}."
            self.feedback_timer = self.feedback_duration


    def _voltar_ao_jogo(self):
        """Retorna para a tela de jogo."""
        jogador_atualizado = self.db_manager.buscar_jogador(self.jogador_id)
        self.gerenciador_telas.mudar_tela(
            CHAVE_TRANSICAO_MAPA, dados_da_ilha=self.dados_retorno_ilha,
            dados_da_area=self.dados_retorno_area, jogador=jogador_atualizado,
            ponto_geracao_jogador=self.ponto_retorno_jogador)

    def update(self, dt):
        """Atualiza o timer do feedback visual."""
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                self.feedback_message = "" # Limpa a mensagem quando o timer acaba
        if self.showing_item_info:
            pass # Nenhuma atualização de lógica para o painel de info no momento

    def _get_lista_atual(self):
        """Retorna a lista de inventário ativa (vendedor ou jogador)."""
        # A tela de inventário não tem modo comprar/vender, então retorna a lista baseada na aba
        if self.aba_ativa_index == 1: # Armas
            return self.lista_armas
        elif self.aba_ativa_index == 2: # Acessórios
            return self.lista_acessorios
        elif self.aba_ativa_index == 3: # Consumíveis
            return self.lista_consumiveis
        elif self.aba_ativa_index == 4: # Outros
            return self.lista_outros
        return [] # Retorna lista vazia para aba de status

    def _get_lista_visivel(self):
        """Retorna a fatia da lista de itens que deve ser visível na tela. (Não usada no momento sem scroll)"""
        return self._get_lista_atual() # No momento, toda a lista é visível

    def draw(self, tela):
        """Desenha todos os elementos da tela da loja."""
        tela.fill(PRETO) 
        if self.snapshot_fundo:
            tela.blit(self.snapshot_fundo, (0, 0))
        fundo_overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        fundo_overlay.fill((0, 0, 10, 150))
        tela.blit(fundo_overlay, (0, 0))

        if self.imagens_ui.get('painel_fundo'):
            tela.blit(self.imagens_ui['painel_fundo'], self.rect_painel)
        
        self._draw_ui_base(tela)

        # Lógica de decisão: desenha APENAS o conteúdo da aba ativa
        if self.aba_ativa_index == 0:
            self._draw_status_view(tela)
        elif self.aba_ativa_index == 1:
            self._draw_item_view(tela, self.lista_armas, "Armas")
        elif self.aba_ativa_index == 2:
            self._draw_item_view(tela, self.lista_acessorios, "Acessórios")
        elif self.aba_ativa_index == 3:
            self._draw_item_view(tela, self.lista_consumiveis, "Consumíveis")
        elif self.aba_ativa_index == 4:
            self._draw_item_view(tela, self.lista_outros, "Outros")

        # NOVO: Desenha os botões de ação e informação
        self._draw_item_action_buttons(tela)
        
        # NOVO: Desenha a mensagem de feedback
        self._draw_feedback_message(tela)

        # NOVO: Desenha o painel de informações do item se estiver ativo (último para sobrepor)
        if self.showing_item_info:
            self._draw_item_details_panel(tela)

        
    def _draw_ui_base(self, tela):
            """Desenha os elementos que aparecem em todas as abas."""
            for i, rect_aba in enumerate(self.rects_abas):
                icone = self.icones_abas[i]
                icone.set_alpha(255 if i == self.aba_ativa_index else 150)
                tela.blit(icone, rect_aba)
            
            if self.imagens_ui.get('botao_fechar'):
                tela.blit(self.imagens_ui['botao_fechar'], self.rect_botao_fechar)

    def _draw_status_view(self, tela):
        """Desenha o conteúdo da aba de Estado, com tudo alinhado ao painel principal."""

        # Referências de posição para facilitar o alinhamento
        painel_topo_y = self.rect_painel.top
        painel_centro_x = self.rect_painel.centerx
        painel_centro_y = self.rect_painel.centery
        painel_esquerda_x = self.rect_painel.left
        painel_direita_x = self.rect_painel.right

        # Rótulos "Equip." e "Estat."
        if self.imagens_ui.get('label_equip'):
            label_equip_rect = self.imagens_ui['label_equip'].get_rect(center=(painel_esquerda_x + 270, painel_topo_y + 160))
            tela.blit(self.imagens_ui['label_equip'], label_equip_rect)
        
        if self.imagens_ui.get('label_estat'):
            label_estat_rect = self.imagens_ui['label_estat'].get_rect(center=(painel_direita_x - 150, painel_topo_y + 160))
            tela.blit(self.imagens_ui['label_estat'], label_estat_rect)

        # Slots de Equipamento (na esquerda)
        y_slot_inicial = painel_topo_y + 150
        x_slot = painel_esquerda_x + 150
        slots_info = {'camisa': (x_slot + 120, y_slot_inicial + 88), 'fruta': (x_slot + 120, y_slot_inicial + 185), 'arma_especial': (x_slot + 120, y_slot_inicial + 285)}
        for nome_slot, pos in slots_info.items():
            if self.icones_slots.get(nome_slot):
                slot_rect = self.icones_slots[nome_slot].get_rect(center=pos)
                tela.blit(self.icones_slots[nome_slot], slot_rect)
        
        # NOVO: Desenha a arma equipada se houver
        if self.arma_equipada:
            # Posição do slot de arma equipada
            pos_x_arma_equipada = slots_info['arma_especial'][0]
            pos_y_arma_equipada = slots_info['arma_especial'][1]
            slot_img = self.imagens_ui.get('inv_slot_arma_equipada') # Use a imagem de slot específica
            
            if slot_img:
                slot_rect = slot_img.get_rect(center=(pos_x_arma_equipada, pos_y_arma_equipada))
                tela.blit(slot_img, slot_rect)
                
                imagem_arma = self._obter_imagem_item(self.arma_equipada)
                if imagem_arma:
                    # Redimensiona para caber no slot (ajuste o tamanho conforme a imagem do slot)
                    img_scaled = pygame.transform.scale(imagem_arma, (slot_img.get_width() - 10, slot_img.get_height() - 10))
                    img_rect = img_scaled.get_rect(center=slot_rect.center)
                    tela.blit(img_scaled, img_rect)
                
                # Desenha o nome da arma equipada abaixo do slot
                self._desenhar_texto_com_borda(tela, self.arma_equipada.nome_item.strip(), self.fonte_texto, BRANCO, PRETO, 1, (slot_rect.centerx, slot_rect.bottom + 5))


        # Personagem e o seu fundo (no centro)
        if self.imagens_ui.get('fundo_personagem'):
            fundo_personagem_rect = self.imagens_ui['fundo_personagem'].get_rect(center=(painel_centro_x + 58,painel_centro_y+80))
            tela.blit(self.imagens_ui['fundo_personagem'], fundo_personagem_rect)
        
        if self.img_jogador_sprite:
            sprite_rect = self.img_jogador_sprite.get_rect(center=(painel_centro_x + 60, painel_centro_y + 80))
            tela.blit(self.img_jogador_sprite, sprite_rect)
        
        # Nome do personagem (no topo)
        self._desenhar_texto_com_borda(tela, self.dados_jogador.nome.strip(), self.fonte_titulo, (255,255,255), (53,38,16), 2, (painel_centro_x + 50, painel_topo_y + 160))

        
        x_base_stats = painel_direita_x - 150
        y_base_stats = painel_topo_y + 150

        # Valor do Nível
        # Para ajustar a altura, mude o valor depois de 'y_base_stats +'
        pos_y_nivel = y_base_stats + 10 
        self._desenhar_texto_com_borda(tela, str(self.dados_jogador.nivel), self.fonte_texto, (255,255,255), (53,38,16), 2, (x_base_stats, pos_y_nivel + 100 ))

        # Valor do PV
        pos_y_pv = y_base_stats + 105
        self._desenhar_texto_com_borda(tela, f"{self.dados_jogador.vida_atual}/{self.dados_jogador.vida}", self.fonte_texto, (255,255,255), (53,38,16), 2, (x_base_stats, pos_y_pv + 85))
        
        # Valor do PE
        pos_y_pe = y_base_stats + 200
        self._desenhar_texto_com_borda(tela, str(self.dados_jogador.energia), self.fonte_texto, (255,255,255), (53,38,16), 2, (x_base_stats, pos_y_pe + 75))
        
        # Adicione este novo método à sua classe

    def _draw_item_view(self, tela, lista_de_itens, titulo_aba):
        """Desenha uma visualização de itens com imagens nos slots."""
        # Desenha o título da aba no topo
        self._desenhar_texto_com_borda(tela, titulo_aba, self.fonte_titulo, BRANCO, PRETO, 2, (self.rect_painel.centerx, self.rect_painel.top + 55))

        # Se a lista de itens estiver vazia, mostra a imagem "Não tem nada aqui!"
        if not lista_de_itens:
            img_nada_aqui = self.imagens_ui.get('inv_nada_aqui')
            if img_nada_aqui:
                pos_x_nada = self.rect_painel.centerx + 50
                pos_y_nada = self.rect_painel.centery + 50
                rect_img = img_nada_aqui.get_rect(center=(pos_x_nada, pos_y_nada))
                tela.blit(img_nada_aqui, rect_img)
            return

        # Se houver itens, desenha a grelha
        slot_img = self.imagens_ui.get('inv_slot_item')
        if not slot_img: return

        # Configurações da grelha
        x_inicial_grelha = self.rect_painel.left + 80
        y_inicial_grelha = self.rect_painel.top + 120
        colunas = 4
        padding_grelha = 20
        largura_slot = slot_img.get_width()
        altura_slot = slot_img.get_height()

        # Loop para desenhar cada item
        for i, item in enumerate(lista_de_itens):
            coluna_atual = i % colunas
            linha_atual = i // colunas
            
            # Posição do slot, ajustada para caber dentro da área cinza
            pos_x_slot = x_inicial_grelha + coluna_atual * (largura_slot + padding_grelha) + 34
            pos_y_slot = y_inicial_grelha + linha_atual * (altura_slot + padding_grelha) - 34
            
            # NOVO: Destaca o slot se for o item selecionado
            

            # 1. Desenha o slot de fundo
            tela.blit(slot_img, (pos_x_slot, pos_y_slot))
            
            # 2. NOVO: Desenha a imagem do item no centro do slot
            imagem_item = self._obter_imagem_item(item)
            if imagem_item:
                # Redimensiona a imagem se necessário para caber no slot
                tamanho_max = min(largura_slot - 10, altura_slot - 10)  # Margem de 5px
                if imagem_item.get_width() > tamanho_max or imagem_item.get_height() > tamanho_max:
                    imagem_item = pygame.transform.scale(imagem_item, (tamanho_max, tamanho_max))
                
                # Centraliza a imagem no slot
                rect_item = imagem_item.get_rect(center=(pos_x_slot + largura_slot//2, pos_y_slot + altura_slot//2))
                tela.blit(imagem_item, rect_item)
            
            # 3. Desenha o nome do item abaixo do slot com seus offsets personalizados
            nome_item = item.nome_item.strip()
            # pos_nome_y original: pos_y_slot + altura_slot + 5
            # Com seus offsets personalizados:
            self._desenhar_texto_com_borda(tela, nome_item, self.fonte_texto, BRANCO, PRETO, 1, 
                                           (pos_x_slot + -110 + largura_slot//2, pos_y_slot + altura_slot + 5 + -300))
            
            # 4. Desenha a quantidade no canto inferior direito do slot com seus offsets personalizados
            texto_qtd = f"x{item.quantidade}"
            # pos_qtd_x original: pos_x_slot + largura_slot - 10
            # pos_qtd_y original: pos_y_slot + altura_slot - 10
            # Com seus offsets personalizados:
            self._desenhar_texto_com_borda(tela, texto_qtd, self.fonte_texto, AMARELO_CLARO, PRETO, 1, 
                                           (pos_x_slot + largura_slot - 10 + -130, pos_y_slot + altura_slot - 10 + -285), align='right')

    def _draw_action_button(self, tela):
        """Desenha o botão de ação (Equipar/Usar) se um item equipável/usável estiver selecionado."""
        if self.item_selecionado:
            # Define o texto do botão com base no tipo de item
            button_text = ""
            if self.item_selecionado.tipo_item == 'arm':
                button_text = "Equipar"
            elif self.item_selecionado.tipo_item == 'con':
                button_text = "Usar"
            elif self.item_selecionado.tipo_item == 'ace': # NOVO: Para acessórios
                button_text = "Equipar"
            elif self.item_selecionado.tipo_item == 'fru':
                button_text = "Comer" # Ou outro texto para frutas
            
            if button_text: # Só desenha o botão se houver uma ação definida
                pygame.draw.rect(tela, VERDE, self.rect_botao_acao, border_radius=5)
                self._desenhar_texto_com_borda(tela, button_text, self.fonte_botao, BRANCO, PRETO, 1, self.rect_botao_acao.center)

    def _draw_feedback_message(self, tela):
        """Desenha a mensagem de feedback na tela."""
        if self.feedback_message and self.feedback_timer > 0:
            alpha = min(255, int(255 * (self.feedback_timer / self.feedback_duration)))
            color = (255, 255, 255, alpha) # Branco com transparência decrescente

            text_surface = self.fonte_titulo.render(self.feedback_message, True, (color[0], color[1], color[2]))
            text_surface.set_alpha(alpha) # Aplica o alpha na superfície do texto
            
            text_rect = text_surface.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA - 50))
            tela.blit(text_surface, text_rect)
    def _equipar_acessorio(self, item_acessorio):
        """Lógica para equipar um acessório."""
        print(f"Tentando equipar acessório: {item_acessorio.nome_item.strip()}")
        sucesso = self.db_manager.equipar_acessorio(self.jogador_id, item_acessorio.identificador_item) # Chamada para o DBManager
        if sucesso:
            print(f"Acessório {item_acessorio.nome_item.strip()} equipado com sucesso!")
            self.feedback_message = f"{item_acessorio.nome_item.strip()} equipado!"
            self.feedback_timer = self.feedback_duration
            self._carregar_dados() # Recarrega dados para atualizar status de equipamento do jogador
        else:
            print(f"Não foi possível equipar o acessório {item_acessorio.nome_item.strip()}.")
            self.feedback_message = f"Não pode equipar {item_acessorio.nome_item.strip()}."
            self.feedback_timer = self.feedback_duration
    def _desequipar_arma(self, item_arma):
        """Lógica para desequipar uma arma."""
        print(f"Tentando desequipar arma: {item_arma.nome_item.strip()}")
        sucesso = self.db_manager.desequipar_arma(self.jogador_id) # Não precisa do ID da arma, apenas do jogador
        if sucesso:
            print(f"Arma {item_arma.nome_item.strip()} desequipada com sucesso!")
            self.feedback_message = f"{item_arma.nome_item.strip()} desequipado!"
            self.feedback_timer = self.feedback_duration
            self._carregar_dados() # Recarrega dados para atualizar status de equipamento do jogador
        else:
            print(f"Não foi possível desequipar a arma {item_arma.nome_item.strip()}.")
            self.feedback_message = f"Não pode desequipar {item_arma.nome_item.strip()}."
            self.feedback_timer = self.feedback_duration
    def _draw_item_action_buttons(self, tela):
            """Desenha os botões de ação (Equipar/Usar/Desequipar) e Informação."""
            if self.item_selecionado:
                # Botão de Ação
                button_text = ""
                button_color = VERDE # Cor padrão para ação
                
                # NOVO: Lógica para o texto do botão de ação
                if self.item_selecionado.tipo_item == 'arm':
                    is_equipped = (self.arma_equipada and 
                                self.arma_equipada.identificador_item == self.item_selecionado.identificador_item)
                    if is_equipped:
                        button_text = "Desequipar"
                        button_color = VERMELHO # Desequipar pode ser vermelho
                    else:
                        button_text = "Equipar"
                elif self.item_selecionado.tipo_item == 'ace':
                    # Você pode adicionar lógica para desequipar acessórios aqui também se tiver um campo no jogador_equipamento
                    button_text = "Equipar"
                elif self.item_selecionado.tipo_item == 'con':
                    button_text = "Usar"
                elif self.item_selecionado.tipo_item == 'fru':
                    button_text = "Comer"
                # Para outros tipos de item (ncn), button_text pode ser vazio ou ter um texto genérico se não houver ação direta

                if button_text: # Só desenha o botão se houver uma ação definida
                    pygame.draw.rect(tela, button_color, self.rect_botao_acao, border_radius=5)
                    
                    self._desenhar_texto_com_borda(tela, button_text, self.fonte_botao, BRANCO, PRETO, 1, self.rect_botao_acao.center)

            # Botão de Informação (aparece para qualquer item selecionado)
                pygame.draw.rect(tela, CINZA, self.rect_botao_informacao, border_radius=5)
                self._desenhar_texto_com_borda(tela, "Informação", self.fonte_botao, BRANCO, PRETO, 1, self.rect_botao_informacao.center)
    def _draw_item_details_panel(self, tela):
        """Desenha o painel com as informações detalhadas do item selecionado."""
        if not self.item_details_to_show:
            return

        # Fundo escuro para o painel de detalhes (overlay)
        overlay_surface = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 180)) # Preto semi-transparente
        tela.blit(overlay_surface, (0, 0))

        # Painel principal do item
        pygame.draw.rect(tela, (150, 100, 50), self.rect_info_panel, border_radius=5) # Cor marrom clara
        pygame.draw.rect(tela, (50, 30, 10), self.rect_info_panel, 3, border_radius=5) # Borda mais escura

        # Título (nome do item)
        self._desenhar_texto_com_borda(tela, self.item_details_to_show.nome_item.strip(), self.fonte_titulo, BRANCO, PRETO, 2, (self.rect_info_panel.centerx, self.rect_info_panel.top + 30))

        # Descrição do item (com quebra de linha)
        desc_rect = self.rect_info_panel.inflate(-40, -100) # Reduz o retângulo para o texto
        desc_rect.top = self.rect_info_panel.top + 70 # Posiciona abaixo do título
        self._draw_text_wrapped(tela, self.item_details_to_show.descricao.strip(), self.fonte_texto, BRANCO, desc_rect)

        # Outras características (Raridade, Tipo, Preços)
        y_start = desc_rect.bottom + 20

        # NOVO: Verificação segura para 'Raridade'
        raridade_text = "N/A"
        if hasattr(self.item_details_to_show, 'raridade') and self.item_details_to_show.raridade is not None:
            raridade_text = self.item_details_to_show.raridade.strip()
        self._desenhar_texto_com_borda(tela, f"Raridade: {raridade_text}", self.fonte_texto, AMARELO_CLARO, PRETO, 1, (self.rect_info_panel.left + 20, y_start -70), align='left')
        
        # NOVO: Verificação segura para 'Preço de Compra'
        preco_compra_text = "Não Comprável"
        if hasattr(self.item_details_to_show, 'preco_compra') and self.item_details_to_show.preco_compra is not None:
             preco_compra_text = f"Custo: {self.item_details_to_show.preco_compra} moedas"
        self._desenhar_texto_com_borda(tela, preco_compra_text, self.fonte_texto, BRANCO, PRETO, 1, (self.rect_info_panel.left + 20, y_start + -50), align='left')

        # NOVO: Verificação segura para 'Preço de Venda'
        preco_venda_text = "Não Vendável"
        if hasattr(self.item_details_to_show, 'preco_venda') and self.item_details_to_show.preco_venda is not None:
             preco_venda_text = f"Venda: {self.item_details_to_show.preco_venda} moedas"
        self._desenhar_texto_com_borda(tela, preco_venda_text, self.fonte_texto, BRANCO, PRETO, 1, (self.rect_info_panel.left + 20, y_start + -30), align='left')

        # Botão de Fechar do painel
        pygame.draw.rect(tela, VERMELHO, self.rect_info_panel_close_button, border_radius=5)
        self._desenhar_texto_com_borda(tela, "X", self.fonte_texto, BRANCO, PRETO, 1, self.rect_info_panel_close_button.center)