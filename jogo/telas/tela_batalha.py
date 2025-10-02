# telas/tela_batalha.py

import pygame
import math
import random
from utilidades.constantes import *
from .tela_modelo import TelaModelo
from componentes import BarraDeEstado
from gerenciadores import GerenciadorDeEntidades
from entidades import Inimigo, Chefe
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import DBManager
    from gerenciadores import GerenciadorDeMissoes


class _IconeAcao:
    def __init__(self, imagem, acao=None):
        self.image = imagem
        self.rect = self.image.get_rect()
        self.acao = acao
    
    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

class TelaBatalha(TelaModelo):
    def __init__(self, gerenciador_telas, gerenciador_recursos, gerenciador_banco_de_dados: 'DBManager', gerenciador_missoes: 'GerenciadorDeMissoes', inimigos_na_batalha: list['Inimigo'], jogador_iniciou=False, numero_inimigos=3, fuga_habilitada=True):
        super().__init__(gerenciador_telas, gerenciador_recursos)

        self.entidades = GerenciadorDeEntidades()
        self.missoes = gerenciador_missoes
        self.banco_de_dados = gerenciador_banco_de_dados

        self.habilidades_visiveis = []
        self.habilidade_selecionada_index = 0

        print(f"[DEBUG] Vida máxima para o jogador {self.entidades.jogador.nome}: {self.entidades.jogador.vida_maxima} (Base: {self.entidades.jogador.vida_maxima_base} + Bônus: {getattr(self, 'bonus_vida', 0)})")
        print(f"[DEBUG] Energia máxima para o jogador {self.entidades.jogador.nome}: {self.entidades.jogador.energia_maxima} (Base: {self.entidades.jogador.energia_maxima_base} + Bônus: {getattr(self, 'bonus_energia', 0)})")
        print(f"[DEBUG] Aumento de ataque para o jogador {self.entidades.jogador.nome}: {self.entidades.jogador.aumento_de_ataque} (Bônus: {getattr(self, 'bonus_ataque', 0)})")
        print(f"[DEBUG] Sorte para o jogador {self.entidades.jogador.nome}: {self.entidades.jogador.sorte} (Base + Bônus: {getattr(self, 'bonus_sorte', 0)})")


        self.bonus_do_jogador = 0
        self.bonus_do_inimigo = 0

        self.inimigo_da_esquerda = None
        self.inimigo_do_meio = None
        self.inimigo_da_direita = None

        # Carrega o fundo da batalha
        self.campo_de_batalha = self.entidades._ilha_atual.nome
        self.fundo_batalha = None
        match self.campo_de_batalha:
            case "Ilha de Borabóia":
                self.fundo_batalha = self.gerenciador_recursos.obter_imagem(CHAVE_CAMPO_DE_BATALHA_CAMPOS)
            case "Cidade de Lurien":
                self.fundo_batalha = self.gerenciador_recursos.obter_imagem(CHAVE_CAMPO_DE_BATALHA_CIDADE)
            case "Ilha Glacial de Frimora":
                self.fundo_batalha = self.gerenciador_recursos.obter_imagem(CHAVE_CAMPO_DE_BATALHA_NEVE)

        if not self.fundo_batalha:
            self.fundo_batalha = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.fundo_batalha.fill(CINZA_ESCURO)
            print("AVISO: Imagem 'batalha_fundo_padrao' não encontrada. Usando fundo cinza.")

        # Inicializa os ícones de ação
        self.icones_acao = [
            _IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_ESTRATEGIAS), acao="estrategias"),
            _IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_MOCHILA), acao="mochila"),
        ]
        self._icones_acao_equipaveis()
        
        # Interface de batalha
        self.barra_de_estado = BarraDeEstado(self.gerenciador_recursos, self.entidades.jogador)
        self.titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TITULO)
        self.tempo_mensagem_onda = 0
        self.texto_mensagem_onda = ""
        self.posicao_jogador = (180, ALTURA_TELA - 120)
        self.caixa_de_texto = self.gerenciador_recursos.obter_imagem(CHAVE_CAIXA_DE_TEXTO)
        self.largura_caixa_de_texto = self.caixa_de_texto.get_width()
        self.altura_caixa_de_texto = self.caixa_de_texto.get_height()
        self.x_central = (LARGURA_TELA - self.largura_caixa_de_texto) // 2

        self.menu_estrategias = self.gerenciador_recursos.obter_imagem(CHAVE_MENU_ESTRATEGIAS)
        self.largura_menu_estrategias = self.menu_estrategias.get_width()
        self.altura_menu_estrategias = self.menu_estrategias.get_height()
        self.x_menu_estrategias = LARGURA_TELA // 4 - self.largura_menu_estrategias // 2
        self.y_menu_estrategias = ALTURA_TELA // 2 - self.altura_menu_estrategias // 2

        self.menu_mochila = self.gerenciador_recursos.obter_imagem(CHAVE_MENU_ITENS)
        self.largura_menu_mochila = self.menu_mochila.get_width()
        self.altura_menu_mochila = self.menu_mochila.get_height()
        self.x_menu_mochila = LARGURA_TELA // 2 - self.largura_menu_mochila // 2
        self.y_menu_mochila = 144

        self.menu_de_habilidade = self.gerenciador_recursos.obter_imagem(CHAVE_MENU_SELECAO_HABILIDADE)
        self.largura_menu_habilidade = self.menu_de_habilidade.get_width()
        self.altura_menu_habilidade = self.menu_de_habilidade.get_height()
        self.x_menu_habilidade = LARGURA_TELA / 3
        self.y_menu_habilidade = ALTURA_TELA / 2

        self.rect_quadro = pygame.Rect(
            self.x_menu_mochila, self.y_menu_mochila, self.largura_menu_mochila, self.altura_menu_mochila
        )

        self.jogador_iniciou = jogador_iniciou
        self.experiencia_acumulada = 0
        self.itens_obtidos = []
        self.fuga_habilitada = fuga_habilitada

        # Prepara a lista de inimigos que serão enfrentados
        self.inimigos: list[InimigoBatalha] = []
        self.inimigos_animados = []
        self.fila_ataques_inimigos = []
        
        # Inimigos
        self.ondas_pendentes: list[InimigoBatalha] = []
        self.numero_da_onda = 0

        self.inimigos_lutando = inimigos_na_batalha

        self.tipo_inimigo = inimigos_na_batalha[0].nome if inimigos_na_batalha else None

        for inimigo_mapa in inimigos_na_batalha:
            nome = inimigo_mapa.nome
            vida = inimigo_mapa.vida_total
            print(f"[DEBUG] Inimigo carregado: {nome} - Vida: {vida}")
            nivel = inimigo_mapa.nivel
            experiencia = inimigo_mapa.experiencia
            habilidade=inimigo_mapa.habilidade[0]
            imagem=inimigo_mapa.imagens_animacao.get(0)

            item = self.banco_de_dados.buscar_item_do_lacaio(inimigo_mapa.identificador_inimigo) if isinstance(inimigo_mapa, Inimigo) else []
            # Cria até 3 clones do mesmo inimigo em versão "batalha"
            onda = [
                InimigoBatalha(nome, vida, nivel, experiencia, habilidade, item, imagem)
                for _ in range(numero_inimigos)
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

        if self.entidades.jogador.kit_do_explorador.arma is None:
            habilidade = self.entidades.jogador.habilidades[0]  # soco
        else:
            habilidade = self.entidades.jogador.habilidades[2]  # arma equipada

        if not habilidade:
            print("[AVISO] Nenhuma habilidade básica disponível para ataque extra.")
            return

        # Determina raridade baseada na arma (ou usa padrão)
        raridade = "★"
        if habilidade.tipo_de_ataque != "soco" and self.entidades.jogador.kit_do_explorador.arma:
            raridade = self.entidades.jogador.kit_do_explorador.arma.raridade

        dano = habilidade.calcular_dano_final(
            nivel_jogador=self.entidades.jogador.nivel,
            valor_do_efeito_ataque=self.entidades.jogador.aumento_de_ataque,
            raridade=raridade
        )

        tipo = habilidade.tipo_de_alvo

        if tipo in ("terrestre", "area"):
            # Aplica em todos os inimigos vivos
            for i, inimigo in enumerate(self.inimigos):
                if inimigo.vida_atual > 0:
                    self._aplicar_dano(i, dano)
                    animado = self.inimigos_animados[i]
                    self.danos_flutuantes.append(
                        DanoFlutuante(str(dano), (animado.pos[0], animado.pos[1] - 30))
                    )
        else:
            # Aplica no primeiro inimigo vivo (geralmente o mais à esquerda)
            for i, inimigo in enumerate(self.inimigos):
                if inimigo.vida_atual > 0:
                    self._aplicar_dano(i, dano)
                    animado = self.inimigos_animados[i]
                    self.danos_flutuantes.append(
                        DanoFlutuante(str(dano), (animado.pos[0], animado.pos[1] - 30))
                    )
                    break



    def _icones_acao_equipaveis(self):
        identificador_de_ataques = self.entidades.jogador.kit_do_explorador.obter_ids_do_equipamento()
        print(f"Identificador de ataques: {identificador_de_ataques}")
        if identificador_de_ataques['id_fruta']:
            self.icones_acao.append(_IconeAcao(self.gerenciador_recursos.obter_imagem(CHAVE_ACAO_FRUTA), acao="fruta"))

        if identificador_de_ataques['id_arma']:
            print(f"Tipo de arma equipada: {self.entidades.jogador.kit_do_explorador.arma.tipo_arma}")
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
        self.inimigo_do_meio = onda[1] if len(onda) > 1 else None
        self.inimigo_da_direita = onda[2] if len(onda) > 2 else None

        # Lista de inimigos em ordem para lógica de batalha
        self.inimigos = [
            self.inimigo_da_esquerda if self.inimigo_da_esquerda else None,
            self.inimigo_do_meio,
            self.inimigo_da_direita if self.inimigo_da_direita else None
        ]

        # Posicionamento dos inimigos na tela de batalha
        posicoes = [
            (LARGURA_TELA - 350, ALTURA_TELA - 175) if self.inimigo_da_esquerda else None,
            (LARGURA_TELA - 250, ALTURA_TELA - 100),
            (LARGURA_TELA - 120, ALTURA_TELA - 150) if self.inimigo_da_direita else None
        ]

        self.inimigos_animados = []

        for i, inimigo in enumerate(self.inimigos):
            if not inimigo:
                continue

            imagem = inimigo.imagem
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



    def _analisar_inimigos(self, index_inimigo):
        if not self.inimigos or index_inimigo is None or index_inimigo >= len(self.inimigos):
            return
        inimigo_escolhido = self.inimigos[index_inimigo]
        if not inimigo_escolhido or not inimigo_escolhido.esta_vivo():
            return
        tipo = inimigo_escolhido.nome
        for inimigo in self.inimigos:
            if inimigo and inimigo.nome == tipo:
                inimigo.analizado = True
        print(f"Inimigos do tipo {tipo} foram analisados!")



    def usar_item_da_mochila(self, item):
        self.entidades.jogador.usar_item_da_mochila(item)
        
        # Fecha o menu e passa a vez
        self.estado_batalha = "turno_jogador"
        print("Passa o turno depois de usar o item")
        self._realizar_turno_inimigo()



    def _preparar_habilidade(self):
        self.habilidade_usando = self.habilidades_visiveis[self.habilidade_selecionada_index]
        
        if self.entidades.jogador.energia_atual < self.habilidade_usando.custo:
            print(f"[DEBUG] Energia insuficiente para usar {self.habilidade_usando.nome}")
            self.estado_batalha = "turno_jogador"  # ou mantém no menu
            return  # Cancela a preparação
        
        if self.habilidade_usando.tipo_de_ataque in ["fruta"]:
            for efeito in self.entidades.jogador.efeitos_ativos:
                if efeito["nome"] == "Molhado":
                    print("😰 Não pode usar frutas estando molhado!")
                    self.estado_batalha = "turno_jogador"
                    return

        self.estado_batalha = "selecao_de_alvo"



    def _executar_ataque_jogador(self, alvo_index):
        self.entidades.jogador.energia_atual -= self.habilidade_usando.custo
        self.entidades.jogador.energia_atual = max(0, self.entidades.jogador.energia_atual)

        dano = self._calcular_dano(self.habilidade_usando)
        
        tipo = self.habilidade_usando.tipo_de_alvo
        if tipo in ["area", "terrestre"]:
            for i in range(len(self.inimigos)):
                if self.inimigos[i] and self.inimigos[i].esta_vivo():
                    self._aplicar_dano(i, dano, self.habilidade_usando.efeito)
        else:
            tontura_aplicada = False
            for efeito in self.entidades.jogador.efeitos_ativos:
                if efeito["nome"] == "Tontura":
                    tontura_aplicada = True
                    break
            if tontura_aplicada:
                inimigos_vivos = [inimigo for inimigo in self.inimigos if inimigo and inimigo.esta_vivo()]
                if inimigos_vivos:
                    alvo = random.choice(inimigos_vivos)
                else:
                    alvo = -1
                self._aplicar_dano(self.inimigos.index(alvo), dano, self.habilidade_usando.efeito)
                print(f"😵 Tontura ativa! Ataque pode errar e atingir inimigo aleatório (índice {self.inimigos.index(alvo)})")
            else:
                if tipo in ["fila"]:
                    alvo = self._proximo_inimigo_vivo()
                    if alvo:
                        self._aplicar_dano(self.inimigos.index(alvo), dano, self.habilidade_usando.efeito)
                else:
                    self._aplicar_dano(alvo_index, dano, self.habilidade_usando.efeito)
        
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
        self.bonus_do_jogador = 0

        # Determinar raridade da fonte
        if habilidade.tipo_de_ataque in ["espada", "estilingue", "arco"]:
            raridade = self.entidades.jogador.kit_do_explorador.arma.raridade
        elif habilidade.tipo_de_ataque == "fruta":
            raridade = self.entidades.jogador.kit_do_explorador.fruta.raridade
        else:
            raridade = "★"

        dano_final = habilidade.calcular_dano_final(nivel, ataque, raridade=raridade)

        for efeito in self.entidades.jogador.efeitos_ativos:
            if efeito["nome"] == "Molhado":
                self.bonus_do_jogador -= 20         # Reduz dano em 20% 
            if efeito["nome"] == "Envenenado":
                self.bonus_do_jogador -= 10         # Reduz dano em 10%

        dano_final = dano_final * (1 + self.bonus_do_jogador / 100)

        return dano_final

    def _calcular_esquiva(self):
        chance = self.entidades.jogador.sorte * 5
        roll = random.randint(1, 100)
        return roll <= chance

    def _aplicar_dano(self, index, dano, efeito_da_habilidade=None):
        if not (0 <= index < len(self.inimigos)):
            print(f"[AVISO] Índice de inimigo inválido: {index}")
            return

        chance_de_errar = 0
        for efeito in self.entidades.jogador.efeitos_ativos:
            if efeito["nome"] == "Cegueira":
                chance_de_errar = 0.25  # 25% de chance de errar

        inimigo = self.inimigos[index]
        animado = self.inimigos_animados[index]

        # Garante que dano mínimo seja 0 (caso algo negativo escape)
        dano_final = max(0, dano)

        # Verifica se o inimigo tem efeitos que alteram o dano recebido
        for efeito in inimigo.efeitos_ativos:
            if efeito["nome"] == "Queimadura":
                dano_final = math.floor(dano_final * 1.1)  # Aumenta dano em 10%

        # Adiciona dano flutuante visual
        x, y = animado.pos

        if chance_de_errar > 0 and random.random() < chance_de_errar:
            print("❌ Ataque errou devido à cegueira!")
            self.danos_flutuantes.append(DanoFlutuante("Errou!", (x, y - 30), CINZA))
            return
        
        self.danos_flutuantes.append(DanoFlutuante(str(dano), (x, y - 30)))

        inimigo.vida_atual = max(0, inimigo.vida_atual - dano)
        print(f"💥 {inimigo.nome} recebeu {dano} de dano! Vida restante: {inimigo.vida_atual}/{inimigo.vida_total}")

        # Devolve dano ao jogador se inimigo estiver eletrificado
        x, y = self.posicao_jogador
        for efeito in inimigo.efeitos_ativos:
            if efeito["nome"] == "Eletrificado":
                self.entidades.jogador.vida_atual = max(0, self.entidades.jogador.vida_atual - 2)
                self.danos_flutuantes.append(DanoFlutuante(2, (x, y - 30)))
                if self.entidades.jogador.vida_atual <= 0:
                    self._finalizar_batalha(venceu=False)
                    return

        if efeito_da_habilidade:
            chance_de_aplicar_efeito = 0.3  # 30% de chance padrão
            if random.random() < chance_de_aplicar_efeito:
                inimigo.aplicar_efeitos([efeito_da_habilidade])  



    def _proximo_inimigo_vivo(self):
        for inimigo in self.inimigos:
            if inimigo and inimigo.esta_vivo():
                return inimigo
        return None



    def _encerrar_turno_jogador(self):
        self.entidades.jogador.processar_efeitos_de_fim_de_turno()
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
            i for i, inimigo in enumerate(self.inimigos) if inimigo and inimigo.esta_vivo()
        ]
    
    def _executar_ataque_inimigo(self):
        i = self.fila_ataques_inimigos.pop(0)

        if i >= len(self.inimigos) or i >= len(self.inimigos_animados):
            print(f"[ERRO] Índice inválido na fila de inimigos: {i}")
            return

        inimigo = self.inimigos[i]
        animado = self.inimigos_animados[i]
        
        if inimigo.processar_efeitos_de_inicio_de_turno():
            print(inimigo)
            dano = inimigo.habilidade.calcular_dano_final(inimigo.nivel, 0, "★")

            for efeito in self.entidades.jogador.efeitos_ativos:
                if efeito["nome"] == "Queimadura":
                    dano = math.floor(dano * 1.1)  # Aumenta dano em 10%

            chance_de_errar = 0
            for efeito in inimigo.efeitos_ativos:
                if efeito["nome"] == "Envenenado":
                    dano = math.floor(dano * 0.9)  # Reduz dano em 10%
                if efeito["nome"] == "Cegueira":
                    chance_de_errar = 0.25  # 25% de chance de errar

            animado.iniciar_ataque()

            pos = self.posicao_jogador
            if chance_de_errar > 0 and random.random() < chance_de_errar:
                print("❌ Ataque errou devido à cegueira!")
                self.danos_flutuantes.append(DanoFlutuante("Errou!", (pos[0], pos[1] - 50), CINZA))
            else:
                if self._calcular_esquiva():
                    self.danos_flutuantes.append(DanoFlutuante("Por pouco!", (pos[0], pos[1] - 50), AMARELO))
                    print(f"{self.entidades.jogador.nome} esquivou do ataque!")
                else:
                    self.entidades.jogador.vida_atual = max(0, self.entidades.jogador.vida_atual - dano)

                    self.danos_flutuantes.append(
                        DanoFlutuante(str(dano), (pos[0], pos[1] - 50))
                    )

                    print(f"🧟 Inimigo ({inimigo.nome}) atacou! Jogador perdeu {dano} PV.")

                    if self.entidades.jogador.vida_atual <= 0:
                        self._finalizar_batalha(venceu=False)
                        return

                    for efeito in self.entidades.jogador.efeitos_ativos:
                        if efeito["nome"] == "Eletrificado":
                            inimigo.vida_atual = max(0, inimigo.vida_atual - 2)
                            inimigo.danos_flutuantes.append(
                                DanoFlutuante(2, (animado.pos[0], animado.pos[1] - 30))
                            )
                            if inimigo.vida_atual <= 0:
                                print(f"💀 Inimigo ({inimigo.nome}) foi derrotado pela eletricidade!")
                            break

                    # Aplica efeito do ataque do inimigo, se houver
                    if inimigo.habilidade.efeito:
                        chancer_de_aplicar_efeito = 0.3  # 30% de chance padrão
                        if random.random() < chancer_de_aplicar_efeito:
                            self.entidades.jogador.aplicar_efeitos([inimigo.habilidade.efeito])
        
        inimigo.processar_efeitos_de_fim_de_turno()

        self.tempo_proximo_ataque = 0.7  # Delay entre ataques

        
    
    def _finalizar_batalha(self, venceu):
        self.entidades.jogador.efeitos_ativos = [
            e for e in self.entidades.jogador.efeitos_ativos 
            if e["nome"] not in ["Sangramento", "Queimadura", "Envenenado"]
        ]

        if venceu:
            print("Todos os inimigos foram derrotados! Você venceu a batalha!")
    
            # Ganha experiência e retorna ao mapa
            self.entidades.jogador.experiencia_atual += self.experiencia_acumulada
            self.entidades.jogador.atualizar_atributos_por_nivel()

            self._adiconar_item_ao_invetario_do_jogador(self.itens_obtidos)
    
            self.banco_de_dados.atualizar_atributos_de_batalha_do_jogador(
                self.entidades.jogador.identificador,
                self.entidades.jogador.energia_maxima_base,
                self.entidades.jogador.vida_maxima_base,
                self.entidades.jogador.nivel,
                self.entidades.jogador.sorte_base,
                self.entidades.jogador.energia_atual,
                self.entidades.jogador.vida_atual,
                self.entidades.jogador.experiencia_atual,
                self.entidades.jogador.moedas
            )

            self.missoes.notificar_vitoria_em_batalha(self.tipo_inimigo)
    
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
            self.entidades.jogador.atualizar_atributos_por_nivel()

            self._adiconar_item_ao_invetario_do_jogador(self.itens_obtidos)
    
            self.banco_de_dados.atualizar_atributos_de_batalha_do_jogador(
                self.entidades.jogador.identificador,
                self.entidades.jogador.energia_maxima_base,
                self.entidades.jogador.vida_maxima_base,
                self.entidades.jogador.nivel,
                self.entidades.jogador.sorte_base,
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
        if evento.type == pygame.MOUSEBUTTONDOWN and self.estado_batalha == "menu_mochila":
            if evento.button != 1:
                return

            margem_lateral = 16
            margem_superior = 56
            altura_item = 32
            espacamento = 8

            itens_visiveis = self.mochila_batalha[
                self.scroll_offset_mochila : self.scroll_offset_mochila + self.itens_visiveis_por_pagina
            ]

            for i, item in enumerate(itens_visiveis):
                y_item = self.y_menu_mochila + margem_superior + i * (altura_item + espacamento)
                rect_item = pygame.Rect(
                    self.x_menu_mochila + margem_lateral,
                    y_item,
                    self.largura_menu_mochila - 2 * margem_lateral,
                    altura_item
                )

                if rect_item.collidepoint(evento.pos):
                    self.usar_item_da_mochila(item)
                    return

            if not self.rect_quadro.collidepoint(evento.pos):
                print("Clique fora da caixa – fechando mochila.")
                self.estado_batalha = "turno_jogador"
                return


        elif evento.type == pygame.MOUSEWHEEL and self.estado_batalha == "menu_mochila":
            total_itens = len(self.mochila_batalha)
            max_offset = max(0, total_itens - self.itens_visiveis_por_pagina)

            # Rola para cima (y > 0) ou para baixo (y < 0)
            self.scroll_offset_mochila = max(0, min(self.scroll_offset_mochila - evento.y, max_offset))

        elif evento.type == pygame.MOUSEBUTTONDOWN and self.estado_batalha == "selecionando_habilidade":
            habilidades = self.habilidades_visiveis
            clicou_em_habilidade = False
            print(f"[DEBUG] Habilidades visíveis: {[h.nome for h in habilidades]}")
            for i, habilidade in enumerate(habilidades):
                y = self.y_menu_habilidade + 56 + i * 40
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
                
        elif evento.type == pygame.MOUSEBUTTONDOWN and self.estado_batalha == "menu_estrategias":
            mouse_pos = pygame.mouse.get_pos()

            # Define regiões para os botões (pode ser um pequeno quadro)
            rect_analisar = pygame.Rect(self.x_menu_estrategias + 8, self.y_menu_estrategias + 56, self.largura_menu_estrategias - 16, 32)
            rect_fugir = pygame.Rect(self.x_menu_estrategias, self.y_menu_estrategias + 96, self.largura_menu_estrategias - 16, 32)

            if rect_analisar.collidepoint(mouse_pos):
                self.estado_batalha = "selecionando_inimigo_para_analise"
                return

            if rect_fugir.collidepoint(mouse_pos):
                if self.fuga_habilitada:
                    self.entidades.jogador.efeitos_ativos = [
                        e for e in self.entidades.jogador.efeitos_ativos 
                        if e["nome"] not in ["Sangramento", "Queimadura", "Envenenado"]
                    ]
                    self.gerenciador_telas.mudar_tela(CHAVE_TRANSICAO_MAPA)
                else:
                    print("Fuga não está habilitada nesta batalha.")
                return

            # clique fora → volta para turno normal
            if not rect_analisar.collidepoint(mouse_pos) and not rect_fugir.collidepoint(mouse_pos):
                self.estado_batalha = "turno_jogador"

        elif evento.type == pygame.MOUSEBUTTONDOWN and self.estado_batalha == "selecionando_inimigo_para_analise":
            for i, animado in enumerate(self.inimigos_animados):
                rect = animado.imagem.get_rect(topleft=animado.pos)
                if rect.collidepoint(evento.pos):
                    self._analisar_inimigos(i)
                    self._encerrar_turno_jogador()
                    break
            # Se clicar fora, volta ao turno do jogador
            #self.estado_batalha = "turno_jogador"

        elif evento.type == pygame.MOUSEBUTTONDOWN and self.estado_batalha == "turno_jogador":
            for icone in self.icones_acao:
                if icone.rect.collidepoint(evento.pos):
                    match icone.acao:
                        case "estrategias":
                            print("Abrir menu de estratégias")
                            self.estado_batalha = "menu_estrategias"
                            return


                        case "mochila":
                            print("Abrir mochila")
                            self.estado_batalha = "menu_mochila"
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
            if all(animado.estado == "parado" for animado in self.inimigos_animados):
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
                self._executar_ataque_inimigo()
            elif not self.fila_ataques_inimigos:
                # Se não há mais inimigos na fila, volta para o turno do jogador
                self.estado_batalha = "turno_jogador"
                if not self.entidades.jogador.processar_efeitos_de_inicio_de_turno():
                    self._encerrar_turno_jogador()
                for inimigo in self.inimigos:
                    if inimigo is not None:
                        inimigo.atualizar_efeitos()

        for dano in self.danos_flutuantes:
            dano.update(dt)
        self.danos_flutuantes = [d for d in self.danos_flutuantes if not d.acabou()]


        # 1) Atualiza TODAS as animações visuais
        for animado in self.inimigos_animados:
            animado.update(dt)

        # 2) Dispara fade‑out nos inimigos que acabaram de ficar com PV <= 0
        for i, inimigo in enumerate(self.inimigos):
            if inimigo is not None and inimigo.vida_atual <= 0 and self.inimigos_animados[i].estado == "parado":
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
        if all(not inimigo.esta_vivo() for inimigo in self.inimigos if inimigo is not None):
            self.experiencia_acumulada += inimigo.experiencia if inimigo is not None else 0
            if inimigo:
                self.itens_obtidos.append(inimigo.item)
            inimigo_pop = self.inimigos_lutando.pop(0)
            print(f"Inimigo derrotado: {inimigo_pop.identificador_instancia_lacaio if hasattr(inimigo_pop, 'identificador_instancia_lacaio') else inimigo_pop.identificador}")
            self.banco_de_dados.sekishiki_meikai_ha(inimigo_pop.identificador_instancia_lacaio if hasattr(inimigo_pop, 'identificador_instancia_lacaio') else inimigo_pop.identificador, self.entidades.progresso_do_jogo.identificador_progresso)
            if not self._carregar_proxima_onda():
                print("Todas as ondas foram derrotadas!")
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

        if self.entidades.jogador.frames_animacao['parado']:
            imagem = self.entidades.jogador.frames_animacao['parado'][0]
            if self.tempo_dano_jogador > 0:
                imagem = pygame.transform.rotate(imagem, 15)  # inclina para trás

            rect = imagem.get_rect(center=self.posicao_jogador)
            tela.blit(imagem, rect)

        # Desenhar todos os inimigos da onda atual
        for animado in self.inimigos_animados:
            animado.draw(tela)

        # Desenha os ícones de efeito acima do jogador
        self._desenhar_efeitos_ativos(tela, self.entidades.jogador.efeitos_ativos, (self.posicao_jogador[0], self.posicao_jogador[1] - 50))

        for i, inimigo in enumerate(self.inimigos):
            if inimigo and inimigo.esta_vivo():
                animado = self.inimigos_animados[i]
                x, y = animado.pos

                # Desenha os ícones de efeito acima dos inimigos
                self._desenhar_efeitos_ativos(tela, inimigo.efeitos_ativos, (x + animado.imagem.get_width() // 2, y - 20))
                
                # se analisado → mostrar barra de vida
                if hasattr(inimigo, "analizado") and inimigo.analizado:
                    fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
                    texto = fonte.render(f"{inimigo.vida_atual}/{inimigo.vida_total}", True, PRETO)
                    rect = texto.get_rect(center=(x + animado.imagem.get_width() // 2, y - 50))
                    tela.blit(texto, rect)

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

        if self.estado_batalha == "menu_estrategias":
            tela.blit(self.menu_estrategias, (self.x_menu_estrategias, self.y_menu_estrategias))

            fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
            texto_estrategias = fonte_titulo.render("Estratégias", True, BRANCO_CLARO)
            rect_estrategias = texto_estrategias.get_rect(center=(self.x_menu_estrategias + self.largura_menu_estrategias // 2, self.y_menu_estrategias + 16))
            tela.blit(texto_estrategias, rect_estrategias)

            # Opções do menu
            opcoes = [
                ("Olhar feio e estudar", self.x_menu_estrategias + 16, self.y_menu_estrategias + 50),
                ("Operação pernas pra que te quero", self.x_menu_estrategias + 16, self.y_menu_estrategias + 100)
            ]
            mouse_pos = pygame.mouse.get_pos()
            item_em_foco = None

            for texto, x, y in opcoes:
                rect_item = pygame.Rect(x, y, self.largura_menu_estrategias - 32, 32)
                mouse_sobre = rect_item.collidepoint(mouse_pos)

                tamanho_fonte = 32 if mouse_sobre else 28
                fonte = self.gerenciador_recursos.obter_fonte(
                    CHAVE_FONTE_CHERRY_SUBTITULO if mouse_sobre else CHAVE_FONTE_CHERRY_TEXTO
                )

                if mouse_sobre:
                    item_em_foco = texto

                largura_texto_max = self.largura_menu_estrategias - 32
                texto_nome = self.renderizar_texto_limitado(fonte, texto, BRANCO_CLARO, largura_texto_max)
                self._desenhar_texto_com_borda(
                    tela,
                    texto_nome,
                    fonte,
                    BRANCO_CLARO,
                    PRETO,
                    1,
                    (self.x_menu_estrategias + self.largura_menu_estrategias // 2, y + 4 - (tamanho_fonte - 28) // 2),
                )

        if self.estado_batalha == "menu_mochila":
            tela.blit(self.menu_mochila, (self.x_menu_mochila, self.y_menu_mochila))

            fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
            texto_mochila = fonte_titulo.render("Mochila", True, BRANCO_CLARO)
            rect_mochila = texto_mochila.get_rect(center=(self.x_menu_mochila + self.largura_menu_mochila // 2, self.y_menu_mochila + 16))
            tela.blit(texto_mochila, rect_mochila)

            inicio = self.scroll_offset_mochila
            fim = inicio + self.itens_visiveis_por_pagina
            itens_visiveis = self.mochila_batalha[inicio:fim]
        
            mouse_pos = pygame.mouse.get_pos()
            item_em_foco = None
        
            for i, item in enumerate(itens_visiveis):
                y = self.y_menu_mochila + 56 + i * 40
                rect_item = pygame.Rect(self.x_menu_mochila + 8, y, self.largura_menu_mochila - 16, 32)
        
                mouse_sobre = rect_item.collidepoint(mouse_pos)
        
                # Escolhe a fonte com base no hover
                tamanho_fonte = 32 if mouse_sobre else 28
                if mouse_sobre:
                    fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
                else:
                    fonte = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_TEXTO)
                
                if mouse_sobre:
                    item_em_foco = item
                largura_texto_max = self.largura_menu_mochila - 32  # margem lateral + margem direita
                texto_nome = self.renderizar_texto_limitado(fonte, f" {item.nome} x{item.quantidade} ", (255, 255, 255), largura_texto_max)
                self._desenhar_texto_com_borda(
                    tela,
                    texto_nome,
                    fonte,
                    BRANCO_CLARO,
                    PRETO,
                    1,
                    (self.x_menu_mochila + self.largura_menu_mochila // 2, y + 4 - (tamanho_fonte - 28) // 2),
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

            fonte_titulo = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_CHERRY_SUBTITULO)
            texto_habilidade = fonte_titulo.render("Habilidades", True, BRANCO_CLARO)
            rect_habilidade = texto_habilidade.get_rect(center=(self.x_menu_habilidade + self.largura_menu_habilidade // 2, self.y_menu_habilidade + 16))
            tela.blit(texto_habilidade, rect_habilidade)

            habilidades = self.habilidades_visiveis
            inicio = 0  # por agora sem scroll
            fim = len(habilidades)
            habilidades_visiveis = habilidades[inicio:fim]

            mouse_pos = pygame.mouse.get_pos()
            habilidade_em_foco = None

            for i, habilidade in enumerate(habilidades_visiveis):
                y = self.y_menu_habilidade + 56 + i * 40
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



    def _desenhar_efeitos_ativos(self, tela, efeitos, pos_centro):
        espacamento = 4
        tamanho_icone = 24
        largura_total = len(efeitos) * (tamanho_icone + espacamento)
        x, y = pos_centro

        for efeito in efeitos:
            match efeito["nome"]:
                case "Cegueira":
                    icone = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_CEGUEIRA)
                case "Congelado":
                    icone = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_CONGELADO)
                case "Eletrificado":
                    icone = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_ELETRIFICADO)
                case "Envenenado":
                    icone = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_ENVENENADO)
                case "Molhado":
                    icone = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_MOLHADO)
                case "Queimadura":
                    icone = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_QUEIMADURA)
                case "Sangramento":
                    icone = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_SANGRAMENTO)
                case "Tontura":
                    icone = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_TONTURA)
                case _:
                    icone = None

            if icone:
                # Cria uma superfície fumê (translúcida) para o fundo do ícone
                fundo = pygame.Surface((tamanho_icone + 4, tamanho_icone + 4), pygame.SRCALPHA)
                fundo.fill((30, 30, 30, 160))  # RGBA: cor escura + alpha (160 = ~60% opaco)
                rect = icone.get_rect()
                rect.center = (x - largura_total // 2 + tamanho_icone // 2, y)
                rect_fundo = fundo.get_rect(center=rect.center)
                tela.blit(fundo, rect_fundo)  # desenha o fundo fumê
                tela.blit(icone, rect)        # desenha o ícone por cima
                x += tamanho_icone + espacamento



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
    def __init__(self, nome, vida_total, nivel, experiencia, habilidade, item, imagem):
        self.nome = nome
        self.imagem = imagem
        self.vida_total = vida_total
        self.vida_atual = vida_total
        self.nivel = nivel
        self.experiencia = experiencia
        self.habilidade = habilidade
        self.item = item
        self.analizado = False
        self.efeitos_ativos = []  # status como 'Envenenado', 'Tontura', etc.

    def clonar(self):
        return InimigoBatalha(
            self.nome,
            self.imagem,
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

            match tipo:
                case "Eletrificado":  # Aplica o status eletrificado
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": 2,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Congelado":  # Aplica o status congelado
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "duracao": 1,
                        "tipo": "status"
                    })

                case "Molhado":  # Aplica o status molhado
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Envenenado":  # Aplica o status envenenado
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": 1,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Sangramento":  # Aplica o status sangramento
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": 2,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Queimadura":  # Aplica o status queimadura
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": 1,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Tontura":  # Aplica o status tontura
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case "Cegueira":  # Aplica o status cegueira
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "duracao": 2,
                        "tipo": "status"
                    })

                case _:  # Caso o efeito não seja reconhecido
                    print(f"Efeito desconhecido: {tipo}")

    def processar_efeitos_de_inicio_de_turno(self) -> bool:
        """
        Processa efeitos que ocorrem ANTES da ação da unidade.
        Isso inclui dano por turno (DoT) e status que impedem a ação.
        Retorna True se a unidade pode agir, False caso contrário.
        """
        print(f"--- Início do turno de {self.nome} ---")
        pode_agir = True
        
        # Copia a lista para iterar, pois podemos modificar a original indiretamente
        for efeito in list(self.efeitos_ativos):
            nome = efeito["nome"]

            # 1. Verifica status que impedem a ação
            if nome == "Congelado":
                print(f"{self.nome} está congelado e não pode agir!")
                pode_agir = False

            # 2. Aplica dano contínuo (DoT)
            if nome in ["Queimadura", "Envenenado", "Sangramento"]:
                print(efeito)
                dano = efeito["valor"]
                self.vida_atual = max(0, self.vida_atual - dano)
                print(f"{self.nome} sofreu {dano} de dano de {nome}. Vida restante: {self.vida_atual}")
                if self.vida_atual == 0:
                    print(f"{self.nome} foi derrotado por {nome}!")
                    pode_agir = False # Morreu antes de agir
                    break

        return pode_agir
    
    def processar_efeitos_de_fim_de_turno(self):
        """
        Atualiza a duração dos efeitos e remove os que expiraram.
        Isso acontece DEPOIS que a unidade agiu (ou tentou agir).
        """
        efeitos_restantes = []
        for efeito in self.efeitos_ativos:
            efeito["duracao"] -= 1
            if efeito["duracao"] > 0:
                efeitos_restantes.append(efeito)
            else:
                # O efeito expirou, informa o jogador
                print(f"O efeito '{efeito['nome']}' em {self.nome} acabou.")
        
        self.efeitos_ativos = efeitos_restantes
        print(f"Efeitos de {self.nome} atualizados.")
        print("-" * 20)

    def atualizar_efeitos(self):
        novos = []
        for efeito in self.efeitos_ativos:
            efeito["duracao"] -= 1
            if efeito["duracao"] > 0:
                novos.append(efeito)
        self.efeitos_ativos = novos




  
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
    def __init__(self, texto, pos, cor=(255, 60, 60)):
        self.texto = str(texto)
        self.pos = list(pos)
        self.tempo = 0
        self.max_tempo = 0.8
        self.alpha = 255
        self.cor = cor

    def update(self, dt):
        self.tempo += dt
        self.pos[1] -= 30 * dt
        self.alpha = max(0, 255 * (1 - self.tempo / self.max_tempo))

    def draw(self, tela, fonte):
        if self.tempo < self.max_tempo:
            img = fonte.render(self.texto, True, self.cor)
            img.set_alpha(int(self.alpha))
            rect = img.get_rect(center=self.pos)
            tela.blit(img, rect)

    def acabou(self):
        return self.tempo >= self.max_tempo
