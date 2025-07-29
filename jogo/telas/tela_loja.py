# Em jogo/telas/tela_loja.py

import pygame
from .tela_modelo import TelaModelo
from utilidades.constantes import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import DBManager
    from gerenciadores import GerenciadorDeRecursos
    from gerenciadores import GerenciadorDeTelas
    from gerenciadores import GerenciadorDeEntidades

class TelaLoja(TelaModelo):
    """
    Representa a interface da loja, onde o jogador pode comprar itens de um
    vendedor ou vender itens de seu próprio inventário.
    """
    def __init__(self, gerenciador_telas: 'GerenciadorDeTelas', gerenciador_recursos: 'GerenciadorDeRecursos', db_manager: 'DBManager', gerenciador_etidades: 'GerenciadorDeEntidades', vendedor_id, nome_vendedor):
        super().__init__(gerenciador_telas, gerenciador_recursos)
        self.db_manager = db_manager
        self.vendedor_id = vendedor_id
        self.nome_vendedor = nome_vendedor
        self.entidades = gerenciador_etidades


        # Estado da UI
        self.modo = 'comprar'  # Pode ser 'comprar' ou 'vender'
        self.item_selecionado = None
        self.indice_item_selecionado = 0
        self.scroll_offset = 0
        self.quantidade_selecionada = 1
        
        # --- NOVO: Feedback de transação ---
        self.feedback_message = None
        self.feedback_timer = 0
        self.feedback_color = BRANCO

        # Carregamento de recursos visuais
        self._carregar_recursos()

        # Carregamento inicial de dados
        self._carregar_dados_loja()

        # Definição do layout da UI
        self._definir_layout()

    def _carregar_recursos(self):
        """Carrega as fontes e imagens necessárias para a tela da loja."""
        self.fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TITULO)
        self.fonte_texto = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO)
        self.fonte_botao = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_BOTAO)
        self.imagem_fundo = self.gerenciador_recursos.obter_imagem(CHAVE_LOJA_INTERIOR)

    def _carregar_dados_loja(self):
        """
        Carrega os dados iniciais do jogador e do vendedor do banco de dados.
        Esta função é chamada apenas uma vez na inicialização da tela.
        """
        self.inventario_vendedor = self.db_manager.buscar_inventario_vendedor(self.vendedor_id, self.entidades.progresso_do_jogo.identificador_progresso)

        self.inventario_jogador = self.db_manager.buscar_inventario(identificador_personagem=self.entidades.jogador.identificador_jogador, identificador_progresso= self.entidades.progresso_do_jogo.identificador_progresso)

        self.dados_jogador = self.db_manager.buscar_jogador(self.entidades.jogador.identificador_jogador)

        self.id_inventario_jogador = self.db_manager.buscar_id_inventario(self.entidades.jogador.identificador_jogador, 'moc', self.entidades.progresso_do_jogo.identificador_progresso)

        self.id_inventario_vendedor = self.db_manager.buscar_id_inventario(self.vendedor_id, 'moc', self.entidades.progresso_do_jogo.identificador_progresso)
        
        self._resetar_selecao()

    def _resetar_selecao(self):
        """Reseta a seleção de item e o scroll."""
        self.item_selecionado = None
        self.indice_item_selecionado = 0
        self.scroll_offset = 0
        self.quantidade_selecionada = 1

    def _definir_layout(self):
        """Define os retângulos para os elementos da UI da loja com base na resolução da tela."""
        largura = LARGURA_TELA
        altura = ALTURA_TELA

        margem_x = largura * 0.05
        margem_y = altura * 0.05

        self.rect_aba_comprar = pygame.Rect(margem_x, margem_y+20, largura * 0.15, altura * 0.07)
        self.rect_aba_vender = pygame.Rect(margem_x + largura * 0.17, margem_y+20, largura * 0.15, altura * 0.07)

        self.rect_lista_itens = pygame.Rect(margem_x, margem_y + altura * 0.13, largura * 0.4, altura * 0.65)
        self.rect_painel_info = pygame.Rect(margem_x + largura * 0.45, margem_y + altura * 0.13, largura * 0.45, altura * 0.45)

        # --- NOVO: Layout para seleção de quantidade ---
        y_botoes_qtd = self.rect_painel_info.bottom - 70
        x_centro_botoes_qtd = self.rect_painel_info.centerx
        self.rect_botao_menos = pygame.Rect(x_centro_botoes_qtd - 60, y_botoes_qtd, 40, 40)
        self.rect_botao_mais = pygame.Rect(x_centro_botoes_qtd + 20, y_botoes_qtd, 40, 40)

        self.rect_botao_transacao = pygame.Rect(margem_x + largura * 0.45, self.rect_painel_info.bottom + altura * 0.02, largura * 0.45, altura * 0.07)
        self.rect_botao_voltar = pygame.Rect(margem_x + largura * 0.45, self.rect_botao_transacao.bottom + altura * 0.015, largura * 0.45, altura * 0.07)

    def processar_eventos(self, evento):
        """Gerencia todas as entradas do usuário nesta tela."""
        super().processar_eventos(evento)
        self._handle_scroll(evento)
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self._handle_clicks(evento.pos)

    def _handle_scroll(self, evento):
        """Gerencia a rolagem da lista de itens com o mouse."""
        if not self.rect_lista_itens.collidepoint(pygame.mouse.get_pos()):
            return
        
        lista_atual = self._get_lista_atual()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 4:  # Roda para cima
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif evento.button == 5:  # Roda para baixo
                max_scroll = max(0, len(lista_atual) - 10) # 10 itens visíveis
                self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

    def _handle_clicks(self, pos):
        """Gerencia os cliques do mouse nos elementos da UI."""
        if self.rect_aba_comprar.collidepoint(pos):
            self.modo = 'comprar'
            self._resetar_selecao()
        elif self.rect_aba_vender.collidepoint(pos):
            self.modo = 'vender'
            self._resetar_selecao()
        elif self.rect_botao_voltar.collidepoint(pos):
            # Busca os dados mais recentes do jogador no banco de dados
            jogador_atualizado = self.db_manager.buscar_jogador(self.entidades.jogador.identificador_jogador)
            
            # Usa a transição de mapa para voltar ao jogo com os dados atualizados
            self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MAPA)
        elif self.rect_botao_transacao.collidepoint(pos) and self.item_selecionado:
            self._realizar_transacao()
        # --- NOVO: Lógica para botões de quantidade ---
        elif self.rect_botao_menos.collidepoint(pos) and self.item_selecionado:
            self.quantidade_selecionada = max(1, self.quantidade_selecionada - 1)
        elif self.rect_botao_mais.collidepoint(pos) and self.item_selecionado:
            max_qtd = self.item_selecionado.quantidade
            self.quantidade_selecionada = min(max_qtd, self.quantidade_selecionada + 1)
        else:
            self._handle_item_selection(pos)

    def _handle_item_selection(self, pos):
        """Gerencia a seleção de um item na lista."""
        lista_visivel = self._get_lista_visivel()
        for i, item in enumerate(lista_visivel):
            item_rect = pygame.Rect(self.rect_lista_itens.x + 5, self.rect_lista_itens.y + 5 + i * 40, 390, 38)
            if item_rect.collidepoint(pos):
                self.indice_item_selecionado = self.scroll_offset + i
                self.item_selecionado = item
                self.quantidade_selecionada = 1
                break

    def _realizar_transacao(self):
        """Executa a lógica de compra ou venda do item selecionado."""
        if self.modo == 'comprar':
            self._comprar_item()
        elif self.modo == 'vender':
            # Evita tentar vender item sem preço definido
            if self.item_selecionado.preco_de_venda is None or self.item_selecionado.preco_de_venda <= 0:
                self._mostrar_feedback("Este item não pode ser vendido.", False)
                return
            self._vender_item()
        self._resetar_selecao()

    def _comprar_item(self):
        """Processa a compra de um item."""
        if self.item_selecionado.preco_de_compra is None:
            self._mostrar_feedback("Este item não pode ser comprado.", False)
            return
            
        preco = self.item_selecionado.preco_de_compra * self.quantidade_selecionada
        if self.entidades.jogador.moedas >= preco:
            resultado = self.db_manager.realizar_compra(
                self.entidades.jogador.identificador_jogador, self.vendedor_id, self.id_inventario_jogador,
                self.id_inventario_vendedor, self.item_selecionado.identificador_item,
                self.quantidade_selecionada, preco, self.entidades.progresso_do_jogo.identificador_progresso
            )
            if resultado.get('sucesso'):
                self._mostrar_feedback("Compra realizada com sucesso!", True)
                self.entidades.jogador.moedas -= preco
                self._atualizar_dados_da_tela()
            else:
                self._mostrar_feedback(f"Falha na compra: {resultado.get('erro', 'Erro')}", False)
        else:
            self._mostrar_feedback("Moedas insuficientes.", False)

    def _vender_item(self):
        """Processa a venda de um item."""
        preco_unitario = self.item_selecionado.preco_de_venda

        if preco_unitario is not None and preco_unitario > 0:
            preco = preco_unitario * self.quantidade_selecionada
            print(f"Vendendo {self.quantidade_selecionada}x {self.item_selecionado.nome_item} por {preco} moedas. Identificador do jogador: {self.entidades.jogador.identificador_jogador}, Identificador do vendedor: {self.vendedor_id}, ID Inventário Jogador: {self.id_inventario_jogador}, ID Inventário Vendedor: {self.id_inventario_vendedor}, ID Item: {self.item_selecionado.identificador_item}")
            resultado = self.db_manager.realizar_venda(
                self.entidades.jogador.identificador_jogador, self.vendedor_id, self.id_inventario_jogador,
                self.id_inventario_vendedor, self.item_selecionado.identificador_item,
                self.quantidade_selecionada, preco, self.entidades.progresso_do_jogo.identificador_progresso
            )
            print(f"Resultado da venda: {resultado}")
            if resultado.get('sucesso'):
                self._mostrar_feedback("Venda realizada com sucesso!", True)
                self.entidades.jogador.moedas += preco
                self._atualizar_dados_da_tela()
            else:
                self._mostrar_feedback(f"Falha na venda: {resultado.get('erro', 'Erro')}", False)
        else:
            self._mostrar_feedback("Este item não pode ser vendido.", False)

    # --- NOVO: Método para mostrar feedback ---
    def _mostrar_feedback(self, mensagem, sucesso=True):
        """Define uma mensagem de feedback para ser exibida na tela."""
        self.feedback_message = mensagem
        self.feedback_color = VERDE if sucesso else VERMELHO
        self.feedback_timer = 3  # Exibir por 3 segundos
        
        # Tocar som (exemplo, requer carregar os sons no gerenciador de recursos)
        if sucesso:
                 self.gerenciador_recursos.obter_som('som_compra_sucesso').play()
        else:
                self.gerenciador_recursos.obter_som('som_compra_falha').play()


    def atualizar(self, dt):
        """Atualiza o timer do feedback visual."""
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                self.feedback_message = None

    def _atualizar_inventarios_localmente(self, id_item, quantidade, tipo_transacao):
        """Atualiza os inventários em memória após uma transação."""
        # Atualiza inventário do jogador
        inv_jogador = list(self.inventario_jogador)
        item_encontrado = False
        for i, item in enumerate(inv_jogador):
            if item.identificador_item == id_item:
                nova_qtd = item.quantidade + quantidade if tipo_transacao == 'comprar' else item.quantidade - quantidade
                if nova_qtd > 0:
                    inv_jogador[i] = item._replace(quantidade=nova_qtd)
                else:
                    inv_jogador.pop(i)
                item_encontrado = True
                break
        if not item_encontrado and tipo_transacao == 'comprar':
             # Se o item não existia, busca os dados completos e adiciona
             # (Esta parte ainda pode necessitar de uma consulta se os dados completos do item não estiverem disponíveis)
             # Para simplificar, vamos recarregar apenas o inventário do jogador neste caso.
             self.inventario_jogador = self.db_manager.buscar_inventario(self.entidades.jogador.identificador_jogador, 'moc', self.entidades.progresso_do_jogo.identificador_progresso)
        else:
            self.inventario_jogador = inv_jogador


        # Atualiza inventário do vendedor
        inv_vendedor = list(self.inventario_vendedor)
        item_encontrado = False
        for i, item in enumerate(inv_vendedor):
            if item.identificador_item == id_item:
                nova_qtd = item.quantidade - quantidade if tipo_transacao == 'comprar' else item.quantidade + quantidade
                if nova_qtd > 0:
                    inv_vendedor[i] = item._replace(quantidade=nova_qtd)
                else:
                    inv_vendedor.pop(i)
                item_encontrado = True
                break
        if not item_encontrado and tipo_transacao == 'vender':
            # Recarrega o inventário do vendedor se um novo item foi adicionado
            self.inventario_vendedor = self.db_manager.buscar_inventario_vendedor(self.vendedor_id)
        else:
            self.inventario_vendedor = inv_vendedor

    def _get_lista_atual(self):
        """Retorna a lista de inventário ativa (vendedor ou jogador)."""
        return self.inventario_vendedor if self.modo == 'comprar' else self.inventario_jogador

    def _get_lista_visivel(self):
        """Retorna a fatia da lista de itens que deve ser visível na tela."""
        lista_atual = self._get_lista_atual()
        return lista_atual[self.scroll_offset:self.scroll_offset + 10]

    def desenhar(self, tela):
        """Desenha todos os elementos da tela da loja."""
        imagem_escalada = pygame.transform.scale(self.imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
        tela.blit(imagem_escalada, (0, 0))
        self._desenhar_texto_com_borda(tela, f"Loja de {self.nome_vendedor}", self.fonte_titulo, BRANCO, PRETO, 2, (LARGURA_TELA / 2, 30))

        self._draw_tabs(tela)
        self._draw_item_list(tela)
        self._draw_info_panel(tela)
        self._draw_buttons(tela)
        self._draw_player_coins(tela)
        
        # --- NOVO: Desenha o feedback na tela ---
        if self.feedback_message:
            self._desenhar_texto_com_borda(tela, self.feedback_message, self.fonte_botao, self.feedback_color, PRETO, 2, 
                                           (LARGURA_TELA / 2, ALTURA_TELA - 30))

        
    def _draw_tabs(self, tela):
        """Desenha as abas de Comprar e Vender."""
        # Aba Comprar
        cor_comprar = CINZA if self.modo == 'comprar' else CINZA_ESCURO
        pygame.draw.rect(tela, cor_comprar, self.rect_aba_comprar)
        self._desenhar_texto_com_borda(tela, "Comprar", self.fonte_botao, BRANCO, PRETO, 1, self.rect_aba_comprar.center)
        
        # Aba Vender
        cor_vender = CINZA if self.modo == 'vender' else CINZA_ESCURO
        pygame.draw.rect(tela, cor_vender, self.rect_aba_vender)
        self._desenhar_texto_com_borda(tela, "Vender", self.fonte_botao, BRANCO, PRETO, 1, self.rect_aba_vender.center)

    def _draw_item_list(self, tela):
        """Desenha a lista de itens rolável."""
        pygame.draw.rect(tela, CINZA_ESCURO, self.rect_lista_itens)
        lista_visivel = self._get_lista_visivel()
        
        for i, item in enumerate(lista_visivel):
            item_rect = pygame.Rect(self.rect_lista_itens.x + 5, self.rect_lista_itens.y + 5 + i * 40, 390, 38)
            
            # Destaque visual para o item selecionado
            if item == self.item_selecionado:
                pygame.draw.rect(tela, AMARELO_CLARO, item_rect, 2)

            if item.nome_item:
                texto = f"{item.quantidade}x {item.nome_item}"
                self._desenhar_texto_com_borda(tela, texto, self.fonte_texto, BRANCO, PRETO, 1, (item_rect.left + 10, item_rect.centery), align='left')

    def _draw_info_panel(self, tela):
        """Desenha o painel com as informações do item selecionado."""
        pygame.draw.rect(tela, CINZA_ESCURO, self.rect_painel_info)
        if not self.item_selecionado:
            return

        # Nome do Item
        self._desenhar_texto_com_borda(tela, self.item_selecionado.nome_item, self.fonte_botao, BRANCO, PRETO, 1, (self.rect_painel_info.centerx, self.rect_painel_info.top + 30))
        
        # Descrição do Item (com quebra de linha)
        self._draw_text_wrapped(tela, self.item_selecionado.descricao, self.fonte_texto, BRANCO, self.rect_painel_info.inflate(-20, -100))

        # --- NOVO: Lógica de preço e quantidade ---
        if self.modo == 'comprar':
            preco_unitario = self.item_selecionado.preco_de_compra
            preco_total = preco_unitario * self.quantidade_selecionada if preco_unitario else 0
            preco_texto = f"Preço Total: {preco_total} moedas"
        else: # modo 'vender'
            preco_unitario = self.item_selecionado.preco_de_venda
            preco_total = preco_unitario * self.quantidade_selecionada if preco_unitario else 0
            preco_texto = f"Vender por: {preco_total} moedas" if preco_unitario is not None else "Não pode ser vendido"
        
        # Botões e display de quantidade
        pygame.draw.rect(tela, CINZA, self.rect_botao_menos)
        self._desenhar_texto_com_borda(tela, "-", self.fonte_botao, PRETO, BRANCO, 1, self.rect_botao_menos.center)
        
        pygame.draw.rect(tela, CINZA, self.rect_botao_mais)
        self._desenhar_texto_com_borda(tela, "+", self.fonte_botao, PRETO, BRANCO, 1, self.rect_botao_mais.center)
        
        self._desenhar_texto_com_borda(tela, str(self.quantidade_selecionada), self.fonte_botao, BRANCO, PRETO, 1, 
                                       (self.rect_painel_info.centerx, self.rect_botao_menos.centery))

        # Exibe o preço total
        self._desenhar_texto_com_borda(tela, preco_texto, self.fonte_texto, AMARELO, PRETO, 1, (self.rect_painel_info.centerx, self.rect_painel_info.bottom - 10))

    def _draw_buttons(self, tela):
        """Desenha os botões de transação e de voltar."""
        # Botão de Transação
        cor_transacao = VERDE if self.item_selecionado else CINZA_ESCURO
        pygame.draw.rect(tela, cor_transacao, self.rect_botao_transacao)
        texto_botao = "Comprar" if self.modo == 'comprar' else "Vender"
        self._desenhar_texto_com_borda(tela, texto_botao, self.fonte_botao, BRANCO, PRETO, 1, self.rect_botao_transacao.center)
        
        # Botão Voltar
        pygame.draw.rect(tela, VERMELHO, self.rect_botao_voltar)
        self._desenhar_texto_com_borda(tela, "Voltar ao Jogo", self.fonte_botao, BRANCO, PRETO, 1, self.rect_botao_voltar.center)

    def _draw_player_coins(self, tela):
        """Exibe a quantidade de moedas do jogador."""
        texto_moedas = f"Suas Moedas: {self.dados_jogador.moedas_totais}"
        self._desenhar_texto_com_borda(tela, texto_moedas, self.fonte_texto, AMARELO, PRETO, 1, (self.rect_lista_itens.centerx, self.rect_lista_itens.bottom + 30))
            
    def _atualizar_dados_da_tela(self):
        """
        Recarrega todos os dados do jogador e do vendedor do banco de dados
        para garantir que a tela esteja sempre sincronizada.
        """
        print("Sincronizando dados da loja com o banco de dados...")
        self.inventario_vendedor = self.db_manager.buscar_inventario_vendedor(self.vendedor_id, self.entidades.progresso_do_jogo.identificador_progresso)
        self.inventario_jogador = self.db_manager.buscar_inventario(self.entidades.jogador.identificador_jogador, 'moc', self.entidades.progresso_do_jogo.identificador_progresso)
        
        self.entidades.jogador.mochila = self.db_manager.carregar_mochila_do_jogador(
            self.entidades.jogador.identificador_jogador, self.entidades.progresso_do_jogo.identificador_progresso
        )

        self.dados_jogador = self.db_manager.buscar_jogador(self.entidades.jogador.identificador_jogador)
        
        # Reseta a seleção para evitar interações com itens que podem ter sumido
        self._resetar_selecao()