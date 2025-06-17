# entidades/jogador.py

import pygame
from utilidades.constantes import * # Importa as constantes

class Jogador(pygame.sprite.Sprite):
    """Representa o jogador no jogo."""

    def __init__(self, gerenciador_recursos, x_inicial, y_inicial, personagem, olhando_direita_inicial=True):
        super().__init__()
        print(f"Inicializando Jogador: {personagem} em ({x_inicial}, {y_inicial}), olhando_direita={olhando_direita_inicial}")
        self.gerenciador_recursos = gerenciador_recursos
        self.personagem = personagem
        # REMOVIDO: self.fator_de_escala = fator_de_escala

        # Estado do jogador
        self.mundo_x = float(x_inicial) # Usar float para movimento mais suave, depois converter para int para o rect
        self.mundo_y = float(y_inicial) # Usar float para movimento mais suave, depois converter para int para o rect
        self.velocidade = VELOCIDADE_JOGADOR
        self.olhando_direita = olhando_direita_inicial

        # Animação e estado
        self.estado = 'parado' # 'parado', 'caminhando'
        self.frames_animacao = {
            'parado': [],
            'caminhando': []
        }
        self.indice_frame = 0
        self.tempo_desde_ultimo_frame = 0.0 # Usado com dt
        self.taxa_animacao = VELOCIDADE_ANIMACAO_CAMINHADA # Constante de constantes.py

        # Carregar frames de animação
        self.carregar_animacoes()

        # Configura o sprite inicial
        # Garante que 'parado' tenha pelo menos um frame
        if self.frames_animacao['parado']: # Verifica se a lista não está vazia
            self.image = self.frames_animacao[self.estado][self.indice_frame]
        else:
            # Fallback robusto caso todas as imagens falhem
            print("ERRO GRAVE: frames_animacao['parado'] está vazio no __init__ do Jogador. Criando superfície vazia para evitar crash.")
            self.image = pygame.Surface((LARGURA_JOGADOR, ALTURA_JOGADOR))
            self.image.fill(AZUL) # Uma cor diferente para indicar um erro mais grave
        
        self.rect = self.image.get_rect(topleft=(int(self.mundo_x), int(self.mundo_y)))

        # Flags de movimento contínuo (agora gerenciadas internamente por handle_input_continuo)
        self.movendo_esquerda = False
        self.movendo_direita = False
        self.movendo_cima = False
        self.movendo_baixo = False

        # Variáveis para o ícone de interação
        self.mostrar_icone_interacao = False
        self.icone_interacao = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_INTERACAO)


    def carregar_animacoes(self):
        # Carrega imagens. Assume-se que elas já estão escaladas pelo GerenciadorDeRecursos.
        imagem_parado = self.gerenciador_recursos.obter_imagem(self.personagem + '_em_repouso')
        imagem_caminhar_frame_1 = self.gerenciador_recursos.obter_imagem(self.personagem + '_caminhando_1')
        imagem_caminhar_frame_2 = self.gerenciador_recursos.obter_imagem(self.personagem + '_caminhando_2')
        imagem_caminhar_frame_3 = self.gerenciador_recursos.obter_imagem(self.personagem + '_caminhando_3')

        # Adiciona frame 'parado'
        if imagem_parado:
            self.frames_animacao['parado'].append(imagem_parado)
        else:
            print(f"AVISO: Imagem '{self.personagem}_em_repouso' não encontrada para o jogador. Usando fallback padrão.")
            fallback_surface = pygame.Surface((LARGURA_JOGADOR, ALTURA_JOGADOR), pygame.SRCALPHA)
            fallback_surface.fill(PRETO)
            self.frames_animacao['parado'].append(fallback_surface)

        # Adiciona frames 'caminhando'
        valid_caminhada_frames = []
        if imagem_caminhar_frame_1:
            valid_caminhada_frames.append(imagem_caminhar_frame_1)
        if imagem_caminhar_frame_2:
            valid_caminhada_frames.append(imagem_caminhar_frame_2)
        if imagem_caminhar_frame_3:
            valid_caminhada_frames.append(imagem_caminhar_frame_3)

        # Se não houver frames de caminhada carregados, usa o frame 'parado' como fallback
        if not valid_caminhada_frames:
            print(f"AVISO: Nenhuma imagem de caminhada para '{self.personagem}' carregada. Usando imagem parada como fallback para caminhada.")
            if self.frames_animacao['parado']:
                fallback = self.frames_animacao['parado'][0]
                valid_caminhada_frames = [fallback, fallback, fallback]
            else:
                fallback_surface = pygame.Surface((LARGURA_JOGADOR, ALTURA_JOGADOR), pygame.SRCALPHA)
                fallback_surface.fill(VERMELHO)
                valid_caminhada_frames = [fallback_surface, fallback_surface, fallback_surface]

        # Define a sequência de caminhada: 1 → 2 → 3 → 2
        if len(valid_caminhada_frames) >= 3:
            self.frames_animacao['caminhando'] = [
                valid_caminhada_frames[0],
                valid_caminhada_frames[1],
                valid_caminhada_frames[2],
                valid_caminhada_frames[1]
            ]
        else:
            print("AVISO: Nem todos os 3 frames de caminhada disponíveis. Repetindo os existentes.")
            self.frames_animacao['caminhando'] = valid_caminhada_frames * 2  # Loop com o que tiver

        # Garante pelo menos um frame em 'parado'
        if not self.frames_animacao['parado']:
            print("ERRO CRÍTICO: frames_animacao['parado'] ainda está vazio após todos os fallbacks.")
            fallback_surface = pygame.Surface((LARGURA_JOGADOR, ALTURA_JOGADOR), pygame.SRCALPHA)
            fallback_surface.fill(VERMELHO)
            self.frames_animacao['parado'].append(fallback_surface)

        self.frame_parada_apos_caminhada = valid_caminhada_frames[1] if len(valid_caminhada_frames) > 1 else self.frames_animacao['parado'][0]


    def handle_input_continuo(self):
        """
        Processa as entradas contínuas do teclado usando pygame.key.get_pressed().
        Este método substitui a lógica baseada em eventos KEYDOWN/KEYUP para movimento contínuo.
        """
        keys = pygame.key.get_pressed()
        self.movendo_esquerda = False
        self.movendo_direita = False
        self.movendo_cima = False
        self.movendo_baixo = False

        if keys[pygame.K_a]:
            self.movendo_esquerda = True
            self.olhando_direita = False # Olhando para a esquerda
        if keys[pygame.K_d]:
            self.movendo_direita = True
            self.olhando_direita = True # Olhando para a direita
        if keys[pygame.K_w]:
            self.movendo_cima = True
        if keys[pygame.K_s]:
            self.movendo_baixo = True

    def update(self, dt, obstaculos):
        """
        Atualiza a posição do jogador e a animação a cada frame do jogo.
        :param dt: Delta time (tempo em segundos desde o último frame).
        :param obstaculos: Um grupo de sprites de obstáculos para colisão.
        """
        self.handle_input_continuo() # Processa as entradas do teclado continuamente

        # Salva a posição anterior para reverter em caso de colisão
        pos_anterior_x = self.mundo_x
        pos_anterior_y = self.mundo_y

        # Calcula o movimento
        dx = 0
        dy = 0
        if self.movendo_esquerda:
            dx -= self.velocidade
        if self.movendo_direita:
            dx += self.velocidade
        if self.movendo_cima:
            dy -= self.velocidade
        if self.movendo_baixo:
            dy += self.velocidade

        # Atualiza a posição X e verifica colisão
        self.mundo_x += dx
        self.rect.x = int(self.mundo_x) # Atualiza o rect para colisão

        # Verifica colisão em X com obstáculos
        if pygame.sprite.spritecollideany(self, obstaculos):
            self.mundo_x = pos_anterior_x # Reverte o movimento em X
            self.rect.x = int(self.mundo_x) # Atualiza o rect para a posição revertida

        # Atualiza a posição Y e verifica colisão
        self.mundo_y += dy
        self.rect.y = int(self.mundo_y) # Atualiza o rect para colisão

        # Verifica colisão em Y com obstáculos
        if pygame.sprite.spritecollideany(self, obstaculos):
            self.mundo_y = pos_anterior_y # Reverte o movimento em Y
            self.rect.y = int(self.mundo_y) # Atualiza o rect para a posição revertida


        # --- Atualizar Animação ---
        esta_movendo = (self.movendo_esquerda or self.movendo_direita or
                        self.movendo_cima or self.movendo_baixo)

        if esta_movendo:
            self.estado = 'caminhando'
            self.tempo_desde_ultimo_frame += dt
            if self.tempo_desde_ultimo_frame >= self.taxa_animacao:
                # Garante que a lista de frames de caminhada não esteja vazia
                if self.frames_animacao['caminhando']:
                    self.indice_frame = (self.indice_frame + 1) % len(self.frames_animacao['caminhando'])
                else:
                    self.indice_frame = 0 # Fallback se não houver frames
                self.tempo_desde_ultimo_frame = 0.0
        else:
            self.estado = 'parado'
            self.indice_frame = 0 # Volta para o primeiro frame de parado
            self.tempo_desde_ultimo_frame = 0.0

            # Quando parar, primeiro mostra o frame 2 de caminhada, depois repouso
            if hasattr(self, 'frame_parada_apos_caminhada') and self.frame_parada_apos_caminhada:
                self.image = self.frame_parada_apos_caminhada
                # Remove o atributo para que isso só aconteça uma vez ao parar
                del self.frame_parada_apos_caminhada
                # Return aqui interromperia a atualização da imagem para o estado parado
                # O ideal é que na próxima chamada do update ele já esteja no estado parado
                # Remova o 'return' e deixe a lógica de seleção de imagem abaixo cuidar disso.
                # Não é necessário um 'return' aqui.
                pass # Apenas passa para a próxima linha

        # Selecionar a imagem do frame atual
        imagem_atual = None
        if self.estado == 'parado' and self.frames_animacao['parado']:
            imagem_atual = self.frames_animacao['parado'][self.indice_frame]
        elif self.estado == 'caminhando' and self.frames_animacao['caminhando']:
            imagem_atual = self.frames_animacao['caminhando'][self.indice_frame]
        else:
            # Fallback final se nada foi encontrado
            print(f"ERRO FATAL (Fallback): Imagem para estado '{self.estado}' e índice '{self.indice_frame}' não encontrada. Criando superfície de erro.")
            imagem_atual = pygame.Surface((LARGURA_JOGADOR, ALTURA_JOGADOR), pygame.SRCALPHA)
            imagem_atual.fill(VERMELHO)

        # Aplicar inversão horizontal se estiver olhando para a esquerda
        if not self.olhando_direita:
            imagem_atual = pygame.transform.flip(imagem_atual, True, False)

        self.image = imagem_atual

    def draw(self, screen, camera_x, camera_y):
        """
        Desenha o jogador na tela, ajustando pela posição da câmera.
        :param screen: A superfície do Pygame onde desenhar.
        :param camera_x: A posição X da câmera.
        :param camera_y: A posição Y da câmera (se o jogo rolar verticalmente).
        """
        # A posição do jogador na tela é sua posição no mundo menos a posição da câmera
        posicao_tela_x = self.mundo_x - camera_x
        posicao_tela_y = self.mundo_y - camera_y
        
        screen.blit(self.image, (int(posicao_tela_x), int(posicao_tela_y)))

        # Desenha o ícone de interação se aplicável
        if self.mostrar_icone_interacao and self.icone_interacao:
            icone_x = posicao_tela_x + self.rect.width // 2 - self.icone_interacao.get_width() // 2
            icone_y = posicao_tela_y - self.icone_interacao.get_height() + 10
            screen.blit(self.icone_interacao, (int(icone_x), int(icone_y)))

        # DEBUG: Desenha o retângulo de colisão do jogador
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            debug_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height)
            pygame.draw.rect(screen, COR_CAIXA_COLISAO, debug_rect, 1)