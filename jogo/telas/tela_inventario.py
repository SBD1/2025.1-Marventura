# Em jogo/telas/tela_inventario.py

import pygame
from .tela_modelo import TelaModelo
from utilidades.constantes import *

class TelaInventario(TelaModelo):
    """
    Representa a interface do inventário do jogador, com abas para status,
    equipamentos e itens.
    """
    def __init__(self, gerenciador_telas, gerenciador_recursos, db_manager, jogador_id,
                 dados_retorno_ilha, dados_retorno_area, ponto_retorno_jogador):
        super().__init__(gerenciador_telas, gerenciador_recursos)
        # --- Atributos essenciais ---
        self.db_manager = db_manager
        self.jogador_id = jogador_id
        self.dados_retorno_ilha = dados_retorno_ilha
        self.dados_retorno_area = dados_retorno_area
        self.ponto_retorno_jogador = ponto_retorno_jogador
        
        # --- Estado da UI ---
        self.aba_ativa_index = 0

        # --- Carregamento e Configuração ---
        self._carregar_recursos()
        self._carregar_dados()
        self._definir_layout()

    # 1. MÉTODOS DE CONFIGURAÇÃO
    # ======================================================================
    def _carregar_recursos(self):
        """Carrega todas as fontes e imagens da UI de uma vez."""
        self.fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_BOTAO)
        self.fonte_stats = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO) # Use a fonte de texto
        self.fonte_texto = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO)
        # Carrega o sprite do personagem que está jogando
        dados_jogador_temp = self.db_manager.buscar_jogador(self.jogador_id)
        self.img_jogador_sprite = self.gerenciador_recursos.obter_imagem(f'{dados_jogador_temp.nome.strip()}_inventario')
        
        # Carrega todas as imagens da UI
        self.imagens_ui = {
            'painel_fundo': self.gerenciador_recursos.obter_imagem('inv_painel_fundo'),
            'botao_fechar': self.gerenciador_recursos.obter_imagem('inv_botao_fechar'),
            'label_equip': self.gerenciador_recursos.obter_imagem('inv_label_equip'),
            'label_estat': self.gerenciador_recursos.obter_imagem('inv_label_estat'),
            'fundo_personagem': self.gerenciador_recursos.obter_imagem('inv_fundo_personagem'),
        }
        self.icones_abas = { i: self.gerenciador_recursos.obter_imagem(k) for i, k in enumerate(['inv_tab_status', 'inv_tab_arma', 'inv_tab_acessorio', 'inv_tab_consumivel', 'inv_tab_outros'])}
        self.icones_slots = {k: self.gerenciador_recursos.obter_imagem(f'inv_slot_{k}') for k in ['camisa', 'fruta', 'arma_especial']}

    def _carregar_dados(self):
        """Carrega e filtra os dados do inventário e do jogador."""
        self.dados_jogador = self.db_manager.buscar_jogador(self.jogador_id)
        # TODO: Implementar busca de equipamento real
        self.equipamento_atual = {'arma': 'Nenhuma', 'acessorio': 'Nenhum'}

    def _definir_layout(self):
        """Define o retângulo principal do painel E os retângulos dos botões."""
        painel_img = self.imagens_ui.get('inv_painel_fundo')
        if painel_img:
            self.rect_painel = painel_img.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
        else: # Fallback se a imagem não carregar
            self.rect_painel = pygame.Rect(0, 0, 800, 500)
            self.rect_painel.center = (LARGURA_TELA // 2, ALTURA_TELA // 2)

        # --- CORREÇÃO: Define os retângulos dos botões aqui, como atributos da classe ---
        
        # Botão de Fechar
        icone_fechar = self.imagens_ui['botao_fechar']
        if icone_fechar:
            pos_x_fechar = self.rect_painel.right + (icone_fechar.get_width() / 2) - 15
            pos_y_fechar = self.rect_painel.top + 40
            self.rect_botao_fechar = icone_fechar.get_rect(center=(pos_x_fechar, pos_y_fechar))
        else:
            self.rect_botao_fechar = pygame.Rect(0,0,0,0)

        # Abas Laterais (COM AJUSTES DE POSIÇÃO E ESPAÇAMENTO)
        self.rects_abas = []
        for i, icone in self.icones_abas.items():
            if icone:
                largura_icone = icone.get_width()
                pos_x_aba = self.rect_painel.left - (largura_icone / 2) + 100                
                # AJUSTES AQUI:
                pos_y_inicial = self.rect_painel.top + 500  # Sobe o conjunto de ícones
                espacamento_vertical = 800              # Diminui a distância entre eles
                
                pos_y_aba = pos_y_inicial + (i * espacamento_vertical)
                
                rect_aba = icone.get_rect(center=(pos_x_aba, pos_y_aba))
                self.rects_abas.append(rect_aba)

        # Abas Laterais
        self.rects_abas = []
        for i, icone in self.icones_abas.items():
            if icone:
                largura_icone = icone.get_width()
                pos_x_aba = self.rect_painel.left - (largura_icone / 2) + 15 # Ajuste fino de 15px
                pos_y_aba = self.rect_painel.top + 70 + i * 95
                rect_aba = icone.get_rect(center=(pos_x_aba, pos_y_aba))
                self.rects_abas.append(rect_aba)

    # 2. MÉTODOS DE LÓGICA E EVENTOS
    # ======================================================================
    def handle_input(self, evento):
        """Gerencia cliques do mouse e teclas."""
        if evento.type == pygame.KEYDOWN and (evento.key == pygame.K_ESCAPE or evento.key == pygame.K_i):
            self._voltar_ao_jogo()
            return

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos

            # --- CORREÇÃO: Usa os retângulos já definidos ---

            # Checa clique no botão de fechar
            if self.rect_botao_fechar.collidepoint(pos):
                self._voltar_ao_jogo()
                return

            # Checa cliques nas abas
            for i, rect_aba in enumerate(self.rects_abas):
                if rect_aba.collidepoint(pos):
                    self.aba_ativa_index = i
                    return

    def _voltar_ao_jogo(self):
        """Retorna para a tela de jogo."""
        jogador_atualizado = self.db_manager.buscar_jogador(self.jogador_id)
        self.gerenciador_telas.mudar_tela(
            CHAVE_TRANSICAO_MAPA, dados_da_ilha=self.dados_retorno_ilha,
            dados_da_area=self.dados_retorno_area, jogador=jogador_atualizado,
            ponto_geracao_jogador=self.ponto_retorno_jogador)

    # 3. MÉTODOS DE DESENHO
    # ======================================================================
    def draw(self, tela):
        """Função principal de desenho."""
        # Fundo escuro
        fundo_overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        fundo_overlay.fill((0, 0, 100, 150))
        tela.blit(fundo_overlay, (0, 0))

        # Painel de fundo
        if self.imagens_ui['painel_fundo']:
            tela.blit(self.imagens_ui['painel_fundo'], self.rect_painel)
        else:
            pygame.draw.rect(tela, (123, 93, 62), self.rect_painel, border_radius=15)

        # Conteúdo do painel
        self._draw_ui_base(tela)
        if self.aba_ativa_index == 0:
            self._draw_status_view(tela)
        else:
            self._desenhar_texto_com_borda(tela, f"Aba de Itens {self.aba_ativa_index}", self.fonte_titulo, BRANCO, PRETO, 2, self.rect_painel.center)

    def _draw_ui_base(self, tela):
        """Desenha os elementos que aparecem em todas as abas."""
        
        # --- Abas Verticais (Posicionadas FORA do painel, à esquerda) ---
        for i, icone in self.icones_abas.items():
            if icone:
                # Pega a largura do ícone para calcular a posição
                largura_icone = icone.get_width()
                
                # POSICIONA O ÍCONE À ESQUERDA DO PAINEL:
                # Pega a borda esquerda do painel e subtrai metade da largura do ícone
                # para que o ícone fique "colado" do lado de fora.
                # O "+ 5" é um pequeno ajuste para um encaixe visual melhor.
                pos_x = self.rect_painel.left - (largura_icone / 4) + 5
                pos_y = self.rect_painel.top + 70 + i * 95
                
                rect_aba = icone.get_rect(center=(pos_x, pos_y))
                icone.set_alpha(255 if i == self.aba_ativa_index else 150)
                tela.blit(icone, rect_aba)
        
        # --- Botão de Fechar (Posicionado FORA do painel, à direita) ---
        if self.imagens_ui['botao_fechar']:
            icone_fechar = self.imagens_ui['botao_fechar']
            largura_icone_fechar = icone_fechar.get_width()

            # POSICIONA O ÍCONE À DIREITA DO PAINEL:
            # Pega a borda direita do painel e adiciona metade da largura do ícone.
            # O "- 5" é um pequeno ajuste para um encaixe visual melhor.
            pos_x = self.rect_painel.right + (largura_icone_fechar / 2) - 55
            pos_y = self.rect_painel.top + 405

            rect_botao_fechar = icone_fechar.get_rect(center=(pos_x, pos_y))
            tela.blit(icone_fechar, rect_botao_fechar)

    def _draw_status_view(self, tela):
        """Desenha o conteúdo da aba de Estado."""
        painel_topo_y = self.rect_painel.top
        
        # --- Rótulos (Labels) - AJUSTADOS ---
        label_equip_rect = self.imagens_ui['label_equip'].get_rect(
            center=(self.rect_painel.left + 50, painel_topo_y + 0) # Posição ajustada
        )
        tela.blit(self.imagens_ui['label_equip'], label_equip_rect)
        
        label_estat_rect = self.imagens_ui['label_estat'].get_rect(
            center=(self.rect_painel.right - 105, painel_topo_y + 5) # Posição ajustada
        )
        tela.blit(self.imagens_ui['label_estat'], label_estat_rect)

        # --- Slots de Equipamento - AJUSTADOS ---
        y_slot_inicial = painel_topo_y + 105  # Posição Y inicial ajustada
        x_slot = self.rect_painel.left + 150  # Posição X ajustada para centralizar
        
        # Dicionário para simplificar o desenho dos slots
        slots_info = {
            'camisa': (x_slot, y_slot_inicial),
            'fruta': (x_slot, y_slot_inicial + 85),
            'arma_especial': (x_slot, y_slot_inicial + 170)
        }
        for nome_slot, pos in slots_info.items():
            if self.icones_slots.get(nome_slot):
                slot_rect = self.icones_slots[nome_slot].get_rect(center=pos)
                tela.blit(self.icones_slots[nome_slot], slot_rect)
        
        # --- Personagem (AJUSTADO PARA O CENTRO) ---
        centro_x_personagem = self.rect_painel.centerx
        # Usa o centro Y do painel como referência para centralizar melhor na vertical
        centro_y_personagem = self.rect_painel.centery + 20
        
        tela.blit(self.imagens_ui['fundo_personagem'], self.imagens_ui['fundo_personagem'].get_rect(center=(centro_x_personagem, centro_y_personagem)))
        tela.blit(self.img_jogador_sprite, self.img_jogador_sprite.get_rect(center=(centro_x_personagem, centro_y_personagem + 5))) # Pequeno ajuste para o sprite
        self._desenhar_texto_com_borda(tela, self.dados_jogador.nome.strip(), self.fonte_titulo, (255,255,255), (53,38,16), 2, (centro_x_personagem, painel_topo_y + 55))

        # --- Estatísticas ---
        centro_x_stats = self.rect_painel.right - 105
        y_offset = painel_topo_y + 105 # Ajuste inicial de Y
        stats = {"Nível": self.dados_jogador.nivel, "PV": f"{self.dados_jogador.vida_atual}/{self.dados_jogador.vida}", "PE": self.dados_jogador.energia}

        for nome, valor in stats.items():
            self._desenhar_texto_com_borda(tela, nome, self.fonte_texto, (255,255,255), (53,38,16), 2, (centro_x_stats, y_offset))
            y_offset += 35 # Espaçamento ajustado
            self._desenhar_texto_com_borda(tela, str(valor), self.fonte_texto, (255,255,255), (53,38,16), 2, (centro_x_stats, y_offset))
            y_offset += 60 # Espaçamento entre blocos