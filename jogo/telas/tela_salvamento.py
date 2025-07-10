# telas/tela_salvamento.py

import pygame
from .tela_modelo import TelaModelo
from utilidades.constantes import *
from gerenciadores import GerenciadorDeEntidades
from entidades import Jogador

class TelaSalvamento(TelaModelo):
    """
    Representa a tela de seleção de espaços de salvamento.
    Contém 3 espaços de salvamento representados por imagens e um botão "Voltar".
    Verifica se os slots estão ocupados com dados estáticos e permite iniciar um
    novo jogo (levando para seleção de personagem) ou carregar um jogo salvo.
    Acessa recursos visuais e fontes via gerenciador de recursos.
    """
    def __init__(self, gerenciador_telas, gerenciador_recursos, gerenciador_banco_de_dados):
        super().__init__(gerenciador_telas, gerenciador_recursos)
        self.gerenciador_entidades = GerenciadorDeEntidades()
        self.banco_de_dados = gerenciador_banco_de_dados

        self.gerenciador_entidades.dados_salvos = gerenciador_banco_de_dados.carregar_dados_dos_slots()

        # --- Recursos específicos da Tela de Salvamento ---
        self.imagem_cartaz_procurado = self.gerenciador_recursos.obter_imagem(CHAVE_CARTAZ_PROCURADO)
        self.imagem_cartaz_procurada = self.gerenciador_recursos.obter_imagem(CHAVE_CARTAZ_PROCURADA)
        self.imagem_cartaz_vazio = self.gerenciador_recursos.obter_imagem(CHAVE_CARTAZ_VAZIO)

        self.fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TITULO)
        self.fonte_botoes = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_BOTAO)
        self.fonte_nome_cartaz = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_PAYFAIR_TEXTO) # Fonte para o nome/tipo no cartaz
        self.fonte_data_cartaz = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_HEART_TEXTO) # Fonte para data/dados no cartaz

        # Imagem de fundo comum para telas de menu
        self.imagem_fundo = self.gerenciador_recursos.obter_imagem(CHAVE_TELA_INICIAL)
        if not self.imagem_fundo:
            self.imagem_fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.imagem_fundo.fill(CINZA_ESCURO) # Fallback

        # --- Configuração visual dos slots de salvamento ---
        # Determina o tamanho base dos slots usando as imagens carregadas (priorizando vazio, depois menino, depois menina)
        largura_img, altura_img = (150, 200) # Tamanho padrão de fallback
        if self.imagem_cartaz_vazio:
             largura_img = self.imagem_cartaz_vazio.get_width()
             altura_img = self.imagem_cartaz_vazio.get_height()
        elif self.imagem_cartaz_procurado: # Tenta usar o tamanho da imagem do menino como fallback
             largura_img = self.imagem_cartaz_procurado.get_width()
             altura_img = self.imagem_cartaz_procurado.get_height()
        elif self.imagem_cartaz_procurada: # Tenta usar o tamanho da imagem da menina como fallback
             largura_img = self.imagem_cartaz_procurada.get_width()
             altura_img = self.imagem_cartaz_procurada.get_height()

        # Cria um fallback visual genérico para quando nenhuma imagem específica estiver disponível para desenhar
        self.cartaz_procurado_fallback_generico = pygame.Surface((largura_img, altura_img))
        self.cartaz_procurado_fallback_generico.fill(CINZA) # Preenche com uma cor de fallback (CINZA deve estar em constantes.py)

        # --- Constantes de Layout da Tela de Salvamento ---
        self._grossura_borda = 2 # Espessura da borda para o texto
        _num_slots = 3 # O número de slots de salvamento a exibir
        _espacamento_horizontal = 30 # Espaço horizontal entre os slots

        # Calcula as posições X e Y para centralizar o bloco de slots na tela
        _largura_total_slots = (_num_slots * largura_img) + ((_num_slots - 1) * _espacamento_horizontal)
        _inicio_x = (LARGURA_TELA - _largura_total_slots) // 2
        _slot_y = (ALTURA_TELA - altura_img) // 2 - 50 # Posiciona um pouco acima do centro vertical

        # Cria os retângulos de colisão/posicionamento para cada slot de salvamento
        self._rect_slot1 = pygame.Rect(_inicio_x, _slot_y, largura_img, altura_img)
        self._rect_slot2 = pygame.Rect(_inicio_x + largura_img + _espacamento_horizontal, _slot_y, largura_img, altura_img)
        self._rect_slot3 = pygame.Rect(_inicio_x + 2 * (largura_img + _espacamento_horizontal), _slot_y, largura_img, altura_img)

        # Armazena os retângulos dos slots em uma lista para fácil acesso
        self._rects_slots = [self._rect_slot1, self._rect_slot2, self._rect_slot3]

        # Botão "Voltar"
        self._rect_botao_voltar = pygame.Rect(
            LARGURA_TELA // 2 - 100, # Centralizado
            ALTURA_TELA - 80,       # Perto da parte inferior da tela
            200, 50                 # Largura e altura do botão
        )
        self._texto_botao_voltar = "Voltar"

    def processar_eventos(self, evento):
        # Chama o handle_input da base para eventos comuns (ex: QUIT)
        super().processar_eventos(evento)

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Clique com o botão esquerdo do mouse
                # Verifica clique nos slots de salvamento
                for i, rect_slot in enumerate(self._rects_slots):
                    if rect_slot.collidepoint(evento.pos):
                        self.gerenciador_entidades.progresso_do_jogo = self.gerenciador_entidades.dados_salvos[i]
                        if self.gerenciador_entidades.progresso_do_jogo.ocupado:
                            print(f"Carregando jogo do Slot {i+1}...\n{self.gerenciador_entidades.progresso_do_jogo}")
                            jogador, mochila_jogador, kit_jogador, ilha, area, id_inventario = self.banco_de_dados.carregar_dados_do_progresso(self.gerenciador_entidades.progresso_do_jogo.identificador_jogador, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

                            self.gerenciador_entidades.jogador = Jogador(
                                gerenciador_banco_de_dados=self.banco_de_dados,
                                gerenciador_recursos=self.gerenciador_recursos,
                                x_inicial=jogador.coordenada_x,
                                y_inicial=jogador.coordenada_y,
                                identificador_jogador=jogador.identificador_jogador,
                                nome=jogador.nome,
                                descricao=jogador.descricao,
                                energia_maxima=jogador.energia_maxima,
                                vida_maxima=jogador.vida_maxima,
                                nivel=jogador.nivel,
                                sorte=jogador.sorte,
                                energia_atual=jogador.energia_atual,
                                vida_atual=jogador.vida_atual,
                                experiencia_atual=jogador.experiencia_atual,
                                moedas=jogador.moedas_totais,
                                orientacao='direita',
                                mochila=mochila_jogador,
                                kit=kit_jogador,
                                id_inventario=id_inventario
                            )
                            
                            self.gerenciador_entidades.ilha_atual = ilha
                            self.gerenciador_entidades.area_atual = area

                            print("progresso_do_jogo:",self.gerenciador_entidades.progresso_do_jogo)
                            
                            self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_CARREGAR_JOGO)
                        else:
                            print(f"Slot {i+1} vazio. Iniciando novo jogo a partir daqui (ou indo para seleção de personagem).")
                            self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_SELECAO_PERSONAGEM) # Ou CHAVE_TRANSICAO_NOVO_JOGO se for direto

                # Verifica clique no botão "Voltar"
                if self._rect_botao_voltar.collidepoint(evento.pos):
                    print("Voltando ao Menu Principal...")
                    self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MENU_PRINCIPAL)
        return None

    def atualizar(self, dt):
        return None

    def desenhar(self, tela):
        # Desenha o fundo
        tela.blit(self.imagem_fundo, (0, 0))

        # Desenha o título da tela
        if self.fonte_titulo:
            self._desenhar_texto_com_borda(
                tela, "Carregar Jogo", self.fonte_titulo, BRANCO, PRETO, self._grossura_borda, (LARGURA_TELA // 2, 80)
            )

        # --- Desenha os slots de salvamento (imagem e textos) ---
        for i, dados_slot in enumerate(self.gerenciador_entidades.dados_salvos):
            rect_slot = self._rects_slots[i] # Obtém o retângulo de posicionamento para este slot

            # --- Seleciona a imagem do cartaz com base no status do slot e tipo de personagem ---
            imagem_a_desenhar = None # Inicializa a variável da imagem a ser desenhada como None

            if dados_slot.ocupado:
                 # Se o slot está ocupado, seleciona a imagem com base no tipo de personagem salvo no dicionário de dados
                 if dados_slot.nome_jogador == SHUAN: # Compara com a constante PERSONAGEM_MENINO
                      imagem_a_desenhar = self.imagem_cartaz_procurado # Usa o atributo que armazena a imagem do cartaz de menino
                 elif dados_slot.nome_jogador == SILVIE: # Compara com a constante PERSONAGEM_MENINA
                      imagem_a_desenhar = self.imagem_cartaz_procurada # Usa o atributo que armazena a imagem do cartaz de menina
                 else:
                      # Se o tipo de personagem salvo for desconhecido nos dados, usa o fallback genérico visual
                      #print(f"AVISO: Tipo de personagem desconhecido '{dados_slot.get('personagem', 'N/A')}' no Slot {i + 1}. Usando fallback genérico para imagem.") # Print de aviso
                      imagem_a_desenhar = self.cartaz_procurado_fallback_generico # Usa o fallback genérico
            # Se o slot não está ocupado (dados_slot.ocupado é False), a imagem a desenhar permanece None inicialmente

            # Se nenhuma imagem específica foi selecionada (slot vazio ou falha no carregamento de imagem específica)
            if imagem_a_desenhar is None:
                 # Usa a imagem de slot vazio se ela foi carregada, caso contrário, usa o fallback genérico.
                 imagem_a_desenhar = self.imagem_cartaz_vazio if self.imagem_cartaz_vazio else self.cartaz_procurado_fallback_generico


            # Desenha a imagem selecionada para o slot
            # Verifica se a imagem_a_desenhar é válida (não None) antes de blitar
            if imagem_a_desenhar:
                tela.blit(imagem_a_desenhar, rect_slot.topleft) # Desenha a imagem no canto superior esquerdo do retângulo do slot
            else:
                # Último recurso visual se nem a imagem de vazio nem o fallback genérico estiverem disponíveis
                print(f"ERRO VISUAL: Nenhuma imagem disponível para desenhar Slot {i + 1}.") # Print de erro
                pygame.draw.rect(tela, VERMELHO, rect_slot) # Desenha um retângulo vermelho como indicador de erro visual


            # --- Desenha os textos do slot ---
            # Verifica se a fonte para o nome/tipo no cartaz está disponível
            if self.fonte_nome_cartaz:
                # O texto principal mostra o tipo de personagem salvo
                texto_principal = dados_slot.nome_jogador.upper() if dados_slot.ocupado else "" # Adapta o texto principal
                superficie_texto_principal = self.fonte_nome_cartaz.render(texto_principal, True, COR_TEXTO_SALVAR) # Renderiza o texto
                # Calcula a posição do retângulo do texto principal (centralizado no slot com offset Y)
                rect_texto_principal = superficie_texto_principal.get_rect(center=(rect_slot.center[0], rect_slot.center[1] + 55))
                tela.blit(superficie_texto_principal, rect_texto_principal) # Desenha o texto principal na tela

                # Texto de dados/hora ou mapa (APENAS se o slot estiver ocupado)
                # Verifica se o slot está ocupado E a fonte para dados está disponível
                if dados_slot.ocupado and self.fonte_data_cartaz:
                     # O texto de dados mostra a data salva (exemplo)
                     texto_dados = dados_slot.data_ultimo_salvamento.strftime('%d/%m/%Y %H:%M') # Pega a data salva ou "Sem Data"
                     # Você pode adicionar mais informações aqui (progresso, mapa, etc.)
                     # texto_dados += f" - Mapa: {dados_slot.get('id_mapa', 'N/A')}"
                     # texto_dados += f" - Progresso: {dados_slot.get('progresso', 'N/A')}"

                     superficie_texto_dados = self.fonte_data_cartaz.render(texto_dados, True, COR_TEXTO_SALVAR) # Renderiza o texto de dados
                     # Calcula a posição do retângulo do texto de dados (centralizado no slot com offset Y maior)
                     rect_texto_dados = superficie_texto_dados.get_rect(center=(rect_slot.center[0] + 5, rect_slot.center[1] + 75))
                     tela.blit(superficie_texto_dados, rect_texto_dados) # Desenha o texto de dados na tela

                # else: se o slot está ocupado mas a fonte de dados não está disponível, um aviso já é impresso.
                # else: se o slot não está ocupado, não desenhamos o texto de dados.

            else:
                 print(f"AVISO: Fonte para textos de slots de salvamento (chave 'nome_cartaz') não disponível para Slot {i + 1}.") # Print de aviso


        # Desenha o botão "Voltar"
        if self.fonte_botoes:
            self._desenhar_texto_com_borda(
                tela, self._texto_botao_voltar, self.fonte_botoes, BRANCO, PRETO, self._grossura_borda, self._rect_botao_voltar.center
            )
        else:
            print("AVISO: Fonte para botão 'Voltar' (chave 'botao') não disponível.")

        # Opcional: desenhar retângulos de colisão para debug
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            for rect_slot in self._rects_slots:
                pygame.draw.rect(tela, COR_CAIXA_COLISAO, rect_slot, 1) # Desenha o contorno do retângulo do slot
            pygame.draw.rect(tela, COR_CAIXA_COLISAO, self._rect_botao_voltar, 1) # Desenha o contorno do botão Voltar