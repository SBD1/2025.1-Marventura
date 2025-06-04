# telas/tela_jogo.py

import pygame
import sys
from utilidades.constantes import *
from entidades import Jogador
from entidades import Inimigo
from entidades import Obstaculo
from entidades import AreaInteracao
from utilidades import Camera
from mapa_dados import mapas_data
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
    def __init__(self, gerenciador_telas, gerenciador_recursos, id_mapa_atual, personagem, ponto_de_destino, coordenada_x = None, coordenada_y = None, olhando_direita = None):
        super().__init__(gerenciador_telas, gerenciador_recursos) # Chama o construtor da TelaModelo

        self.id_mapa = id_mapa_atual
        self.personagem = personagem
        self.ponto_de_destino = ponto_de_destino
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y
        self.olhando_direita = olhando_direita

        self.mapa_data = mapas_data[self.id_mapa]

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
        map_data = mapas_data.get(self.id_mapa)
        if not map_data:
            print(f"ERRO: Dados para o mapa com ID '{self.id_mapa}' não encontrados. Usando posição padrão.")
            return {'x': 100, 'y': 400, 'olhando_direita': True} # Posição padrão segura

        # 1. Tenta usar o ponto de destino se fornecido
        if self.ponto_de_destino:
            pontos_de_entrada = map_data.get('pontos_de_entrada_no_mapa', {})
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

        # 3. Se nenhuma opção acima, retorna uma posição padrão
        print(f"AVISO: Nenhuma posição inicial específica fornecida para o mapa '{self.id_mapa}'. Usando posição padrão.")
        return {'x': 100, 'y': 400, 'olhando_direita': True}


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


    def handle_input(self, evento):
        transicao_info = super().handle_input(evento)
        if transicao_info:
            return transicao_info

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
