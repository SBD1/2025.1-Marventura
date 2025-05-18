# telas/tela_de_jogo.py

import pygame
import sys
from utilidades.constantes import *
from entidades import Jogador
from entidades import Obstaculo
from entidades import AreaInteracao
from mapa_dados import get_mapa_data

class TelaJogo:
    """
    Representa a tela principal do jogo para um mapa específico.
    Onde a jogabilidade acontece, com fundo rolante, jogador, obstáculos e áreas de interação.
    Carrega e exibe elementos do mapa com base nos dados do mapa, ponto de entrada ou dados salvos.
    """
    # O construtor recebe ID do mapa, tipo de personagem, e OPCIONALMENTE ID do ponto de entrada (ao mudar de área)
    # OU coordenadas e orientação salvas (ao carregar um jogo).
    def __init__(self, gerenciador_recursos, id_mapa, tipo_personagem, id_entrada_alvo=None, coordenada_x=None, coordenada_y=None, olhando_para_direita=None): # <-- Adiciona parâmetros para dados salvos
        self.gerenciador_recursos = gerenciador_recursos
        self.id_mapa = id_mapa
        self.tipo_personagem = tipo_personagem
        self.id_entrada_alvo = id_entrada_alvo # <-- Armazena o ID do ponto de entrada desejado ao mudar de área
        # self.coordenada_x = coordenada_x # <-- Armazena coordenadas salvas (não precisamos armazenar se as usamos imediatamente)
        # self.coordenada_y = coordenada_y
        # self.olhando_para_direita = olhando_para_direita
        print(f"TelaJogo __init__ - Mapa: '{id_mapa}', Personagem: '{tipo_personagem}', Alvo Entrada: '{id_entrada_alvo}', Posição Salva: ({coordenada_x}, {coordenada_y}), Olhando Salvo: {olhando_para_direita}") # Debug print


        # --- Carregar Dados do Mapa ---
        self.mapa_data = get_mapa_data(self.id_mapa) # <-- Obtém os dados do mapa usando a função
        if self.mapa_data is None:
            print(f"ERRO FATAL: Dados para o mapa ID '{self.id_mapa}' não encontrados.")
            # Fallback mínimo para dados do mapa se o ID do mapa for inválido
            # Define um ponto padrão de fallback para evitar crashes
            self.mapa_data = {
                'chave_cenario': None,
                'pontos_entrada_saida': {'entrada_padrao': {'x': 100, 'y': 100, 'olhando_direita': True}}, # Define um ponto padrão de fallback
                'obstaculos': [],
                'areas_interacao': [],
                'npcs': [],
                'inimigos': []
            }
            # Se os dados do mapa falharam, garantimos que o id_entrada_alvo usa o fallback padrão
            self.id_entrada_alvo = 'entrada_padrao' # Garante que a lógica abaixo encontrará este ponto

        # --- Determinar Posição e Orientação Inicial do Jogador ---
        jogador_inicio_x = 100 # Padrão fallback manual
        jogador_inicio_y = 370 # Padrão fallback manual
        jogador_olhando_direita = True # Padrão fallback manual

        # VERIFICAÇÃO 1: Há coordenadas salvas fornecidas?
        if coordenada_x is not None and coordenada_y is not None:
             # --- Se houver coordenadas salvas, use-as ---
             print(f"Iniciando jogo no mapa '{self.id_mapa}' com posição salva: ({coordenada_x}, {coordenada_y})") # Debug print
             jogador_inicio_x = coordenada_x
             jogador_inicio_y = coordenada_y
             # Usa a orientação salva se fornecida (não None), caso contrário, usa o padrão manual (True)
             jogador_olhando_direita = olhando_para_direita if olhando_para_direita is not None else True

        # VERIFICAÇÃO 2: Não há coordenadas salvas, mas há um ID de ponto de entrada especificado?
        elif self.id_entrada_alvo:
             # --- Se houver um ID de ponto de entrada de destino, use os dados desse ponto ---
             pontos_entrada_saida = self.mapa_data.get('pontos_entrada_saida', {})
             dados_ponto_entrada = pontos_entrada_saida.get(self.id_entrada_alvo)

             if dados_ponto_entrada:
                  # Ponto de entrada específico encontrado nos dados do mapa
                  print(f"Iniciando jogo no mapa '{self.id_mapa}' no ponto de entrada especificado: '{self.id_entrada_alvo}'") # Debug print
                  jogador_inicio_x = dados_ponto_entrada.get('x', 100) # Pega x, usa 100 como padrão se a chave 'x' faltar no ponto
                  jogador_inicio_y = dados_ponto_entrada.get('y', 370) # Pega y, usa 370 como padrão se a chave 'y' faltar no ponto
                  # Pega a orientação, usa True (direita) como padrão se a chave 'olhando_direita' faltar
                  jogador_olhando_direita = dados_ponto_entrada.get('olhando_direita', True)
             else:
                  # Se o ponto de entrada especificado NÃO foi encontrado nos dados do mapa
                  print(f"AVISO: Ponto de entrada especificado '{self.id_entrada_alvo}' não encontrado nos dados do mapa '{self.id_mapa}'. Tentando 'entrada_padrao'.") # Debug print
                  # Tenta usar o ponto 'entrada_padrao' definido nos dados deste mapa.
                  dados_ponto_entrada_padrao = pontos_entrada_saida.get('entrada_padrao')
                  if dados_ponto_entrada_padrao:
                      print(f"Usando ponto de entrada 'entrada_padrao' no mapa '{self.id_mapa}'.") # Debug print
                      jogador_inicio_x = dados_ponto_entrada_padrao.get('x', 100)
                      jogador_inicio_y = dados_ponto_entrada_padrao.get('y', 370)
                      jogador_olhando_direita = dados_ponto_entrada_padrao.get('olhando_direita', True)
                  else:
                      # Se nem o ponto de entrada padrão existir
                      print(f"AVISO: Ponto de entrada 'entrada_padrao' também não encontrado. Usando fallback manual.") # Debug print
                      # Coordenadas de fallback manual já estão definidas no início deste bloco

        # VERIFICAÇÃO 3: Não há coordenadas salvas nem ID de ponto de entrada especificado.
        # Usa o ponto de entrada padrão do mapa como último recurso antes do fallback manual.
        else:
             # --- Usa o ponto de entrada padrão do mapa ---
             pontos_entrada_saida = self.mapa_data.get('pontos_entrada_saida', {})
             dados_ponto_entrada_padrao = pontos_entrada_saida.get('entrada_padrao')

             if dados_ponto_entrada_padrao:
                  print(f"Iniciando jogo no mapa '{self.id_mapa}' no ponto de entrada padrão 'entrada_padrao'.") # Debug print
                  jogador_inicio_x = dados_ponto_entrada_padrao.get('x', 100)
                  jogador_inicio_y = dados_ponto_entrada_padrao.get('y', 370)
                  jogador_olhando_direita = dados_ponto_entrada_padrao.get('olhando_direita', True)
             else:
                  # Se o ponto de entrada padrão não existir
                  print(f"AVISO: Ponto de entrada 'entrada_padrao' não encontrado. Usando fallback manual.") # Debug print
                  # Coordenadas de fallback manual já estão definidas no início deste bloco

        print(f"Posição Final Inicial do Jogador: ({jogador_inicio_x}, {jogador_inicio_y}), Olhando Direita: {jogador_olhando_direita}") # Debug print


        # --- Configurar Fundo do Jogo ---
        # Obtém a chave da imagem de fundo dos dados do mapa
        chave_cenario = self.mapa_data.get('chave_cenario')
        if chave_cenario:
             self.fundo_jogo = self.gerenciador_recursos.get_image(chave_cenario)
        else:
             self.fundo_jogo = None # Não há chave de fundo ou carregamento falhou


        # Verifica se a imagem de fundo foi carregada com sucesso e obtém suas dimensões
        if self.fundo_jogo is None:
             print(f"ERRO: Imagem de fundo para o mapa '{self.id_mapa}' não carregada ou chave inválida.")
             self.largura_fundo = LARGURA_TELA
             self.altura_fundo = ALTURA_TELA
             self.fundo_jogo_fallback = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
             self.fundo_jogo_fallback.fill(VERMELHO) # Fallback visual
        else:
            self.largura_fundo = self.fundo_jogo.get_width()
            self.altura_fundo = self.fundo_jogo.get_height()
            self.fundo_jogo_fallback = None # Não precisa de fallback se o fundo carregou


        # Obtém a fonte grande (continua a ser um recurso comum)
        self.fonte_grande = self.gerenciador_recursos.get_font('titulo') # <-- Usando chave 'titulo'


        # Variáveis para controle da câmera (scroll)
        self.camera_x = 0
        self.velocidade_scroll = 10 # Pode se tornar um dado do mapa se quiser velocidades diferentes

        # --- Criação do Jogador ---
        # Cria a instância da classe Jogador, usando as coordenadas e orientação determinadas pela lógica acima
        self.jogador = Jogador(self.gerenciador_recursos, jogador_inicio_x, jogador_inicio_y, self.tipo_personagem) # <-- Passa as coordenadas iniciais e o tipo de personagem

        # Define a orientação inicial do jogador (atributo da classe Jogador) após a criação
        # Isso garante que o sprite inicial esteja virado na direção correta.
        self.jogador.olhando_direita = jogador_olhando_direita # <-- Define a orientação inicial do sprite

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
        self.icone_interacao = self.gerenciador_recursos.get_image(CHAVE_ICONE_INTERACAO) # Chave da constante

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
        # Passa o evento para o objeto jogador para ele processar seus próprios inputs (movimento, etc.)
        self.jogador.handle_event(event)

        # --- Lógica específica da Tela de Jogo ---
        if event.type == pygame.KEYDOWN:
            # Se a tecla ESC foi pressionada
            if event.key == pygame.K_ESCAPE:
                print("Pressionou ESC -> Voltando para o Menu Inicial")
                # Em um jogo completo, o ESC levaria para um menu de pausa/salvar.
                # Por enquanto, voltamos diretamente para o menu inicial.
                return ESTADO_MENU_INICIAL # <-- Retorna apenas o ID do estado

            # --- Verifica se a tecla de interação foi pressionada ---
            # Usa a constante para a tecla de interação
            if event.key == TECLA_INTERACAO:
                # Verifica se o jogador está colidindo com alguma área de interação
                if self.areas_interacao_colididas:
                     # Pega a primeira área de interação na lista de colisões (simplificado para esta lógica)
                     area_ativa = self.areas_interacao_colididas[0]
                     print(f"Interagindo com área de tipo: {area_ativa.tipo_evento}") # Print de debug

                     # --- Aciona o evento com base no tipo ---
                     if area_ativa.tipo_evento == 'mudar_mapa':
                         # Obtém o ID do próximo mapa dos dados do evento da área de interação
                         proximo_mapa_id = area_ativa.dados_evento.get('proximo_mapa_id')
                         # Extrai o ID do ponto de entrada de destino dos DADOS DO EVENTO da área de interação
                         ponto_entrada_destino_id = area_ativa.dados_evento.get('ponto_entrada_destino_id') # <-- Extrai o ID do ponto de entrada aqui

                         if proximo_mapa_id: # Verifica se o ID do próximo mapa é válido
                             print(f"Sinalizando mudança para o mapa: {proximo_mapa_id}, ponto de entrada: {ponto_entrada_destino_id}") # Debug print
                             # Retorna um dicionário com todos os dados necessários para criar a próxima TelaJogo:
                             # 'estado': O estado para onde ir (ESTADO_JOGO, pois é outro mapa do jogo).
                             # 'id_mapa': O ID do mapa para carregar.
                             # 'tipo_personagem': O tipo de personagem atual do jogador (obtido de self.tipo_personagem).
                             # 'ponto_entrada_destino_id': O ID do ponto de entrada NO MAPA DE DESTINO.
                             return {'estado': ESTADO_JOGO,
                                     'id_mapa': proximo_mapa_id,
                                     'tipo_personagem': self.tipo_personagem, # Usa o tipo de personagem atual
                                     'ponto_entrada_destino_id': ponto_entrada_destino_id} # <-- Inclui o ID do ponto de entrada extraído aqui

                         else:
                             # Se a área de interação 'mudar_mapa' não especificou 'proximo_mapa_id' nos dados do mapa
                             print("ERRO: Área de interação 'mudar_mapa' sem 'proximo_mapa_id' nos dados.") # Print de erro

                     elif area_ativa.tipo_evento == 'dialogo':
                          # Lógica para iniciar um diálogo
                          dialogo_key = area_ativa.dados_evento.get('dialogo_key')
                          if dialogo_key:
                              print(f"Acionando diálogo com chave: {dialogo_key}") # Debug print
                              # Aqui você mudaria para um estado de diálogo (se tiver)
                              # ou acionaria o sistema de diálogo diretamente, possivelmente passando a chave do diálogo.
                              # return ESTADO_DIALOGO # Exemplo se tiver estado de diálogo
                              pass # Por enquanto, apenas printa e continua no jogo

                          else:
                              print("ERRO: Área de interação 'dialogo' sem 'dialogo_key' nos dados.") # Print de erro

                     elif area_ativa.tipo_evento == 'comprar_item':
                          # Lógica para interagir com uma loja/item
                          item_id = area_ativa.dados_evento.get('item_id')
                          preco = area_ativa.dados_evento.get('preco')
                          if item_id and preco is not None:
                               print(f"Acionando compra de item: {item_id} por {preco}") # Debug print
                               # Aqui você mudaria para um estado de loja/compra (se tiver)
                               # ou acionaria a UI de compra diretamente, possivelmente passando os dados do item.
                               # return ESTADO_LOJA # Exemplo se tiver estado de loja
                               pass # Por enquanto, apenas printa e continua no jogo

                          else:
                              print("ERRO: Área de interação 'comprar_item' com dados inválidos (faltando item_id ou preco).") # Print de erro

                     # Adicione outros tipos de eventos de interação aqui (usar item no mundo, ativar mecanismo, etc.)

                # else: Tecla de interação pressionada, mas o jogador não está colidindo com nenhuma área de interação ativa.

        # Se nenhum evento tratado nesta tela causou uma mudança de estado, retorna None
        return None # Continua na mesma tela (TelaJogo)


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
        # Esta lista self.areas_interacao_colididas é usada em handle_event e draw
        self.areas_interacao_colididas = pygame.sprite.spritecollide(self.jogador, self.areas_interacao, False) # <-- Atualiza a lista de áreas ativas

        # --- Implementação de Colisão com Deslize (Axis-Aligned Bounding Box - AABB) ---
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
        # Atualiza o rect do jogador para a nova posição X no mundo para a checagem de colisão
        self.jogador.rect.x = self.jogador.mundo_x

        # --- Verificar e Resolver Colisão no Eixo X ---
        # Verifica colisões entre o jogador (na nova posição X) e os obstáculos de caminho
        obstaculos_colididos_x = pygame.sprite.spritecollide(self.jogador, self.obstaculos_caminho, False)

        if obstaculos_colididos_x:
             # Se houver colisão no eixo X, corrigir a posição X do jogador
             for obstaculo in obstaculos_colididos_x:
                  # Determine de que lado do obstáculo o jogador colidiu com base na direção do movimento
                  if delta_x > 0: # Movendo para a direita, colidiu com o lado esquerdo do obstáculo
                       # Empurra o jogador de volta para a borda esquerda do obstáculo
                       self.jogador.mundo_x = obstaculo.rect.left - self.jogador.rect.width
                  elif delta_x < 0: # Movendo para a esquerda, colidiu com o lado direito do obstáculo
                       # Empurra o jogador de volta para a borda direita do obstáculo
                       self.jogador.mundo_x = obstaculo.rect.right

                  # Atualiza o rect do jogador para a posição X corrigida antes de verificar o Y
                  self.jogador.rect.x = self.jogador.mundo_x

                  # Para esta lógica simples, corrigimos apenas para a primeira colisão encontrada no eixo X.
                  break # Corrigiu a posição X, não precisa verificar outros obstáculos nesta iteração X


        # --- Tentar mover no eixo Y ---
        # Mover a posição Y do jogador no mundo (partindo da posição X corrigida/não colidida)
        self.jogador.mundo_y += delta_y
        # Atualiza o rect do jogador para a nova posição Y no mundo para a checagem de colisão
        self.jogador.rect.y = self.jogador.mundo_y

        # --- Verificar e Resolver Colisão no Eixo Y ---
        # Verifica colisões entre o jogador (agora na nova posição Y) e os obstáculos de caminho
        obstaculos_colididos_y = pygame.sprite.spritecollide(self.jogador, self.obstaculos_caminho, False)

        if obstaculos_colididos_y:
             # Se houver colisão no eixo Y, corrigir a posição Y do jogador
             for obstaculo in obstaculos_colididos_y:
                  # Determine de que lado do obstáculo o jogador colidiu com base na direção do movimento
                  if delta_y > 0: # Movendo para baixo, colidiu com o lado superior do obstáculo
                       # Empurra o jogador de volta para a borda superior do obstáculo
                       self.jogador.mundo_y = obstaculo.rect.top - self.jogador.rect.height
                  elif delta_y < 0: # Movendo para cima, colidiu com o lado inferior do obstáculo
                       # Empurra o jogador de volta para a borda inferior do obstáculo
                       self.jogador.mundo_y = obstaculo.rect.bottom

                  # Atualiza o rect do jogador para a posição Y corrigida
                  self.jogador.rect.y = self.jogador.mundo_y

                  # Para esta lógica simples, corrigimos apenas para a primeira colisão encontrada no eixo Y.
                  break # Corrigiu a posição Y, não precisa verificar outros obstáculos nesta iteração Y

        # --- Fim da Resolução de Colisão ---
        # A posição self.jogador.mundo_x e self.jogador.mundo_y agora é a posição final válida para este frame.
        # O rect do jogador (self.jogador.rect) já foi atualizado durante as verificações de colisão para refletir essa posição final.


        # --- Aplicar limites gerais do mundo (se aplicável, após colisões com obstáculos) ---
        # Limite horizontal: o jogador não pode sair das bordas externas do mapa grande.
        # Note: se os obstáculos de caminho já cobrem todas as bordas externas, este limite pode ser redundante,
        # mas é uma boa prática mantê-lo como fallback.
        self.jogador.mundo_x = max(0, self.jogador.mundo_x)
        self.jogador.mundo_x = min(self.largura_fundo - self.jogador.rect.width, self.jogador.mundo_x)

        # Limite vertical geral: se o mundo tiver um "teto" ou "chão" que não são obstáculos de caminho específicos.
        # Se todos os limites Y são tratados por obstáculos de caminho, esta parte pode ser removida ou ajustada.
        # self.jogador.mundo_y = max(0, self.jogador.mundo_y)
        # self.jogador.mundo_y = min(self.altura_fundo - self.jogador.rect.height, self.jogador.mundo_y)

        # Certifica-se de que o rect do jogador está na posição mundo final após todos os ajustes (limites e colisões)
        self.jogador.rect.topleft = (self.jogador.mundo_x, self.jogador.mundo_y)


        # --- Lógica de seguir o jogador com a câmera ---
        # Centraliza a câmera horizontalmente no jogador.
        # A posição X da câmera é a posição X do jogador no mundo menos metade da largura da tela.
        self.camera_x = self.jogador.mundo_x - LARGURA_TELA // 2

        # --- Limitar a movimentação da câmera dentro dos limites da imagem de fundo ---
        # A câmera não pode ir para a esquerda além de 0 (limite esquerdo do mundo)
        self.camera_x = max(0, self.camera_x)

        # A borda direita da tela (camera_x + LARGURA_TELA) não pode exceder a largura total do fundo do jogo.
        # A posição X máxima da câmera é a largura total do fundo menos a largura da tela.
        camera_x_max = self.largura_fundo - LARGURA_TELA
        if camera_x_max < 0: # Se o fundo for menor que a tela, a câmera não se move
             camera_x_max = 0
        self.camera_x = min(self.camera_x, camera_x_max)

        # Atualiza outros elementos do jogo (inimigos, projéteis, etc.)
        # self.areas_interacao.update() # Áreas estáticas não precisam de update
        # self.npcs.update() # Se eles tiverem update
        # self.inimigos.update() # Se eles tiverem update
        # self.projeteis.update() # Se eles tiverem update


    def draw(self, tela):
        """Desenha todos os elementos da tela do jogo."""
        # Desenha o fundo rolante (obtido do gerenciador)
        if self.fundo_jogo:
            # Desenha a porção da imagem de fundo que está visível na tela
            # screen.blit(source_surface, dest_position, area_on_source)
            # source_surface: a imagem grande do fundo do jogo
            # dest_position: (0, 0) - o canto superior esquerdo da tela
            # area_on_source: (self.camera_x, 0, LARGURA_TELA, ALTURA_TELA) - o retângulo da imagem de fundo a ser desenhado, ajustado pela câmera X
            tela.blit(self.fundo_jogo, (0, 0), (self.camera_x, 0, LARGURA_TELA, ALTURA_TELA))
        # Desenha o fallback se a imagem principal não carregou
        elif hasattr(self, 'fundo_jogo_fallback') and self.fundo_jogo_fallback:
             tela.blit(self.fundo_jogo_fallback, (0, 0))
        else:
             # Último recurso: preenche a tela com a cor preta se nenhum fundo válido existir
             tela.fill(PRETO)


        # --- Desenha os sprites (jogador, inimigos, npcs, etc.), ajustando a posição pela câmera ---
        # Itera sobre todos os sprites visíveis (no grupo self.todos_sprites)
        for sprite in self.todos_sprites:
             # Calcula a posição de desenho do sprite na tela, offset pela posição da câmera
             # A posição X na tela é a posição X do sprite no mundo (sprite.rect.x) menos o scroll da câmera (self.camera_x)
             # A posição Y na tela é a mesma posição Y no mundo (sprite.rect.y) se a câmera não rolar verticalmente
             tela_x = sprite.rect.x - self.camera_x
             tela_y = sprite.rect.y
             # Desenha a imagem do sprite na posição calculada na tela
             tela.blit(sprite.image, (tela_x, tela_y))

        # Se você tiver outros grupos de sprites (ex: inimigos, npcs, projeteis), desenhe-os aqui
        # for inimigo in self.inimigos:
        #      tela_x = inimigo.rect.x - self.camera_x
        #      tela_y = inimigo.rect.y
        #      tela.blit(inimigo.image, (tela_x, tela_y))


        # --- Desenha as caixas de colisão dos obstáculos (se DEBUG_DESENHAR_CAIXAS_COLISAO for True) ---
        # Cada obstáculo tem seu próprio método draw que verifica a flag DEBUG_DESENHAR_CAIXAS_COLISAO internamente.
        # Itera sobre todos os obstáculos no grupo self.obstaculos_caminho
        for obstaculo in self.obstaculos_caminho:
            # Chama o método draw do obstáculo, passando a superfície da tela e a posição da câmera para ajuste
            obstaculo.draw(tela, self.camera_x)


        # --- Desenha as caixas de colisão das áreas de interação (se DEBUG_DESENHAR_CAIXAS_COLISAO for True) ---
        # Nota: O método draw de AreaInteracao só desenha se a flag DEBUG_DESENHAR_CAIXAS_COLISAO for True
        for area in self.areas_interacao:
            area.draw(tela, self.camera_x)


        # --- Desenha o ícone de interação (balão de fala) se o jogador estiver em uma área interativa ---
        # Verifica se há colisões com áreas de interação E o ícone foi carregado
        if self.areas_interacao_colididas and self.icone_interacao:
             # Posiciona o ícone acima da cabeça do jogador na tela
             # Obtém a posição do jogador na tela (ajustada pela câmera)
             jogador_tela_x = self.jogador.rect.x - self.camera_x
             jogador_tela_y = self.jogador.rect.y
             # Posição do ícone acima do jogador (ajuste o offset vertical conforme necessário)
             icone_offset_y = 40 # Ajuste quantos pixels acima do jogador o ícone deve aparecer
             # Centraliza o ícone horizontalmente acima do jogador
             icone_pos_x = jogador_tela_x + (self.jogador.rect.width // 2) - (self.icone_interacao.get_width() // 2)
             icone_pos_y = jogador_tela_y - icone_offset_y
             # Desenha o ícone na tela
             tela.blit(self.icone_interacao, (icone_pos_x, icone_pos_y))


        # Opcional: Desenhar a caixa de colisão do jogador (para debug)
        # Verifica se a flag de debug de colisão está ativa
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            # Cria um retângulo para desenhar na tela, baseado no rect do jogador e na posição da câmera
            rect_colisao_jogador = pygame.Rect(
                self.jogador.rect.x - self.camera_x, # Ajusta a posição X pela câmera
                self.jogador.rect.y,              # A posição Y geralmente não rola, então não precisa ajustar
                self.jogador.rect.width,          # Largura do jogador
                self.jogador.rect.height         # Altura do jogador
            )
            # Desenha o contorno do retângulo de colisão do jogador na tela
            pygame.draw.rect(tela, COR_CAIXA_COLISAO, rect_colisao_jogador, 1) # Desenha apenas o contorno (grossura 1)


        # --- Desenha outros elementos fixos na tela (UI, placar, etc.) ---
        # Estes elementos não são afetados pela posição da câmera (ex: placar de pontos)

        # Exemplo: Desenha um texto simples na tela
        # if self.fonte_grande: # Verifica se a fonte grande (chave 'titulo') foi carregada
        #      # Renderiza um texto simples na tela de jogo (pode ser removido/alterado)
        #      texto_jogo = self.fonte_grande.render("Tela do Jogo!", True, BRANCO)
        #      rect_jogo = texto_jogo.get_rect(center=(LARGURA_TELA // 2, 50)) # Posição fixa na tela
        #      tela.blit(texto_jogo, rect_jogo)
        # else:
        #      print("AVISO: Fonte grande (chave 'titulo') não disponível para texto na tela de jogo.") # Print de aviso


        pass # Espaço para adicionar mais elementos de UI (score, vida, etc.)