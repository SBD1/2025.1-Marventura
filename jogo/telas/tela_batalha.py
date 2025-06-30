# telas/tela_batalha.py

import pygame
import math
from utilidades.constantes import *
from .tela_modelo import TelaModelo
from componentes import BarraDeEstado



class _IconeAcao:
    def __init__(self, imagem, acao=None):
        self.image = imagem
        self.rect = self.image.get_rect()
        self.acao = acao
    
    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

class TelaBatalha(TelaModelo):
    _kit_do_explorador_personagem = {
        'espaco_arma': {
            'arma': 'None',
            'habilidades': ['Ataque Rápido', 'Golpe Poderoso']
        },
        'espaco_acessorio': {
            'acessorio': 'Anel de Proteção',
            'efeitos': ['+5 PV', 'Resistência a Fogo']
        },
        'espaco_fruta': {
            'fruta': 'Mimi Mimi no Mi',
            'habilidades': ['Golpe sônico', 'Ilusão de som']
        }
    }
    _mochila = {
        'item 1': {
            'nome': 'Fruta do Mar Azul 🫐',
            'efeitos': [
                {'tipo': 'PE', 'valor': 2}
            ]
        },
        'item 2': {
            'nome': 'Fruta do Mar Vermelha 🍒',
            'efeitos': [
                {'tipo': 'PV', 'valor': 2}
            ]
        },
        'item 3': {
            'nome': 'Folha de Hortelã 🍃',
            'efeitos': [
                {'tipo': 'PE', 'valor': 1},
                {'tipo': 'PV', 'valor': 1}
            ]
        }
    }

    def __init__(self, gerenciador_telas, gerenciador_recursos, personagem, inimigos_na_batalha, jogador_x, jogador_y, jogador_olhando_direita, mapa_retorno_id):
        super().__init__(gerenciador_telas, gerenciador_recursos)
        self.personagem = personagem
        self.vida_jogador = 10
        self.vida_jogador_max = 10
        self.energia_jogador = 5
        self.energia_jogador_max = 5

        
        # Dados do jogador para retornar ao mapa
        self.jogador_x_retorno = jogador_x
        self.jogador_y_retorno = jogador_y
        self.jogador_olhando_direita_retorno = jogador_olhando_direita
        self.mapa_retorno_id = mapa_retorno_id

        # Carrega o fundo da batalha
        self.fundo_batalha = self.gerenciador_recursos.obter_imagem(CHAVE_CAMPO_DE_BATALHA_CAMPOS)
        if not self.fundo_batalha:
            self.fundo_batalha = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.fundo_batalha.fill(CINZA_ESCURO)
            print("AVISO: Imagem 'batalha_fundo_padrao' não encontrada. Usando fundo cinza.")

        # Carrega a imagem do personagem
        self.imagem_jogador = self.gerenciador_recursos.obter_imagem(f'{SHUAN}_em_repouso' if self.personagem == SHUAN else f'{SILVIE}_em_repouso')
        if not self.imagem_jogador:
            print(f"AVISO: Imagem de batalha para o personagem '{self.personagem}' não encontrada.")
            self.imagem_jogador = pygame.Surface((100, 100))
            self.imagem_jogador.fill(AZUL)

        # Inicializa os ícones de ação
        self.icones_acao = [
            _IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_ESTRATEGIAS), acao="fugir"),
            _IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_MOCHILA), acao="mochila"),
        ]
        self._icones_acao_equipaveis()
        
        # Interface de batalha
        self.barra_de_estado = BarraDeEstado(self.gerenciador_recursos)
        self.titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TITULO)
        self.tempo_mensagem_onda = 0
        self.texto_mensagem_onda = ""
        self.posicao_jogador = (180, ALTURA_TELA - 170)

        # Prepara a lista de inimigos que serão enfrentados
        self.ondas_pendentes = inimigos_na_batalha
        self.numero_da_onda = 0
        self._carregar_proxima_onda()

        self.imagens_de_inimigos = []
        for inimigo in self.inimigos:
            self.imagens_de_inimigos.append(self.gerenciador_recursos.obter_imagem(inimigo['imagem']))
            if not self.imagens_de_inimigos:
                print(f"AVISO: Imagem de batalha para '{inimigo['tipo']}' não encontrada. Usando cor fallback.")
                self.imagem_inimigo = pygame.Surface((150, 150))
                self.imagem_inimigo.fill(VERMELHO)

        self.estado_batalha = "turno_jogador"  # outros: "turno_inimigo", "esperando_ataque"
        self.tempo_proximo_ataque = 0
        self.inimigo_index_atacando = 0

        self.tempo_dano_jogador = 0
        self.danos_flutuantes = []


        self.menu_mochila_ativo = False
        self.item_selecionado = None

    def _icones_acao_equipaveis(self):
        fruta = self._kit_do_explorador_personagem['espaco_fruta']['fruta']
        arma = self._kit_do_explorador_personagem['espaco_arma']['arma']

        if fruta == "Mimi Mimi no Mi":
            self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_FRUTA), acao="fruta"))

        if arma == "Espada":
            self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_ESPADA), acao="espada"))
        elif arma == "Arco e Flecha":
            self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_PROJETIL), acao="projetil"))
        else:
            chave_soco = CHAVE_ACAO_SOCO_SILVIE if self.personagem == SILVIE else CHAVE_ACAO_SOCO_SHUAN
            self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(chave_soco), acao="soco"))
        
    def _carregar_proxima_onda(self):
        if not self.ondas_pendentes:
            self.inimigos = []        # força término da batalha
            return False

        self.inimigos = self.ondas_pendentes.pop(0)            # lista de 3 dicts
        
        # Posicionamento dos inimigos (exemplo com 3 posições)
        posicoes = [
            (LARGURA_TELA - 350, ALTURA_TELA - 225),  # Inimigo 1 (esquerda)
            (LARGURA_TELA - 250, ALTURA_TELA - 150),  # Inimigo 2 (centro, mais à frente)
            (LARGURA_TELA - 120, ALTURA_TELA - 200)    # Inimigo 3 (direita)
        ]

        self.inimigos_animados = []
        for i, inimigo in enumerate(self.inimigos):
            imagem = self.gerenciador_recursos.obter_imagem(inimigo['imagem'])
            posicao_final = posicoes[i % len(posicoes)]
            animado = InimigoAnimado(imagem, posicao_final)
            self.inimigos_animados.append(animado)

        """self.imagens_de_inimigos = [
            self.gerenciador_recursos.obter_imagem(inimigo['imagem'])
            for inimigo in self.inimigos
        ]"""
        self.numero_da_onda += 1
        print(f"🌊 Iniciando onda {self.numero_da_onda} com {self.inimigos[0]['tipo']}")
        
        # Mostrar texto "Onda x/n"
        total_ondas = self.numero_da_onda + len(self.ondas_pendentes)
        self.texto_mensagem_onda = f"Onda {self.numero_da_onda}/{total_ondas}"
        self.tempo_mensagem_onda = 2.5  # segundos visíveis

        # garantir que o turno recomeça do jogador
        self.estado_batalha = "turno_jogador"
        self.tempo_proximo_ataque = 0
        self.inimigo_index_atacando = 0
        
        return True

    def usar_item_da_mochila(self, chave_item):
        item = self._mochila.get(chave_item)
        if not item:
            return

        for efeito in item["efeitos"]:
            if efeito["tipo"] == "PV":
                self.vida_jogador += efeito["valor"]
                if self.vida_jogador > self.vida_jogador_max:
                    self.vida_jogador = self.vida_jogador_max
                print(f"+{efeito['valor']} PV → atual: {self.vida_jogador}")
    
            elif efeito["tipo"] == "PE":
                self.energia_jogador += efeito["valor"]
                if self.energia_jogador > self.energia_jogador_max:
                    self.energia_jogador = self.energia_jogador_max
                print(f"+{efeito['valor']} PE → atual: {self.energia_jogador}")

        # Atualiza a barra de estado do jogador
        self.barra_de_estado.atualizar_estado(
            self.vida_jogador,
            self.vida_jogador_max,
            self.energia_jogador,
            self.energia_jogador_max
        )

        # Remove da mochila (ou marque como usado)
        del self._mochila[chave_item]

        # Fecha o menu e passa a vez
        self.menu_mochila_ativo = False
        print("Passa o turno depois de usar o item")
        self.inimigos_realizam_turno()

    def inimigos_realizam_turno(self):
        print("Turno dos inimigos!")
        self.estado_batalha = "turno_inimigo"
        self.tempo_proximo_ataque = 0.5  # tempo de espera antes do primeiro ataque
        self.inimigo_index_atacando = 0
        

        # Atualiza a barra de estado do jogador
        self.barra_de_estado.atualizar_estado(
            self.vida_jogador,
            self.vida_jogador_max,
            self.energia_jogador,
            self.energia_jogador_max
        )

        # Checar se jogador morreu
        if self.vida_jogador <= 0:
            print("Jogador foi derrotado!")
            self.fim_batalha(venceu=False)
    
    def fim_batalha(self, venceu):
        if venceu:
            print("Todos os inimigos foram derrotados! Você venceu a batalha!")
        else:
            print("Você foi derrotado! A batalha terminou.")
        # Retorna para a tela do mapa
        self.gerenciador_telas.mudar_tela(
            CHAVE_TRANSICAO_MAPA,
            id_mapa=self.mapa_retorno_id,
            personagem=self.personagem,
            coordenada_x=self.jogador_x_retorno,
            coordenada_y=self.jogador_y_retorno,
            olhando_para_direita=self.jogador_olhando_direita_retorno
        )
 
    def draw(self, tela):
        tela.blit(self.fundo_batalha, (0, 0))

        if self.imagem_jogador:
            imagem = self.imagem_jogador
            if self.tempo_dano_jogador > 0:
                imagem = pygame.transform.rotate(imagem, 15)  # inclina para trás

            rect = imagem.get_rect(center=self.posicao_jogador)
            tela.blit(imagem, rect)


        # Desenhar todos os inimigos da onda atual
        for animado in self.inimigos_animados:
            animado.draw(tela)

        fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
        for dano in self.danos_flutuantes:
            dano.draw(tela, fonte)

        # Desenha a barra de estado
        self.barra_de_estado.desenhar(tela)

        centro = (self.posicao_jogador)
        raio = 220  # distância do personagem

        if self.estado_batalha == "turno_jogador":
            # Suponha que icones_acao seja uma lista de objetos que têm .image e .rect
            self.distribuir_icones_em_arco(self.icones_acao, centro, raio)

            # Depois desenhe normalmente:
            for icone in self.icones_acao:
                tela.blit(icone.image, icone.rect)

        if self.tempo_mensagem_onda > 0:
            texto = self.titulo.render(self.texto_mensagem_onda, True, BRANCO_CLARO)
            rect = texto.get_rect(center=(LARGURA_TELA * 4/5, 125))
            tela.blit(texto, rect)

        if self.menu_mochila_ativo:
            fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
            y_base = 100
            largura_caixa = 400
            altura_caixa = 40
            x = LARGURA_TELA // 2 - largura_caixa // 2

            if not self._mochila:
                texto = fonte.render("Mochila vazia.", True, BRANCO_CLARO)
                tela.blit(texto, (x + 20, y_base + 20))
            else:
                    for i, chave in enumerate(self._mochila.keys()):
                        item = self._mochila[chave]
                        nome = item['nome']
                        texto = fonte.render(f"{i+1}. {nome}", True, BRANCO_CLARO)
                        y = y_base + i * altura_caixa
                        pygame.draw.rect(tela, (30, 30, 30), (x, y, largura_caixa, altura_caixa))
                        tela.blit(texto, (x + 10, y + 10))

    def distribuir_icones_em_arco(self, icones, centro, raio, angulo_inicial=-90, angulo_total=90):
        """
        Distribui os ícones em arco.
        - icones: lista de surfaces ou objetos com .image e .rect
        - centro: (x, y) onde ficará o centro do arco (geralmente o personagem)
        - raio: distância do centro até os ícones
        - angulo_inicial: ângulo onde o primeiro ícone aparecerá (em graus, -90 é topo)
        - angulo_total: arco total em graus (ex: 180 para meio círculo)
        """
        total = len(icones)
        
        if total == 0:
            return
        if total == 1:
            angulos = [math.radians(angulo_inicial)]
        else:
            passo = angulo_total / (total - 1)
            angulos = [math.radians(angulo_inicial + i * passo) for i in range(total)]
        for i, angulo in enumerate(angulos):
            x = centro[0] + raio * math.cos(angulo)
            y = centro[1] + raio * math.sin(angulo)
            rect = icones[i].image.get_rect(center=(x, y))
            icones[i].rect = rect  # Se for um objeto

    def handle_input(self, evento):
        # Chama o handle_input da base para eventos comuns (ex: QUIT)
        super().handle_input(evento)

        """# Fecha a mochila com ESC
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE and self.menu_mochila_ativo:
                print("Fechando mochila")
                self.menu_mochila_ativo = False
                return
        """
        if self.estado_batalha != "turno_jogador":
            return
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Se o menu da mochila está aberto, verifica clique nos itens
            if self.menu_mochila_ativo:
                x = LARGURA_TELA // 2 - 200
                y_base = 100
                altura_caixa = 40

                if not self._mochila:
                    print("Mochila vazia – nada para usar.")
                else:
                    for i, chave in enumerate(self._mochila.keys()):
                        y = y_base + i * altura_caixa
                        rect = pygame.Rect(x, y, 400, altura_caixa)
                        if rect.collidepoint(evento.pos):
                            print(f"Usar item: {self._mochila[chave]['nome']}")
                            self.usar_item_da_mochila(chave)
                            return

                # Se clicou fora da área dos itens → fecha mochila
                print("Clique fora da mochila – fechando.")
                self.menu_mochila_ativo = False
                return

            for icone in self.icones_acao:
                if icone.rect.collidepoint(evento.pos):
                    match icone.acao:
                        case "fugir":
                            self.gerenciador_telas.mudar_tela(
                                CHAVE_TRANSICAO_MAPA,
                                id_mapa=self.mapa_retorno_id,
                                personagem=self.personagem,
                                coordenada_x=self.jogador_x_retorno,
                                coordenada_y=self.jogador_y_retorno,
                                olhando_para_direita=self.jogador_olhando_direita_retorno
                            )
                            return

                        case "mochila":
                            print("Abrir mochila")
                            self.menu_mochila_ativo = True

                        case "fruta":
                            print("Usar fruta")
                            dano = 8
                            if self.inimigos:
                                self.inimigos[0]['PV'] -= dano  # Supondo que o inimigo é um dicionário com 'vida'
                                #self.log_batalha.append(f"Jogador usou fruta! ({dano} de dano)")
                                print("Vida do inimigo:", self.inimigos[0]['PV'])
                                self.inimigos_realizam_turno()

                        case "espada" | "projetil" | "soco":
                            print(f"Ação de ataque: {icone.acao}")
                            #self.realizar_turno(icone.acao)
                            dano = 5
                            if self.inimigos:
                                self.inimigos[0]['PV'] -= dano
                                print("Vida do inimigo:", self.inimigos[0]['PV'])
                                self.inimigos_realizam_turno()

                        case _:
                            print(f"Ação desconhecida: {icone.acao}")
        return None

    def update(self, dt):
        if self.tempo_mensagem_onda > 0:
            self.tempo_mensagem_onda -= dt

        if self.tempo_dano_jogador > 0:
            self.tempo_dano_jogador -= dt

        if self.estado_batalha == "turno_inimigo":
            self.tempo_proximo_ataque -= dt
            if self.tempo_proximo_ataque <= 0:
                if self.inimigo_index_atacando < len(self.inimigos):
                    inimigo = self.inimigos[self.inimigo_index_atacando]
                    if inimigo['PV'] > 0:
                        self.inimigos_animados[self.inimigo_index_atacando].iniciar_ataque()

                        dano = 1
                        self.vida_jogador -= dano
                        print(f"{inimigo['tipo']} atacou! Jogador perdeu {dano} PV.")
                        self.tempo_dano_jogador = 0.25  # dura 0.25s
                        pos = self.posicao_jogador
                        self.danos_flutuantes.append(DanoFlutuante(str(dano), (pos[0], pos[1] - 50)))
                        
                        self.barra_de_estado.atualizar_estado(
                            self.vida_jogador,
                            self.vida_jogador_max,
                            self.energia_jogador,
                            self.energia_jogador_max
                        )

                        if self.vida_jogador <= 0:
                            self.fim_batalha(venceu=False)
                            return

                    self.inimigo_index_atacando += 1
                    self.tempo_proximo_ataque = 0.7  # tempo entre ataques
                else:
                    self.estado_batalha = "turno_jogador"

        for dano in self.danos_flutuantes:
            dano.update(dt)
        self.danos_flutuantes = [d for d in self.danos_flutuantes if not d.acabou()]


        # 1) Atualiza TODAS as animações visuais
        for animado in self.inimigos_animados:
            animado.update(dt)

        # 2) Dispara fade‑out nos inimigos que acabaram de ficar com PV <= 0
        for i, inimigo in enumerate(self.inimigos):
            if inimigo["PV"] <= 0 and self.inimigos_animados[i].estado == "parado":
                self.inimigos_animados[i].iniciar_morte()           ### dispara fade
                # NÃO remova ainda — deixe o fade acontecer

        # 3) Constrói novas listas, jogando fora só quem terminou a animação
        vivos, animados_vivos = [], []
        for i in range(len(self.inimigos)):
            if self.inimigos_animados[i].estado != "removido":
                vivos.append(self.inimigos[i])
                animados_vivos.append(self.inimigos_animados[i])
        self.inimigos = vivos
        self.inimigos_animados = animados_vivos
        self.imagens_de_inimigos = [a.imagem for a in self.inimigos_animados]

        # 4) Verifica se a onda acabou
        if not self.inimigos:
            if not self._carregar_proxima_onda():
                self.fim_batalha(venceu=True)
    
