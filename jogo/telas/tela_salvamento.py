# tela_salvamento.py

import pygame
from .tela_modelo import TelaModelo
from utilidades.constantes import *

class TelaSalvamento(TelaModelo):
    """
    Representa a tela de seleção de espaços de salvamento.
    Contém 3 espaços de salvamento representados por imagens e um botão "Voltar".
    Acessa recursos visuais e fontes via gerenciador de recursos.
    """
    # --- Dados estáticos de salvamento (substituir por carregamento real depois) ---
    # Esta lista representa os slots de salvamento.
    # Cada dicionário representa os dados de um slot.
    _dados_salvamento_estatico = [
        {
            'ocupado': True, # True se o slot tem um jogo salvo
            'map_id': MAPA_INICIAL_ID, # O ID do mapa onde o jogo foi salvo
            'character': PERSONAGEM_MENINO, # O tipo de personagem salvo neste slot
            'data_salva': '05/05/2025 13:02', # Data/hora do último salvamento
            'progresso': '30%' # Exemplo de informação de progresso (opcional)
        },
        {
            'ocupado': False, # Slot vazio
            'map_id': None,
            'character': None,
            'data_salva': None, # Texto a exibir para slot vazio
            'progresso': None
        },
         {
            'ocupado': True, # Outro slot salvo
            'map_id': 'outra_ilha', # Exemplo de salvo em outro mapa
            'character': PERSONAGEM_MENINA, # Exemplo de personagem diferente
            'data_salva': '06/05/2025 10:15',
            'progresso': '60%'
        },
    ]

    # Construtor agora recebe APENAS o gerenciador de recursos
    def __init__(self, gerenciador_recursos):
        # Chama o construtor da classe base, passando o gerenciador
        super().__init__(gerenciador_recursos)

        # --- Obtém os recursos necessários do gerenciador ---
        self.imagem_cartaz_procurado = self.gerenciador_recursos.get_image('cartaz_de_procurado')
        self.imagem_cartaz_procurada = self.gerenciador_recursos.get_image('cartaz_de_procurada')
        self.imagem_cartaz_procurado_vazio = self.gerenciador_recursos.get_image('cartaz_de_procurado_vazio')
        
        self.fonte_botoes = self.gerenciador_recursos.get_font('botao')
        self.fonte_grande = self.gerenciador_recursos.get_font('titulo')
        self.fonte_nome_cartaz = self.gerenciador_recursos.get_font('nome_cartaz')
        self.fonte_data_cartaz = self.gerenciador_recursos.get_font('data_cartaz')

        # --- Configuração visual dos slots de salvamento ---
        # Baseia o tamanho na imagem de cartaz VAZIA (ou em um tamanho padrão se todas falharem)
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

        # Não precisamos mais do wanted_poster_fallback localmente se o ResourceManager já fornece None/imagem de erro
        # self.cartaz_procurado_fallback = None

        _num_slots = 3 # Mantém nome comum
        _espacamento_horizontal = 30 # Espaço entre as imagens

        # Calcula a largura total ocupada pelos slots e o espaço entre eles
        _largura_total_slots = (_num_slots * largura_img) + ((_num_slots - 1) * _espacamento_horizontal)
        # Calcula o ponto X inicial para centralizar o bloco de slots horizontalmente
        _inicio_x = (LARGURA_TELA - _largura_total_slots) // 2
        # Calcula a posição Y para centralizar os slots verticalmente, com um pequeno offset para cima
        _slot_y = (ALTURA_TELA - altura_img) // 2 - 50


        # Cria os retângulos de colisão/posicionamento para cada slot
        self._rect_slot1 = pygame.Rect(_inicio_x, _slot_y, largura_img, altura_img)
        self._rect_slot2 = pygame.Rect(_inicio_x + largura_img + _espacamento_horizontal, _slot_y, largura_img, altura_img)
        self._rect_slot3 = pygame.Rect(_inicio_x + 2 * (largura_img + _espacamento_horizontal), _slot_y, largura_img, altura_img)

        # Armazena os retângulos dos slots em uma lista para fácil acesso
        self._rects_slots = [self._rect_slot1, self._rect_slot2, self._rect_slot3]

        # --- Botão "Voltar" ---
        _largura_botao_voltar = 200
        _altura_botao_voltar = 50
        # Calcula a posição e cria o retângulo para o botão Voltar (centralizado embaixo)
        _rect_botao_voltar = pygame.Rect((LARGURA_TELA - _largura_botao_voltar) // 2, ALTURA_TELA - 70, _largura_botao_voltar, _altura_botao_voltar)
        self._rect_botao_voltar = _rect_botao_voltar

        # Texto do botão Voltar
        self._texto_botao_voltar = "Voltar"

        # Espessura da borda do texto para o botão Voltar
        self._espessura_borda = 2


    def handle_event(self, event):
        """
        Processa um evento para a tela de salvamento.
        Verifica cliques nos slots de salvar e no botão "Voltar".
        Retorna um dicionário para iniciar o jogo/seleção de personagem,
        um ID de estado simples (ESTADO_MENU_INICIAL), ou sys.exit para sair.
        Retorna None para continuar na mesma tela.
        """
        proximo_estado = super().handle_event(event)
        if proximo_estado is not None:
             return proximo_estado

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Botão esquerdo do mouse
                posicao_mouse = event.pos

                # Verifica cliques nos slots de salvamento
                for i, rect_slot in enumerate(self._rects_slots): # Itera sobre os retângulos e seus índices (0, 1, 2)
                     if rect_slot.collidepoint(posicao_mouse):
                          print(f"Clicou no Slot {i + 1}") # Print de debug (Slot 1, 2 ou 3)

                          # Obtém os dados estáticos para este slot
                          dados_slot = self._dados_salvamento_estatico[i]

                          if dados_slot['ocupado']:
                               # --- Slot Ocupado: Carregar Jogo ---
                               print("Slot ocupado. Carregando jogo salvo.")
                               # Obtém os dados necessários para iniciar o jogo a partir do slot
                               map_id_salvo = dados_slot['map_id']
                               character_type_salvo = dados_slot['character']
                               # Você também precisaria carregar a posição do jogador, inventário, etc.

                               # Sinaliza para ir para o estado de JOGO, passando o ID do mapa e o tipo de personagem salvos
                               return {'estado': ESTADO_JOGO, 'map_id': map_id_salvo, 'character_type': character_type_salvo}

                          else:
                               # --- Slot Vazio: Iniciar Novo Jogo ---
                               print("Slot vazio. Iniciando novo jogo.")
                               # Sinaliza para ir para a tela de seleção de personagem
                               return ESTADO_SELECAO_PERSONAGEM # Retorna apenas o ID do novo estado

                # Verifica colisão com o retângulo do botão "Voltar"
                if self._rect_botao_voltar.collidepoint(posicao_mouse):
                    print("Clicou em Voltar -> Voltando para o Menu Inicial")
                    return ESTADO_MENU_INICIAL # Retorna apenas o ID do estado do menu inicial


        return None # Continua na mesma tela (TelaSalvamento)

    def draw(self, tela):
        """
        Desenha todos os elementos da tela de salvamento na superfície da tela.
        Desenha o fundo, título, imagens dos slots e textos.
        :param tela: A superfície principal (tela) onde desenhar.
        """
        # Desenha o fundo comum usando o método da classe base (que obtém o fundo do gerenciador)
        super().draw(tela) # <-- Chama o método draw da base

        # --- Desenha os slots de salvamento (imagem e textos) ---
        # Itera sobre os dados estáticos e os retângulos dos slots
        for i, dados_slot in enumerate(self._dados_salvamento_estatico):
            rect_slot = self._rects_slots[i] # Obtém o retângulo correspondente

            # --- Seleciona a imagem do cartaz com base no status do slot e personagem ---
            imagem_a_desenhar = None # Inicializa como None

            if dados_slot['ocupado']:
                 # Se o slot está ocupado, seleciona a imagem com base no tipo de personagem salvo
                 if dados_slot['character'] == PERSONAGEM_MENINO:
                      imagem_a_desenhar = self.imagem_cartaz_procurado
                 elif dados_slot['character'] == PERSONAGEM_MENINA:
                      imagem_a_desenhar = self.imagem_cartaz_procurada
                 else:
                      # Fallback se o tipo de personagem salvo for desconhecido
                      print(f"AVISO: Tipo de personagem desconhecido '{dados_slot['character']}' no Slot {i + 1}. Usando cartaz vazio.")
                      imagem_a_desenhar = self.imagem_cartaz_procurado_vazio # Usa a imagem de slot vazio como fallback

            else:
                 # Se o slot está vazio, usa a imagem de slot vazio
                 imagem_a_desenhar = self.imagem_cartaz_procurado_vazio

            # --- Desenha a imagem selecionada no slot ---
            if imagem_a_desenhar: # Verifica se alguma imagem válida foi selecionada/carregada
                 tela.blit(imagem_a_desenhar, rect_slot.topleft)
            else:
                 # Fallback final visual se nenhuma imagem (nem mesmo a de vazio) foi carregada
                 print(f"AVISO: Nenhuma imagem de cartaz disponível para Slot {i + 1}. Desenhando retângulo simples.")
                 pygame.draw.rect(tela, CINZA, rect_slot)

            # --- Desenha os textos do slot ---
            if self.fonte_nome_cartaz: # Verifica se a fonte principal dos slots está disponível
                # Texto principal do slot ("Arquivo X" ou "Slot Vazio")
                texto_principal = dados_slot['character'] if dados_slot['ocupado'] else "Slot Vazio" # Adapta o texto
                superficie_texto_principal = self.fonte_nome_cartaz.render(texto_principal, True, COR_TEXTO_SALVAR)
                rect_texto_principal = superficie_texto_principal.get_rect(center=(rect_slot.center[0], rect_slot.center[1] + 55)) # Posição ajustada
                tela.blit(superficie_texto_principal, rect_texto_principal)

                # Texto de dados/hora (APENAS se o slot estiver ocupado)
                if dados_slot['ocupado'] and self.fonte_data_cartaz: # Verifica se o slot está ocupado E a fonte de dados está disponível
                     texto_dados = dados_slot['data_salva'] # Exibe o ID do mapa salvo (exemplo)
                     # Você pode adicionar mais informações aqui (progresso, etc.)
                     # texto_dados += f" - Progresso: {dados_slot.get('progresso', 'N/A')}"

                     superficie_texto_dados = self.fonte_data_cartaz.render(texto_dados, True, COR_TEXTO_SALVAR)
                     rect_texto_dados = superficie_texto_dados.get_rect(center=(rect_slot.center[0], rect_slot.center[1] + 75)) # Posição ajustada (abaixo do texto principal)
                     tela.blit(superficie_texto_dados, rect_texto_dados)
                elif dados_slot['ocupado'] and not self.fonte_data_cartaz:
                     print(f"AVISO: Fonte para dados de slots ({i + 1}) não disponível, mas slot ocupado.")


            else:
                 print(f"AVISO: Fonte para textos de slots de salvamento ({i + 1}) não disponível.")

        # --- Desenha o botão "Voltar" com borda ---
        # Usa a fonte para botões (obtida do gerenciador e armazenada em atributo)
        if self.fonte_botoes: # Verifica se a fonte está disponível
             # Chama o método auxiliar de desenho de texto com borda da classe base
             self._desenhar_texto_com_borda(
                 tela, # Superfície onde desenhar
                 self._texto_botao_voltar, # Texto
                 self.fonte_botoes, # Fonte
                 BRANCO, PRETO, # Cores
                 self._espessura_borda, # Espessura da borda
                 self._rect_botao_voltar.center # Posição central
             )
        else:
             print("AVISO: Fonte para botão 'Voltar' não disponível.")


        # Opcional: desenhar retângulos de colisão para debug
        # Verifica se a flag de debug de colisão está ativa (obtida das constantes)
        # if DEBUG_DESENHAR_CAIXAS_COLISAO:
        #    pygame.draw.rect(tela, VERMELHO, self._rect_slot1, 1) # Desenha contorno
        #    pygame.draw.rect(tela, VERMELHO, self._rect_slot2, 1) # Desenha contorno
        #    pygame.draw.rect(tela, VERMELHO, self._rect_slot3, 1) # Desenha contorno
        #    pygame.draw.rect(tela, VERMELHO, self._rect_botao_voltar, 1) # Desenha contorno