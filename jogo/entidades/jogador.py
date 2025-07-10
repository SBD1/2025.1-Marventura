# entidades/jogador.py

import pygame
from utilidades.constantes import * # Importa as constantes
from entidades.mochila import Mochila
from entidades.kit import KitDoExplorador
from entidades.habilidades import Habilidade

class Jogador(pygame.sprite.Sprite):
    """Representa o jogador no jogo."""

    def __init__(self, gerenciador_banco_de_dados, gerenciador_recursos, x_inicial, y_inicial, identificador_jogador, nome, descricao, energia_maxima, vida_maxima, nivel, sorte, energia_atual, vida_atual, experiencia_atual, moedas, orientacao='direita', mochila = [], kit = [], id_inventario = None):
        super().__init__()
        self.gerenciador_recursos = gerenciador_recursos
        self.banco_de_dados = gerenciador_banco_de_dados
        # REMOVIDO: self.fator_de_escala = fator_de_escala

        # Estado do jogador
        self.mundo_x = float(x_inicial) # Usar float para movimento mais suave, depois converter para int para o rect
        self.mundo_y = float(y_inicial) # Usar float para movimento mais suave, depois converter para int para o rect
        self.velocidade = VELOCIDADE_JOGADOR
        self.orientacao = orientacao
        self.identificador_jogador = identificador_jogador
        self.nome = nome
        self.descricao = descricao
        self.energia_maxima = energia_maxima
        self.vida_maxima = vida_maxima
        self.nivel = nivel
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
        
        self.rect = self.imagem.get_rect(topleft=(int(self.mundo_x), int(self.mundo_y)))

        altura_pes = 18
        self.pes_rect = pygame.Rect(
            self.rect.x,
            self.rect.bottom - altura_pes,
            self.rect.width,
            altura_pes
        )

        # Flags de movimento contínuo (agora gerenciadas internamente por handle_input_continuo)
        self.movendo_esquerda = False
        self.movendo_direita = False
        self.movendo_cima = False
        self.movendo_baixo = False

        # Variáveis para o ícone de interação
        self.mostrar_icone_interacao = False
        self.icone_interacao = self.gerenciador_recursos.obter_imagem(CHAVE_ICONE_INTERACAO)

        self.mochila = Mochila(mochila)  # Lista de itens na mochila do jogador
        self.kit_do_explorador = KitDoExplorador(kit) # Lista de itens equipados pelo jogador
        self.habilidades = []  # Lista de habilidades do jogador
        self.aplicar_efeito_do_acessorio()  # Aplica o efeito do acessório equipado, se houver
        self.carregar_habilidades()  # Carrega as habilidades do jogador

    def calcular_nivel(self, experiencia_total):
        return experiencia_total // 100
  
    def atualizar_atributos_por_nivel(self, jogador):
        novo_nivel = self.calcular_nivel(jogador.experiencia_atual)
        ganho_de_niveis = novo_nivel - jogador.nivel

        if ganho_de_niveis > 0:
            jogador.nivel = novo_nivel
            jogador.vida_maxima += ganho_de_niveis
            jogador.energia_maxima += ganho_de_niveis
            jogador.vida_atual = jogador.vida_maxima
            jogador.energia_atual = jogador.energia_maxima
            print(f"O jogador subiu {ganho_de_niveis} nível(s)!")

    def aplicar_efeito_do_acessorio(self):
        ids = self.kit_do_explorador.obter_ids_do_equipamento()
        if ids["id_acessorio"]:
            efeito_acessorio = self.banco_de_dados.buscar_efeito_por_acessorio(ids["id_acessorio"])
            print(f"[DEBUG] Efeito do acessório encontrado: {efeito_acessorio}")
            if efeito_acessorio:
                lista_de_efeitos = [
                    {
                        "nome": efeito.efeito_nome,
                        "valor": efeito.efeito_valor
                    }
                    for efeito in efeito_acessorio
                ]
                self.aplicar_efeitos(lista_de_efeitos)

    def aplicar_efeitos(self, efeitos):
        """
        Aplica os efeitos do item ao jogador. A quantidade deve ser controlada fora.
        """
        for efeito in efeitos:
            tipo = efeito["nome"]
            valor = efeito["valor"]

            match tipo:
                case "Cura":  # Cura de vida
                    self.vida_atual += valor
                    self.vida_atual = min(self.vida_atual, self.vida_maxima)

                case "Energia":  # Recupera de energia
                    self.energia_atual += valor
                    self.energia_atual = min(self.energia_atual, self.energia_maxima)

                case "Vida Máxima":  # Aumenta a vida máxima
                    self.vida_maxima += valor

                case "Energia Máxima":  # Aumenta a energia máxima
                    self.energia_maxima += valor
                
                case "Ataque":  # Aumenta o ataque
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 3,  # duração em turnos
                        "tipo": "buff"
                    })
                    self.aumento_de_ataque += valor

                case "Sorte":  # Aumenta a sorte
                    self.efeitos_ativos.append({
                        "nome": tipo,
                        "valor": valor,
                        "duracao": 3,  # duração em turnos
                        "tipo": "buff"
                    })
                    self.sorte += valor

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

    def atualizar_efeitos(self):
        novos = []
        for efeito in self.efeitos_ativos:
            efeito["duracao"] -= 1
            if efeito["duracao"] > 0:
                novos.append(efeito)
            else:
                # Efeito expirou
                if efeito["nome"] == "Ataque":
                    self.aumento_de_ataque = max(0, self.aumento_de_ataque - efeito["valor"])

                    print(f"[DEBUG] Efeito de ataque expirou (-{efeito['valor']})")

                elif efeito["nome"] == "Sorte":
                    self.sorte = max(1, self.sorte - efeito["valor"])
                    print(f"[DEBUG] Efeito de sorte expirou (-{efeito['valor']})")
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
                self.vida_atual -= valor
                self.vida_atual = max(0, self.vida_atual)  # Garante que a vida não fique negativa
                print(f"{self.nome} sofreu {valor} de dano por {nome} (antes de agir).")
    
            elif momento == "depois" and nome in ["Envenenado", "Sangramento"]:
                self.vida_atual -= valor
                self.vida_atual = max(0, self.vida_atual)  # Garante que a vida não fique negativa
                print(f"{self.nome} sofreu {valor} de dano por {nome} (após agir).")



    def atualizar_posicao_jogador(self, x_inicial, y_inicial, orientacao='direita'):
        self.mundo_x = float(x_inicial) # Usar float para movimento mais suave, depois converter para int para o rect
        self.mundo_y = float(y_inicial) # Usar float para movimento mais suave, depois converter para int para o rect
        self.orientacao = orientacao
    


    def carregar_animacoes(self):
        # Carrega imagens. Assume-se que elas já estão escaladas pelo GerenciadorDeRecursos.
        imagem_parado = self.gerenciador_recursos.obter_imagem(self.nome + '_em_repouso')
        imagem_caminhar_frame_1 = self.gerenciador_recursos.obter_imagem(self.nome + '_caminhando_1')
        imagem_caminhar_frame_2 = self.gerenciador_recursos.obter_imagem(self.nome + '_caminhando_2')
        imagem_caminhar_frame_3 = self.gerenciador_recursos.obter_imagem(self.nome + '_caminhando_3')

        # Adiciona frame 'parado'
        if imagem_parado:
            self.frames_animacao['parado'].append(imagem_parado)
        else:
            print(f"AVISO: Imagem '{self.nome}_em_repouso' não encontrada para o jogador. Usando fallback padrão.")
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
            print(f"AVISO: Nenhuma imagem de caminhada para '{self.nome}' carregada. Usando imagem parada como fallback para caminhada.")
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



    def get_area_de_ataque(self):
        """Retorna a área de ataque do jogador com base na posição e orientação."""
        x, y = self.rect.center
    
        if self.orientacao == "direita":
            return pygame.Rect(x, y - 10, 60, 40)
        else:
            return pygame.Rect(x - 60, y - 10, 60, 40)



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
            if self.pes_rect.colliderect(caminho):
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
        habilidades_personagem = self.banco_de_dados.buscar_habilidades_por_personagem(self.identificador_jogador) or []
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



    def update(self, dt, obstaculos, lista_de_caminhos): # NOVO: Adicionado 'lista_de_caminhos'
        """
        Atualiza a posição do jogador e a animação a cada frame do jogo.
        :param dt: Delta time (tempo em segundos desde o último frame).
        :param obstaculos: Um grupo de sprites de obstáculos para colisão.
        :param lista_de_caminhos: Uma lista de objetos Caminho que definem a área andável.
        """
        self.handle_input_continuo()

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

        pos_anterior_x = self.mundo_x
        pos_anterior_y = self.mundo_y

        dx, dy = 0, 0
        if self.movendo_esquerda:
            dx -= velocidade_efetiva
        if self.movendo_direita:
            dx += velocidade_efetiva
        if self.movendo_cima:
            dy -= velocidade_efetiva
        if self.movendo_baixo:
            dy += velocidade_efetiva

        # --- Verificação de colisão em X ---
        self.mundo_x += dx
        self.rect.x = int(self.mundo_x)
        self.pes_rect.centerx = self.rect.centerx # NOVO: Sincroniza o X dos pés
        self.pes_rect.bottom = self.rect.bottom   # NOVO: Sincroniza o Y dos pés

        colidiu_obstaculo_x = False
        for obstaculo in obstaculos:
            if self.pes_rect.colliderect(obstaculo.rect):
                colidiu_obstaculo_x = True
                break
        
        fora_do_caminho_x = not self._esta_dentro_do_caminho(lista_de_caminhos)

        if colidiu_obstaculo_x or fora_do_caminho_x:
            self.mundo_x = pos_anterior_x
            self.rect.x = int(self.mundo_x)
            self.pes_rect.centerx = self.rect.centerx # Re-sincroniza após reverter
            self.pes_rect.bottom = self.rect.bottom

        # --- Verificação de colisão em Y ---
        self.mundo_y += dy
        self.rect.y = int(self.mundo_y)
        self.pes_rect.centerx = self.rect.centerx # NOVO: Sincroniza o X dos pés
        self.pes_rect.bottom = self.rect.bottom   # NOVO: Sincroniza o Y dos pés

        colidiu_obstaculo_y = False
        for obstaculo in obstaculos:
            if self.pes_rect.colliderect(obstaculo.rect):
                colidiu_obstaculo_y = True
                break

        fora_do_caminho_y = not self._esta_dentro_do_caminho(lista_de_caminhos)

        if colidiu_obstaculo_y or fora_do_caminho_y:
            self.mundo_y = pos_anterior_y
            self.rect.y = int(self.mundo_y)
            self.pes_rect.centerx = self.rect.centerx # Re-sincroniza após reverter
            self.pes_rect.bottom = self.rect.bottom

        # --- Atualizar Animação --- (O resto do método permanece idêntico)
        esta_movendo = (self.movendo_esquerda or self.movendo_direita or
                        self.movendo_cima or self.movendo_baixo)
        
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
            imagem_atual = self.frames_animacao['parado'][self.indice_frame]
        elif self.estado == 'caminhando' and self.frames_animacao['caminhando']:
            imagem_atual = self.frames_animacao['caminhando'][self.indice_frame]
        else:
            imagem_atual = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            imagem_atual.fill(VERMELHO)

        if self.orientacao == 'esquerda':
            imagem_atual = pygame.transform.flip(imagem_atual, True, False)

        self.imagem = imagem_atual



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
        
        screen.blit(self.imagem, (int(posicao_tela_x), int(posicao_tela_y)))

        # Desenha o ícone de interação se aplicável
        if self.mostrar_icone_interacao and self.icone_interacao:
            icone_x = posicao_tela_x + self.rect.width // 2 - self.icone_interacao.get_width() // 2
            icone_y = posicao_tela_y - self.icone_interacao.get_height() + 10
            screen.blit(self.icone_interacao, (int(icone_x), int(icone_y)))

        # DEBUG: Desenha o retângulo de colisão do jogador
        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            debug_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height)
            pygame.draw.rect(screen, COR_CAIXA_COLISAO, debug_rect, 1)

            # NOVO: Retângulo dos pés (colisão)
            debug_rect_pes = pygame.Rect(self.pes_rect.x - camera_x, self.pes_rect.y - camera_y, self.pes_rect.width, self.pes_rect.height)
            pygame.draw.rect(screen, VERMELHO, debug_rect_pes, 2) # Cor e espessura diferentes para destacar