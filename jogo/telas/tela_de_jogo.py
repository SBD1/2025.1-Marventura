# telas/tela_jogo.py

import pygame
from utilidades.constantes import *
from entidades import Inimigo
from entidades import Obstaculo
from entidades import Caminho
from entidades import AreaInteracao
from utilidades import Camera
from .tela_modelo import TelaModelo
from gerenciadores import GerenciadorDeEntidades

class TelaJogo(TelaModelo): # Herda de TelaModelo
    """
        Representa a tela principal do jogo para um mapa específico.
        Onde a jogabilidade acontece, com fundo rolante, jogador, obstáculos e áreas de interação.
        Carrega e exibe elementos do mapa com base nos dados do mapa, ponto de entrada ou dados salvos.
        :param gerenciador_telas: O gerenciador de telas.
        :param gerenciador_recursos: O gerenciador de recursos.
        :param id_mapa: O identificador do mapa atual.
        :param jogador: O tipo de jogador ('menino' ou 'menina').
        :param ponto_de_destino: O identificador do ponto de renascimento/reinício do jogador.
        :param coordenada_x: Posição X inicial no mundo.
        :param coordenada_y: Posição Y inicial no mundo.
        :param olhando_para_direita: Se o jogador está olhando para direita ou não.
        """
    def __init__(self, gerenciador_telas, gerenciador_recursos, gerenciador_banco_de_dados):
        super().__init__(gerenciador_telas, gerenciador_recursos) # Chama o construtor da TelaModelo
        self.gerenciador_entidades = GerenciadorDeEntidades()

        self.dados_da_area = self.gerenciador_entidades.area_atual
        self.dados_da_ilha = self.gerenciador_entidades.ilha_atual
        self.dados_do_progresso = self.gerenciador_entidades.progresso_do_jogo
        self.banco_de_dados = gerenciador_banco_de_dados

        # --- Atributos para o menu de viagem ---
        self.menu_viagem = None # Será uma instância de _MenuViagemFlutuante quando ativo
        self.menu_viagem_ativo = False

        self.tempo_ocioso = 0  # Tempo que o jogador está ocioso
        self.limite_ocioso = 5  # Tempo limite em segundos para exibir a barra de estado
        self.barra_de_estado_visivel = False  # Controla a visibilidade da barra de estado

        # --- Atributo para exibição do nome da ilha ---
        self.exibicao_nome_ilha = None # Será uma instância de _ExibicaoNomeIlha

        # Inicializa a exibição do nome da ilha (chamando o método auxiliar)
        self._marcar_ilha_visitada_e_exibir_nome()

        self.mapa_fundo_imagem = self.gerenciador_recursos.obter_imagem(self.dados_da_area.chave_imagem_fundo)

        # --- Carregar a camada superior (opcional) ---
        self.camada_superior_imagem = None
        if self.dados_da_area.chave_imagem_frente:
            self.camada_superior_imagem = self.gerenciador_recursos.obter_imagem(self.dados_da_area.chave_imagem_frente)

        self.largura_mundo = self.mapa_fundo_imagem.get_width()
        self.altura_mundo = self.mapa_fundo_imagem.get_height()

        self.camera = Camera(
            largura_janela=LARGURA_TELA,
            altura_janela=ALTURA_TELA,
            tamanho_mundo=(self.largura_mundo, self.altura_mundo)
        )

        self.jogador = self.gerenciador_entidades.jogador

        self.obstaculos_caminho = pygame.sprite.Group()
        self.obstaculos_visao = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.areas_interacao = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()

        # --- Variáveis para rastrear áreas de interação ativas ---
        self.areas_interacao_colididas = [] # Lista das áreas de interação onde o jogador está colidindo
        self.caminhos = []

        self._carregar_entidades_dos_dados_do_mapa()

        self.efeitos_visuais = []
        self.sprites_efeito_ataque = [
            pygame.image.load(f"recursos/efeitos/slash_{i}.png").convert_alpha()
            for i in range(5)
        ]
        # print("Sprites de ataque carregadas:", len(self.sprites_efeito_ataque))


    def _carregar_entidades_dos_dados_do_mapa(self):
        id_area_atual = self.dados_da_area.identificador_area
        obstaculos = self.banco_de_dados.buscar_obstaculos_da_area(id_area_atual)
        for obj_data in obstaculos:
            obstaculo = Obstaculo(
                self.gerenciador_recursos,
                obj_data.x, obj_data.y,
                obj_data.largura, obj_data.altura
            )
            self.obstaculos_caminho.add(obstaculo)
            self.obstaculos_visao.add(obstaculo)
        
        caminhos = self.banco_de_dados.buscar_caminhos_da_area(id_area_atual)
        caminho_arena = None 
        for dado_do_caminho in caminhos:
            caminho = Caminho(dado_do_caminho.x, dado_do_caminho.y,
                              dado_do_caminho.largura, dado_do_caminho.altura,
                              dado_do_caminho.tipo_terreno)
            if caminho.tipo_terreno == 'arena':
                # O inimigo sampre fica restringido dentro de um caminho. Aqui encontra qual é esse caminho.
                caminho_arena = caminho
            self.caminhos.append(caminho)

        if not caminho_arena:
            print("AVISO: Nenhum caminho do tipo 'arena' foi encontrado no mapa. Os inimigos não serão carregados.")
        else:
            inimigos = self.banco_de_dados.buscar_lacaios_por_area(self.dados_do_progresso.identificador_progresso, id_area_atual)

            # Carrega os inimigos, agora passando o caminho da arena
            for dado_do_inimigo in inimigos:
                habilidades = self.banco_de_dados.buscar_habilidades_por_personagem(dado_do_inimigo.identificador_instancia_lacaio)
                itens = self.banco_de_dados.buscar_inventario(dado_do_inimigo.identificador_instancia_lacaio, 'moc', self.dados_do_progresso.identificador_progresso)

                novo_inimigo = Inimigo(
                    self.gerenciador_recursos,
                    dado_do_inimigo.x, dado_do_inimigo.y,
                    dado_do_inimigo.nome_lacaio,
                    dado_do_inimigo.descricao_lacaio,
                    dado_do_inimigo.vida_atual,
                    dado_do_inimigo.vida_total,
                    dado_do_inimigo.nivel,
                    dado_do_inimigo.experiencia,
                    habilidade=habilidades,
                    inventario=itens,
                    caminho_container=caminho_arena, # Passa o caminho encontrado
                )
                self.inimigos.add(novo_inimigo)

        areas_interativas = self.banco_de_dados.buscar_areas_interativas_da_area(id_area_atual)
        for area_data in areas_interativas:
            area = AreaInteracao(area_data.x, area_data.y,
                                area_data.largura, area_data.altura,
                                area_data.tipo_evento,
                                area_data.chance_sucesso,
                                area_data.area_destino,
                                area_data.chave_imagem)

            self.areas_interacao.add(area)



    def _marcar_ilha_visitada_e_exibir_nome(self):
        """
        Marca a ilha atual como visitada e inicializa a exibição do nome da ilha e da área.
        """
        # db.marcar_ilha_como_visitada(self.dados_da_ilha.identificador_ilha)

        if self.dados_da_ilha.nome or self.dados_da_area.nome: # Só cria a exibição se houver algo para mostrar
            self.exibicao_nome_ilha = _ExibicaoNomeIlha(self.dados_da_ilha.nome, self.dados_da_area.nome, self.gerenciador_recursos)
        else:
            self.exibicao_nome_ilha = None
            print(f"AVISO: Nenhuma informação de ilha ou área para exibir para o mapa ID: {self.dados_da_area.identificador_area}")



    def busca_dados_do_inimigo(self, tipos_inimigos):
        """
        Busca os dados de uma lista de tipos de inimigos.
        :param tipos_inimigos: Uma lista de tipos de inimigos.
        :return: Uma lista de dicionários com os dados dos inimigos.
        """
        dados_dos_inimigos = []
    
        for tipo in tipos_inimigos:
            match tipo:
                case 'Lobo':
                    dados_dos_inimigos.append({
                        'tipo': 'Lobo',
                        'imagem': 'Lobo_0',
                        'PV': 15,
                        'XP': 10,
                        'dano': 5,
                        'item': 'Presa Afiada'
                    })
                case 'Corvo':
                    dados_dos_inimigos.append({
                        'tipo': 'Corvo',
                        'imagem': 'Corvo_0',
                        'PV': 10,
                        'XP': 8,
                        'dano': 3,
                        'item': 'Carne de Ave Brava'
                    })
                case _:
                    print(f"Tipo de inimigo desconhecido: {tipo}")
        
        return dados_dos_inimigos



    def _ataque_no_mapa(self):
        # Definir posição do efeito baseado na direção do jogador
        x, y = self.jogador.rect.center
        if self.jogador.orientacao == "direita":
            efeito_pos = (x + 20, y - 10)
        else:
            efeito_pos = (x - 80, y - 10)

        # Adiciona efeito à lista (dura 0.2 segundos)
        self.efeitos_visuais.append({
            "sprites": self.sprites_efeito_ataque,
            "pos": efeito_pos,
            "frame": 0,
            "tempo_por_frame": 0.05,
            "tempo_restante": 0.05
        })


        # Defina um retângulo de ataque à frente (ex: 40 pixels)
        if self.jogador.orientacao == "direita":
            area_ataque = pygame.Rect(x, y - 10, 60, 40)
        else:
            area_ataque = pygame.Rect(x - 60, y - 10, 60, 40)

        # Verifica se algum inimigo colidiu com essa área
        inimigos_acertados = [i for i in self.inimigos if area_ataque.colliderect(i.rect)]

        if inimigos_acertados:
            print("Ataque no mapa acertou inimigo!")
            ondas = self._montar_ondas(inimigos_acertados)

            self.gerenciador_telas.mudar_tela(
                CHAVE_TRANSICAO_BATALHA,
                inimigos_na_batalha=ondas,
                jogador_iniciou=True
            )



    def _montar_ondas(self, sprites_colididos):
        """
        Recebe uma lista de sprites (cada um representa um grupo no mapa)
        e devolve [[dict, dict, dict],  ...]   (1 lista por onda, 3 cópias cada)
        """
        ondas = []
        for sprite in sprites_colididos:          # cada sprite vira uma onda
            base = self.busca_dados_do_inimigo([sprite.tipo_inimigo])[0]
            # cópias independentes para PV, XP, etc.
            ondas.append([base.copy() for _ in range(3)])
        return ondas



    def handle_input(self, evento):
        transicao_info = super().handle_input(evento)
        if transicao_info:
            return transicao_info
        
        # --- Lógica do Menu de Viagem (se estiver ativo) ---
        if self.menu_viagem_ativo and self.menu_viagem:
            resultado_menu = self.menu_viagem.handle_input(evento)
            if resultado_menu is not None:
                if resultado_menu == "cancelar":
                    self.menu_viagem_ativo = False
                    self.menu_viagem = None # Limpa a instância do menu
                    return None # Consome o evento
                else: # Uma ilha foi selecionada
                    ilha_selecionada = resultado_menu
                    print(f"Viajando para: {ilha_selecionada.identificador_ilha}")

                    if ilha_selecionada:
                        porto_destino = self.banco_de_dados.buscar_porto_da_ilha(ilha_selecionada.identificador_ilha, self.dados_do_progresso.identificador_progresso)
                        print(f"porto_destino: {porto_destino}")
                        if porto_destino:
                            self.menu_viagem_ativo = False
                            self.menu_viagem = None # Limpa a instância do menu
                            id_area = porto_destino.identificador_area

                            self.gerenciador_entidades.ilha_atual = ilha_selecionada

                            self.gerenciador_entidades.area_atual = porto_destino

                            informacoes_de_destino = self.banco_de_dados.buscar_conexao_entre_areas(self.dados_da_area.identificador_area, id_area)
                            
                            self.gerenciador_entidades.jogador.atualizar_posicao_jogador(
                                informacoes_de_destino.ponto_geracao_x,
                                informacoes_de_destino.ponto_geracao_y,
                                informacoes_de_destino.orientacao
                            )
                            return {'estado': CHAVE_TRANSICAO_MAPA}
                        else:
                            print(f"AVISO: Não foi possível determinar o mapa de destino para a ilha '{ilha_selecionada.nome}'.")
                    else:
                        print(f"AVISO: ID da ilha não encontrado para o nome '{ilha_selecionada.nome}'.")
            return None # Consome o evento, não processa o input do jogador normal


        # --- Lógica de Interação com Áreas de Interação (Eventos KEYDOWN) ---
        # SOMENTE reage a um evento KEYDOWN, não ao estado contínuo da tecla.
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e: # Tecla de interação
                # Verifica colisões APÓS o jogador já ter se movido no último update
                # (ou no próximo, dependendo da ordem do loop principal)
                # O importante é que a interação só aconteça uma vez por apertar de tecla.
                
                # Obtém as áreas de interação que estão colidindo com o jogador
                areas_colidindo_agora = pygame.sprite.spritecollide(self.jogador, self.areas_interacao, False)
                
                for area in areas_colidindo_agora:
                    if area.tipo_evento == 'mudar_area':
                        print(f"Detectou interação para mudar mapa para {area.area_destino}")
                        self.gerenciador_entidades.area_atual = self.banco_de_dados.buscar_info_area(area.area_destino, self.dados_do_progresso.identificador_progresso)

                        informacoes_de_destino = self.banco_de_dados.buscar_conexao_entre_areas(self.dados_da_area.identificador_area, area.area_destino)

                        self.gerenciador_entidades.jogador.atualizar_posicao_jogador(
                            informacoes_de_destino.ponto_geracao_x,
                            informacoes_de_destino.ponto_geracao_y,
                            informacoes_de_destino.orientacao
                        )

                        return {'estado': CHAVE_TRANSICAO_MAPA}
                    elif area.tipo_evento == 'embarcar':
                        if not self.menu_viagem_ativo:
                            print('Embarcando na viagem...')
                            self.ilhas_vizinhas = self.banco_de_dados.buscar_conexoes_ilha(self.dados_da_area.identificador_ilha, self.dados_do_progresso.identificador_progresso)

                            self.menu_viagem = _MenuViagemFlutuante(self.ilhas_vizinhas)
                            self.menu_viagem_ativo = True
                            return None # Consome o evento
                    
                    # Adicione outros tipos de interação aqui (ex: diálogo com NPC)
                    # elif area.tipo_evento == 'dialogo_npc':
                    #     return {'estado': CHAVE_TRANSICAO_DIALOGO, 'npc_id': area.dados_evento['npc_id']}

            elif evento.key == pygame.K_x:
                self._ataque_no_mapa()

        return None # Nenhuma transição de tela por eventos de interação



    def update(self, dt):
        super().update(dt)

        if self.menu_viagem_ativo and self.menu_viagem:
            return None

        # Atualiza o jogador (ele apenas tenta se mover, sem clamping ainda)
        self.jogador.update(dt, self.obstaculos_caminho, self.caminhos)

        # Lógica de clamping do jogador para não sair dos limites do mundo
        largura_mundo_atual = self.mapa_fundo_imagem.get_width()
        altura_mundo_atual = self.mapa_fundo_imagem.get_height()

        # Limita a posição X do jogador
        if self.jogador.rect.left < 0:
            self.jogador.rect.left = 0
        if self.jogador.rect.right > largura_mundo_atual:
            self.jogador.rect.right = largura_mundo_atual

        # Limita a posição Y do jogador
        if self.jogador.rect.top < 0:
            self.jogador.rect.top = 0
        if self.jogador.rect.bottom > altura_mundo_atual:
            self.jogador.rect.bottom = altura_mundo_atual

        # Se o jogador colidiu com obstáculos OU foi aparado pelos limites do mapa,
        # sua posição `rect` já estará correta. Apenas atualize `mundo_x` e `mundo_y`.
        self.jogador.mundo_x = self.jogador.rect.x
        self.jogador.mundo_y = self.jogador.rect.y

        # Atualiza a visibilidade do ícone de interação
        self.areas_interacao_colididas = pygame.sprite.spritecollide(self.jogador, self.areas_interacao, False)
        self.inimigos_lutando = pygame.sprite.spritecollide(self.jogador, self.inimigos, False)
        self.jogador.mostrar_icone_interacao = len(self.areas_interacao_colididas) > 0


        self.camera.update(self.jogador.rect)

        for inimigo in self.inimigos:
            inimigo.update(dt, self.jogador, self.obstaculos_caminho, self.obstaculos_visao)
            if inimigo.atingiu_jogador:
                ondas_de_inimigos = self._montar_ondas(self.inimigos_lutando)
                print(f"self.inimigos: {ondas_de_inimigos}")
                # Sinaliza para o gerenciador de telas que uma batalha deve começar
                self.gerenciador_telas.mudar_tela(
                    CHAVE_TRANSICAO_BATALHA,
                    inimigos_na_batalha=ondas_de_inimigos
                )
                return # Termina o update aqui para não processar mais nada após a transição
            
        # --- Atualiza a exibição do nome da ilha ---
        if self.exibicao_nome_ilha:
            self.exibicao_nome_ilha.update()

        # Atualizar duração dos efeitos
        novos_efeitos = []

        for efeito in self.efeitos_visuais:
            efeito["tempo_restante"] -= dt
            if efeito["tempo_restante"] <= 0:
                efeito["frame"] += 1
                if efeito["frame"] < len(efeito["sprites"]):
                    efeito["tempo_restante"] = efeito["tempo_por_frame"]
                    novos_efeitos.append(efeito)
                # senão: animação acabou, não adiciona de novo
            else:
                novos_efeitos.append(efeito)

        self.efeitos_visuais = novos_efeitos



        return None



    def draw(self, tela):
        # Desenha a imagem de fundo
        tela.blit(self.mapa_fundo_imagem, (self.mapa_fundo_imagem.get_rect(topleft=(-self.camera.rect.x, -self.camera.rect.y))))
        
        # Desenha o jogador
        self.jogador.draw(tela, self.camera.rect.x, self.camera.rect.y)

        # Desenha os inimigos
        for inimigo in self.inimigos:
            inimigo.draw(tela, self.camera.rect.x)

        # Desenha o efeito do ataque no mapa
        for efeito in self.efeitos_visuais:
            # print(f"Desenhando efeito: {efeito['frame']}, Tempo restante: {efeito['tempo_restante']:.2f}s")
            sprite = efeito["sprites"][efeito["frame"]]
            sprite = pygame.transform.scale(sprite, (60, 60))
            if self.jogador.orientacao == "direita":
                sprite = pygame.transform.flip(sprite, True, False)
            pos = efeito["pos"]
            tela.blit(sprite, (pos[0]-self.camera.rect.x, pos[1]-self.camera.rect.y))

        # --- Desenhar a camada superior (se existir) ---
        if self.camada_superior_imagem:
            tela.blit(self.camada_superior_imagem, (self.camada_superior_imagem.get_rect(topleft=(-self.camera.rect.x, -self.camera.rect.y))))

        for caminho in self.caminhos:
            caminho.desenhar(tela, self.camera.rect.x)

        if DEBUG_DESENHAR_CAIXAS_COLISAO:
            for area in self.areas_interacao:
                area_rect_tela = pygame.Rect(
                    area.rect.x - self.camera.rect.x,
                    area.rect.y - self.camera.rect.y,
                    area.rect.width,
                    area.rect.height
                )
                pygame.draw.rect(tela, AZUL, area_rect_tela, 2)

            for obstaculo in self.obstaculos_caminho:
                rect_colisao_tela = pygame.Rect(
                    obstaculo.rect.x - self.camera.rect.x,
                    obstaculo.rect.y - self.camera.rect.y,
                    obstaculo.rect.width,
                    obstaculo.rect.height
                )
                pygame.draw.rect(tela, COR_CAIXA_COLISAO, rect_colisao_tela, 1)

        # --- Desenha o nome da ilha com fade ---
        if self.exibicao_nome_ilha:
            self.exibicao_nome_ilha.draw(tela)
        
        # --- Desenha o menu de viagem se estiver ativo ---
        if self.menu_viagem_ativo and self.menu_viagem:
            self.menu_viagem.draw(tela)




