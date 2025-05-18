# jogador.py

import pygame
from utilidades.constantes import *

class Jogador(pygame.sprite.Sprite):
    """Representa o jogador no jogo."""

    def __init__(self, gerenciador_recursos, x_inicial, y_inicial, tipo_personagem):
        """
        Inicializa o jogador.
        :param resource_manager: O gerenciador de recursos.
        :param x_inicial: Posição X inicial no mundo.
        :param y_inicial: Posição Y inicial no mundo.
        :param tipo_personagem: O tipo de personagem ('menino' ou 'menina').
        """
        super().__init__()
        # Armazena a referência ao gerenciador de recursos
        self.gerenciador_recursos = gerenciador_recursos
        self.tipo_personagem = tipo_personagem

        # --- Carregar e armazenar frames de animação do gerenciador ---
        prefixo_chave = f'protagonista_{self.tipo_personagem}_' # Ex: 'protagonista_menina_' ou 'protagonista_menina_'
        
        imagem_parado = self.gerenciador_recursos.get_image(prefixo_chave + 'em_repouso')
        imagem_caminhar_frame_1 = self.gerenciador_recursos.get_image(prefixo_chave + 'caminhando_1')
        imagem_caminhar_frame_2 = self.gerenciador_recursos.get_image(prefixo_chave + 'caminhando_2')

        # --- Verificar se as imagens foram carregadas e fornecer fallbacks ---
        # Verifica se a imagem parada foi carregada. Se não, cria um fallback.
        if imagem_parado is None:
             print(f"AVISO: Imagem '{prefixo_chave}em_repouso' não carregada. Usando fallback.")
             # Criar uma Surface de fallback com tamanho e cor
             # Certifique-se de que este tamanho é razoável para o sprite (width, height)
             imagem_parado = pygame.Surface((50, 80)) # Tamanho de fallback (ajuste se necessário)
             imagem_parado.fill(AZUL) # Cor de fallback (AZUL deve estar em constantes.py)

        # Verifica se os frames de caminhada foram carregados. Se não, usa a imagem parada como fallback para eles.
        # Cria uma lista com os frames obtidos
        frames_caminhada = [imagem_caminhar_frame_1, imagem_caminhar_frame_2]
        # Verifica se a lista não está vazia E se algum item na lista é None
        if not frames_caminhada or any(img is None for img in frames_caminhada):
             print("AVISO: Frames de animação de caminhada incompletos ou não carregados. Usando imagem parada como fallback para caminhada.")
             # Usa a imagem parada (ou seu fallback) como fallback para AMBOS os frames de caminhada
             frames_caminhada = [imagem_parado, imagem_parado]


        # --- Montar as sequências de animação ---
        # Armazena as imagens/sequências usando chaves descritivas
        self.imagens = {
            'parado': imagem_parado, # A imagem parada é armazenada diretamente
            # Define a sequência de caminhada: Perna Direita -> Parado -> Perna Esquerda -> Parado
            # Usando os nomes das chaves que você usa para carregar em main.py
            'caminhar': [frames_caminhada[0], imagem_parado, frames_caminhada[1], imagem_parado]
            # Se você prefere a sequência original [Perna Direita, Perna Esquerda]:
            # 'caminhar': frames_caminhada
        }

        # --- Variáveis de Animação ---
        self.estado = 'parado' # Estado atual: 'parado' ou 'caminhar'
        self.indice_frame = 0 # Índice do frame atual na sequência de animação
        self.contador_animacao = 0 # Contador para controlar a troca de frames
        self.olhando_direita = True # Direção para onde o jogador está olhando (True = Direita)

        # --- Inicializar a imagem e o rect ---
        # self.image é o atributo que o pygame.sprite.Group.draw usa para desenhar o sprite
        self.image = self.imagens[self.estado] # Começa com a imagem do estado 'parado' (ou seu fallback)
        self.rect = self.image.get_rect() # O rect inicialmente usa o tamanho da imagem atual

        # Posição no mundo do jogo (coordenadas do jogo, não da tela)
        self.mundo_x = x_inicial
        self.mundo_y = y_inicial

        # Posicionar o rect no mundo inicialmente (será ajustado pela GameScreen)
        self.rect.topleft = (self.mundo_x, self.mundo_y)

        # Velocidade de movimento do jogador
        self.velocidade = 3 # Ajuste a velocidade conforme necessário

        # Flags de movimento contínuo (controladas pelos eventos de teclado)
        self.movendo_esquerda = False
        self.movendo_direita = False
        self.movendo_cima = False
        self.movendo_baixo = False

    def handle_event(self, event):
        """
        Processa eventos específicos do jogador (como pressionar/soltar teclas de movimento).
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: # Tecla 'A' para mover para a esquerda
                self.movendo_esquerda = True
                self.olhando_direita = False # Olhando para a esquerda
            elif event.key == pygame.K_d: # Tecla 'D' para mover para a direita
                self.movendo_direita = True
                self.olhando_direita = True # Olhando para a direita
            elif event.key == pygame.K_w: # Tecla 'W' para mover para cima
                self.movendo_cima = True
            elif event.key == pygame.K_s: # Tecla 'S' para mover para baixo
                self.movendo_baixo = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.movendo_esquerda = False
            elif event.key == pygame.K_d:
                self.movendo_direita = False
            elif event.key == pygame.K_w:
                self.movendo_cima = False
            elif event.key == pygame.K_s:
                self.movendo_baixo = False

    def update(self):
        """
        Atualiza a posição do jogador e a animação a cada frame do jogo.
        A GameScreen aplicará os limites de colisão e atualizará a posição final do rect.
        """
        # --- Atualizar Posição no Mundo ---
        if self.movendo_esquerda:
            self.mundo_x -= self.velocidade
        if self.movendo_direita:
            self.mundo_x += self.velocidade
        if self.movendo_cima:
            self.mundo_y -= self.velocidade
        if self.movendo_baixo:
            self.mundo_y += self.velocidade

        # --- Atualizar Animação ---
        # Verifica se o jogador está se movendo em qualquer direção
        esta_movendo = self.movendo_esquerda or self.movendo_direita or self.movendo_cima or self.movendo_baixo

        # Determina o estado da animação com base no movimento
        if esta_movendo:
             # Se houver qualquer movimento, está no estado de caminhada
             self.estado = 'caminhar'
        else:
             # Se não houver movimento, está no estado parado
             self.estado = 'parado'
             # Ao parar, podemos resetar o frame index para o estado parado
             self.indice_frame = 0
             self.contador_animacao = 0 # Resetar o timer de animação ao parar


        # Atualiza o timer de animação APENAS se estiver no estado de caminhada
        if self.estado == 'caminhar':
             # Verifica se a sequência de caminhada existe e tem frames antes de tentar acessar
             if self.imagens.get('caminhar') and len(self.imagens['caminhar']) > 0:
                try:
                    # Use a constante FPS importada de constantes.py para um timer baseado em tempo
                    # Verifique se FPS está importado corretamente e é um número
                    self.contador_animacao += 1/FPS
                except (NameError, TypeError):
                    # Fallback se FPS não estiver definido ou for inválido
                    print("AVISO: FPS não definido ou inválido para animação. Verifique importação de constantes. Usando incremento fixo.")
                    self.contador_animacao += 0.01 # Incremento pequeno fixo para fallback

                if self.contador_animacao >= VELOCIDADE_ANIMACAO_CAMINHADA:
                    # Passa para o próximo frame na sequência de caminhada
                    self.indice_frame = (self.indice_frame + 1) % len(self.imagens['caminhar'])
                    self.contador_animacao = 0 # Resetar o timer
             else:
                 # Não há frames de caminhada válidos, a animação não pode ocorrer
                 self.indice_frame = 0 # Fica no frame 0 (geralmente o primeiro fallback)
                 self.contador_animacao = 0 # Resetar o timer


        # --- Selecionar a imagem do frame atual ---
        imagem_atual = None # Começa como None

        if self.estado == 'parado':
            # Se o estado é parado, usa a imagem única parada
            imagem_atual = self.imagens.get('parado')

        elif self.estado == 'caminhar':
             # Se o estado é caminhar, pega o frame correto da sequência
             # Verifica se a sequência 'caminhar' existe, não está vazia e o frame index é válido
             if self.imagens.get('caminhar') and len(self.imagens['caminhar']) > self.indice_frame:
                imagem_atual = self.imagens['caminhar'][self.indice_frame]
             else:
                 # Fallback se faltarem frames de caminhada, usa a imagem parada
                 imagem_atual = self.imagens.get('parado')


        # Se por algum motivo imagem_atual ainda for None (ex: parada também falhou), usa um fallback final visual
        if imagem_atual is None:
             print(f"ERRO FATAL (Fallback): Imagem para estado '{self.estado}' e índice '{self.indice_frame}' não encontrada. Criando fallback visual.")
             imagem_atual = pygame.Surface((50, 80)) # Último recurso de fallback visual
             imagem_atual.fill(VERMELHO) # Cor de erro/fallback (VERMELHO deve estar em constantes.py)


        # Aplicar inversão horizontal se estiver olhando para a esquerda
        # A inversão só faz sentido se a imagem precisar ser espelhada para a direção
        # E se a animação de caminhada for simétrica e precisar ser espelhada.
        # Se o jogador está parado mas olhando_direita é False, ele continua olhando para a esquerda.
        # A imagem parada também deve ser invertida.
        if not self.olhando_direita: # Se não estiver olhando para a direita (olhando para a esquerda)
            # Certifique-se de que a imagem_atual não é None antes de tentar inverter
            if imagem_atual:
                 imagem_atual = pygame.transform.flip(imagem_atual, True, False)

        # Atribuir a imagem selecionada ao self.image do Sprite
        # Este é o atributo que o Pygame usa para desenhar o sprite na tela
        self.image = imagem_atual

        # Nota: A atualização de self.rect.topleft = (self.mundo_x, self.mundo_y)
        # será feita *depois* pela GameScreen, após aplicar os limites de colisão.