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
    def __init__(self, gerenciador_telas, gerenciador_recursos, gerenciador_banco_de_dados, inimigos_na_batalha, jogador_iniciou=False):
        super().__init__(gerenciador_telas, gerenciador_recursos)

        self.entidades = GerenciadorDeEntidades()
        self.banco_de_dados = gerenciador_banco_de_dados

        self.habilidades_visiveis = []
        self.habilidade_selecionada_index = 0

        self.inimigo_da_esquerda = None
        self.inimigo_do_meio = None
        self.inimigo_da_direita = None

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

        self.menu_de_habilidade = self.gerenciador_recursos.obter_imagem(CHAVE_MENU_SELECAO_HABILIDADE)
        self.largura_menu_habilidade = self.menu_de_habilidade.get_width()
        self.altura_menu_habilidade = self.menu_de_habilidade.get_height()
        self.x_menu_habilidade = LARGURA_TELA / 3
        self.y_menu_habilidade = ALTURA_TELA / 2

        self.rect_quadro = pygame.Rect(
            self.x_quadro, self.y_quadro, self.largura_quadro, self.altura_quadro
        )

        self.jogador_iniciou = jogador_iniciou
        self.experiencia_acumulada = 0
        self.itens_obtidos = []

        # Prepara a lista de inimigos que serão enfrentados
        self.inimigos = []
        self.inimigos_animados = []
        self.fila_ataques_inimigos = []
        
        # Inimigos
        self.ondas_pendentes = []
        self.numero_da_onda = 0

        self.inimigos_lutando = inimigos_na_batalha

        for inimigo_mapa in inimigos_na_batalha:
            nome = inimigo_mapa.nome
            vida = inimigo_mapa.vida_total
            print(f"[DEBUG] Inimigo carregado: {nome} - Vida: {vida}")
            nivel = inimigo_mapa.nivel
            experiencia = inimigo_mapa.experiencia
            habilidade=inimigo_mapa.habilidade[0]
            item = self.banco_de_dados.buscar_item_do_lacaio(inimigo_mapa.identificador_inimigo)

            # Cria 3 clones do mesmo inimigo em versão "batalha"
            onda = [
                InimigoBatalha(nome, vida, nivel, experiencia, habilidade, item)
                for _ in range(3)
            ]

            self.ondas_pendentes.append(onda)

        self._carregar_proxima_onda()

        self.batalha_ja_aconteceu = False
        self.estado_batalha = "turno_jogador"  # outros: "turno_inimigo", "esperando_ataque", "selecionando_habilidade"
        self.tempo_proximo_ataque = 0
        self.inimigo_index_atacando = 0
        
        self.tempo_dano_jogador = 0
        self.danos_flutuantes = []
        
        self.mochila_batalha = [
            item for item in self.entidades.jogador.mochila.itens
            if item.tipo == "con"
        ]
        
        self.menu_mochila_ativo = False
        self.item_selecionado = None

        self.indice_item_mochila = 0
        self.itens_visiveis_por_pagina = 4  # pode ajustar
        self.scroll_offset_mochila = 0
        
        self.fade_alpha = 0



    # Usa um ataque extra se o jogador tiver iniciado a batalha
    # Executa o ataque básico da arma, estilingue, arco ou soco automaticamente
    # Não passa a vez para o inimigo
    def _usar_ataque_extra(self):
        if not self.inimigos:
            return

        jogador = self.entidades.jogador

        # Define prioridades: arma > estilingue/arco > soco
        habilidades_disponiveis = [
            h for h in jogador.habilidades
            if h.tipo_de_ataque in ("espada", "estilingue", "arco", "soco")
        ]

        if not habilidades_disponiveis:
            print("[AVISO] Nenhuma habilidade básica disponível para ataque extra.")
            return

        habilidade = habilidades_disponiveis[0]

        # Determina raridade baseada na arma (ou usa padrão)
        raridade = "★"
        if habilidade.tipo_de_ataque != "soco" and jogador.kit_do_explorador.arma:
            raridade = jogador.kit_do_explorador.armararidade

        dano = habilidade.calcular_dano_final(
            nivel_jogador=jogador.nivel,
            valor_do_efeito_ataque=self.entidades.jogador.aumento_de_ataque,
            raridade=raridade
        )

        tipo = habilidade.tipo_de_alvo
        aplicou_dano = False

        if tipo == "fila":
            # Aplica no primeiro inimigo vivo (geralmente o mais à esquerda)
            for i, inimigo in enumerate(self.inimigos):
                if inimigo.vida_atual > 0:
                    self._aplicar_dano(i, dano)
                    animado = self.inimigos_animados[i]
                    self.danos_flutuantes.append(
                        DanoFlutuante(str(dano), (animado.pos[0], animado.pos[1] - 30))
                    )
                    aplicou_dano = True
                    break

        elif tipo in ("terrestre", "area"):
            # Aplica em todos os inimigos vivos
            for i, inimigo in enumerate(self.inimigos):
                if inimigo.vida_atual > 0:
                    self._aplicar_dano(i, dano)
                    animado = self.inimigos_animados[i]
                    self.danos_flutuantes.append(
                        DanoFlutuante(str(dano), (animado.pos[0], animado.pos[1] - 30))
                    )
                    aplicou_dano = True

        elif tipo in ("alvo_terrestre", "alvo_livre"):
            # Aplica em um único inimigo vivo (qualquer um, pode ser o primeiro)
            for i, inimigo in enumerate(self.inimigos):
                if inimigo.vida_atual > 0:
                    self._aplicar_dano(i, dano)
                    animado = self.inimigos_animados[i]
                    self.danos_flutuantes.append(
                        DanoFlutuante(str(dano), (animado.pos[0], animado.pos[1] - 30))
                    )
                    aplicou_dano = True
                    break

        else:
            print(f"[AVISO] Tipo de alvo não reconhecido: {tipo}")

        if aplicou_dano:
            print(f"[DEBUG] Ataque extra com: {habilidade.nome} ({habilidade.tipo_de_ataque}) → Dano: {dano}")



    def _icones_acao_equipaveis(self):
        identificador_de_ataques = self.entidades.jogador.kit_do_explorador.obter_ids_do_equipamento()
        print(f"Identificador de ataques: {identificador_de_ataques}")
        if identificador_de_ataques['id_fruta']:
            self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_FRUTA), acao="fruta"))

        if identificador_de_ataques['id_arma']:
            if self.entidades.jogador.kit_do_explorador.arma.tipo_arma == 'esp':
                self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_ESPADA), acao="espada"))
            elif self.entidades.jogador.kit_do_explorador.arma.tipo_arma == 'est':
                self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_PROJETIL), acao="projetil"))
            elif self.entidades.jogador.kit_do_explorador.arma.tipo_arma == 'arco':
                self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_PROJETIL), acao="projetil"))
        else:
            chave_soco = CHAVE_ACAO_SOCO_SILVIE if self.entidades.jogador.nome == SILVIE else CHAVE_ACAO_SOCO_SHUAN
            self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(chave_soco), acao="soco"))



    def _carregar_proxima_onda(self):
        if not self.ondas_pendentes:
            self.inimigos = []  # força término da batalha
            return False

        # Pega o inimigo base da próxima onda (InimigoBatalha)
        onda = self.ondas_pendentes.pop(0)

        # Atribui diretamente os três inimigos
        self.inimigo_da_esquerda = onda[0]
        self.inimigo_do_meio = onda[1]
        self.inimigo_da_direita = onda[2]

        # Lista de inimigos em ordem para lógica de batalha
        self.inimigos = [
            self.inimigo_da_esquerda,
            self.inimigo_do_meio,
            self.inimigo_da_direita
        ]

        # Posicionamento dos inimigos na tela de batalha
        posicoes = [
            (LARGURA_TELA - 350, ALTURA_TELA - 225),
            (LARGURA_TELA - 250, ALTURA_TELA - 150),
            (LARGURA_TELA - 120, ALTURA_TELA - 200),
        ]

        self.inimigos_animados = []

        for i, inimigo in enumerate(self.inimigos):
            imagem = self.gerenciador_recursos.obter_imagem(inimigo.imagem_id)
            posicao = posicoes[i]
            sprite_animado = InimigoAnimado(imagem, posicao)
            self.inimigos_animados.append(sprite_animado)

        self.numero_da_onda += 1
        total_ondas = self.numero_da_onda + len(self.ondas_pendentes)

        inimigo_referencia = self.inimigo_da_esquerda  # pode ser qualquer um dos 3
        print(f"\n=== 🌊 Onda {self.numero_da_onda}/{total_ondas} iniciada ===")
        print(f"Inimigo base: {inimigo_referencia.nome} — Nível {inimigo_referencia.nivel}")


        self.texto_mensagem_onda = f"Onda {self.numero_da_onda}/{total_ondas}"
        self.tempo_mensagem_onda = 2.5

        # Reinicia o estado da batalha
        self.estado_batalha = "turno_jogador"
        self.tempo_proximo_ataque = 0
        self.inimigo_index_atacando = 0

        return True



    def usar_item_da_mochila(self, item):
        self.entidades.jogador.usar_item_da_mochila(item)
        
        # Fecha o menu e passa a vez
        self.menu_mochila_ativo = False
        print("Passa o turno depois de usar o item")
        self._realizar_turno_inimigo()



    def _preparar_habilidade(self):
        self.habilidade_usando = self.habilidades_visiveis[self.habilidade_selecionada_index]
        
        if self.entidades.jogador.energia_atual < self.habilidade_usando.custo:
            print(f"[DEBUG] Energia insuficiente para usar {self.habilidade_usando.nome}")
            self.estado_batalha = "turno_jogador"  # ou mantém no menu
            return  # Cancela a preparação
      
        self.estado_batalha = "selecao_de_alvo"



    def _executar_ataque_jogador(self, alvo_index):
        self.entidades.jogador.energia_atual -= self.habilidade_usando.custo
        self.entidades.jogador.energia_atual = max(0, self.entidades.jogador.energia_atual)

        dano = self._calcular_dano(self.habilidade_usando)
        
        tipo = self.habilidade_usando.tipo_de_alvo
        if tipo in ["area", "terrestre"]:
            for i in range(len(self.inimigos)):
                self._aplicar_dano(i, dano)
        elif tipo in ["fila"]:
            alvo = self._proximo_inimigo_vivo()
            if alvo:
                self._aplicar_dano(self.inimigos.index(alvo), dano)
        else:
            self._aplicar_dano(alvo_index, dano)

        # Recupera energia se for ataque básico
        if self.habilidade_usando.custo == 0:
            energia_recuperada = 1  # ou outro valor que preferir
            self.entidades.jogador.energia_atual = min(
                self.entidades.jogador.energia_atual + energia_recuperada,
                self.entidades.jogador.energia_maxima
            )

        self._encerrar_turno_jogador()



    def _calcular_dano(self, habilidade):
        nivel = self.entidades.jogador.nivel
        ataque = self.entidades.jogador.aumento_de_ataque

        # Determinar raridade da fonte
        if habilidade.tipo_de_ataque in ["espada", "estilingue", "arco"]:
            raridade = self.entidades.jogador.kit_do_explorador.arma.raridade
        elif habilidade.tipo_de_ataque == "fruta":
            raridade = self.entidades.jogador.kit_do_explorador.fruta.raridade
        else:
            raridade = "★"

        return habilidade.calcular_dano_final(nivel, ataque, raridade=raridade)



    def _aplicar_dano(self, index, dano):
        if not (0 <= index < len(self.inimigos)):
            print(f"[AVISO] Índice de inimigo inválido: {index}")
            return

        inimigo = self.inimigos[index]
        animado = self.inimigos_animados[index]

        # Garante que dano mínimo seja 0 (caso algo negativo escape)
        dano = max(0, dano)
        inimigo.vida_atual = max(0, inimigo.vida_atual - dano)

        # Adiciona dano flutuante visual
        x, y = animado.pos
        self.danos_flutuantes.append(DanoFlutuante(str(dano), (x, y - 30)))

        print(f"💥 {inimigo.nome} recebeu {dano} de dano! Vida restante: {inimigo.vida_atual}/{inimigo.vida_total}")



    def _proximo_inimigo_vivo(self):
        for inimigo in self.inimigos:
            if inimigo.esta_vivo():
                return inimigo
        return None



    def _encerrar_turno_jogador(self):
        self.entidades.jogador.aplicar_dano_continuo("depois")
        self.estado_batalha = "turno_inimigo"
        self.inimigo_index_atacando = 0
        self.tempo_proximo_ataque = 0.7
        self._preparar_fila_de_ataque_inimiga()



    def _realizar_turno_inimigo(self):
        print("🔺 Turno dos inimigos!")
        self.estado_batalha = "turno_inimigo"
        self._preparar_fila_de_ataque_inimiga()
        self.tempo_proximo_ataque = 0.5
        self.inimigo_index_atacando = 0

    def _preparar_fila_de_ataque_inimiga(self):
        self.fila_ataques_inimigos = [
            i for i, inimigo in enumerate(self.inimigos) if inimigo.esta_vivo()
        ]
    
    def _executar_ataque_inimigo(self):
        i = self.fila_ataques_inimigos.pop(0)

        if i >= len(self.inimigos) or i >= len(self.inimigos_animados):
            print(f"[ERRO] Índice inválido na fila de inimigos: {i}")
            return

        inimigo = self.inimigos[i]
        animado = self.inimigos_animados[i]

        print(inimigo)
        dano = inimigo.habilidade.calcular_dano_final(inimigo.nivel, 0, "★")
        animado.iniciar_ataque()

        self.entidades.jogador.vida_atual = max(0, self.entidades.jogador.vida_atual - dano)

        pos = self.posicao_jogador
        self.danos_flutuantes.append(
            DanoFlutuante(str(dano), (pos[0], pos[1] - 50))
        )

        print(f"🧟 Inimigo ({inimigo.nome}) atacou! Jogador perdeu {dano} PV.")

        if self.entidades.jogador.vida_atual <= 0:
            self._finalizar_batalha(venceu=False)
            return
        
        inimigo.aplicar_dano_continuo("depois")

        self.tempo_proximo_ataque = 0.7  # Delay entre ataques

        
    
    def _finalizar_batalha(self, venceu):
        if venceu:
            print("Todos os inimigos foram derrotados! Você venceu a batalha!")
    
            # Ganha experiência e retorna ao mapa
            self.entidades.jogador.experiencia_atual += self.experiencia_acumulada
            self.entidades.jogador.atualizar_atributos_por_nivel(self.entidades.jogador)

            self._adiconar_item_ao_invetario_do_jogador(self.itens_obtidos)
    
            self.banco_de_dados.atualizar_atributos_de_batalha_do_jogador(
                self.entidades.jogador.identificador_jogador,
                self.entidades.jogador.energia_maxima,
                self.entidades.jogador.vida_maxima,
                self.entidades.jogador.nivel,
                self.entidades.jogador.sorte,
                self.entidades.jogador.energia_atual,
                self.entidades.jogador.vida_atual,
                self.entidades.jogador.experiencia_atual,
                self.entidades.jogador.moedas
            )
    
            self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MAPA)
    
        else:
            print("Você foi derrotado! A batalha terminou.")
    
            self.estado_batalha = "derrota"
            self.tempo_derrota = 5.0  # Segundos restantes para o retorno
    
            # Move para o ponto de renascimento
            x, y = self.entidades.ponto_de_renascimento
            self.entidades.jogador.atualizar_posicao_jogador(x, y)
    
            # Ressuscita com metade da vida
            self.entidades.jogador.vida_atual = int(self.entidades.jogador.vida_maxima / 2)
    
            # Salva o progresso
            self.entidades.jogador.experiencia_atual += self.experiencia_acumulada
            self.entidades.jogador.atualizar_atributos_por_nivel(self.entidades.jogador)

            self._adiconar_item_ao_invetario_do_jogador(self.itens_obtidos)
    
            self.banco_de_dados.atualizar_atributos_de_batalha_do_jogador(
                self.entidades.jogador.identificador_jogador,
                self.entidades.jogador.energia_maxima,
                self.entidades.jogador.vida_maxima,
                self.entidades.jogador.nivel,
                self.entidades.jogador.sorte,
                self.entidades.jogador.energia_atual,
                self.entidades.jogador.vida_atual,
                self.entidades.jogador.experiencia_atual,
                self.entidades.jogador.moedas
            )

 

    def _adiconar_item_ao_invetario_do_jogador(self, itens):
        if not itens:
            print("[AVISO] Tentativa de adicionar item vazio ao inventário.")
            return

        for item in itens:
            self.entidades.jogador.inserir_item_na_mochila(item, self.entidades.progresso_do_jogo.identificador_progresso)



    def processar_eventos(self, evento):
        # Chama o processar_eventos da base para eventos comuns (ex: QUIT)
        super().processar_eventos(evento)
        #print(f"[DEBUG] Estado da batalha no clique: {self.estado_batalha}")

        # Se o menu da mochila está aberto, verifica clique nos itens
        if evento.type == pygame.MOUSEBUTTONDOWN and self.menu_mochila_ativo:
            if evento.button != 1:
                return

            margem_lateral = 16
            margem_superior = 16
            altura_item = 32
            espacamento = 8

            itens_visiveis = self.mochila_batalha[
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
                    self.usar_item_da_mochila(item)
                    return

            if not self.rect_quadro.collidepoint(evento.pos):
                print("Clique fora da caixa – fechando mochila.")
                self.menu_mochila_ativo = False
                return


        elif evento.type == pygame.MOUSEWHEEL and self.menu_mochila_ativo:
            total_itens = len(self.mochila_batalha)
            max_offset = max(0, total_itens - self.itens_visiveis_por_pagina)

            # Rola para cima (y > 0) ou para baixo (y < 0)
            self.scroll_offset_mochila = max(0, min(self.scroll_offset_mochila - evento.y, max_offset))

        elif evento.type == pygame.MOUSEBUTTONDOWN and self.estado_batalha == "selecionando_habilidade":
            habilidades = self.habilidades_visiveis
            clicou_em_habilidade = False
            print(f"[DEBUG] Habilidades visíveis: {[h.nome for h in habilidades]}")
            for i, habilidade in enumerate(habilidades):
                y = self.y_menu_habilidade + 16 + i * 40
                rect_item = pygame.Rect(self.x_menu_habilidade + 8, y, self.largura_menu_habilidade - 16, 32)
                print(f"[DEBUG] Verificando clique na habilidade: {habilidade.nome} (índice {i})")
                if rect_item.collidepoint(evento.pos):
                    print(f"[DEBUG] Clicou na habilidade: {habilidade.nome}")
                    self.habilidade_selecionada_index = i
                    self._preparar_habilidade()
                    clicou_em_habilidade = True
                    break
                
            # Clicou fora do quadro → fecha o menu
            rect_menu_de_habilidades = pygame.Rect(self.x_menu_habilidade, self.y_menu_habilidade, self.largura_menu_habilidade, self.altura_menu_habilidade)
            if not rect_menu_de_habilidades.collidepoint(evento.pos) and not clicou_em_habilidade:
                self.estado_batalha = "turno_jogador"

        elif evento.type == pygame.MOUSEBUTTONDOWN and self.estado_batalha == "selecao_de_alvo":
            for i, animado in enumerate(self.inimigos_animados):
                rect = animado.imagem.get_rect(topleft=animado.pos)
                if rect.collidepoint(evento.pos):
                    self._executar_ataque_jogador(i)
                    break

        elif evento.type == pygame.MOUSEBUTTONDOWN and self.estado_batalha == "turno_jogador":
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
                            if self.habilidades_visiveis:
                                self.estado_batalha = "selecionando_habilidade"
                                self.habilidade_selecionada_index = 0

                        case "espada" | "projetil" | "soco":
                            print(f"Ação de ataque: {icone.acao}")
                            self.habilidades_visiveis = [
                                h for h in self.entidades.jogador.habilidades if h.tipo_de_ataque == icone.acao
                            ]
                            if self.habilidades_visiveis:
                                self.estado_batalha = "selecionando_habilidade"
                                self.habilidade_selecionada_index = 0

                        case _:
                            print(f"Ação desconhecida: {icone.acao}")
    
        return None



    def atualizar(self, dt):
        # Verifica se o jogador iniciou a luta
        if self.jogador_iniciou:
            self._usar_ataque_extra()
            self.jogador_iniciou = False

        # Atualiza contadores de tempo
        if self.tempo_mensagem_onda > 0:
            self.tempo_mensagem_onda -= dt

        if self.tempo_dano_jogador > 0:
            self.tempo_dano_jogador -= dt

        if self.estado_batalha == "turno_inimigo":
            self.tempo_proximo_ataque -= dt
            if self.tempo_proximo_ataque <= 0 and self.fila_ataques_inimigos:
                index = self.fila_ataques_inimigos[self.inimigo_index_atacando]
                inimigo = self.inimigos[index]  # ← Isso aqui é uma instância de InimigoBatalha
                inimigo.aplicar_dano_continuo("antes")
                self._executar_ataque_inimigo()
            elif not self.fila_ataques_inimigos:
                # Se não há mais inimigos na fila, volta para o turno do jogador
                self.estado_batalha = "turno_jogador"
                self.entidades.jogador.aplicar_dano_continuo("antes")
                # E atualiza os efeitos aplicados (se houver) decrementando a duração em 1 turno
                self.entidades.jogador.atualizar_efeitos()
                for inimigo in self.inimigos:
                    inimigo.atualizar_efeitos()

        for dano in self.danos_flutuantes:
            dano.update(dt)
        self.danos_flutuantes = [d for d in self.danos_flutuantes if not d.acabou()]


        # 1) Atualiza TODAS as animações visuais
        for animado in self.inimigos_animados:
            animado.update(dt)

        # 2) Dispara fade‑out nos inimigos que acabaram de ficar com PV <= 0
        for i, inimigo in enumerate(self.inimigos):
            if inimigo.vida_atual <= 0 and self.inimigos_animados[i].estado == "parado":
                self.inimigos_animados[i].iniciar_morte()           ### dispara fade
                # NÃO remova ainda — deixe o fade acontecer

        # 3) Constrói novas listas, jogando fora só quem terminou a animação
        if self.batalha_ja_aconteceu:
            vivos, animados_vivos = [], []
            for i in range(len(self.inimigos)):
                if self.inimigos_animados[i].estado != "removido":
                    vivos.append(self.inimigos[i])
                    animados_vivos.append(self.inimigos_animados[i])

            self.inimigos = vivos
            self.inimigos_animados = animados_vivos

        #self.imagens_de_inimigos = [a.imagem for a in self.inimigos_animados]

        # Verifica se todos os inimigos da onda foram derrotados
        if all(not inimigo.esta_vivo() for inimigo in self.inimigos):
            self.experiencia_acumulada += inimigo.experiencia
            self.itens_obtidos.append(inimigo.item)
            inimigo_pop = self.inimigos_lutando.pop(0)
            print(f"Inimigo derrotado: {inimigo_pop.identificador_instancia_lacaio}")
            self.banco_de_dados.sekishiki_meikai_ha(inimigo_pop.identificador_instancia_lacaio, self.entidades.progresso_do_jogo.identificador_progresso)
            if not self._carregar_proxima_onda():
                self._finalizar_batalha(venceu=True)

        if self.estado_batalha == "derrota":
            if self.fade_alpha < 255:
                self.fade_alpha = min(255, self.fade_alpha + 300 * dt)  # 300 = velocidade de fade
            else:
                self.tempo_derrota -= dt
                if self.tempo_derrota <= 0:
                    self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MAPA)



    def desenhar(self, tela):
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
        if not self.estado_batalha == 'derrota':
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

            print(f"[DEBUG] Itens na mochila: {[item.nome for item in self.mochila_batalha]}")

            inicio = self.scroll_offset_mochila
            fim = inicio + self.itens_visiveis_por_pagina
            itens_visiveis = self.mochila_batalha[inicio:fim]
        
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
                texto_nome = self.renderizar_texto_limitado(fonte, f" {item.nome} x{item.quantidade} ", (255, 255, 255), largura_texto_max)
                self._desenhar_texto_com_borda(
                    tela,
                    texto_nome,
                    fonte,
                    BRANCO_CLARO,
                    PRETO,
                    1,
                    (self.x_quadro + self.largura_quadro // 2, y + 4 - (tamanho_fonte - 28) // 2),
                )
        
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
                    self._desenhar_texto_com_borda(
                        tela,
                        efeitos,
                        fonte_info,
                        VERDE_CLARO,
                        PRETO,
                        1,
                        (LARGURA_TELA / 3, 540),
                        'left'
                    )
        
        # Mostrar lista de habilidades
        if self.estado_batalha == "selecionando_habilidade":
            tela.blit(self.menu_de_habilidade, (self.x_menu_habilidade, self.y_menu_habilidade))

            habilidades = self.habilidades_visiveis
            inicio = 0  # por agora sem scroll
            fim = len(habilidades)
            habilidades_visiveis = habilidades[inicio:fim]

            mouse_pos = pygame.mouse.get_pos()
            habilidade_em_foco = None

            for i, habilidade in enumerate(habilidades_visiveis):
                y = self.y_menu_habilidade + 16 + i * 40
                rect_item = pygame.Rect(self.x_menu_habilidade + 8, y, self.largura_menu_habilidade - 16, 32)
                mouse_sobre = rect_item.collidepoint(mouse_pos)

                # Hover aumenta fonte
                tamanho_fonte = 32 if mouse_sobre else 28
                fonte = self.gerenciador_recursos.obter_fonte(
                    CHAVE_FONTE_CHERRY_SUBTITULO if mouse_sobre else CHAVE_FONTE_CHERRY_TEXTO
                )

                if mouse_sobre:
                    habilidade_em_foco = habilidade

                texto_nome = self.renderizar_texto_limitado(
                    fonte, habilidade.nome, BRANCO_CLARO, self.largura_menu_habilidade - 32
                )
                centro_texto_x = self.x_menu_habilidade + self.largura_menu_habilidade // 2

                self._desenhar_texto_com_borda(
                    tela,
                    texto_nome,
                    fonte,
                    BRANCO_CLARO,
                    PRETO,
                    1,
                    (centro_texto_x, y + 4 - (tamanho_fonte - 28) // 2)
                )


            # Mostrar descrição da habilidade em foco
            if habilidade_em_foco:
                tela.blit(self.caixa_de_texto, (self.x_central, 447))

                fonte_info = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
                largura_caixa = self.caixa_de_texto.get_width() - 32

                # Quebra a descrição em várias linhas
                linhas_desc = self.quebrar_texto(habilidade_em_foco.descricao, fonte_info, largura_caixa)
                for i, linha in enumerate(linhas_desc):
                    texto = fonte_info.render(linha, True, PRETO)
                    tela.blit(texto, (self.x_central + 16, 455 + i * 22))


                # Mostrar custo de energia com borda (alinhado com as tags)
                texto_custo = f"Custo: {habilidade_em_foco.custo} PE"
                altura_tag = fonte_info.get_linesize() + 8  # altura estimada da tag com padding
                y_tags = 455 + len(linhas_desc) * 22 + 10 + altura_tag // 2  # centraliza com base no meio da tag

                self._desenhar_texto_com_borda(
                    tela,
                    texto_custo,
                    fonte_info,
                    AZUL_CLARO,
                    PRETO,
                    1,
                    (self.x_central + 16, y_tags),
                    'left'
                )

                # Calcular largura do texto
                largura_texto_custo = fonte_info.size(texto_custo)[0]

                # Mostrar tags de tipo de alvo
                tags = TAGS_DE_ALVO.get(habilidade_em_foco.tipo_de_alvo, ["???"])
                espaco = 8
                x_tag = self.x_central + 16 + largura_texto_custo + 16

                for tag in tags:
                    texto = fonte_info.render(tag, True, PRETO)
                    largura = texto.get_width() + 12
                    altura = texto.get_height() + 8

                    rect = pygame.Rect(x_tag, y_tags - altura // 2, largura, altura)
                    pygame.draw.rect(tela, AZUL_CLARO, rect, border_radius=6)
                    tela.blit(texto, (rect.x + 6, rect.y + 4))

                    x_tag += largura + espaco



        if self.estado_batalha == "derrota":
            # Fundo preto com transparência crescente
            tela_sombra = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            tela_sombra.fill((0, 0, 0))
            tela_sombra.set_alpha(int(self.fade_alpha))
            tela.blit(tela_sombra, (0, 0))

            # Mostrar texto só após fade completo
            if self.fade_alpha >= 255:
                tempo_restante = int(self.tempo_derrota) + 1
                fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
                texto = fonte.render(
                    f"Você foi derrotado... Retornando ao mundo em {tempo_restante}s",
                    True,
                    BRANCO
                )
                rect = texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
                tela.blit(texto, rect)



    def desenhar_tags_de_alvo(tela, fonte, tags, pos_x_inicial, pos_y_final, cor_texto, cor_fundo, raio_borda=6):
        x = pos_x_inicial
        espacamento = 8
    
        for tag in tags:
            texto = fonte.render(tag, True, cor_texto)
            largura = texto.get_width() + 12
            altura = texto.get_height() + 8
    
            rect = pygame.Rect(x, pos_y_final - altura - 8, largura, altura)
            pygame.draw.rect(tela, cor_fundo, rect, border_radius=raio_borda)
            tela.blit(texto, (rect.x + 6, rect.y + 4))
    
            x += largura + espacamento



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



    def renderizar_texto_limitado(self, fonte, texto, cor, largura_max):
        texto_final = texto
        while fonte.size(texto_final)[0] > largura_max and len(texto_final) > 0:
            texto_final = texto_final[:-1]
        if texto_final != texto:
            texto_final = texto_final[:-3] + "..."
        return texto_final



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
    


class InimigoBatalha:
    def __init__(self, nome, vida_total, nivel, experiencia, habilidade, item):
        self.nome = nome
        self.imagem_id = f"{nome}_0"  # Ex: "Lobo_0"
        self.vida_total = vida_total
        self.vida_atual = vida_total
        self.nivel = nivel
        self.experiencia = experiencia
        self.habilidade = habilidade
        self.item = item
        self.efeitos_ativos = []  # status como 'Envenenado', 'Tontura', etc.

    def clonar(self):
        return InimigoBatalha(
            self.nome,
            self.imagem_id,
            self.vida_total,
            self.nivel,
            self.experiencia
        )
    
    def receber_dano(self, dano):
        self.vida_atual = max(0, self.vida_atual - dano)

    def esta_vivo(self):
        return self.vida_atual > 0
    
    def aplicar_efeitos(self, efeitos):
        """
        Aplica os efeitos do item ao inimigo alvo. A quantidade deve ser controlada fora.
        """
        for efeito in efeitos:
            tipo = efeito["nome"]
            valor = efeito["valor"]

            match tipo:
                case "Eletrificado":  # Aplica o status eletrificado
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Congelado":  # Aplica o status congelado
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 1,
                        "tipo": "status"
                    })

                case "Molhado":  # Aplica o status molhado
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Envenenado":  # Aplica o status envenenado
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Sangramento":  # Aplica o status sangramento
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Queimadura":  # Aplica o status queimadura
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Tontura":  # Aplica o status tontura
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Cegueira":  # Aplica o status cegueira
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case _:  # Caso o efeito não seja reconhecido
                    print(f"Efeito desconhecido: {tipo}")

            # Você pode adicionar suporte a outros tipos de efeito aqui futuramente

    def atualizar_efeitos(self):
        novos = []
        for efeito in self.efeitos_ativos:
            efeito["duracao"] -= 1
            if efeito["duracao"] > 0:
                novos.append(efeito)
        self.efeitos_ativos = novos

    def aplicar_dano_continuo(self, momento: str):
        """
        Aplica dano de efeitos por turno com base no momento:
        - "antes": antes da ação da unidade (ex: Queimadura)
        - "depois": após a ação da unidade (ex: Envenenado, Sangramento)
        """
        for efeito in self.efeitos_ativos:
            nome = efeito["nome"]
            valor = efeito["valor"]

            if momento == "antes" and nome == "Queimadura":
                self.receber_dano(valor)
                print(f"{self.nome} sofreu {valor} de dano por {nome} (antes de agir).")

            elif momento == "depois" and nome in ["Envenenado", "Sangramento"]:
                self.receber_dano(valor)
                print(f"{self.nome} sofreu {valor} de dano por {nome} (após agir).")


  
class InimigoAnimado:
    def __init__(self, imagem, posicao_final):
        self.imagem = imagem
        print(f"[DEBUG] Criando InimigoAnimado com imagem: {imagem} e posição final: {posicao_final}")
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
        self.imagem_base = imagem
        self.imagem = imagem.copy()

    

    def iniciar_ataque(self):
        self.atacando = True
        self.avanco_progresso = 0

    def resetar(self, nova_imagem, nova_posicao):
        self.imagem = nova_imagem.copy()
        self.pos_final = nova_posicao
        self.pos = [LARGURA_TELA + 150, nova_posicao[1]]
        self.alpha = 255
        self.estado = "entrando"
        self.atacando = False
        self.avanco_progresso = 0


    def iniciar_morte(self):
        if self.estado != "morrendo":
            self.estado = "morrendo"



    def update(self, dt):
        if self.estado == "entrando":
            self.pos[0] -= self.velocidade * dt
            if self.pos[0] <= self.pos_final[0]:
                self.pos[0] = self.pos_final[0]
                self.estado = "parado"

        elif self.estado == "morrendo":
            self.alpha -= 400 * dt
            if self.alpha <= 0:
                self.alpha = 0
                self.estado = "removido"

        if self.atacando:
            self.avanco_progresso += dt / self.avanco_duracao
            if self.avanco_progresso >= 1:
                self.avanco_progresso = 1
                self.atacando = False

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

        self.imagem.set_alpha(int(self.alpha))
        tela.blit(self.imagem, (self.pos[0] - offset, self.pos[1]))



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
