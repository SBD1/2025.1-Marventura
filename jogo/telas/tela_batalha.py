# telas/tela_batalha.py

import pygame
import math
from utilidades.constantes import *
from .tela_modelo import TelaModelo
from componentes import BarraDeEstado
from gerenciadores import GerenciadorDeEntidades



class _IconeAcao:
    def __init__(self, imagem, acao=None):
        self.image = imagem
        self.rect = self.image.get_rect()
        self.acao = acao
    
    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

class TelaBatalha(TelaModelo):
    def __init__(self, gerenciador_telas, gerenciador_recursos, inimigos_na_batalha, jogador_iniciou=False):
        super().__init__(gerenciador_telas, gerenciador_recursos)

        self.entidades = GerenciadorDeEntidades()

        self.habilidades_visiveis = []
        self.habilidade_selecionada_index = 0

        # Carrega o fundo da batalha
        self.fundo_batalha = self.gerenciador_recursos.obter_imagem(CHAVE_CAMPO_DE_BATALHA_CAMPOS)
        if not self.fundo_batalha:
            self.fundo_batalha = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.fundo_batalha.fill(CINZA_ESCURO)
            print("AVISO: Imagem 'batalha_fundo_padrao' não encontrada. Usando fundo cinza.")

        # Inicializa os ícones de ação
        self.icones_acao = [
            _IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_ESTRATEGIAS), acao="fugir"),
            _IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_MOCHILA), acao="mochila"),
        ]
        self._icones_acao_equipaveis()
        
        # Interface de batalha
        self.barra_de_estado = BarraDeEstado(self.gerenciador_recursos, self.entidades.jogador)
        self.titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TITULO)
        self.tempo_mensagem_onda = 0
        self.texto_mensagem_onda = ""
        self.posicao_jogador = (180, ALTURA_TELA - 170)
        self.caixa_de_texto = self.gerenciador_recursos.obter_imagem(CHAVE_CAIXA_DE_TEXTO)
        self.largura_caixa_de_texto = self.caixa_de_texto.get_width()
        self.altura_caixa_de_texto = self.caixa_de_texto.get_height()
        self.x_central = (LARGURA_TELA - self.largura_caixa_de_texto) // 2

        self.quadro_de_itens = self.gerenciador_recursos.obter_imagem(CHAVE_MENU_ITENS)
        self.largura_quadro = self.quadro_de_itens.get_width()
        self.altura_quadro = self.quadro_de_itens.get_height()
        self.x_quadro = LARGURA_TELA // 2 - self.largura_quadro // 2
        self.y_quadro = 144  # ou calcule centralizado em Y também se quiser

        self.rect_quadro = pygame.Rect(
            self.x_quadro, self.y_quadro, self.largura_quadro, self.altura_quadro
        )



        self.jogador_iniciou = jogador_iniciou

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

        self.estado_batalha = "turno_jogador"  # outros: "turno_inimigo", "esperando_ataque", "selecionando_habilidade"
        self.tempo_proximo_ataque = 0
        self.inimigo_index_atacando = 0

        self.tempo_dano_jogador = 0
        self.danos_flutuantes = []

        self.menu_mochila_ativo = False
        self.item_selecionado = None

        self.indice_item_mochila = 0
        self.itens_visiveis_por_pagina = 6  # pode ajustar
        self.scroll_offset_mochila = 0




    def _usar_ataque_extra(self):
        if self.inimigos:
            inimigo = self.inimigos[0]
            dano = 2  # ataque básico
            inimigo["PV"] -= dano
            print(f"O jogador iniciou com um ataque extra! {inimigo['tipo']} levou {dano} de dano.")
            self.danos_flutuantes.append(DanoFlutuante(str(dano), self.inimigos_animados[0].pos))



    def _icones_acao_equipaveis(self):
        identificador_de_ataques = self.entidades.jogador.kit_do_explorador.obter_ids_do_equipamento()

        if identificador_de_ataques['id_fruta']:
            self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_FRUTA), acao="fruta"))

        if identificador_de_ataques['id_arma']:
            if identificador_de_ataques['id_arma'][:3] == 'esp':
                self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_ESPADA), acao="espada"))
            elif identificador_de_ataques['id_arma'][:3] == 'est':
                self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_PROJETIL), acao="projetil"))
        else:
            chave_soco = CHAVE_ACAO_SOCO_SILVIE if self.entidades.jogador.nome == SILVIE else CHAVE_ACAO_SOCO_SHUAN
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



    def usar_item_da_mochila(self, identificador_item):
        self.entidades.jogador.mochila.usar_item(identificador_item, self.entidades.jogador)

        # Atualiza a barra de estado do jogador
        self.barra_de_estado.atualizar_estado(
            self.entidades.jogador.vida_atual,
            self.entidades.jogador.vida_maxima,
            self.entidades.jogador.energia_atual,
            self.entidades.jogador.energia_maxima,
            self.entidades.jogador.nivel,
            self.entidades.jogador.experiencia_atual
        )

        # Fecha o menu e passa a vez
        self.menu_mochila_ativo = False
        print("Passa o turno depois de usar o item")
        self.inimigos_realizam_turno()



    def _preparar_habilidade(self):
        self.habilidade_usando = self.habilidades[self.habilidade_selecionada_index]
        self.estado_batalha = "selecao_de_alvo" if self.habilidade_usando.tipo_de_alvo in ["alvo_terrestre", "alvo_livre"] else "executando_ataque"

        tipo_alvo = self.habilidade_usando.tipo_de_alvo

        if tipo_alvo in ["alvo_terrestre", "alvo_livre"]:
            self.estado_batalha = "selecao_de_alvo"
        elif tipo_alvo in ["fila", "terrestre", "area"]:
            self._executar_ataque_auto()



    def _executar_ataque_manual(self, alvo_index):
        dano = self._calcular_dano(self.habilidade_usando)
        self._aplicar_dano(alvo_index, dano)
        self._encerrar_turno_jogador()



    def _executar_ataque_auto(self):
        dano = self._calcular_dano(self.habilidade_usando)
        tipo = self.habilidade_usando.tipo_de_alvo

        if tipo == "fila":
            self._aplicar_dano(0, dano)
        else:  # terrestre ou área
            for i in range(len(self.inimigos)):
                self._aplicar_dano(i, dano)

        self._encerrar_turno_jogador()



    def _calcular_dano(self, habilidade):
        nivel = self.entidades.jogador.nivel

        # Determinar raridade da fonte
        if habilidade.tipo_de_ataque in ["espada", "estilingue", "arco"]:
            raridade = self.entidades.jogador.kit.arma["raridade"]
        elif habilidade.tipo_de_ataque == "fruta":
            raridade = self.entidades.jogador.kit.fruta["raridade"]
        else:
            raridade = "★"

        return habilidade.calcular_dano_final(nivel, raridade=raridade)



    def _aplicar_dano(self, index, dano):
        if 0 <= index < len(self.inimigos):
            inimigo = self.inimigos[index]
            inimigo["PV"] -= dano
            pos = self.inimigos_animados[index].pos
            self.danos_flutuantes.append(DanoFlutuante(str(dano), (pos[0], pos[1] - 30)))



    def _encerrar_turno_jogador(self):
        self.estado_batalha = "turno_inimigo"
        self.inimigo_index_atacando = 0
        self.tempo_proximo_ataque = 0.7



    def inimigos_realizam_turno(self):
        print("Turno dos inimigos!")
        self.estado_batalha = "turno_inimigo"
        self.fila_turnos = []

        # Adiciona todos os inimigos vivos na fila
        for i, inimigo in enumerate(self.inimigos):
            if inimigo["PV"] > 0:
                self.fila_turnos.append(i)

        self.tempo_proximo_ataque = 0.5  # tempo de espera antes do primeiro ataque
        self.inimigo_index_atacando = 0      

        
    
    def fim_batalha(self, venceu):
        if venceu:
            print("Todos os inimigos foram derrotados! Você venceu a batalha!")
        else:
            print("Você foi derrotado! A batalha terminou.")

        # Retorna para a tela do mapa
        self.gerenciador_telas.mudar_tela(
            CHAVE_TRANSICAO_MAPA
        )
 


    def renderizar_texto_limitado(self, fonte, texto, cor, largura_max):
        texto_final = texto
        while fonte.size(texto_final)[0] > largura_max and len(texto_final) > 0:
            texto_final = texto_final[:-1]
        if texto_final != texto:
            texto_final = texto_final[:-3] + "..."
        return fonte.render(texto_final, True, cor)



    def quebrar_texto(self, texto, fonte, largura_max):
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            test_linha = linha_atual + palavra + " "
            if fonte.size(test_linha)[0] <= largura_max:
                linha_atual = test_linha
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + " "

        if linha_atual:
            linhas.append(linha_atual.strip())

        return linhas



    def draw(self, tela):
        tela.blit(self.fundo_batalha, (0, 0))

        if self.entidades.jogador.imagem:
            imagem = self.entidades.jogador.imagem
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
        raio = 220  # distância do jogador

        if self.estado_batalha == "turno_jogador" :
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
            tela.blit(self.quadro_de_itens, (self.x_quadro, self.y_quadro))
        
            itens = self.entidades.jogador.mochila.itens
            inicio = self.scroll_offset_mochila
            fim = inicio + self.itens_visiveis_por_pagina
            itens_visiveis = itens[inicio:fim]
        
            mouse_pos = pygame.mouse.get_pos()
            item_em_foco = None
        
            for i, item in enumerate(itens_visiveis):
                y = self.y_quadro + 16 + i * 40
                rect_item = pygame.Rect(self.x_quadro + 8, y, self.largura_quadro - 16, 32)
        
                mouse_sobre = rect_item.collidepoint(mouse_pos)
        
                # Escolhe a fonte com base no hover
                tamanho_fonte = 32 if mouse_sobre else 28
                if mouse_sobre:
                    fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
                else:
                    fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
                
                if mouse_sobre:
                    item_em_foco = item
                largura_texto_max = self.largura_quadro - 32  # margem lateral + margem direita
                texto_nome = self.renderizar_texto_limitado(fonte, item.nome, (255, 255, 255), largura_texto_max)
                tela.blit(texto_nome, (self.x_quadro + 16, y + 4 - (tamanho_fonte - 28) // 2))  # Compensa o y se a fonte ficar maior
        
            # Mostrar descrição e efeitos do item em foco
            if item_em_foco:
                tela.blit(self.caixa_de_texto, (self.x_central, 447))

                fonte_info = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
                largura_caixa = self.caixa_de_texto.get_width() - 32  # margem lateral

                # Descrição com múltiplas linhas
                linhas_desc = self.quebrar_texto(item_em_foco.descricao, fonte_info, largura_caixa)
                for i, linha in enumerate(linhas_desc):
                    texto_descricao = fonte_info.render(linha, True, PRETO)
                    tela.blit(texto_descricao, (self.x_central + 16, 455 + i * 22))

                efeitos = item_em_foco.resumir_efeitos()
                if efeitos:
                    efeitos_texto = fonte_info.render(efeitos, True, VERDE_CLARO)
                    tela.blit(efeitos_texto, (LARGURA_TELA / 3, 540))
        



        # Mostrar lista de habilidades
        if self.estado_batalha == "selecionando_habilidade":
            fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
            x, y = 50, 400
            for i, self.entidades.jogador.habilidade in enumerate(self.entidades.jogador.habilidades):
                cor = (255, 255, 0) if i == self.habilidade_selecionada_index else (255, 255, 255)
                texto = fonte.render(self.entidades.jogador.habilidade.nome, True, cor)
                tela.blit(texto, (x, y + i * 30))



    def distribuir_icones_em_arco(self, icones, centro, raio, angulo_inicial=-90, angulo_total=90):
        """
        Distribui os ícones em arco.
        - icones: lista de surfaces ou objetos com .image e .rect
        - centro: (x, y) onde ficará o centro do arco (geralmente o jogador)
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

        if self.estado_batalha != "turno_jogador":
            return
        # Se o menu da mochila está aberto, verifica clique nos itens
        if evento.type == pygame.MOUSEBUTTONDOWN and self.menu_mochila_ativo:
            if evento.button != 1:
                return

            margem_lateral = 16
            margem_superior = 16
            altura_item = 32
            espacamento = 8

            itens_visiveis = self.entidades.jogador.mochila.itens[
                self.scroll_offset_mochila : self.scroll_offset_mochila + self.itens_visiveis_por_pagina
            ]

            for i, item in enumerate(itens_visiveis):
                y_item = self.y_quadro + margem_superior + i * (altura_item + espacamento)
                rect_item = pygame.Rect(
                    self.x_quadro + margem_lateral,
                    y_item,
                    self.largura_quadro - 2 * margem_lateral,
                    altura_item
                )

                if rect_item.collidepoint(evento.pos):
                    index_real = self.scroll_offset_mochila + i
                    self.indice_item_mochila = index_real
                    self.usar_item_da_mochila(item)
                    return

            if not self.rect_quadro.collidepoint(evento.pos):
                print("Clique fora da caixa – fechando mochila.")
                self.menu_mochila_ativo = False
                return


        elif evento.type == pygame.MOUSEWHEEL and self.menu_mochila_ativo:
            total_itens = len(self.entidades.jogador.mochila.itens)
            max_offset = max(0, total_itens - self.itens_visiveis_por_pagina)

            # Rola para cima (y > 0) ou para baixo (y < 0)
            self.scroll_offset_mochila = max(0, min(self.scroll_offset_mochila - evento.y, max_offset))

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            for icone in self.icones_acao:
                if icone.rect.collidepoint(evento.pos):
                    match icone.acao:
                        case "fugir":
                            self.gerenciador_telas.mudar_tela(
                                CHAVE_TRANSICAO_MAPA
                            )
                            return

                        case "mochila":
                            print("Abrir mochila")
                            self.menu_mochila_ativo = True
                            return

                        case "fruta":
                            print("Usar fruta")
                            self.habilidades_visiveis = [
                                h for h in self.entidades.jogador.habilidades if h.tipo_de_ataque == icone.acao
                            ]
                            if self.entidades.jogador.habilidades:
                                self.estado_batalha = "selecionando_habilidade"
                                self.habilidade_selecionada_index = 0

                        case "espada" | "projetil" | "soco":
                            print(f"Ação de ataque: {icone.acao}")
                            self.habilidades_visiveis = [
                                h for h in self.habilidades if h.tipo_de_ataque == icone.acao
                            ]
                            if self.habilidades:
                                self.estado_batalha = "selecionando_habilidade"
                                self.habilidade_selecionada_index = 0

                        case _:
                            print(f"Ação desconhecida: {icone.acao}")
    
        elif evento.type == pygame.MOUSEBUTTONDOWN and self.estado_batalha == "selecao_de_alvo":
            for i, animado in enumerate(self.inimigos_animados):
                rect = animado.imagem.get_rect(topleft=animado.pos)
                if rect.collidepoint(evento.pos):
                    self._executar_ataque_manual(i)
                    break
                
        elif evento.type == pygame.KEYDOWN and self.estado_batalha == "selecionando_habilidade":
            print(self.estado_batalha)
            print(self.entidades.jogador.habilidades)
            print(self.habilidade_selecionada_index)
            if evento.key == pygame.K_UP:
                self.habilidade_selecionada_index = (self.habilidade_selecionada_index - 1) % len(self.habilidades_visiveis)
            elif evento.key == pygame.K_DOWN:
                self.habilidade_selecionada_index = (self.habilidade_selecionada_index + 1) % len(self.habilidades_visiveis)
            elif evento.key == pygame.K_RETURN:
                self._preparar_habilidade()

        



        return None



    def update(self, dt):
        # Verifica se o jogador iniciou a luta
        if self.jogador_iniciou:
            self._usar_ataque_extra()
            self.jogador_iniciou = False

        if self.tempo_mensagem_onda > 0:
            self.tempo_mensagem_onda -= dt

        if self.tempo_dano_jogador > 0:
            self.tempo_dano_jogador -= dt

        if self.estado_batalha == "turno_inimigo":
            self.tempo_proximo_ataque -= dt
            if self.tempo_proximo_ataque <= 0 and self.fila_turnos:
                i = self.fila_turnos.pop(0)
                if i < len(self.inimigos) and i < len(self.inimigos_animados):
                    inimigo = self.inimigos[i]
                    animado = self.inimigos_animados[i]

                    animado.iniciar_ataque()
                    dano = 1
                    self.entidades.jogador.vida_atual -= dano
                    print(f"{inimigo['tipo']} atacou! Jogador perdeu {dano} PV.")
                    self.tempo_dano_jogador = 0.25  # dura 0.25s
                    pos = self.posicao_jogador
                    self.danos_flutuantes.append(DanoFlutuante(str(dano), (pos[0], pos[1] - 50)))

                    self.barra_de_estado.atualizar_estado(
                        self.entidades.jogador.vida_atual,
                        self.entidades.jogador.vida_maxima,
                        self.entidades.jogador.energia_atual,
                        self.entidades.jogador.energia_maxima,
                        self.entidades.jogador.nivel,
                        self.entidades.jogador.experiencia_atual
                    )

                    if self.entidades.jogador.vida_atual <= 0:
                        self.fim_batalha(venceu=False)
                        return

                    self.tempo_proximo_ataque = 0.7  # tempo entre ataques
                else:
                    print(f"Índice inválido na fila de turnos: {i}")
            elif not self.fila_turnos:
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
