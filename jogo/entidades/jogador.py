# entidades/jogador.py

import pygame
from utilidades.constantes import * # Importa as constantes
from entidades.habilidades import Habilidade
from .personagem import Personagem

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores.db_manager import DBManager
    from gerenciadores import GerenciadorDeRecursos
    from gerenciadores import GerenciadorDeMissoes
    from entidades.item_inventario import ItemInventario
    from entidades.mochila import Mochila
    from entidades.kit import KitDoExplorador

class Jogador(Personagem):
    """Representa o jogador no jogo."""

    def __init__(self, gerenciador_banco_de_dados: 'DBManager', gerenciador_recursos: 'GerenciadorDeRecursos', progresso, coordenada_x, coordenada_y, identificador_jogador, nome, descricao, energia_maxima, vida_maxima, nivel, sorte, energia_atual, vida_atual, experiencia_atual, moedas, orientacao='direita', mochila: 'Mochila' = [], kit: 'KitDoExplorador' = [], id_inventario = None):
        super().__init__(gerenciador_recursos, identificador_jogador, coordenada_x, coordenada_y, nome, descricao)
        
        self.banco_de_dados = gerenciador_banco_de_dados
        self.gerenciador_missoes: 'GerenciadorDeMissoes' = None
        self.fator_de_escala = 1.0

        # Estado do jogador
        self.velocidade = VELOCIDADE_JOGADOR
        self.orientacao = orientacao
        self.identificador_progresso = progresso
        self.descricao = descricao
        self.vida_maxima_base = vida_maxima
        self.energia_maxima_base = energia_maxima
        self.energia_maxima = energia_maxima
        self.vida_maxima = vida_maxima
        self.nivel = nivel
        self.sorte_base = sorte
        self.sorte = sorte
        self.energia_atual = energia_atual  # Energia atual do jogador
        self.vida_atual = vida_atual
        self.experiencia_atual = experiencia_atual
        self.moedas = moedas                # Quantidade de moedas do jogador
        self.experiencia_por_nivel = 100    # Experiência necessária para subir de nível
        self.efeitos_ativos = []            # Cada efeito será um dicionário
        self.aumento_de_ataque = 0          # Efeito de ataque, que pode ser aumentado com itens e/ou acessórios, será somado ao dano final da habilidade
        self.id_mochila = id_inventario     # ID da mochila do jogador, usado para persistência no banco de dados

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
            self.imagem = self.frames_animacao[self.estado][self.indice_frame]
        else:
            # Fallback robusto caso todas as imagens falhem
            print("ERRO GRAVE: frames_animacao['parado'] está vazio no __init__ do Jogador. Criando superfície vazia para evitar crash.")
            self.imagem = pygame.Surface((LARGURA_JOGADOR, ALTURA_JOGADOR))
            self.imagem.fill(AZUL) # Uma cor diferente para indicar um erro mais grave
        
        self.rect = self.imagem.get_rect(topleft=(int(self.coordenada_x), int(self.coordenada_y)))

        altura_pes = 18
        self.pes_rect = pygame.Rect(
            self.rect.x,
            self.rect.bottom - altura_pes,
            self.rect.width,
            altura_pes
        )

        # Flags de movimento contínuo (agora gerenciadas internamente por processar_eventos_continuo)
        self.movendo_esquerda = False
        self.movendo_direita = False
        self.movendo_cima = False
        self.movendo_baixo = False

        # Variáveis para o ícone de interação
        self.mostrar_icone_interacao = False
        self.icone_interacao = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_INTERACAO)

        # NOVO: Flag para bloquear o movimento controlado pelo jogador
        self.movimento_bloqueado = False 

        self.mochila = mochila  # Lista de itens na mochila do jogador
        self.kit_do_explorador = kit # Lista de itens equipados pelo jogador
        self.habilidades = []  # Lista de habilidades do jogador
        self.aplicar_efeito_do_acessorio()  # Aplica o efeito do acessório equipado, se houver
        self.carregar_habilidades()  # Carrega as habilidades do jogador



    def inserir_item_na_mochila(self, item: 'ItemInventario', identificador_progresso):
        if self.banco_de_dados.adicionar_item_ao_inventario(self.id_mochila, item.identificador_item, item.quantidade):
            self.mochila = self.banco_de_dados.carregar_mochila_do_jogador(self.identificador, identificador_progresso)



    def usar_item_da_mochila(self, item: 'ItemInventario'):
        if self.banco_de_dados.remover_item_do_inventario(self.id_mochila, item.identificador_item):
            print(f"[DEBUG] Item {item.identificador_item} removido do inventário do jogador {self.identificador}.")
            self.mochila.usar_item(item.identificador_item, self)



    def remover_item_da_mochila(self, identificador_item, quantidade=1):
        if self.banco_de_dados.remover_item_do_inventario(self.id_mochila, identificador_item, quantidade):
            self.mochila.subtrair_quantidade(identificador_item, quantidade)



    def equipar_item(self, item: 'ItemInventario', identificador_progresso):
        if self.banco_de_dados.equipar_item_no_kit(
            self.identificador,
            item.identificador_item,
            item.tipo,
            identificador_progresso
        ):
            # 1. Remove o item da mochila
            self.mochila.remover(item.identificador_item)

            # 2. Verifica se já havia item do mesmo tipo no kit
            item_substituido = None

            match item.tipo:
                case "arma":
                    if self.kit_do_explorador.arma:
                        item_substituido = self.kit_do_explorador.arma
                    self.kit_do_explorador.arma = item
                case "fruta":
                    if self.kit_do_explorador.fruta:
                        item_substituido = self.kit_do_explorador.fruta
                    self.kit_do_explorador.fruta = item
                case "acessorio":
                    if self.kit_do_explorador.acessorio:
                        item_substituido = self.kit_do_explorador.acessorio
                    self.kit_do_explorador.acessorio = item

            # 3. Adiciona item substituído de volta à mochila
            if item_substituido:
                self.mochila.adicionar(item_substituido)



    def calcular_nivel(self, experiencia_total):
        return experiencia_total // 100 + 1  # Nível começa em 1, então adicionamos 1 ao resultado da divisão
  


    def atualizar_atributos_por_nivel(self):
        novo_nivel = self.calcular_nivel(self.experiencia_atual)
        ganho_de_niveis = novo_nivel - self.nivel

        if ganho_de_niveis > 0:
            self.nivel = novo_nivel
            self.vida_maxima += ganho_de_niveis
            self.energia_maxima += ganho_de_niveis
            self.vida_atual = self.vida_maxima
            self.energia_atual = self.energia_maxima
            print(f"O jogador subiu {ganho_de_niveis} nível(s)!")
            if self.gerenciador_missoes and self.nivel == 10:
                self.gerenciador_missoes.iniciar_missao('mis011')



    def aplicar_efeito_do_acessorio(self):
        ids = self.kit_do_explorador.obter_ids_do_equipamento()
        self.bonus_vida = 0
        self.bonus_energia = 0
        self.bonus_ataque = 0
        self.bonus_sorte = 0
        print(f"[DEBUG] Equipamento atual do jogador {self.nome}: {ids}")
        if ids["id_acessorio"]:
            efeito_acessorio = self.banco_de_dados.buscar_efeito_por_acessorio(ids["id_acessorio"])
            if efeito_acessorio:
                for efeito in efeito_acessorio:
                    match efeito.efeito_nome:
                        case "Vida Máxima":
                            self.bonus_vida += efeito.efeito_valor
                        case "Energia Máxima":
                            self.bonus_energia += efeito.efeito_valor
                        case "Ataque":
                            self.bonus_ataque += efeito.efeito_valor
                        case "Sorte":
                            self.bonus_sorte += efeito.efeito_valor
        print(f"[DEBUG] Bônus do acessório aplicado ao jogador {self.nome}: Vida +{self.bonus_vida}, Energia +{self.bonus_energia}, Ataque +{self.bonus_ataque}, Sorte +{self.bonus_sorte}")
        self.recalcular_atributos()

    def recalcular_atributos(self):
        self.vida_maxima = self.vida_maxima_base + getattr(self, "bonus_vida", 0)
        print(f"[DEBUG] Vida máxima recalculada para o jogador {self.nome}: {self.vida_maxima} (Base: {self.vida_maxima_base} + Bônus: {getattr(self, 'bonus_vida', 0)})")
        self.energia_maxima = self.energia_maxima_base + getattr(self, "bonus_energia", 0)
        print(f"[DEBUG] Energia máxima recalculada para o jogador {self.nome}: {self.energia_maxima} (Base: {self.energia_maxima_base} + Bônus: {getattr(self, 'bonus_energia', 0)})")
        self.aumento_de_ataque = getattr(self, "bonus_ataque", 0)
        print(f"[DEBUG] Aumento de ataque recalculado para o jogador {self.nome}: {self.aumento_de_ataque} (Bônus: {getattr(self, 'bonus_ataque', 0)})")
        self.sorte = max(1, self.sorte + getattr(self, "bonus_sorte", 0))  # Sorte nunca deve ser menor que 1
        print(f"[DEBUG] Sorte recalculada para o jogador {self.nome}: {self.sorte} (Base + Bônus: {getattr(self, 'bonus_sorte', 0)})")

        # garante que vida/energia atuais não passem do máximo
        self.vida_atual = min(self.vida_atual, self.vida_maxima)
        self.energia_atual = min(self.energia_atual, self.energia_maxima)



    def aplicar_efeitos(self, efeitos):
        """
        Aplica os efeitos do item ao jogador. A quantidade deve ser controlada fora.
        """
        for efeito in efeitos:
            tipo = efeito["nome"]
            valor = efeito["valor"]
            print(f"[DEBUG] Aplicando efeito: {tipo} com valor {valor} ao jogador {self.nome}")
            match tipo:
                case "Cura":  # Cura de vida
                    self.vida_atual += valor
                    self.vida_atual = min(self.vida_atual, self.vida_maxima)

                case "Energia":  # Recupera de energia
                    self.energia_atual += valor
                    self.energia_atual = min(self.energia_atual, self.energia_maxima)
                
                case "Ataque":  # Aumenta o ataque
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 3,  # duração em turnos
                        "tipo": "buff"
                    })
                    self.aumento_de_ataque += valor

                case "Sorte":  # Aumenta a sorte: Aumente a chance de esquivar-se de um ataque
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 3,  # duração em turnos
                        "tipo": "buff"
                    })
                    self.sorte += valor

                case "Eletrificado":  # Aplica o status eletrificado: Cause 2 de dano ao ser atacado
                    existente = False
                    for e in self.efeitos_ativos:
                        if e["nome"] == "Eletrificado":
                            existente = True
                            e["duracao"] = 2  # Reinicia a duração
                            print(f"[DEBUG] Jogador {self.nome} já está eletrificado. Não reaplicando.")
                            break

                    if not existente:
                        self.efeitos_ativos.append({
                            "nome": tipo,
                            "valor": 2,
                            "duracao": 2,
                            "tipo": "status"
                        })

                case "Congelado":  # Aplica o status congelado: Passe a vez
                    existente = False
                    for e in self.efeitos_ativos:
                        if e["nome"] == "Congelado":
                            existente = True
                            e["duracao"] = 1  # Reinicia a duração
                            print(f"[DEBUG] Jogador {self.nome} já está Congelado. Não reaplicando.")
                            break
                    
                    if not existente:
                        self.efeitos_ativos.append({
                            "nome": tipo,
                            "duracao": 1,
                            "tipo": "status"
                        })

                case "Molhado":  # Aplica o status molhado: Bloqueia habilidades de Akuma no Mi e reduz o dano causado em 20%
                    existente = False
                    for e in self.efeitos_ativos:
                        if e["nome"] == "Molhado":
                            existente = True
                            e["duracao"] = 2  # Reinicia a duração
                            print(f"[DEBUG] Jogador {self.nome} já está Molhado. Não reaplicando.")
                            break

                    if not existente:
                        self.efeitos_ativos.append({
                            "nome": tipo,
                            "duracao": 2,
                            "tipo": "status"
                        })

                case "Envenenado":  # Aplica o status envenenado: Causa 1 de dano antes de agir e reduz o dano causado em 10%
                    existente = False
                    for e in self.efeitos_ativos:
                        if e["nome"] == "Envenenado":
                            existente = True
                            e["duracao"] = 2  # Reinicia a duração
                            print(f"[DEBUG] Jogador {self.nome} já está Envenenado. Não reaplicando.")
                            break

                    if not existente:
                        self.efeitos_ativos.append({
                            "nome": tipo,
                            "valor": 1,
                            "duracao": 2,
                            "tipo": "status"
                        })

                case "Sangramento":  # Aplica o status sangramento: Causa 2 de dano antes de agir
                    existente = False
                    for e in self.efeitos_ativos:
                        if e["nome"] == "Sangramento":
                            existente = True
                            e["duracao"] = 2  # Reinicia a duração
                            print(f"[DEBUG] Jogador {self.nome} já está com Sangramento. Não reaplicando.")
                            break

                    if not existente:
                        self.efeitos_ativos.append({
                            "nome": tipo,
                            "valor": 2,
                            "duracao": 2,
                            "tipo": "status"
                        })

                case "Queimadura":  # Aplica o status queimadura: Causa 1 de dano antes de agir e aumenta o dano sofrido em 10%
                    existente = False
                    for e in self.efeitos_ativos:
                        if e["nome"] == "Queimadura":
                            existente = True
                            e["duracao"] = 2  # Reinicia a duração
                            print(f"[DEBUG] Jogador {self.nome} já está com Queimadura. Não reaplicando.")
                            break

                    if not existente:
                        self.efeitos_ativos.append({
                            "nome": tipo,
                            "valor": 1,
                            "duracao": 2,
                            "tipo": "status"
                        })

                case "Tontura":  # Aplica o status tontura: Aumenta a chance de errar o alvo
                    existente = False
                    for e in self.efeitos_ativos:
                        if e["nome"] == "Tontura":
                            existente = True
                            e["duracao"] = 2  # Reinicia a duração
                            print(f"[DEBUG] Jogador {self.nome} já está com Tontura. Não reaplicando.")
                            break

                    if not existente:
                        self.efeitos_ativos.append({
                            "nome": tipo,
                            "duracao": 2,
                            "tipo": "status"
                        })

                case "Cegueira":  # Aplica o status cegueira: Aumenta a chance de errar o ataque
                    existente = False
                    for e in self.efeitos_ativos:
                        if e["nome"] == "Cegueira":
                            existente = True
                            e["duracao"] = 2  # Reinicia a duração
                            print(f"[DEBUG] Jogador {self.nome} já está com Cegueira. Não reaplicando.")
                            break

                    if not existente:
                        self.efeitos_ativos.append({
                            "nome": tipo,
                            "duracao": 2,
                            "tipo": "status"
                        })

                case "Purificação":
                    efeitos_aplicados = [
                        "Eletrificado", "Molhado", "Envenenado", 
                        "Sangramento", "Queimadura",
                        "Tontura", "Cegueira"
                    ]
                    self.efeitos_ativos = [
                        e for e in self.efeitos_ativos if e["nome"] not in efeitos_aplicados
                    ]

                case _:  # Caso o efeito não seja reconhecido
                    print(f"Efeito desconhecido: {tipo}")

            # Você pode adicionar suporte a outros tipos de efeito aqui futuramente



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



    def atualizar_posicao_jogador(self, x_inicial, y_inicial, orientacao='direita'):
        self.coordenada_x = float(x_inicial) # Usar float para movimento mais suave, depois converter para int para o rect
        self.coordenada_y = float(y_inicial) # Usar float para movimento mais suave, depois converter para int para o rect
        self.orientacao = orientacao
    


    def aplicar_fator_de_escala(self, fator):
        """Troca os frames animados por versões ampliadas ou normais já carregadas."""
        if self.fator_de_escala == fator:
            return

        self.fator_de_escala = fator
        self.carregar_animacoes()  # Recarrega frames com o novo sufixo (_ampliada)

        self.imagem = self.frames_animacao[self.estado][self.indice_frame]
        self.rect = self.imagem.get_rect(topleft=(int(self.coordenada_x), int(self.coordenada_y)))

        altura_pes = int(18 * fator)
        self.pes_rect = pygame.Rect(
            self.rect.x,
            self.rect.bottom - altura_pes,
            self.rect.width,
            altura_pes
        )



    def carregar_animacoes(self):
        """Carrega as animações com base no nome do jogador e no fator de escala atual."""
        sufixo = "_ampliada" if self.fator_de_escala > 1.0 else ""

        def obter_chave_da_imagem(nome_base):
            chave = self.nome + nome_base + sufixo
            return self.gerenciador_recursos.obter_imagem(chave)

        self.frames_animacao = {
            'parado': [],
            'caminhando': []
        }

        imagem_parado = obter_chave_da_imagem('_em_repouso')
        imagem_caminhar_1 = obter_chave_da_imagem('_caminhando_1')
        imagem_caminhar_2 = obter_chave_da_imagem('_caminhando_2')
        imagem_caminhar_3 = obter_chave_da_imagem('_caminhando_3')

        if imagem_parado:
            self.frames_animacao['parado'].append(imagem_parado)
        else:
            fallback_surface = pygame.Surface((LARGURA_JOGADOR, ALTURA_JOGADOR), pygame.SRCALPHA)
            fallback_surface.fill(PRETO)
            self.frames_animacao['parado'].append(fallback_surface)

        valid_caminhada_frames = [img for img in [imagem_caminhar_1, imagem_caminhar_2, imagem_caminhar_3] if img]
        if not valid_caminhada_frames:
            valid_caminhada_frames = self.frames_animacao['parado'] * 3

        self.frames_animacao['caminhando'] = (
            [valid_caminhada_frames[0], valid_caminhada_frames[1], valid_caminhada_frames[2], valid_caminhada_frames[1]]
            if len(valid_caminhada_frames) >= 3
            else valid_caminhada_frames * 2
        )

        self.frame_parada_apos_caminhada = (
            self.frames_animacao['caminhando'][1]
            if len(self.frames_animacao['caminhando']) > 1
            else self.frames_animacao['parado'][0]
        )



    def get_area_de_ataque(self):
        """Retorna a área de ataque do jogador com base na posição e orientação."""
        x, y = self.rect.center
    
        if self.orientacao == "direita":
            return pygame.Rect(x, y - 10, 60, 40)
        else:
            return pygame.Rect(x - 60, y - 10, 60, 40)



    def processar_eventos_continuos(self):
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
            self.orientacao = 'esquerda'
        if keys[pygame.K_d]:
            self.movendo_direita = True
            self.orientacao = 'direita'
        if keys[pygame.K_w]:
            self.movendo_cima = True
        if keys[pygame.K_s]:
            self.movendo_baixo = True



    def _obter_terreno_atual(self, lista_de_caminhos):
        """
        Verifica o tipo de terreno sob os pés do jogador.
        Prioriza 'neve' se houver múltiplos terrenos.
        Retorna:
            str: O tipo de terreno ('neve', 'grama', etc.) ou 'normal' se nenhum for encontrado.
        """
        terreno_encontrado = 'normal' # Valor padrão se não estiver em nenhum caminho

        for caminho in lista_de_caminhos:
            # Verifica se os pés do jogador colidem com o retângulo do caminho
            if self.pes_rect.colliderect(caminho) and hasattr(caminho, 'tipo_terreno'):
                terreno_encontrado = caminho.tipo_terreno
                # Se o terreno for neve, ele tem prioridade máxima, então já podemos retornar.
                if terreno_encontrado == 'neve':
                    return 'neve'
        
        return terreno_encontrado



    def _esta_dentro_do_caminho(self, lista_de_caminhos):
        """
        Método privado que verifica se os 4 cantos do jogador estão em algum
        dos retângulos da lista de caminhos. Retorna True se a posição for válida.
        """
        # Se não houver caminhos definidos, qualquer lugar é válido.
        if not lista_de_caminhos:
            return True

        cantos = [self.pes_rect.topleft, self.pes_rect.topright,
                  self.pes_rect.bottomleft, self.pes_rect.bottomright]
        
        for canto in cantos:
            canto_esta_valido = False
            # Itera sobre cada objeto Caminho na lista
            for caminho in lista_de_caminhos:
                if caminho.collidepoint(canto):
                    canto_esta_valido = True
                    break # Encontrou um caminho válido para este canto, pode testar o próximo canto
            
            # Se este canto específico não estava em nenhum caminho, a posição geral é inválida
            if not canto_esta_valido:
                return False
        
        # Se todos os cantos passaram na verificação, a posição é válida
        return True



    def carregar_habilidades(self):
        identificadores_do_equipamento = self.kit_do_explorador.obter_ids_do_equipamento()
        habilidades_personagem = self.banco_de_dados.buscar_habilidades_por_personagem(self.identificador) or []
        habilidades_arma = self.banco_de_dados.buscar_habilidades_por_arma(identificadores_do_equipamento["id_arma"]) if identificadores_do_equipamento["id_arma"] else []
        habilidades_fruta = self.banco_de_dados.buscar_habilidades_por_fruta(identificadores_do_equipamento["id_fruta"]) if identificadores_do_equipamento["id_fruta"] else []

        print("identificadores_do_equipamento:", identificadores_do_equipamento)

        print("Habilidades do jogador:")
        for row in habilidades_personagem:
            print(row)

        print("Habilidades da arma:")
        for row in habilidades_arma:
            print(row)

        print("Habilidades da Akuma no Mi:")
        for row in habilidades_fruta:
            print(row)

        conjunto_de_habilidades = habilidades_personagem + habilidades_arma + habilidades_fruta

        self.habilidades = [
            Habilidade(
                id=h.identificador_habilidade,
                nome=h.nome.strip(),  # Remove espaços extras
                descricao=h.descricao.strip(),
                tipo_de_ataque=h.tipo_de_ataque.strip(),
                tipo_de_alvo=h.tipo_de_alvo.strip(),
                dano=h.dano,
                custo=h.custo,
                efeito=(
                    {"nome": h.efeito_nome.strip(), "valor": h.efeito_valor} if h.efeito_nome else None
                )
            )
            for h in conjunto_de_habilidades
        ]



    def atualizar(self, dt, obstaculos, lista_de_caminhos, largura_mundo, altura_mundo, limitar_posicao_no_mundo=True):
        """
        Atualiza a posição do jogador e a animação a cada frame do jogo.
        :param dt: Delta time (tempo em segundos desde o último frame).
        :param obstaculos: Um grupo de sprites de obstáculos para colisão.
        :param lista_de_caminhos: Uma lista de objetos Caminho que definem a área andável.
        """
        dx, dy = 0, 0 # Zera os deltas

        # Só processa input e movimento se não estiver bloqueado
        if not self.movimento_bloqueado:
            self.processar_eventos_continuos()

            # --- NOVO: LÓGICA DE VELOCIDADE BASEADA NO TERRENO ---
            
            # 1. Obtém o terreno atual sob os pés do jogador
            terreno_atual = self._obter_terreno_atual(lista_de_caminhos)

            # 2. Define o modificador de velocidade com base no terreno
            modificador_velocidade = 1.0  # 100% da velocidade por padrão
            if terreno_atual == 'neve':
                modificador_velocidade = 0.7  # 70% da velocidade (redução de 30%)
            
            # 3. Calcula a velocidade efetiva para este quadro
            velocidade_efetiva = self.velocidade * modificador_velocidade

            # --- FIM DA NOVA LÓGICA ---

            pos_anterior_x = self.coordenada_x
            pos_anterior_y = self.coordenada_y

            if self.movendo_esquerda:
                dx -= velocidade_efetiva
            if self.movendo_direita:
                dx += velocidade_efetiva
            if self.movendo_cima:
                dy -= velocidade_efetiva
            if self.movendo_baixo:
                dy += velocidade_efetiva

            # --- Verificação de colisão em X ---
            self.coordenada_x += dx
            self.rect.x = int(self.coordenada_x)
            self.pes_rect.centerx = self.rect.centerx # NOVO: Sincroniza o X dos pés
            self.pes_rect.bottom = self.rect.bottom   # NOVO: Sincroniza o Y dos pés

            colidiu_obstaculo_x = False
            for obstaculo in obstaculos:
                if self.pes_rect.colliderect(obstaculo.rect):
                    colidiu_obstaculo_x = True
                    break
            
            fora_do_caminho_x = not self._esta_dentro_do_caminho(lista_de_caminhos)

            if colidiu_obstaculo_x or fora_do_caminho_x:
                self.coordenada_x = pos_anterior_x
                self.rect.x = int(self.coordenada_x)
                self.pes_rect.centerx = self.rect.centerx # Re-sincroniza após reverter
                self.pes_rect.bottom = self.rect.bottom

            # --- Verificação de colisão em Y ---
            self.coordenada_y += dy
            self.rect.y = int(self.coordenada_y)
            self.pes_rect.centerx = self.rect.centerx # NOVO: Sincroniza o X dos pés
            self.pes_rect.bottom = self.rect.bottom   # NOVO: Sincroniza o Y dos pés

            colidiu_obstaculo_y = False
            for obstaculo in obstaculos:
                if self.pes_rect.colliderect(obstaculo.rect):
                    colidiu_obstaculo_y = True
                    break

            fora_do_caminho_y = not self._esta_dentro_do_caminho(lista_de_caminhos)

            if colidiu_obstaculo_y or fora_do_caminho_y:
                self.coordenada_y = pos_anterior_y
                self.rect.y = int(self.coordenada_y)
                self.pes_rect.centerx = self.rect.centerx # Re-sincroniza após reverter
                self.pes_rect.bottom = self.rect.bottom

            if limitar_posicao_no_mundo:
                self.coordenada_x = max(0, min(self.coordenada_x, largura_mundo - self.rect.width))
                self.coordenada_y = max(0, min(self.coordenada_y, altura_mundo - self.rect.height))
        
            # --- Atualizar Animação --- (O resto do método permanece idêntico)
            esta_movendo = (self.movendo_esquerda or self.movendo_direita or
                            self.movendo_cima or self.movendo_baixo)
            
        else:
            # Determina se o jogador está se movendo (pela missão)
            esta_movendo = self.estado == 'caminhando'
        
        # (O restante da sua lógica de animação continua aqui, sem alterações)
        if esta_movendo:
            self.estado = 'caminhando'
            self.tempo_desde_ultimo_frame += dt
            if self.tempo_desde_ultimo_frame >= self.taxa_animacao:
                if self.frames_animacao['caminhando']:
                    self.indice_frame = (self.indice_frame + 1) % len(self.frames_animacao['caminhando'])
                else:
                    self.indice_frame = 0
                self.tempo_desde_ultimo_frame = 0.0
        else:
            self.estado = 'parado'
            self.indice_frame = 0
            self.tempo_desde_ultimo_frame = 0.0
            if hasattr(self, 'frame_parada_apos_caminhada') and self.frame_parada_apos_caminhada:
                self.imagem = self.frame_parada_apos_caminhada
                del self.frame_parada_apos_caminhada
                pass

        imagem_atual = None
        if self.estado == 'parado' and self.frames_animacao['parado']:
            # print(self.mundo_x, self.mundo_y)
            imagem_atual = self.frames_animacao['parado'][self.indice_frame]
        elif self.estado == 'caminhando' and self.frames_animacao['caminhando']:
            imagem_atual = self.frames_animacao['caminhando'][self.indice_frame]
        else:
            imagem_atual = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            imagem_atual.fill(VERMELHO)

        if self.orientacao == 'esquerda':
            imagem_atual = pygame.transform.flip(imagem_atual, True, False)

        self.imagem = imagem_atual



    def desenhar(self, tela, camera_x, camera_y):
        """
        Desenha o jogador na tela, ajustando pela posição da câmera.
        :param tela: A superfície do Pygame onde desenhar.
        :param camera_x: A posição X da câmera.
        :param camera_y: A posição Y da câmera (se o jogo rolar verticalmente).
        """
        # A posição do jogador na tela é sua posição no mundo menos a posição da câmera
        posicao_tela_x = self.coordenada_x - camera_x
        posicao_tela_y = self.coordenada_y - camera_y
        
        tela.blit(self.imagem, (int(posicao_tela_x), int(posicao_tela_y)))

        # Desenha o ícone de interação se aplicável
        if self.mostrar_icone_interacao and self.icone_interacao:
            icone_x = posicao_tela_x + self.rect.width // 2 - self.icone_interacao.get_width() // 2
            icone_y = posicao_tela_y - self.icone_interacao.get_height() + 10
            tela.blit(self.icone_interacao, (int(icone_x), int(icone_y)))

        # DEBUG: Desenha o retângulo de colisão do jogador
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            debug_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height)
            pygame.draw.rect(tela, COR_CAIXA_COLISAO, debug_rect, 1)

            # NOVO: Retângulo dos pés (colisão)
            debug_rect_pes = pygame.Rect(self.pes_rect.x - camera_x, self.pes_rect.y - camera_y, self.pes_rect.width, self.pes_rect.height)
            pygame.draw.rect(tela, VERMELHO, debug_rect_pes, 2) # Cor e espessura diferentes para destacar