class InimigoAnimado:
    def __init__(self, imagem, posicao_final):
        self.imagem = imagem
        self.pos = [LARGURA_TELA + 150, posicao_final[1]]  # entra da direita
        self.pos_final = posicao_final
        self.velocidade = 300
        self.alpha = 255
        self.estado = "entrando"  # pode ser: "entrando", "parado", "morrendo"
        self.tempo_morte = 0
        self.atacando = False
        self.avanco_total = 80  # pixels que o inimigo avança
        self.avanco_duracao = 0.3  # segundos (ida + volta)
        self.avanco_progresso = 0 
    
    def iniciar_ataque(self):
        self.atacando = True
        self.avanco_progresso = 0


    def update(self, dt):
        if self.estado == "entrando":
            self.pos[0] -= self.velocidade * dt
            if self.pos[0] <= self.pos_final[0]:
                self.pos[0] = self.pos_final[0]
                self.estado = "parado"
        
        if self.atacando:
            self.avanco_progresso += dt / self.avanco_duracao
            if self.avanco_progresso >= 1:
                self.avanco_progresso = 1
                self.atacando = False


        elif self.estado == "morrendo":
            self.alpha -= 400 * dt  # fade rápido (~0.6s)
            if self.alpha <= 0:
                self.alpha = 0
                self.estado = "removido"

    def draw(self, tela):
        if self.estado == "removido":
            return

        offset = 0
        if self.atacando:
            t = self.avanco_progresso
            deslocamento = self.avanco_total
            if t < 0.5:
                offset = deslocamento * (t * 2)  # avança
            else:
                offset = deslocamento * (1 - (t - 0.5) * 2)  # recua

        img = self.imagem.copy()
        img.set_alpha(int(self.alpha))
        tela.blit(img, (self.pos[0] - offset, self.pos[1]))

    def iniciar_morte(self):
        if self.estado != "morrendo":
            self.estado = "morrendo"

class DanoFlutuante:
    def __init__(self, texto, pos):
        self.texto = texto
        self.pos = list(pos)
        self.tempo = 0
        self.max_tempo = 0.8
        self.alpha = 255

    def update(self, dt):
        self.tempo += dt
        self.pos[1] -= 30 * dt
        self.alpha = max(0, 255 * (1 - self.tempo / self.max_tempo))

    def draw(self, tela, fonte):
        if self.tempo < self.max_tempo:
            img = fonte.render(self.texto, True, (255, 60, 60))
            img.set_alpha(int(self.alpha))
            rect = img.get_rect(center=self.pos)
            tela.blit(img, rect)

    def acabou(self):
        return self.tempo >= self.max_tempo
