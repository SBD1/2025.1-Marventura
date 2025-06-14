# telas/tela_jogo.py

import pygame
import sys
from utilidades.constantes import *
from entidades import Jogador
from entidades import Inimigo
from entidades import Obstaculo
from entidades import AreaInteracao
from utilidades import Camera
from mapa_dados import dados_das_ilhas, get_ilhas_vizinhas, get_ilha_por_mapa_id, obter_dados_da_sala, obter_dados_da_ilha
from .tela_modelo import TelaModelo

class TelaJogo(TelaModelo): # Herda de TelaModelo
    """
        Representa a tela principal do jogo para um mapa específico.
        Onde a jogabilidade acontece, com fundo rolante, jogador, obstáculos e áreas de interação.
        Carrega e exibe elementos do mapa com base nos dados do mapa, ponto de entrada ou dados salvos.
        :param gerenciador_telas: O gerenciador de telas.
        :param gerenciador_recursos: O gerenciador de recursos.
        :param id_mapa: O identificador do mapa atual.
        :param personagem: O tipo de personagem ('menino' ou 'menina').
        :param ponto_de_destino: O identificador do ponto de renascimento/reinício do jogador.
        :param coordenada_x: Posição X inicial no mundo.
        :param coordenada_y: Posição Y inicial no mundo.
        :param olhando_para_direita: Se o jogador está olhando para direita ou não.
        """
    def __init__(self, gerenciador_telas, gerenciador_recursos, id_mapa_atual, personagem, ponto_de_destino = None, coordenada_x = None, coordenada_y = None, olhando_direita = None):
        super().__init__(gerenciador_telas, gerenciador_recursos) # Chama o construtor da TelaModelo

        self.id_mapa = id_mapa_atual
        self.personagem = personagem
        self.ponto_de_destino = ponto_de_destino
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y
        self.olhando_direita = olhando_direita

        # --- Atributos para o menu de viagem ---
        self.menu_viagem = None # Será uma instância de _MenuViagemFlutuante quando ativo
        self.menu_viagem_ativo = False

        # --- Atributo para exibição do nome da ilha ---
        self.exibicao_nome_ilha = None # Será uma instância de _ExibicaoNomeIlha

        # Inicializa a exibição do nome da ilha (chamando o método auxiliar)
        self._marcar_ilha_visitada_e_exibir_nome()

        self.mapa_data = obter_dados_da_sala(self.id_mapa)

        self.mapa_fundo_imagem = self.gerenciador_recursos.obter_imagem(self.mapa_data['chave_cenario'])
        if not self.mapa_fundo_imagem:
            print(f"ERRO: Imagem de cenário '{self.mapa_data['chave_cenario']}' não encontrada para o mapa '{self.id_mapa}'!")
            sys.exit()

        # --- Carregar a camada superior (opcional) ---
        self.camada_superior_imagem = None
        if 'chave_camada_superior' in self.mapa_data:
            self.camada_superior_imagem = self.gerenciador_recursos.obter_imagem(self.mapa_data['chave_camada_superior'])
            if not self.camada_superior_imagem:
                print(f"AVISO: Imagem de camada superior '{self.mapa_data['chave_camada_superior']}' não encontrada para o mapa '{self.id_mapa}'. A camada superior não será exibida.")


        self.largura_mundo = self.mapa_fundo_imagem.get_width()
        self.altura_mundo = self.mapa_fundo_imagem.get_height()

        self.camera = Camera(
            largura_janela=LARGURA_TELA,
            altura_janela=ALTURA_TELA,
            tamanho_mundo=(self.largura_mundo, self.altura_mundo)
        )

        pos_info = self._definir_posicao_inicial_jogador()
        pos_x_jogador = pos_info['x']
        pos_y_jogador = pos_info['y']
        olhando_direita_inicial = pos_info['olhando_direita']

        self.jogador = Jogador(
            self.gerenciador_recursos,
            pos_x_jogador,
            pos_y_jogador,
            self.personagem,
            olhando_direita_inicial
        )

        self.obstaculos_caminho = pygame.sprite.Group()
        self.obstaculos_visao = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.areas_interacao = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()

        # --- Variáveis para rastrear áreas de interação ativas ---
        self.areas_interacao_colididas = [] # Lista das áreas de interação onde o jogador está colidindo

        self._carregar_entidades_dos_dados_do_mapa()



    def _definir_posicao_inicial_jogador(self):
        """
        Determina a posição inicial do jogador e a direção para onde ele está olhando.
        Prioriza um ponto de destino específico do mapa, depois coordenadas de fallback.
        Retorna um dicionário {'x': int, 'y': int, 'olhando_direita': bool}.
        """
        sala_atual = obter_dados_da_sala(self.id_mapa)
        if not sala_atual:
            print(f"ERRO: Dados para o mapa com ID '{self.id_mapa}' não encontrados. Usando posição padrão.")
            return {'x': 100, 'y': 400, 'olhando_direita': True} # Posição padrão segura

        # 1. Tenta usar o ponto de destino se fornecido
        if self.ponto_de_destino:
            pontos_de_entrada = sala_atual.get('pontos_de_entrada_no_mapa', {})
            entrada = pontos_de_entrada.get(self.ponto_de_destino)
            if entrada:
                return {
                    'x': entrada.get('x', 100),
                    'y': entrada.get('y', 400),
                    'olhando_direita': entrada.get('olhando_direita', True)
                }
            else:
                print(f"AVISO: Ponto de destino '{self.ponto_de_destino}' não encontrado no mapa '{self.id_mapa}'. Usando coordenadas de fallback ou padrão.")

        # 2. Se o ponto de destino não foi encontrado ou não foi fornecido, usa as coordenadas de fallback
        if self.coordenada_x is not None and self.coordenada_y is not None:
            return {
                'x': self.coordenada_x,
                'y': self.coordenada_y,
                'olhando_direita': self.olhando_direita if self.olhando_direita is not None else True
            }

        # 3. Se nenhuma opção acima, retorna o primeiro ponto de entrada do mapa
        primeiro_ponto = next(iter(sala_atual.get('pontos_de_entrada_no_mapa', {}).values()), None)
        if primeiro_ponto:
            return {
                'x': primeiro_ponto.get('x', 100),
                'y': primeiro_ponto.get('y', 400),
                'olhando_direita': primeiro_ponto.get('olhando_direita', True)
            }
        else:
            print('Nenhum ponto de entrada encontrado.')
            return {
                'x': 100,
                'y': 400,
                'olhando_direita': True
            }



    def _carregar_entidades_dos_dados_do_mapa(self):
        for obj_data in self.mapa_data['obstaculos']:
            obstaculo = Obstaculo(
                self.gerenciador_recursos,
                obj_data['x'], obj_data['y'],
                obj_data['largura'], obj_data['altura']
            )
            self.obstaculos_caminho.add(obstaculo)
            self.obstaculos_visao.add(obstaculo)

        for inimigo_data in self.mapa_data.get('inimigos', []):
            novo_inimigo = Inimigo(
                self.gerenciador_recursos,
                inimigo_data['x'], inimigo_data['y'],
                inimigo_data['tipo'],
                inimigo_data['velocidade_caminhada'],
                inimigo_data['velocidade_corrida'],
                inimigo_data['alcance_visao'],
                inimigo_data['angulo_visao_graus'],
                inimigo_data['tempo_reacao_ms'],
                alcance_ataque=inimigo_data.get('alcance_ataque', DISTANCIA_ATAQUE_INIMIGO),
                duracao_ataque_ms=inimigo_data.get('duracao_ataque_ms', DURACAO_ATAQUE_INIMIGO_MS)
            )
            self.inimigos.add(novo_inimigo)

        for area_data in self.mapa_data.get('areas_interacao', []):
            area = AreaInteracao(area_data['x'], area_data['y'],
                                 area_data['largura'], area_data['altura'],
                                 area_data['tipo_evento'], area_data['dados_evento'])
            self.areas_interacao.add(area)

    def _marcar_ilha_visitada_e_exibir_nome(self):
        """
        Marca a ilha atual como visitada e inicializa a exibição do nome da ilha e da área.
        """
        id_ilha_atual = get_ilha_por_mapa_id(self.id_mapa)
        
        nome_ilha = ""
        dados_da_ilha_atual = obter_dados_da_ilha(id_ilha_atual)
        if id_ilha_atual and dados_da_ilha_atual:
            nome_ilha = dados_da_ilha_atual['nome']
            # Marca a ilha como visitada
            dados_das_ilhas[id_ilha_atual]['visitada'] = True
            
        nome_area_atual = ""
        area_atual = obter_dados_da_sala(self.id_mapa)

        if area_atual and 'nome' in area_atual:
            nome_area_atual = area_atual['nome']
        else:
            print(f"AVISO: Nome da área não encontrado para o mapa ID: {self.id_mapa}")

        if nome_ilha or nome_area_atual: # Só cria a exibição se houver algo para mostrar
            self.exibicao_nome_ilha = _ExibicaoNomeIlha(nome_ilha, nome_area_atual, self.gerenciador_recursos)
            print(f"Exibindo Ilha: {nome_ilha}, Área: {nome_area_atual}")
            if id_ilha_atual:
                print(f"(Ilha {nome_ilha} visitada: {dados_da_ilha_atual['visitada']})")
        else:
            self.exibicao_nome_ilha = None
            print(f"AVISO: Nenhuma informação de ilha ou área para exibir para o mapa ID: {self.id_mapa}")


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
                    print(f"Viajando para: {ilha_selecionada}")

                    id_proxima_ilha = None
                    for ilha_id, dados_ilha in dados_das_ilhas.items():
                        if dados_ilha['nome'] == ilha_selecionada:
                            id_proxima_ilha = ilha_id
                            break

                    if id_proxima_ilha:
                        mapa_destino = None
                        if id_proxima_ilha in dados_das_ilhas and 'areas' in dados_das_ilhas[id_proxima_ilha]:
                            mapa_destino = dados_das_ilhas[id_proxima_ilha]['pier']

                        if mapa_destino:
                            self.menu_viagem_ativo = False
                            self.menu_viagem = None # Limpa a instância do menu
                            return {'estado': CHAVE_TRANSICAO_MAPA,
                                    'id_mapa': mapa_destino,
                                    'ponto_de_destino': 'pier',
                                    'personagem': self.personagem}
                        else:
                            print(f"AVISO: Não foi possível determinar o mapa de destino para a ilha '{ilha_selecionada}'.")
                    else:
                        print(f"AVISO: ID da ilha não encontrado para o nome '{ilha_selecionada}'.")
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
                    if area.tipo_evento == 'mudar_mapa':
                        print(f"Detectou interação para mudar mapa para {area.dados_evento.get('id_proximo_mapa')}")
                        return {'estado': CHAVE_TRANSICAO_MAPA, # Sempre volta para TelaJogo para outro mapa
                                'id_mapa': area.dados_evento['id_proximo_mapa'],
                                'ponto_de_destino': area.dados_evento['ponto_de_destino'],
                                'personagem': self.personagem} # Mantenha o tipo de personagem
                    elif area.tipo_evento == 'embarcar':
                        if not self.menu_viagem_ativo:
                            print('Embarcando na viagem...')
                            ilhas_destino_ids = get_ilhas_vizinhas(self.id_mapa)
                            print(f"Ilhas vizinhas encontradas: {ilhas_destino_ids} para o mapa '{self.id_mapa}'")
                            nomes_ilhas_destino = []
                            for ilha_id_vizinha in ilhas_destino_ids:
                                if ilha_id_vizinha in dados_das_ilhas:
                                    nomes_ilhas_destino.append(dados_das_ilhas[ilha_id_vizinha]['nome'])
                            print(f"Nomes das ilhas vizinhas: {nomes_ilhas_destino}")

                            if nomes_ilhas_destino:
                                self.menu_viagem = _MenuViagemFlutuante(nomes_ilhas_destino, self.gerenciador_recursos)
                                self.menu_viagem_ativo = True
                                print(f"Detectou interação para embarcar. Ilhas vizinhas: {nomes_ilhas_destino}")
                            return None # Consome o evento
                    
                    elif area.tipo_evento == 'iniciar_batalha':
                        print(f"Detectou interação para iniciar batalha com {area.dados_evento.get('inimigos')}")
                        return {'estado': CHAVE_TRANSICAO_BATALHA,
                                'inimigos': area.dados_evento['inimigos'], # Passe os inimigos da área
                                'jogador_x': self.jogador.mundo_x,
                                'jogador_y': self.jogador.mundo_y,
                                'olhando_direita': self.jogador.olhando_direita,
                                'id_mapa': self.id_mapa,
                                'personagem': self.personagem}
                    # Adicione outros tipos de interação aqui (ex: diálogo com NPC)
                    # elif area.tipo_evento == 'dialogo_npc':
                    #     return {'estado': CHAVE_TRANSICAO_DIALOGO, 'npc_id': area.dados_evento['npc_id']}

        return None # Nenhuma transição de tela por eventos de interação



    def update(self, dt):
        super().update(dt)

        # Atualiza o jogador (ele apenas tenta se mover, sem clamping ainda)
        self.jogador.update(dt, self.obstaculos_caminho)

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
        self.jogador.mostrar_icone_interacao = len(self.areas_interacao_colididas) > 0


        self.camera.update(self.jogador.rect)

        for inimigo in self.inimigos:
            inimigo.update(dt, self.jogador, self.obstaculos_caminho, self.obstaculos_visao)
            if inimigo.atingiu_jogador:
                print(f"Inimigo '{inimigo.tipo_inimigo}' acertou o jogador! Iniciando batalha...")
                # Sinaliza para o gerenciador de telas que uma batalha deve começar
                self.gerenciador_telas.mudar_tela(
                    CHAVE_TRANSICAO_BATALHA,
                    inimigo_batalha=inimigo.tipo_inimigo,
                    jogador_atual_x=self.jogador.mundo_x,
                    jogador_atual_y=self.jogador.mundo_y,
                    jogador_olhando_direita=self.jogador.olhando_direita,
                    mapa_atual_id=self.id_mapa,
                    personagem=self.personagem
                )
                return # Termina o update aqui para não processar mais nada após a transição
            
        # --- Atualiza a exibição do nome da ilha ---
        if self.exibicao_nome_ilha:
            self.exibicao_nome_ilha.update()

        return None



    def draw(self, tela):
        # Desenha a imagem de fundo
        tela.blit(self.mapa_fundo_imagem, (self.mapa_fundo_imagem.get_rect(topleft=(-self.camera.rect.x, -self.camera.rect.y))))
        
        # Desenha o jogador
        self.jogador.draw(tela, self.camera.rect.x, self.camera.rect.y)

        # Desenha os inimigos
        for inimigo in self.inimigos:
            inimigo.draw(tela, self.camera.rect.x)

        # --- Desenhar a camada superior (se existir) ---
        if self.camada_superior_imagem:
            tela.blit(self.camada_superior_imagem, (self.camada_superior_imagem.get_rect(topleft=(-self.camera.rect.x, -self.camera.rect.y))))

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
    def __init__(self, opcoes_viagem, gerenciador_recursos):
        self.opcoes = opcoes_viagem
        self.indice_selecionado = 0
        self.fonte_menu = pygame.font.Font(None, 36) # Ou gerenciador_recursos.obter_fonte(...)
        self.cor_texto_normal = (255, 255, 255) # Branco
        self.cor_texto_selecionado = (255, 255, 0) # Amarelo
        self.cor_fundo_menu = (50, 50, 50, 200) # Cinza escuro com transparência
        self.cor_borda_menu = (200, 200, 200) # Cinza claro

    def handle_input(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)
            elif evento.key == pygame.K_DOWN:
                self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)
            elif evento.key == pygame.K_RETURN:
                if self.opcoes:
                    return self.opcoes[self.indice_selecionado] # Retorna a opção selecionada
                return None # Nenhuma opção para selecionar
            elif evento.key == pygame.K_ESCAPE:
                return "cancelar" # Sinaliza para fechar o menu

        return None # Evento não tratado por este menu

    def draw(self, tela):
        if not self.opcoes: # Não desenha se não houver opções
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
            cor_texto = self.cor_texto_selecionado if i == self.indice_selecionado else self.cor_texto_normal
            texto_renderizado = self.fonte_menu.render(opcao, True, cor_texto)
            
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