class _MenuViagemFlutuante:
    def __init__(self, opcoes_viagem):
        self.opcoes = opcoes_viagem  # Lista de objetos Row com id, nome_ilha, visitada
        self.indice_selecionado = 0
        self.fonte_menu = pygame.font.Font(None, 36)
        self.cor_texto_normal = (255, 255, 255)
        self.cor_texto_selecionado = (255, 255, 0)
        self.cor_fundo_menu = (50, 50, 50, 200)
        self.cor_borda_menu = (200, 200, 200)

    def handle_input(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)
            elif evento.key == pygame.K_DOWN:
                self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)
            elif evento.key == pygame.K_RETURN:
                if self.opcoes:
                    return self.opcoes[self.indice_selecionado]  # Retorna o ID da ilha
                return None
            elif evento.key == pygame.K_ESCAPE:
                return "cancelar"

        return None

    def draw(self, tela):
        if not self.opcoes:
            return

        largura_menu = 300
        altura_linha = self.fonte_menu.get_height() + 10
        altura_menu = (len(self.opcoes) * altura_linha) + 40

        pos_x_menu = (LARGURA_TELA - largura_menu) // 2
        pos_y_menu = (ALTURA_TELA - altura_menu) // 2

        retangulo_menu = pygame.Rect(pos_x_menu, pos_y_menu, largura_menu, altura_menu)

        s = pygame.Surface((largura_menu, altura_menu), pygame.SRCALPHA)
        s.fill(self.cor_fundo_menu)
        tela.blit(s, retangulo_menu.topleft)

        pygame.draw.rect(tela, self.cor_borda_menu, retangulo_menu, 3)

        y_offset = pos_y_menu + 20
        for i, opcao in enumerate(self.opcoes):
            nome_ilha = opcao.nome  # Usa o nome da ilha para exibir
            cor_texto = self.cor_texto_selecionado if i == self.indice_selecionado else self.cor_texto_normal
            texto_renderizado = self.fonte_menu.render(nome_ilha, True, cor_texto)

            pos_x_texto = pos_x_menu + (largura_menu - texto_renderizado.get_width()) // 2
            tela.blit(texto_renderizado, (pos_x_texto, y_offset))
            y_offset += altura_linha



