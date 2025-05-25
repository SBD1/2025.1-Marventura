# entidades/inimigo.py
import pygame
import random
import math
from utilidades.constantes import *

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, resource_manager, x_inicial, y_inicial, tipo_inimigo,
                 velocidade_caminhada, velocidade_corrida, alcance_visao, angulo_visao_graus,
                 tempo_reacao_ms, imagem_chave, cor_fallback=VERMELHO,
                 alcance_ataque=DISTANCIA_ATAQUE_INIMIGO, duracao_ataque_ms=DURACAO_ATAQUE_INIMIGO_MS):
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
        self.image = self.imagem_original if self.imagem_original else pygame.Surface((80, 80), pygame.SRCALPHA)
        if not self.imagem_original:
            print(f"AVISO: Imagem '{imagem_chave}' não encontrada para o inimigo '{tipo_inimigo}'. Usando fallback.")
            self.image.fill(self.cor_fallback)

        self.rect = self.image.get_rect(topleft=(x_inicial, y_inicial))
        self.mundo_x = x_inicial
        self.mundo_y = y_inicial
        self.olhando_direita = True

        self.estado = ESTADO_INIMIGO_PARADO
        self.timer_reacao = 0
        self.ultimo_ataque_tempo = 0
        self.duracao_ataque_ms = duracao_ataque_ms
        self.alcance_ataque = alcance_ataque
        self.alvo_identificado = False
        self.atingiu_jogador = False

        # Patrulha
        self.direcao_patrulha = pygame.math.Vector2(0, 0)
        self.tempo_patrulha_restante = 0  # ms
        self.icone_alerta = self.resource_manager.get_image(CHAVE_ICONE_ALERTA)
        self.icone_interrogacao = self.resource_manager.get_image(CHAVE_ICONE_INTERROGACAO)


    def update(self, dt, jogador, obstaculos_caminho, obstaculos_visao):
        self.atingiu_jogador = False

        inimigo_centro = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        jogador_centro = pygame.math.Vector2(jogador.rect.centerx, jogador.rect.centery)
        distancia_ao_jogador = inimigo_centro.distance_to(jogador_centro)

        self.olhando_direita = jogador_centro.x > inimigo_centro.x

        # Visão
        if distancia_ao_jogador <= self.alcance_visao:
            self.alvo_identificado = self._verifica_linha_de_visao(inimigo_centro, jogador.rect, obstaculos_visao)

        else:
            self.alvo_identificado = False

        if self.alvo_identificado:
            self.timer_reacao += dt * 1000
            if self.timer_reacao >= self.tempo_reacao_ms:
                if self.estado in (ESTADO_INIMIGO_PARADO, ESTADO_INIMIGO_MOVENDO):
                    if distancia_ao_jogador <= self.alcance_ataque:
                        self._tenta_atacar(jogador_centro)
                    else:
                        self.estado = ESTADO_INIMIGO_MOVENDO
                        self._perseguir_jogador(dt, jogador_centro, obstaculos_caminho)
                elif self.estado == ESTADO_INIMIGO_ATACANDO:
                    if pygame.time.get_ticks() - self.ultimo_ataque_tempo > self.duracao_ataque_ms:
                        self.estado = ESTADO_INIMIGO_RECARGA
                elif self.estado == ESTADO_INIMIGO_RECARGA:
                    if pygame.time.get_ticks() - self.ultimo_ataque_tempo > TEMPO_RECARGA_ATAQUE_INIMIGO_MS:
                        self.estado = ESTADO_INIMIGO_PARADO
        else:
            self.timer_reacao = 0
            if self.estado != ESTADO_INIMIGO_RECARGA:
                self.estado = ESTADO_INIMIGO_MOVENDO
                self._patrulhar(dt, obstaculos_caminho)

        if self.imagem_original:
            if self.olhando_direita:
                print("Olhando para DIREITA → aplicando flip")
                self.image = pygame.transform.flip(self.imagem_original, True, False)
            else:
                print("Olhando para ESQUERDA → imagem normal")
                self.image = self.imagem_original


        self.rect.topleft = (int(self.mundo_x), int(self.mundo_y))

    def _patrulhar(self, dt, obstaculos):
        if self.tempo_patrulha_restante <= 0:
            direcoes = [
                pygame.math.Vector2(1, 0), pygame.math.Vector2(-1, 0),
                pygame.math.Vector2(0, 1), pygame.math.Vector2(0, -1),
                pygame.math.Vector2(1, 1), pygame.math.Vector2(-1, -1),
                pygame.math.Vector2(1, -1), pygame.math.Vector2(-1, 1),
                pygame.math.Vector2(0, 0)
            ]
            self.direcao_patrulha = random.choice(direcoes)
            if self.direcao_patrulha.length() > 0:
                self.direcao_patrulha = self.direcao_patrulha.normalize()
            self.tempo_patrulha_restante = random.randint(1000, 3000)
        else:
            self.tempo_patrulha_restante -= dt * 1000

            dx = self.direcao_patrulha.x * self.velocidade_caminhada * dt
            dy = self.direcao_patrulha.y * self.velocidade_caminhada * dt

            self.mundo_x += dx
            self.rect.topleft = (int(self.mundo_x), int(self.mundo_y))
            self._resolver_colisoes(obstaculos, 'x', dx)

            self.mundo_y += dy
            self.rect.topleft = (int(self.mundo_x), int(self.mundo_y))
            self._resolver_colisoes(obstaculos, 'y', dy)

            if dx > 0:
                self.olhando_direita = True
            elif dx < 0:
                self.olhando_direita = False


    def _perseguir_jogador(self, dt, jogador_centro, obstaculos):
        direcao = jogador_centro - pygame.math.Vector2(self.mundo_x, self.mundo_y)
        if direcao.length() > 0:
            direcao.normalize_ip()

        dx = direcao.x * self.velocidade_corrida * dt
        dy = direcao.y * self.velocidade_corrida * dt

        self.mundo_x += dx
        self.rect.topleft = (int(self.mundo_x), int(self.mundo_y))
        self._resolver_colisoes(obstaculos, 'x', dx)

        self.mundo_y += dy
        self.rect.topleft = (int(self.mundo_x), int(self.mundo_y))
        self._resolver_colisoes(obstaculos, 'y', dy)

        if dx > 0:
            self.olhando_direita = True
        elif dx < 0:
            self.olhando_direita = False

    def _tenta_atacar(self, jogador_centro):
        agora = pygame.time.get_ticks()
        if self.estado != ESTADO_INIMIGO_ATACANDO and agora - self.ultimo_ataque_tempo >= TEMPO_RECARGA_ATAQUE_INIMIGO_MS:
            self.estado = ESTADO_INIMIGO_ATACANDO
            self.ultimo_ataque_tempo = agora

            inimigo_centro = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
            distancia = inimigo_centro.distance_to(jogador_centro)

            if distancia <= self.alcance_ataque:
                self.atingiu_jogador = True
                print(f"Inimigo '{self.tipo_inimigo}' atacou e atingiu o jogador!")
            else:
                print(f"Inimigo '{self.tipo_inimigo}' atacou, mas o jogador estava fora do alcance.")

    def _resolver_colisoes(self, obstaculos, direcao, delta):
        colisoes = pygame.sprite.spritecollide(self, obstaculos, False)
        for obstaculo in colisoes:
            if direcao == 'x':
                if delta > 0:  # Indo para a direita
                    self.mundo_x = obstaculo.rect.left - self.rect.width
                elif delta < 0:  # Indo para a esquerda
                    self.mundo_x = obstaculo.rect.right
                self.rect.x = int(self.mundo_x)
            elif direcao == 'y':
                if delta > 0:  # Indo para baixo
                    self.mundo_y = obstaculo.rect.top - self.rect.height
                elif delta < 0:  # Indo para cima
                    self.mundo_y = obstaculo.rect.bottom
                self.rect.y = int(self.mundo_y)


    def _verifica_linha_de_visao(self, inimigo_centro, jogador_rect, obstaculos_visao):
        # Verifica se o retângulo do jogador está dentro do cone de visão

        raio = self.alcance_visao
        origem = inimigo_centro
        angulo_base = 0 if self.olhando_direita else math.pi
        angulo_inicio = angulo_base - self.angulo_visao / 2
        angulo_fim = angulo_base + self.angulo_visao / 2

        # Gera pontos do cone
        num_pontos = 20
        pontos_cone = [origem]
        for i in range(num_pontos + 1):
            t = i / num_pontos
            angulo = angulo_inicio + (angulo_fim - angulo_inicio) * t
            ponto = origem + pygame.math.Vector2(math.cos(angulo), math.sin(angulo)) * raio
            pontos_cone.append(ponto)

        # Cria o cone como um polígono
        cone_path = pontos_cone

        # Verifica se algum ponto do retângulo do jogador está dentro do cone
        for corner in self._cantos(jogador_rect):
            if self._ponto_dentro_poligono(corner, cone_path):
                # Verifica linha de visão
                if all(not o.rect.clipline(origem.x, origem.y, corner[0], corner[1]) for o in obstaculos_visao):
                    return True

        return False

    def _cantos(self, rect):
        return [
            (rect.left, rect.top),
            (rect.right, rect.top),
            (rect.right, rect.bottom),
            (rect.left, rect.bottom)
        ]

    def _ponto_dentro_poligono(self, ponto, poligono):
        x, y = ponto
        dentro = False
        j = len(poligono) - 1
        for i in range(len(poligono)):
            xi, yi = poligono[i]
            xj, yj = poligono[j]
            intersecta = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-6) + xi)
            if intersecta:
                dentro = not dentro
            j = i
        return dentro


    def draw(self, tela, camera_x):
        tela.blit(self.image, (self.mundo_x - camera_x, self.mundo_y))

        icone = None
        icone = None
        if self.alvo_identificado and self.timer_reacao < self.tempo_reacao_ms:
            icone = self.icone_interrogacao
        elif self.estado == ESTADO_INIMIGO_MOVENDO and self.alvo_identificado:
            icone = self.icone_alerta
            
        if icone:
            icone_x = self.mundo_x - camera_x + self.rect.width // 2 - icone.get_width() // 2
            icone_y = self.mundo_y - icone.get_height() - 10  # Acima da cabeça, com margem
            tela.blit(icone, (icone_x, icone_y))


        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            centro_x = self.mundo_x - camera_x + self.rect.width // 2
            centro_y = self.mundo_y + self.rect.height // 2
            origem = pygame.math.Vector2(centro_x, centro_y)

            # Desenha o alcance circular
            pygame.draw.circle(tela, (255, 255, 0), (int(centro_x), int(centro_y)), self.alcance_visao, 1)

            # Desenha o cone de visão como um polígono (visualmente mais fácil)
            raio = self.alcance_visao
            angulo_base = 0 if self.olhando_direita else math.pi  # 0 rad = direita, π rad = esquerda

            angulo_inicio = angulo_base - self.angulo_visao / 2
            angulo_fim = angulo_base + self.angulo_visao / 2

            # Gera pontos do cone
            num_pontos = 20  # mais pontos = cone mais liso
            pontos_cone = [origem]
            for i in range(num_pontos + 1):
                t = i / num_pontos
                angulo = angulo_inicio + (angulo_fim - angulo_inicio) * t
                ponto = origem + pygame.math.Vector2(math.cos(angulo), math.sin(angulo)) * raio
                pontos_cone.append(ponto)

            # Desenha o cone como polígono semi-transparente
            pygame.draw.polygon(tela, (0, 255, 0, 100), pontos_cone, 1)
