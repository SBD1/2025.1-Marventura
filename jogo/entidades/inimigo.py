# entidades/inimigo.py
import pygame
import random
import math
from utilidades.constantes import *

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, gerenciador_recursos, x_inicial, y_inicial, id_inimigo, identificador_instancia_lacaio, tipo_inimigo,
                 descricao, vida_atual, vida_total, nivel, experiencia, habilidade, inventario, caminho_container):
        super().__init__()
        self.gerenciador_recursos = gerenciador_recursos
        self.identificador_inimigo = id_inimigo
        self.identificador_instancia_lacaio = identificador_instancia_lacaio
        self.nome = tipo_inimigo
        self.velocidade_caminhada = VELOCIDADE_CAMINHADA_INIMIGO
        self.velocidade_corrida = VELOCIDADE_CORRIDA_INIMIGO
        self.velocidade_atual = VELOCIDADE_CAMINHADA_INIMIGO
        self.alcance_visao = ALCANCE_VISAO
        self.angulo_visao = math.radians(ANGULO_VISAO)
        self.tempo_reacao_ms = TEMPO_REACAO_INIMIGO
        self.caminho_container = caminho_container
        self.descricao = descricao
        self.vida_atual = vida_atual
        self.vida_total = vida_total
        self.nivel = nivel
        self.experiencia = experiencia
        self.habilidade = habilidade
        self.inventario = inventario

        self.imagens_animacao = {}
        self.carregar_animacoes(tipo_inimigo)
        self.frame_atual = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.velocidade_animacao = 150 # ms por frame

        # Define a imagem inicial. Se não houver frames carregados, usa fallback.
        self.image = self.imagens_animacao.get(0)
        if not self.image:
            print(f"AVISO: Imagens de animação para '{tipo_inimigo}' não encontradas. Usando fallback.")
            self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
            self.image.fill(VERMELHO)

        self.rect = self.image.get_rect(topleft=(x_inicial, y_inicial))
        self.mundo_x = x_inicial
        self.mundo_y = y_inicial
        self.olhando_direita = True

        self.estado = ESTADO_INIMIGO_PARADO
        self.timer_reacao = 0
        self.ultimo_ataque_tempo = 0
        self.duracao_ataque_ms = DURACAO_ATAQUE_INIMIGO_MS
        self.alcance_ataque = DISTANCIA_ATAQUE_INIMIGO
        self.alvo_identificado = False
        self.atingiu_jogador = False

        # Patrulha
        self.direcao_patrulha = pygame.math.Vector2(0, 0)
        self.tempo_patrulha_restante = 0  # ms
        self.icone_alerta = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_ALERTA)
        self.icone_interrogacao = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_INTERROGACAO)

    def carregar_animacoes(self, chave_base):
        # Carrega as imagens de animação com base na chave_base (ex: 'lobo', 'corvo')
        # e os sufixos '_0', '_1', etc.
        i = 0
        while True:
            chave_frame = f"{chave_base}_{i}"
            imagem_frame = self.gerenciador_recursos.obter_imagem(chave_frame)
            if imagem_frame:
                self.imagens_animacao[i] = imagem_frame
                i += 1
            else:
                break
        if not self.imagens_animacao:
            print(f"AVISO: Nenhuma imagem de animação encontrada para a chave base: {chave_base}")

    def _atualiza_animacao(self, dt):
        agora = pygame.time.get_ticks()
        # Se o inimigo estiver se movendo, avança a animação
        if self.estado == ESTADO_INIMIGO_PERSEGUINDO or self.estado == ESTADO_INIMIGO_PATRULHANDO:
            if agora - self.tempo_ultimo_frame > self.velocidade_animacao:
                self.frame_atual = (self.frame_atual + 1) % len(self.imagens_animacao)
                self.tempo_ultimo_frame = agora
        else: # Se o inimigo não estiver se movendo, volta para o frame 0 (repouso)
            self.frame_atual = 0

        # Define a imagem atual e aplica o flip se necessário
        current_animation_image = self.imagens_animacao.get(self.frame_atual)
        if current_animation_image:
            if self.olhando_direita:
                self.image = pygame.transform.flip(current_animation_image, True, False)
            else:
                self.image = current_animation_image
        else:
            # Fallback se o frame atual não for encontrado (nunca deveria acontecer se as imagens forem carregadas corretamente)
            self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
            self.image.fill(VERMELHO)

    def atualizar(self, dt, jogador, obstaculos_caminho, obstaculos_visao):
        self.atingiu_jogador = False

        inimigo_centro = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        jogador_centro = pygame.math.Vector2(jogador.rect.centerx, jogador.rect.centery)
        distancia_ao_jogador = inimigo_centro.distance_to(jogador_centro)

        # Atualiza a direção que o inimigo está olhando com base no jogador
        # Apenas se o inimigo estiver perseguindo ou se houver um alvo identificado.
        # Caso contrário, a direção é definida pela patrulha.
        if self.alvo_identificado or self.estado == ESTADO_INIMIGO_PERSEGUINDO:
             self.olhando_direita = jogador_centro.x > inimigo_centro.x

        # Visão
        if distancia_ao_jogador <= self.alcance_visao:
            self.alvo_identificado = self._verifica_linha_de_visao(inimigo_centro, jogador.rect, obstaculos_visao)
            self.estado = ESTADO_INIMIGO_ALERTA
        else:
            self.alvo_identificado = False

        if self.alvo_identificado:
            self.timer_reacao += dt * 1000
            if self.timer_reacao >= self.tempo_reacao_ms:
                if self.estado in (ESTADO_INIMIGO_PARADO, ESTADO_INIMIGO_PATRULHANDO, ESTADO_INIMIGO_ALERTA):
                    if distancia_ao_jogador <= self.alcance_ataque:
                        self._tenta_atacar(jogador_centro)
                    else:
                        self.estado = ESTADO_INIMIGO_PERSEGUINDO # <-- Aqui ele começa a se mover para perseguir
                        self._perseguir_jogador(dt, jogador_centro, obstaculos_caminho)
                elif self.estado == ESTADO_INIMIGO_ATACANDO:
                    if pygame.time.get_ticks() - self.ultimo_ataque_tempo > self.duracao_ataque_ms:
                        self.estado = ESTADO_INIMIGO_RECARGA
                elif self.estado == ESTADO_INIMIGO_RECARGA:
                    if pygame.time.get_ticks() - self.ultimo_ataque_tempo > TEMPO_RECARGA_ATAQUE_INIMIGO_MS:
                        self.estado = ESTADO_INIMIGO_PARADO # <-- Volta para parado após recarga
            else: # Durante o tempo de reação, mas ainda não agiu
                # Adicionar este bloco para garantir que o inimigo pare de se mover
                # e entre no estado 'parado' durante o tempo de reação
                if self.estado == ESTADO_INIMIGO_PERSEGUINDO: # Se ele estava se movendo antes de reagir
                    self.estado = ESTADO_INIMIGO_PARADO # Coloca ele no estado parado
        else: # Sem alvo identificado
            self.timer_reacao = 0
            if self.estado != ESTADO_INIMIGO_RECARGA:
                # Se o estado não for recarga, patrulha
                if self.caminho_container: # Só patrulha se tiver um caminho definido
                    self.estado = ESTADO_INIMIGO_PATRULHANDO
                    self._patrulhar(dt, obstaculos_caminho)
                else:
                    self.estado = ESTADO_INIMIGO_PARADO # Fica parado se não tiver onde patrulhar


        # Primeiro, atualiza o rect com base nas coordenadas do mundo calculadas
        self.rect.topleft = (int(self.mundo_x), int(self.mundo_y))

        # NOVO: Aplica o clamp para confinar o inimigo ao seu caminho
        if self.caminho_container:
            self.rect.clamp_ip(self.caminho_container)
            # Re-sincroniza as coordenadas de mundo com a posição do rect após o clamp
            self.mundo_x = float(self.rect.x)
            self.mundo_y = float(self.rect.y)

        # Atualiza a animação com base no estado de movimento
        self._atualiza_animacao(dt)

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

            # Atualiza a direção que o inimigo está olhando com base no movimento de patrulha
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


    def _tenta_atacar(self, jogador_centro):
        agora = pygame.time.get_ticks()
        if self.estado != ESTADO_INIMIGO_ATACANDO and agora - self.ultimo_ataque_tempo >= TEMPO_RECARGA_ATAQUE_INIMIGO_MS:
            self.estado = ESTADO_INIMIGO_ATACANDO
            self.ultimo_ataque_tempo = agora

            inimigo_centro = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
            distancia = inimigo_centro.distance_to(jogador_centro)

            if distancia <= self.alcance_ataque:
                self.atingiu_jogador = True
                print(f"Inimigo '{self.nome}' atacou e atingiu o jogador!")
            else:
                print(f"Inimigo '{self.nome}' atacou, mas o jogador estava fora do alcance.")

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


    def _verifica_linha_de_visao(self, inimigo_centro, retangulo_do_jogador, obstaculos_visao):
        # NOVO: Só enxerga se o jogador estiver dentro do mesmo caminho_container
        if self.caminho_container and not self.caminho_container.colliderect(retangulo_do_jogador):
            return False

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
        for corner in self._cantos(retangulo_do_jogador):
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


    def desenhar(self, tela, camera_x):
        # --- Desenha o campo de visão do inimigo ---
        centro_x = self.mundo_x - camera_x + self.rect.width // 2
        centro_y = self.mundo_y + self.rect.height // 2
        origem = pygame.math.Vector2(centro_x, centro_y)
    
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
        superficie = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(superficie, (255, 0, 0, 100), pontos_cone)
        tela.blit(superficie, (0, 0))


        # --- Desenha o inimigo ---
        tela.blit(self.image, (self.mundo_x - camera_x, self.mundo_y))

        icone = None
        if self.alvo_identificado and self.timer_reacao < self.tempo_reacao_ms:
            icone = self.icone_interrogacao
        elif self.estado == ESTADO_INIMIGO_PERSEGUINDO and self.alvo_identificado:
            icone = self.icone_alerta
            
        if icone:
            icone_x = self.mundo_x - camera_x + self.rect.width // 2 - icone.get_width() // 2
            icone_y = self.mundo_y - icone.get_height() - 10  # Acima da cabeça, com margem
            tela.blit(icone, (icone_x, icone_y))


        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            # Desenha o alcance circular
            pygame.draw.circle(tela, (255, 255, 0), (int(centro_x), int(centro_y)), self.alcance_visao, 1)
            pygame.draw.polygon(tela, (0, 255, 0), pontos_cone, 1)
            
