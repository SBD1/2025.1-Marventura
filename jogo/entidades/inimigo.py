# entidades/inimigo.py
import pygame
import random
import math
from utilidades.constantes import * # Certifique-se de que todas as constantes estão aqui

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, resource_manager, x_inicial, y_inicial, tipo_inimigo, largura, altura,
                 velocidade_caminhada, velocidade_corrida, alcance_visao, angulo_visao_graus,
                 tempo_reacao_ms, imagem_chave, cor_fallback=VERMELHO,
                 alcance_ataque=DISTANCIA_ATAQUE_INIMIGO, duracao_ataque_ms=DURACAO_ATAQUE_INIMIGO_MS): # Usando nova constante
        super().__init__()
        self.resource_manager = resource_manager
        self.tipo_inimigo = tipo_inimigo
        self.velocidade_caminhada = velocidade_caminhada
        self.velocidade_corrida = velocidade_corrida
        self.velocidade_atual = velocidade_caminhada
        self.alcance_visao = alcance_visao
        self.angulo_visao = math.radians(angulo_visao_graus)
        self.tempo_reacao_ms = tempo_reacao_ms
        self.cor_fallback = cor_fallback

        self.imagem_original = self.resource_manager.get_image(imagem_chave)
        if self.imagem_original:
            self.image = self.imagem_original
        else:
            print(f"AVISO: Imagem '{imagem_chave}' não encontrada para o inimigo '{tipo_inimigo}'. Usando fallback color.")
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill(self.cor_fallback)

        self.rect = self.image.get_rect(topleft=(x_inicial, y_inicial))
        self.mundo_x = x_inicial # Coordenada X real no mundo
        self.mundo_y = y_inicial # Coordenada Y real no mundo
        
        self.olhando_direita = True # Direção inicial

        self.estado = ESTADO_INIMIGO_PARADO # Estado inicial do inimigo
        self.timer_reacao = 0 # Timer para tempo de reação antes de perseguir
        self.ultimo_ataque_tempo = 0 # Timestamp do último ataque
        self.duracao_ataque_ms = duracao_ataque_ms
        self.alcance_ataque = alcance_ataque # Distância para considerar um ataque
        
        self.alvo_identificado = False # Flag para saber se o inimigo tem um alvo
        self.atingiu_jogador = False # Flag para sinalizar se o ataque acertou

    def update(self, dt, jogador, obstaculos_caminho, obstaculos_visao):
        self.atingiu_jogador = False # Reinicia a flag de acerto a cada frame

        # Calcula a posição do centro do inimigo e do jogador
        inimigo_centro = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        jogador_centro = pygame.math.Vector2(jogador.rect.centerx, jogador.rect.centery)
        
        distancia_ao_jogador = inimigo_centro.distance_to(jogador_centro)

        # Atualiza a direção que o inimigo está olhando
        if jogador_centro.x > inimigo_centro.x:
            self.olhando_direita = True
        else:
            self.olhando_direita = False

        # --- Lógica de Visão ---
        if distancia_ao_jogador <= self.alcance_visao:
            if self._verifica_linha_de_visao(inimigo_centro, jogador_centro, obstaculos_visao):
                self.alvo_identificado = True
            else:
                self.alvo_identificado = False # Visão bloqueada
        else:
            self.alvo_identificado = False # Jogador fora do alcance de visão

        # --- Lógica de Comportamento Baseado no Estado ---
        if self.alvo_identificado:
            self.timer_reacao += dt * 1000 # Converte dt para ms
            if self.timer_reacao >= self.tempo_reacao_ms:
                if self.estado == ESTADO_INIMIGO_PARADO or self.estado == ESTADO_INIMIGO_MOVENDO:
                    if distancia_ao_jogador <= self.alcance_ataque:
                        # Jogador ao alcance de ataque, tenta atacar
                        self._tenta_atacar(jogador_centro)
                    else:
                        # Jogador visível, mas fora do alcance de ataque, persegue
                        self.estado = ESTADO_INIMIGO_MOVENDO
                        self._perseguir_jogador(dt, jogador_centro, obstaculos_caminho)
                elif self.estado == ESTADO_INIMIGO_ATACANDO:
                    # Permanece no estado de ataque durante a duração
                    if pygame.time.get_ticks() - self.ultimo_ataque_tempo > self.duracao_ataque_ms:
                        self.estado = ESTADO_INIMIGO_RECARGA # Vai para recarga após o ataque
                elif self.estado == ESTADO_INIMIGO_RECARGA:
                    # Espera o tempo de recarga
                    if pygame.time.get_ticks() - self.ultimo_ataque_tempo > TEMPO_RECARGA_ATAQUE_INIMIGO_MS:
                        self.estado = ESTADO_INIMIGO_PARADO # Volta ao normal após recarga
        else:
            # Se não tem alvo, reseta o timer e volta a patrulhar ou ficar parado
            self.timer_reacao = 0
            if self.estado != ESTADO_INIMIGO_RECARGA: # Não interrompe recarga
                self.estado = ESTADO_INIMIGO_PARADO
            # Implementar patrulha simples aqui se desejar
            # self._patrulhar(dt, obstaculos_caminho)

        # Atualiza a posição do rect do inimigo com as coordenadas do mundo
        self.rect.topleft = (int(self.mundo_x), int(self.mundo_y))

    def _perseguir_jogador(self, dt, jogador_centro, obstaculos_caminho):
        # Move o inimigo em direção ao jogador
        # Vetor de direção normalizado
        direcao = jogador_centro - pygame.math.Vector2(self.mundo_x, self.mundo_y)
        if direcao.length() > 0: # Evita divisão por zero
            direcao.normalize_ip()

        dx = direcao.x * self.velocidade_corrida * dt
        dy = direcao.y * self.velocidade_corrida * dt

        # Tenta mover em X
        self.mundo_x += dx
        self.rect.topleft = (int(self.mundo_x), int(self.mundo_y))
        self._resolver_colisoes(obstaculos_caminho, 'x')

        # Tenta mover em Y
        self.mundo_y += dy
        self.rect.topleft = (int(self.mundo_x), int(self.mundo_y))
        self._resolver_colisoes(obstaculos_caminho, 'y')

    def _tenta_atacar(self, jogador_centro):
        agora = pygame.time.get_ticks()
        if self.estado != ESTADO_INIMIGO_ATACANDO and agora - self.ultimo_ataque_tempo >= TEMPO_RECARGA_ATAQUE_INIMIGO_MS:
            # Entra no estado de ataque
            self.estado = ESTADO_INIMIGO_ATACANDO
            self.ultimo_ataque_tempo = agora
            
            # Lógica para verificar se o ataque *acertou* o jogador
            # Isso é mais robusto na tela de jogo, mas podemos fazer uma verificação simples aqui
            inimigo_centro = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
            distancia = inimigo_centro.distance_to(jogador_centro)

            # Se a distância estiver dentro do alcance de ataque no momento do ataque, considere um acerto
            if distancia <= self.alcance_ataque:
                self.atingiu_jogador = True # Sinaliza que o jogador foi atingido
                print(f"Inimigo '{self.tipo_inimigo}' atacou e atingiu o jogador!")
            else:
                print(f"Inimigo '{self.tipo_inimigo}' atacou, mas o jogador estava fora do alcance imediato.")

    def _resolver_colisoes(self, obstaculos, direcao):
        colisoes = pygame.sprite.spritecollide(self, obstaculos, False)
        for obstaculo in colisoes:
            if direcao == 'x':
                if self.velocidade_atual > 0: # Movendo para a direita
                    self.mundo_x = obstaculo.rect.left - self.rect.width
                if self.velocidade_atual < 0: # Movendo para a esquerda
                    self.mundo_x = obstaculo.rect.right
                self.rect.x = int(self.mundo_x) # Atualiza a posição do rect
            elif direcao == 'y':
                if self.velocidade_atual > 0: # Movendo para baixo
                    self.mundo_y = obstaculo.rect.top - self.rect.height
                if self.velocidade_atual < 0: # Movendo para cima
                    self.mundo_y = obstaculo.rect.bottom
                self.rect.y = int(self.mundo_y) # Atualiza a posição do rect

    def _verifica_linha_de_visao(self, inicio, fim, obstaculos_visao):
        # Implementa um Raycasting simples para verificar a linha de visão.
        # Usa o rect do inimigo e do jogador, não apenas os pontos.
        # Converte para os pontos de mundo para o cálculo.

        # Criar uma "linha" ou "raio" que representa a linha de visão
        # Vamos verificar se esta linha intersecta qualquer obstáculo de visão.
        # Uma forma simples é usar pygame.Rect.clipline para verificar a interseção
        # com os rects dos obstáculos.

        for obstaculo in obstaculos_visao:
            # Se a linha do inimigo para o jogador intersecta o obstáculo
            if obstaculo.rect.clipline(inicio.x, inicio.y, fim.x, fim.y):
                return False # Linha de visão bloqueada
        return True # Linha de visão limpa

    def draw(self, screen, camera_x):
        # Desenha a imagem do inimigo
        screen.blit(self.image, (self.mundo_x - camera_x, self.mundo_y))

        # --- Desenhar círculos de visão e cones (DEBUG) ---
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            centro_inimigo_tela_x = self.mundo_x - camera_x + self.rect.width // 2
            centro_inimigo_tela_y = self.mundo_y + self.rect.height // 2 # Y não tem offset de câmera no seu setup

            # Círculo de alcance de visão
            pygame.draw.circle(screen, (255, 255, 0, 50),
                               (centro_inimigo_tela_x, centro_inimigo_tela_y),
                               self.alcance_visao, 1)

            # Desenha o cone de visão (apenas se tiver um alvo e o timer for maior que 0)
            if self.alvo_identificado and self.timer_reacao > 0:
                # Calcular os pontos para o cone de visão
                raio = self.alcance_visao
                angulo_meio = self.angulo_visao / 2
                
                # Ajusta os ângulos baseados na direção do inimigo
                if self.olhando_direita:
                    start_angle_rad = -angulo_meio
                    end_angle_rad = angulo_meio
                else:
                    start_angle_rad = math.pi - angulo_meio
                    end_angle_rad = math.pi + angulo_meio

                # Desenhar o arco do cone de visão
                pygame.draw.arc(screen, (0, 255, 0),
                                pygame.Rect(centro_inimigo_tela_x - raio,
                                            centro_inimigo_tela_y - raio,
                                            raio * 2, raio * 2),
                                start_angle_rad, end_angle_rad, 2)
                
                # Desenhar linhas do cone (opcional, para visualização mais clara)
                # ponto_foco = pygame.math.Vector2(centro_inimigo_tela_x, centro_inimigo_tela_y)
                # ponta_cone1 = ponto_foco + pygame.math.Vector2(raio * math.cos(start_angle_rad), raio * math.sin(start_angle_rad))
                # ponta_cone2 = ponto_foco + pygame.math.Vector2(raio * math.cos(end_angle_rad), raio * math.sin(end_angle_rad))
                # pygame.draw.line(screen, (0, 255, 0), ponto_foco, ponta_cone1, 2)
                # pygame.draw.line(screen, (0, 255, 0), ponto_foco, ponta_cone2, 2)

            # Desenhar caixa de colisão do inimigo (DEBUG)
            debug_rect = pygame.Rect(self.mundo_x - camera_x, self.mundo_y, self.rect.width, self.rect.height)
            pygame.draw.rect(screen, COR_CAIXA_COLISAO, debug_rect, 2) # Desenha a borda do rect