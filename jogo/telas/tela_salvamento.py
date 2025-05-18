# telas/tela_salvamento.py

import pygame
from .tela_modelo import TelaModelo
from utilidades.constantes import *

class TelaSalvamento(TelaModelo):
    """
    Representa a tela de seleção de espaços de salvamento.
    Contém 3 espaços de salvamento representados por imagens e um botão "Voltar".
    Verifica se os slots estão ocupados com dados estáticos e permite iniciar um
    novo jogo (levando para seleção de personagem) ou carregar um jogo salvo.
    Acessa recursos visuais e fontes via gerenciador de recursos.
    """
    # --- Dados estáticos de salvamento (substituir por carregamento real depois) ---
    # Esta lista representa os slots de salvamento.
    # Cada dicionário representa os dados de um slot salvo.
    # Incluímos 'coordenada_x', 'coordenada_y', 'olhando_para_direita' para simular dados salvos.
    _dados_salvamento_estatico = [
        {
            'ocupado': True, # Indica que este slot tem dados salvos
            'id_mapa': ID_MAPA_CAMPO_VILA, # O ID do mapa onde o jogo foi salvo
            'personagem': PERSONAGEM_MENINO, # O tipo de personagem salvo neste slot
            'data_salva': '05/05/2025 13:02', # Data/hora do último salvamento (para exibição)
            'progresso': '30%', # Exemplo de informação de progresso (opcional)
            # Adicionamos as coordenadas e orientação salvas (mundo do jogo)
            'coordenada_x': 200, # <-- Posição X salva
            'coordenada_y': 400, # <-- Posição Y salva
            'olhando_para_direita': True # <-- Orientação salva (True ou False)
        },
        {
            'ocupado': False, # Indica que este slot está vazio
            'id_mapa': None,
            'personagem': None,
            'data_salva': 'Slot Vazio', # Texto a exibir para slot vazio
            'progresso': None,
            'coordenada_x': None, # Posição salva é None para slot vazio
            'coordenada_y': None,
            'olhando_para_direita': None
        },
         {
            'ocupado': True, # Outro slot salvo
            'id_mapa': ID_MAPA_NEVE_VILA, # Exemplo de salvo no mapa inicial novamente
            'personagem': PERSONAGEM_MENINA, # Exemplo de personagem diferente
            'data_salva': '06/05/2025 10:15',
            'progresso': '60%',
             # Adicionamos as coordenadas e orientação salvas para este slot
            'coordenada_x': 200, # <-- Posição X salva
            'coordenada_y': 400, # <-- Posição Y salva
            'olhando_para_direita': False # <-- Orientação salva
        },
    ]

    # Construtor da Tela de Salvamento
    def __init__(self, gerenciador_recursos):
        # Chama o construtor da classe base (TelaModelo), passando o gerenciador
        super().__init__(gerenciador_recursos)

        # --- Obtém os recursos de imagem necessários do gerenciador ---
        # Usamos as chaves que você definiu para as imagens dos cartazes de procurado
        self.imagem_cartaz_procurado = self.gerenciador_recursos.get_image(CHAVE_CARTAZ_PROCURADO)
        self.imagem_cartaz_procurada = self.gerenciador_recursos.get_image(CHAVE_CARTAZ_PROCURADA)
        self.imagem_cartaz_procurado_vazio = self.gerenciador_recursos.get_image(CHAVE_CARTAZ_VAZIO)

        # --- Obtém os recursos de fonte necessários do gerenciador ---
        # Usamos as chaves que você definiu para as fontes
        self.fonte_botoes = self.gerenciador_recursos.get_font(CHAVE_FONTE_BOTAO)       # Fonte para botões como "Voltar"
        self.fonte_grande = self.gerenciador_recursos.get_font(CHAVE_FONTE_TITULO)     # Fonte para títulos grandes
        self.fonte_nome_cartaz = self.gerenciador_recursos.get_font(CHAVE_FONTE_NOME_CARTAZ) # Fonte para o nome/tipo no cartaz
        self.fonte_data_cartaz = self.gerenciador_recursos.get_font(CHAVE_FONTE_DATA_CARTAZ) # Fonte para data/dados no cartaz


        # --- Configuração visual dos slots de salvamento ---
        # Determina o tamanho base dos slots usando as imagens carregadas (priorizando vazio, depois menino, depois menina)
        largura_img, altura_img = (150, 200) # Tamanho padrão de fallback
        if self.imagem_cartaz_procurado_vazio:
             largura_img = self.imagem_cartaz_procurado_vazio.get_width()
             altura_img = self.imagem_cartaz_procurado_vazio.get_height()
        elif self.imagem_cartaz_procurado: # Tenta usar o tamanho da imagem do menino como fallback
             largura_img = self.imagem_cartaz_procurado.get_width()
             altura_img = self.imagem_cartaz_procurado.get_height()
        elif self.imagem_cartaz_procurada: # Tenta usar o tamanho da imagem da menina como fallback
             largura_img = self.imagem_cartaz_procurada.get_width()
             altura_img = self.imagem_cartaz_procurada.get_height()

        # Cria um fallback visual genérico para quando nenhuma imagem específica estiver disponível para desenhar
        self.cartaz_procurado_fallback_generico = pygame.Surface((largura_img, altura_img))
        self.cartaz_procurado_fallback_generico.fill(CINZA) # Preenche com uma cor de fallback (CINZA deve estar em constantes.py)


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

        # --- Botão "Voltar" ---
        _largura_botao_voltar = 200
        _altura_botao_voltar = 50
        # Calcula a posição e cria o retângulo para o botão Voltar (centralizado na parte inferior)
        _rect_botao_voltar = pygame.Rect((LARGURA_TELA - _largura_botao_voltar) // 2, ALTURA_TELA - 70, _largura_botao_voltar, _altura_botao_voltar)
        self._rect_botao_voltar = _rect_botao_voltar

        # Texto do botão Voltar
        self._texto_botao_voltar = "Voltar"

        # Espessura da borda do texto para o botão Voltar
        self._espessura_borda = 2 # Mantém nome comum

    def handle_event(self, event):
        """
        Processa um evento para a tela de salvamento.
        Verifica cliques nos slots de salvar e no botão "Voltar".
        Se o slot for vazio, retorna o estado para a seleção de personagem.
        Se tiver dados, retorna um dicionário para carregar o jogo salvo,
        incluindo o mapa, personagem, e dados de posição/orientação salvos.
        Retorna um ID de estado simples (ESTADO_MENU_INICIAL) ou sys.exit para sair.
        Retorna None para continuar na mesma tela.
        """
        # Chama o manipulador de eventos da classe base (para eventos comuns, ex: fechar janela, ESC se implementado na base)
        proximo_estado = super().handle_event(event)
        # Se a base já tratou o evento e retornou um estado, retorna-o imediatamente
        if proximo_estado is not None:
             return proximo_estado

        # Lógica específica da Tela de Salvamento para eventos de mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Verifica se o botão clicado foi o botão esquerdo (botão 1)
                posicao_mouse = event.pos

                # Verifica cliques nos slots de salvamento
                # Itera sobre a lista de retângulos dos slots e seus índices (0 para slot1, 1 para slot2, 2 para slot3)
                for i, rect_slot in enumerate(self._rects_slots):
                     if rect_slot.collidepoint(posicao_mouse): # Verifica se a posição do mouse colide com o retângulo do slot
                          print(f"Clicou no Slot {i + 1}") # Print de debug (Slot 1, 2 ou 3)

                          # Obtém os dados estáticos correspondentes a este slot clicado
                          dados_slot = self._dados_salvamento_estatico[i]

                          if dados_slot['ocupado']:
                               # --- Slot Ocupado: Carregar Jogo ---
                               print("Slot ocupado. Carregando jogo salvo.") # Print de debug
                               # Extrai os dados necessários do dicionário salvo
                               # Usa .get() com um valor padrão para evitar KeyError se uma chave estiver faltando
                               id_mapa_salvo = dados_slot.get('id_mapa', ID_MAPA_CAMPO_VILA) # Pega o ID do mapa salvo, ou usa o inicial como padrão
                               tipo_personagem_salvo = dados_slot.get('personagem', PERSONAGEM_MENINA) # Pega o tipo de personagem salvo, ou usa a menina como padrão
                               # Obtém as coordenadas e orientação salvas dos dados do slot
                               coordenada_x = dados_slot.get('coordenada_x') # <-- Obtém a posição X salva (pode ser None)
                               coordenada_y = dados_slot.get('coordenada_y') # <-- Obtém a posição Y salva (pode ser None)
                               olhando_para_direita = dados_slot.get('olhando_para_direita') # <-- Obtém a orientação salva (pode ser None)


                               # Sinaliza para o loop principal em main.py que deve mudar de estado.
                               # Retorna um dicionário contendo:
                               # 'estado': O estado para onde ir (ESTADO_JOGO)
                               # 'id_mapa': O ID do mapa para carregar
                               # 'tipo_personagem': O tipo de personagem a ser carregado
                               # 'coordenada_x', 'coordenada_y', 'olhando_para_direita': Os dados de posição/orientação salvos (podem ser None)
                               # Note: Não incluímos 'ponto_entrada_destino_id' aqui, pois estamos carregando de um save, não entrando por um ponto específico de transição de área.
                               return {'estado': ESTADO_JOGO,
                                       'id_mapa': id_mapa_salvo,
                                       'tipo_personagem': tipo_personagem_salvo,
                                       'coordenada_x': coordenada_x, # <-- Inclui a posição X salva no dicionário retornado
                                       'coordenada_y': coordenada_y, # <-- Inclui a posição Y salva no dicionário retornado
                                       'olhando_para_direita': olhando_para_direita} # <-- Inclui a orientação salva no dicionário retornado


                          else:
                               # --- Slot Vazio: Iniciar Novo Jogo ---
                               print("Slot vazio. Iniciando novo jogo.") # Print de debug
                               # Sinaliza para o loop principal que deve ir para a tela de seleção de personagem.
                               # A tela de seleção de personagem, ao iniciar o jogo, definirá o ponto de entrada inicial ('inicio_novo_jogo').
                               return ESTADO_SELECAO_PERSONAGEM # Retorna apenas o ID do novo estado


                # Verifica colisão com o retângulo do botão "Voltar"
                if self._rect_botao_voltar.collidepoint(posicao_mouse):
                    print("Clicou em Voltar -> Voltando para o Menu Inicial") # Print de debug
                    # O botão "Voltar" não precisa passar dados adicionais, apenas sinaliza para voltar para o menu inicial.
                    return ESTADO_MENU_INICIAL # Retorna apenas o ID do estado do menu inicial


        # Se nenhum evento tratado nesta tela causou uma mudança de estado, retorna None
        return None # Continua na mesma tela (TelaSalvamento)

    def draw(self, tela):
        """
        Desenha todos os elementos da tela de salvamento na superfície da tela.
        Desenha o fundo, título, imagens dos slots (adaptadas pelo tipo de personagem salvo)
        e textos (adaptados se o slot está vazio).
        :param tela: A superfície principal (tela) onde desenhar.
        """
        # Desenha o fundo comum usando o método da classe base (que obtém o fundo do gerenciador)
        super().draw(tela) # <-- Chama o método draw da base

        # --- Desenha o título da tela ---
        # if self.fonte_grande: # Verifica se a fonte grande (chave 'titulo') foi carregada
        #     texto_titulo_surface = self.fonte_grande.render("Escolha um Espaço de Save", True, BRANCO) # Renderiza o texto do título
        #     rect_titulo = texto_titulo_surface.get_rect(center=(LARGURA_TELA // 2, 100)) # Centraliza o retângulo do título na parte superior
        #     tela.blit(texto_titulo_surface, rect_titulo) # Desenha o título na tela
        # else:
        #      print("AVISO: Fonte grande (chave 'titulo') não disponível para título da tela de salvamento.") # Print de aviso

        # --- Desenha os slots de salvamento (imagem e textos) ---
        # Itera sobre os dados estáticos de salvamento e os retângulos dos slots correspondentes
        for i, dados_slot in enumerate(self._dados_salvamento_estatico):
            rect_slot = self._rects_slots[i] # Obtém o retângulo de posicionamento para este slot

            # --- Seleciona a imagem do cartaz com base no status do slot e tipo de personagem ---
            imagem_a_desenhar = None # Inicializa a variável da imagem a ser desenhada como None

            if dados_slot['ocupado']:
                 # Se o slot está ocupado, seleciona a imagem com base no tipo de personagem salvo no dicionário de dados
                 if dados_slot['personagem'] == PERSONAGEM_MENINO: # Compara com a constante PERSONAGEM_MENINO
                      imagem_a_desenhar = self.imagem_cartaz_procurado # Usa o atributo que armazena a imagem do cartaz de menino
                 elif dados_slot['personagem'] == PERSONAGEM_MENINA: # Compara com a constante PERSONAGEM_MENINA
                      imagem_a_desenhar = self.imagem_cartaz_procurada # Usa o atributo que armazena a imagem do cartaz de menina
                 else:
                      # Se o tipo de personagem salvo for desconhecido nos dados, usa o fallback genérico visual
                      print(f"AVISO: Tipo de personagem desconhecido '{dados_slot.get('personagem', 'N/A')}' no Slot {i + 1}. Usando fallback genérico para imagem.") # Print de aviso
                      imagem_a_desenhar = self.cartaz_procurado_fallback_generico # Usa o fallback genérico
            # Se o slot não está ocupado (dados_slot['ocupado'] é False), a imagem a desenhar permanece None inicialmente

            # Se nenhuma imagem específica foi selecionada (slot vazio ou falha no carregamento de imagem específica)
            if imagem_a_desenhar is None:
                 # Usa a imagem de slot vazio se ela foi carregada, caso contrário, usa o fallback genérico.
                 imagem_a_desenhar = self.imagem_cartaz_procurado_vazio if self.imagem_cartaz_procurado_vazio else self.cartaz_procurado_fallback_generico


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
                # O texto principal mostra o tipo de personagem salvo ou "Slot Vazio"
                texto_principal = dados_slot.get('personagem', "Slot Vazio") if dados_slot['ocupado'] else "Slot Vazio" # Adapta o texto principal
                superficie_texto_principal = self.fonte_nome_cartaz.render(texto_principal, True, COR_TEXTO_SALVAR) # Renderiza o texto
                # Calcula a posição do retângulo do texto principal (centralizado no slot com offset Y)
                rect_texto_principal = superficie_texto_principal.get_rect(center=(rect_slot.center[0], rect_slot.center[1] + 55))
                tela.blit(superficie_texto_principal, rect_texto_principal) # Desenha o texto principal na tela

                # Texto de dados/hora ou mapa (APENAS se o slot estiver ocupado)
                # Verifica se o slot está ocupado E a fonte para dados está disponível
                if dados_slot['ocupado'] and self.fonte_data_cartaz:
                     # O texto de dados mostra a data salva (exemplo)
                     texto_dados = dados_slot.get('data_salva', 'Sem Data') # Pega a data salva ou "Sem Data"
                     # Você pode adicionar mais informações aqui (progresso, mapa, etc.)
                     # texto_dados += f" - Mapa: {dados_slot.get('id_mapa', 'N/A')}"
                     # texto_dados += f" - Progresso: {dados_slot.get('progresso', 'N/A')}"

                     superficie_texto_dados = self.fonte_data_cartaz.render(texto_dados, True, COR_TEXTO_SALVAR) # Renderiza o texto de dados
                     # Calcula a posição do retângulo do texto de dados (centralizado no slot com offset Y maior)
                     rect_texto_dados = superficie_texto_dados.get_rect(center=(rect_slot.center[0], rect_slot.center[1] + 75))
                     tela.blit(superficie_texto_dados, rect_texto_dados) # Desenha o texto de dados na tela

                # else: se o slot está ocupado mas a fonte de dados não está disponível, um aviso já é impresso.
                # else: se o slot não está ocupado, não desenhamos o texto de dados.

            else:
                 print(f"AVISO: Fonte para textos de slots de salvamento (chave 'nome_cartaz') não disponível para Slot {i + 1}.") # Print de aviso


        # --- Desenha o botão "Voltar" com borda ---
        # Usa a fonte para botões (obtida do gerenciador e armazenada em atributo)
        if self.fonte_botoes: # Verifica se a fonte está disponível (chave 'botao')
             # Chama o método auxiliar de desenho de texto com borda da classe base (TelaModelo)
             self._desenhar_texto_com_borda(
                 tela, # Superfície onde desenhar
                 self._texto_botao_voltar, # Texto ("Voltar")
                 self.fonte_botoes, # Fonte para botões
                 BRANCO, PRETO, # Cores do texto e borda (constantes traduzidas)
                 self._espessura_borda, # Espessura da borda
                 self._rect_botao_voltar.center # Posição central do retângulo do botão Voltar
             )
        else:
             print("AVISO: Fonte para botão 'Voltar' (chave 'botao') não disponível.") # Print de aviso


        # Opcional: desenhar retângulos de colisão para debug
        # Verifica se a flag de debug de colisão está ativa (obtida das constantes)
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
             # Itera sobre os retângulos dos slots para desenhar seus contornos
             for rect_slot in self._rects_slots:
                 pygame.draw.rect(tela, VERMELHO, rect_slot, 1) # Desenha o contorno do retângulo do slot
             # Desenha o contorno do retângulo do botão Voltar
             pygame.draw.rect(tela, VERMELHO, self._rect_botao_voltar, 1)


# Exemplo de uso (não executado diretamente neste arquivo)
# if __name__ == '__main__':
#    # Código de teste para esta tela específica (requer Pygame, GerenciadorDeRecursos, etc.)
#    pass