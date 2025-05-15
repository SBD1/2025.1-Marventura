# tela_de_jogo.py

import pygame
import sys
from utilidades.constantes import *
from entidades import Jogador
from entidades import Obstaculo
from entidades import AreaInteracao
from mapa_dados import get_mapa_data

class TelaJogo:
    """
    Representa a tela principal do jogo.
    Onde a jogabilidade acontece para um mapa específico.
    Carrega e exibe elementos do mapa com base nos dados.
    """
    # O construtor agora recebe o ID do mapa a ser carregado
    def __init__(self, gerenciador_recursos, map_id, character_type):
        self.gerenciador_recursos = gerenciador_recursos
        self.map_id = map_id # <-- Armazena o ID do mapa atual
        self.character_type = character_type

        # --- Carregar Dados do Mapa ---
        self.mapa_data = get_mapa_data(self.map_id) # <-- Obtém os dados do mapa usando a função
        if self.mapa_data is None:
            print(f"ERRO FATAL: Dados para o mapa ID '{self.map_id}' não encontrados.")
            # Em um jogo real, você provavelmente voltaria para o menu ou exibiria um erro.
            # Por enquanto, podemos sair ou definir dados de fallback.
            # Vamos definir dados mínimos para evitar crashes, mas o jogo não funcionará corretamente.
            self.mapa_data = {
                'background_key': None,
                'player_start_x': 100,
                'player_start_y': 100,
                'obstaculos': [],
                'areas_interacao': [], # <-- Adiciona fallback para areas_interacao
                'npcs': [],
                'inimigos': []
            }


        # --- Configurar Fundo do Jogo ---
        # Obtém a chave da imagem de fundo dos dados do mapa
        background_key = self.mapa_data.get('background_key')
        if background_key:
             self.fundo_jogo = self.gerenciador_recursos.get_image(background_key)
        else:
             self.fundo_jogo = None # Não há chave de fundo ou carregamento falhou


        # Verifica se a imagem de fundo foi carregada com sucesso e obtém suas dimensões
        if self.fundo_jogo is None:
             print(f"ERRO: Imagem de fundo para o mapa '{self.map_id}' não carregada ou chave inválida.")
             self.largura_fundo = LARGURA_TELA
             self.altura_fundo = ALTURA_TELA
             self.fundo_jogo_fallback = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
             self.fundo_jogo_fallback.fill(VERMELHO) # Fallback visual
        else:
            self.largura_fundo = self.fundo_jogo.get_width()
            self.altura_fundo = self.fundo_jogo.get_height()
            self.fundo_jogo_fallback = None # Não precisa de fallback se o fundo carregou


        # Obtém a fonte grande (continua a ser um recurso comum)
        self.fonte_grande = self.gerenciador_recursos.get_font('titulo')


        # Variáveis para controle da câmera (scroll)
        self.camera_x = 0
        self.velocidade_scroll = 10 # Pode se tornar um dado do mapa se quiser velocidades diferentes

        # --- Criação do Jogador ---
        # Posição inicial do jogador baseada nos dados do mapa
        jogador_inicio_x = self.mapa_data.get('player_start_x', 100) # Use 100 como padrão se não estiver nos dados
        jogador_inicio_y = self.mapa_data.get('player_start_y', 370) # Use 370 como padrão

        self.jogador = Jogador(self.gerenciador_recursos, jogador_inicio_x, jogador_inicio_y, self.character_type)

        # Grupo de sprites para gerenciar o jogador e outros elementos visíveis
        self.todos_sprites = pygame.sprite.Group()
        self.todos_sprites.add(self.jogador)

        # --- Grupo para os obstáculos/limites de caminho ---
        self.obstaculos_caminho = pygame.sprite.Group()

        # --- Definição dos limites de caminho como obstáculos (baseado nos dados do mapa) ---
        obstaculos_data = self.mapa_data.get('obstaculos', []) # Obtém a lista de obstáculos dos dados do mapa
        for obstaculo_info in obstaculos_data:
             # Cria uma instância de Obstaculo para cada item na lista de dados
             # As chaves no dicionário obstaculo_info ('x', 'y', 'largura', 'altura')
             # devem corresponder aos parâmetros do construtor de Obstaculo.
             x = obstaculo_info.get('x', 0)
             y = obstaculo_info.get('y', 0)
             largura = obstaculo_info.get('largura', 1)
             altura = obstaculo_info.get('altura', 1)
             # Opcional: obter chave_imagem se os obstáculos tiverem imagens específicas
             # chave_imagem_obstaculo = obstaculo_info.get('image_key')

             # Cria o obstáculo e adiciona ao grupo
             self.obstaculos_caminho.add(Obstaculo(self.gerenciador_recursos, x, y, largura, altura)) # Pode adicionar chave_imagem_obstaculo aqui se necessário

          # --- Grupo para as áreas de interação ---
        self.areas_interacao = pygame.sprite.Group() # <-- Novo grupo para áreas de interação

        # --- Definição das áreas de interação (baseado nos dados do mapa) ---
        areas_interacao_data = self.mapa_data.get('areas_interacao', []) # Obtém a lista de áreas de interação
        for area_info in areas_interacao_data:
            x = area_info.get('x', 0)
            y = area_info.get('y', 0)
            largura = area_info.get('largura', 1)
            altura = area_info.get('altura', 1)
            tipo_evento = area_info.get('tipo_evento', 'desconhecido') # Tipo de evento
            dados_evento = area_info.get('dados_evento', {})          # Dados do evento

            # Cria a instância da Área de Interação e adiciona ao grupo
            self.areas_interacao.add(AreaInteracao(x, y, largura, altura, tipo_evento, dados_evento, self.gerenciador_recursos)) # Passa resource_manager se AreaInteracao precisar

        # --- Variáveis para rastrear áreas de interação ativas ---
        self.areas_interacao_colididas = [] # Lista das áreas de interação onde o jogador está colidindo

        # --- Carregar o ícone de interação (balão de fala) ---
        self.icone_interacao = self.gerenciador_recursos.get_image(ICONE_INTERACAO_KEY) # Chave do constante

        # --- Criação de NPCs e Inimigos (baseado nos dados do mapa) ---
        # Estes grupos precisariam ser criados e preenchidos aqui, similar aos obstáculos.
        # self.npcs = pygame.sprite.Group()
        # self.inimigos = pygame.sprite.Group()

        # npcs_data = self.mapa_data.get('npcs', [])
        # for npc_info in npcs_data:
        #    tipo_npc = npc_info.get('tipo')
        #    npc_x = npc_info.get('x', 0)
        #    npc_y = npc_info.get('y', 0)
        #    # Cria a instância do NPC com base no tipo e dados, e adiciona ao grupo self.npcs
        #    # Ex: if tipo_npc == 'npc_aldeao': self.npcs.add(NpcAldeao(self.gerenciador_recursos, npc_x, npc_y, npc_info))


        # inimigos_data = self.mapa_data.get('inimigos', [])
        # for inimigo_info in inimigos_data:
        #    tipo_inimigo = inimigo_info.get('tipo')
        #    inimigo_x = inimigo_info.get('x', 0)
        #    inimigo_y = inimigo_info.get('y', 0)
        #    # Cria a instância do Inimigo com base no tipo e dados, e adiciona ao grupo self.inimigos
        #    # Ex: if tipo_inimigo == 'inimigo_goblin': self.inimigos.add(InimigoGoblin(self.gerenciador_recursos, inimigo_x, inimigo_y, inimigo_info))

        # Adicionar outros grupos de sprites (projéteis, itens, etc.)
        # self.projeteis = pygame.sprite.Group()
        # self.itens = pygame.sprite.Group()


    def handle_event(self, event):
        """
        Processa um evento de entrada (teclado, mouse) para a tela de jogo.
        Delega eventos de movimento para o jogador. Trata eventos específicos da tela (ex: ESC, Interação).
        Retorna o ID do próximo estado ou None.
        """
        # Passa o evento para o objeto jogador
        self.jogador.handle_event(event)

        # --- Lógica específica da Tela de Jogo ---
        if event.type == pygame.KEYDOWN:
            # Se a tecla ESC foi pressionada
            if event.key == pygame.K_ESCAPE:
                print("Pressionou ESC -> Voltando para o Menu Inicial")
                return ESTADO_MENU_INICIAL

            # --- Verifica se a tecla de interação foi pressionada ---
            if event.key == TECLA_INTERACAO: # Constante da tecla de interação
                # Verifica se o jogador está colidindo com alguma área de interação
                if self.areas_interacao_colididas:
                     # Pega a primeira área de interação na lista de colisões (simplificado)
                     area_ativa = self.areas_interacao_colididas[0]
                     print(f"Interagindo com área de tipo: {area_ativa.tipo_evento}") # Print de debug

                     # --- Aciona o evento com base no tipo ---
                     if area_ativa.tipo_evento == 'mudar_mapa':
                         # Obtém o ID do próximo mapa dos dados do evento
                         proximo_mapa_id = area_ativa.dados_evento.get('proximo_mapa_id')
                         if proximo_mapa_id:
                             print(f"Mudando para o mapa: {proximo_mapa_id}")
                             # Sinaliza para mudar para o estado de JOGO, mas com o novo ID do mapa
                             # O main.py precisará saber qual mapa carregar.
                             # Uma forma é retornar um valor especial ou um dicionário:
                             return {'estado': ESTADO_JOGO, 'map_id': proximo_mapa_id, 'character_type': self.character_type}

                         else:
                             print("ERRO: Área de interação 'mudar_mapa' sem 'proximo_mapa_id' nos dados.")

                     elif area_ativa.tipo_evento == 'dialogo':
                          dialogo_key = area_ativa.dados_evento.get('dialogo_key')
                          if dialogo_key:
                              print(f"Acionando diálogo com chave: {dialogo_key}")
                              # Lógica para iniciar um sistema de diálogo:
                              # Mudar o estado do jogo para ESTADO_DIALOGO (se tiver)
                              # Exibir a caixa de diálogo com o texto correspondente à chave
                              # return ESTADO_DIALOGO # Se tiver estado de diálogo
                          else:
                              print("ERRO: Área de interação 'dialogo' sem 'dialogo_key' nos dados.")

                     elif area_ativa.tipo_evento == 'comprar_item':
                          item_id = area_ativa.dados_evento.get('item_id')
                          preco = area_ativa.dados_evento.get('preco')
                          if item_id and preco is not None:
                               print(f"Acionando compra de item: {item_id} por {preco}")
                               # Lógica para sistema de loja/compra:
                               # Verificar dinheiro do jogador
                               # Exibir UI de compra/confirmacao
                               # return ESTADO_LOJA # Se tiver estado de loja
                          else:
                              print("ERRO: Área de interação 'comprar_item' com dados inválidos (item_id ou preco).")

                     # Adicione outros tipos de eventos aqui (usar item, ativar mecanismo, etc.)

                # else: Tecla de interação pressionada, mas não colidindo com nenhuma área de interação.


        return None # Continua na mesma tela


    def update(self):
        """
        Atualiza o estado de todos os elementos do jogo a cada frame.
        Inclui a atualização do jogador, checagem de colisões e movimentação da câmera.
        """
        # Atualizar a posição e animação do jogador
        self.jogador.update()

        # --- Checagem de Overlap com Áreas de Interação ---
        # Verifica quais áreas de interação o jogador está atualmente sobrepondo (colidindo)
        # False = não remove as áreas do grupo ao colidir
        self.areas_interacao_colididas = pygame.sprite.spritecollide(self.jogador, self.areas_interacao, False) # <-- Atualiza a lista de áreas ativas

        # --- Implementação de Colisão com Deslize (AABB) ---
        # Calcular o movimento desejado com base nas flags do jogador
        delta_x = 0
        delta_y = 0
        if self.jogador.movendo_esquerda:
             delta_x -= self.jogador.velocidade
        if self.jogador.movendo_direita:
             delta_x += self.jogador.velocidade
        if self.jogador.movendo_cima:
             delta_y -= self.jogador.velocidade
        if self.jogador.movendo_baixo:
             delta_y += self.jogador.velocidade

        # --- Tentar mover no eixo X ---
        self.jogador.mundo_x += delta_x
        self.jogador.rect.x = self.jogador.mundo_x

        # --- Verificar e Resolver Colisão no Eixo X ---
        obstaculos_colididos_x = pygame.sprite.spritecollide(self.jogador, self.obstaculos_caminho, False)

        if obstaculos_colididos_x:
             for obstaculo in obstaculos_colididos_x:
                  if delta_x > 0: # Movendo para a direita
                       self.jogador.mundo_x = obstaculo.rect.left - self.jogador.rect.width
                  elif delta_x < 0: # Movendo para a esquerda
                       self.jogador.mundo_x = obstaculo.rect.right

                  self.jogador.rect.x = self.jogador.mundo_x
                  break # Corrigiu a posição X para a primeira colisão encontrada


        # --- Tentar mover no eixo Y ---
        self.jogador.mundo_y += delta_y
        self.jogador.rect.y = self.jogador.mundo_y

        # --- Verificar e Resolver Colisão no Eixo Y ---
        obstaculos_colididos_y = pygame.sprite.spritecollide(self.jogador, self.obstaculos_caminho, False)

        if obstaculos_colididos_y:
             for obstaculo in obstaculos_colididos_y:
                  if delta_y > 0: # Movendo para baixo
                       self.jogador.mundo_y = obstaculo.rect.top - self.jogador.rect.height
                  elif delta_y < 0: # Movendo para cima
                       self.jogador.mundo_y = obstaculo.rect.bottom

                  self.jogador.rect.y = self.jogador.mundo_y
                  break # Corrigiu a posição Y para a primeira colisão encontrada

        # --- Fim da Resolução de Colisão ---
        # A posição final mundo_x/mundo_y e o rect do jogador estão atualizados.


        # --- Aplicar limites gerais do mundo (se aplicável, após colisões com obstáculos) ---
        self.jogador.mundo_x = max(0, self.jogador.mundo_x)
        self.jogador.mundo_x = min(self.largura_fundo - self.jogador.rect.width, self.jogador.mundo_x)
        # Limite vertical geral pode ser adicionado aqui se necessário

        # Certifica-se de que o rect do jogador está na posição mundo final após todos os ajustes
        self.jogador.rect.topleft = (self.jogador.mundo_x, self.jogador.mundo_y)


        # --- Lógica de seguir o jogador com a câmera ---
        self.camera_x = self.jogador.mundo_x - LARGURA_TELA // 2

        # --- Limitar a movimentação da câmera dentro dos limites da imagem de fundo ---
        self.camera_x = max(0, self.camera_x)
        camera_x_max = self.largura_fundo - LARGURA_TELA
        if camera_x_max < 0:
             camera_x_max = 0
        self.camera_x = min(self.camera_x, camera_x_max)

        # Atualiza outros elementos do jogo (inimigos, projéteis, etc.)
        # self.npcs.update() # Se eles tiverem update
        # self.inimigos.update() # Se eles tiverem update
        # self.projeteis.update() # Se eles tiverem update


    def draw(self, tela):
        """Desenha todos os elementos da tela do jogo."""
        # Desenha o fundo rolante
        if self.fundo_jogo:
            tela.blit(self.fundo_jogo, (0, 0), (self.camera_x, 0, LARGURA_TELA, ALTURA_TELA))
        elif hasattr(self, 'fundo_jogo_fallback') and self.fundo_jogo_fallback:
             tela.blit(self.fundo_jogo_fallback, (0, 0))
        else:
             tela.fill(PRETO)

        # --- Desenha os sprites (jogador, inimigos, npcs, etc.), ajustando a posição pela câmera ---
        for sprite in self.todos_sprites:
             tela_x = sprite.rect.x - self.camera_x
             tela_y = sprite.rect.y
             tela.blit(sprite.image, (tela_x, tela_y))

        # Se você tiver outros grupos de sprites, desenhe-os aqui (ajustados pela câmera)
        # for inimigo in self.inimigos: ...
        # for npc in self.npcs: ...


        # --- Desenha as caixas de colisão dos obstáculos (se DEBUG_DESENHAR_CAIXAS_COLISAO for True) ---
        for obstaculo in self.obstaculos_caminho:
            obstaculo.draw(tela, self.camera_x)

        # --- Desenha as caixas de colisão das áreas de interação (se DEBUG_DESENHAR_CAIXAS_COLISAO for True) ---
        # Nota: O método draw de AreaInteracao só desenha se a flag DEBUG_DESENHAR_CAIXAS_COLISAO for True
        for area in self.areas_interacao:
            area.draw(tela, self.camera_x)


        # --- Desenha o ícone de interação (balão de fala) se o jogador estiver em uma área interativa ---
        if self.areas_interacao_colididas and self.icone_interacao: # Verifica se há colisões E o ícone foi carregado
             # Posiciona o ícone acima da cabeça do jogador
             # Obtém a posição do jogador na tela
             jogador_tela_x = self.jogador.rect.x - self.camera_x
             jogador_tela_y = self.jogador.rect.y
             # Posição do ícone acima do jogador (ajuste o offset vertical)
             icone_offset_y = 40 # Ajuste quantos pixels acima do jogador o ícone deve aparecer
             icone_pos_x = jogador_tela_x + (self.jogador.rect.width // 2) - (self.icone_interacao.get_width() // 2) # Centraliza horizontalmente acima do jogador
             icone_pos_y = jogador_tela_y - icone_offset_y
             # Desenha o ícone na tela
             tela.blit(self.icone_interacao, (icone_pos_x, icone_pos_y))


        # Opcional: Desenhar a caixa de colisão do jogador (para debug)
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            rect_colisao_jogador = pygame.Rect(
                self.jogador.rect.x - self.camera_x,
                self.jogador.rect.y,
                self.jogador.rect.width,
                self.jogador.rect.height
            )
            pygame.draw.rect(tela, COR_CAIXA_COLISAO, rect_colisao_jogador, 1)


        # --- Desenha outros elementos fixos na tela (UI, placar, etc.) ---
        # Estes elementos não são afetados pela posição da câmera


        pass