class _ExibicaoNomeIlha:
    def __init__(self, nome_ilha, nome_area_mapa, gerenciador_recursos):
        self.nome_ilha = nome_ilha
        self.nome_area_mapa = nome_area_mapa

        self.fonte_ilha = gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_BOTAO) # Fonte maior para o nome da ilha
        self.fonte_area = gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO) # Fonte menor para o nome da área
        self.cor = (255, 255, 255) # Branco

        self.ativo = True
        self.alpha = 0 # Transparência atual (0-255)
        self.tempo_inicio_animacao = pygame.time.get_ticks()
        self.duracao_fade = 1000 # 1 segundo para fade-in/out
        self.duracao_estatica = 2000 # 2 segundos no máximo de opacidade

    def update(self):
        if not self.ativo:
            return

        tempo_decorrido = pygame.time.get_ticks() - self.tempo_inicio_animacao
        total_duracao = self.duracao_fade + self.duracao_estatica + self.duracao_fade

        if tempo_decorrido < self.duracao_fade: # Fade-in
            self.alpha = int(255 * (tempo_decorrido / self.duracao_fade))
        elif tempo_decorrido < (self.duracao_fade + self.duracao_estatica): # Estático
            self.alpha = 255
        elif tempo_decorrido < total_duracao: # Fade-out
            tempo_decorrido_fade_out = tempo_decorrido - (self.duracao_fade + self.duracao_estatica)
            self.alpha = int(255 * (1 - (tempo_decorrido_fade_out / self.duracao_fade)))
            if self.alpha < 0:
                self.alpha = 0
        else: # Animação completa
            self.ativo = False
            self.alpha = 0

    def draw(self, tela):
        if not self.ativo or not self.nome_ilha:
            return

        # Renderiza o nome da ilha (maior)
        texto_ilha_superficie = self.fonte_ilha.render(self.nome_ilha, True, self.cor)
        texto_ilha_superficie.set_alpha(self.alpha)

        # Renderiza o nome da área do mapa (menor)
        texto_area_superficie = None
        if self.nome_area_mapa: # Só renderiza se houver um nome de área
            texto_area_superficie = self.fonte_area.render(self.nome_area_mapa, True, self.cor)
            texto_area_superficie.set_alpha(self.alpha)

        # Calcula posições para centralizar e empilhar
        pos_x_ilha = (LARGURA_TELA - texto_ilha_superficie.get_width()) // 2
        pos_y_ilha = 50 # Posição vertical inicial no topo

        tela.blit(texto_ilha_superficie, (pos_x_ilha, pos_y_ilha))

        if texto_area_superficie:
            pos_x_area = (LARGURA_TELA - texto_area_superficie.get_width()) // 2
            # Posiciona a área abaixo da ilha, com um pequeno espaçamento
            pos_y_area = pos_y_ilha + texto_ilha_superficie.get_height() + 10 # 10 pixels de espaço

            tela.blit(texto_area_superficie, (pos_x_area, pos_y_area))
