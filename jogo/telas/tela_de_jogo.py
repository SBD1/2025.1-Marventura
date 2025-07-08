# telas/tela_jogo.py

import pygame
from utilidades.constantes import *
from entidades import Inimigo
from entidades import Habitante
from entidades import Obstaculo
from entidades import Caminho
from entidades import AreaInteracao
from utilidades import Camera
from interface import CaixaDeDialogo
from .tela_modelo import TelaModelo
from gerenciadores import GerenciadorDeEntidades
import gerenciadores.gerenciador_missoes # Importa o módulo, não a classe diretamente

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

        # --- Atributos da Caixa de Diálogo ---
        self.caixa_dialogo = CaixaDeDialogo(self.gerenciador_recursos) # Garante que a caixa de diálogo seja sempre criada
        self.dialogos_atuais = []
        self.indice_dialogo_atual = 0
        self.dialogo_ativo = False
        
        # --- NOVO: Atributos para cena estática ---
        self.cena_estatica_ativa = False
        self.imagem_cena_estatica = None # Imagem da cena (tela cheia)

        # --- NOVO: Gerenciador de Missões ---
        # Passe referências importantes para o GerenciadorDeMissoes
        self.gerenciador_missoes = gerenciadores.gerenciador_missoes.GerenciadorDeMissoes(
            self.banco_de_dados,
            self.gerenciador_recursos,
            self.camera, # Passa a instância da câmera
            self.jogador,
            self.caixa_dialogo, # Passa a instância da caixa de diálogo
            self.npcs, # Passa o grupo de NPCs para interação
            self.gerenciador_telas, # Para transições de tela
            self
        )

        #self.gerenciador_missoes.iniciar_missao('mis001')
        # Exemplo de como iniciar um diálogo ao carregar a tela (opcional)
        # self.iniciar_dialogo(["Não com certeza. Mas ouvi histórias, quando era menor… Sobre uma região ao leste, onde a neblina nunca se dissipa. Chamam de Nublária, ou a névoa eterna. Antigamente era rota de fuga para desertores da Marinha, foragidos, estudiosos… Mas os navios pararam de voltar. Dizem que ela esconde uma ilha. Ou que engole quem ousa procurá-la. É um cemitério de navios.", "Espero que se divirta!"])
        
        # Exemplo: Tenta carregar uma missão ativa ao iniciar a tela de jogo
        # self.gerenciador_missoes.carregar_missao_ativa_se_existir(self.dados_do_progresso.identificador_progresso)



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
            area = AreaInteracao(area_data.identificador,
                                area_data.x, area_data.y,
                                area_data.largura, area_data.altura,
                                area_data.tipo_evento,
                                area_data.chance_sucesso,
                                area_data.area_destino,
                                area_data.chave_imagem,
                                gerenciador_recursos=self.gerenciador_recursos if area_data.chave_imagem else None)

            self.areas_interacao.add(area)

        # --- NOVO: Carregar NPCs ---
        dados_habitantes = self.banco_de_dados.buscar_habitante_por_area(id_area_atual)
        for habitante in dados_habitantes:
            dialogos = self.banco_de_dados.buscar_dialogos_sem_missao(habitante.identificador_habitante)
            novo_npc = Habitante(
                self.gerenciador_recursos,
                habitante.identificador_habitante,
                habitante.identificador_area,
                habitante.coordenada_x,
                habitante.coordenada_y,
                habitante.nome,
                habitante.descricao,
                habitante.tipo_habitante,
                habitante.moedas_totais,
                habitante.especialidade,
                habitante.chave_imagem,
                dialogos
            )
            self.npcs.add(novo_npc)



    def iniciar_dialogo(self, lista_de_textos):
        """Inicia uma sequência de diálogos."""
        self.dialogos_atuais = lista_de_textos
        self.indice_dialogo_atual = 0
        self.dialogo_ativo = True
        
        self.caixa_dialogo.definir_texto(self.dialogos_atuais[self.indice_dialogo_atual].dialogo, self.dialogos_atuais[self.indice_dialogo_atual].nome_personagem)
        

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


    def handle_input(self, evento):
        transicao_info = super().handle_input(evento)
        if transicao_info:
            return transicao_info
        
        # --- NOVO: Priorizar o gerenciador de missões/eventos para inputs ---
        # Se o gerenciador de missões estiver em um estado de "cutscene"
        # ou esperando um input específico que ele controla, ele deve ter prioridade.
        if self.gerenciador_missoes.esta_em_evento_controlado():
            self.gerenciador_missoes.handle_input(evento)
            return None # Consome o evento para evitar que o jogador se mova ou faça outra coisa
  
        
        # --- Lógica da Caixa de Diálogo (TEM PRIORIDADE SOBRE OUTROS INPUTS) ---
        if self.dialogo_ativo and self.caixa_dialogo:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if self.caixa_dialogo.esta_digitando:
                        self.caixa_dialogo.pular_digitacao()
                    elif self.caixa_dialogo.esta_finalizado():
                        self.indice_dialogo_atual += 1
                        if self.indice_dialogo_atual < len(self.dialogos_atuais):
                            self.caixa_dialogo.definir_texto(self.dialogos_atuais[self.indice_dialogo_atual].dialogo, self.dialogos_atuais[self.indice_dialogo_atual].nome_personagem)
                        else:
                            self.dialogo_ativo = False # Fim do diálogo
                            self.caixa_dialogo.limpar_dialogo() # Limpa o texto da caixa

            # NOVO: Tratamento do scroll do mouse
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if self.caixa_dialogo.aguardando_input and not self.caixa_dialogo.esta_digitando:
                    if evento.button == 4:  # Scroll para cima
                        self.caixa_dialogo.rolar(-1)
                    elif evento.button == 5: # Scroll para baixo
                        self.caixa_dialogo.rolar(1)
            return None # Consome o evento, o jogador não deve se mover enquanto o diálogo está ativo

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

                            self.banco_de_dados.atualizar_posicao_jogador(
                                self.gerenciador_entidades.jogador.identificador_jogador,
                                id_area,
                                informacoes_de_destino.ponto_geracao_x,
                                informacoes_de_destino.ponto_geracao_y,
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

                        self.banco_de_dados.atualizar_posicao_jogador(
                            self.gerenciador_entidades.jogador.identificador_jogador,
                            area.area_destino,
                            informacoes_de_destino.ponto_geracao_x,
                            informacoes_de_destino.ponto_geracao_y,
                        )

                        return {'estado': CHAVE_TRANSICAO_MAPA}
                    elif area.tipo_evento == 'embarcar':
                        if not self.menu_viagem_ativo:
                            print('Embarcando na viagem...')
                            self.ilhas_vizinhas = self.banco_de_dados.buscar_conexoes_ilha(self.dados_da_area.identificador_ilha, self.dados_do_progresso.identificador_progresso)

                            self.menu_viagem = _MenuViagemFlutuante(self.ilhas_vizinhas)
                            self.menu_viagem_ativo = True
                            return None # Consome o evento
                    
                    elif area.tipo_evento == 'iniciar_batalha':
                        print(f"Detectou interação para iniciar batalha com {area.dados_evento.get('inimigos')}")
                        return {'estado': CHAVE_TRANSICAO_BATALHA,
                                'inimigos': area.dados_evento['inimigos'], # Passe os inimigos da área
                                'jogador_x': self.jogador.mundo_x,
                                'jogador_y': self.jogador.mundo_y,
                                'olhando_direita': self.jogador.orientacao,
                                'id_mapa': self.dados_da_area.identificador_area,
                                'personagem': self.jogador.nome}
                    elif area.tipo_evento == 'investigar':
                        mensagem = self.banco_de_dados.tentar_coletar_item_no_mapa(self.jogador.identificador_jogador, area.identificador)
                        print(mensagem)
                    # Adicione outros tipos de interação aqui (ex: diálogo com NPC)
                    # elif area.tipo_evento == 'dialogo_npc':
                    #     return {'estado': CHAVE_TRANSICAO_DIALOGO, 'npc_id': area.dados_evento['npc_id']}

        return None # Nenhuma transição de tela por eventos de interação



    def update(self, dt):
        super().update(dt)
        dt_ms = dt * 1000 # Converte dt para milissegundos para a câmera e eventos

        # --- NOVO: Atualiza o Gerenciador de Missões PRIMEIRO ---
        # Se um evento de missão estiver ativo, ele pode controlar o jogador, a câmera, etc.
        self.gerenciador_missoes.update(dt_ms) # Passa dt em milissegundos

        # Se o gerenciador de missões estiver em um evento controlado OU CENA ESTÁTICA ATIVA, desativa o input do jogador
        if self.gerenciador_missoes.esta_em_evento_controlado() or self.cena_estatica_ativa: # CENA ESTÁTICA desabilita jogador
            self.jogador.movendo_esquerda = False
            self.jogador.movendo_direita = False
            self.jogador.movendo_cima = False
            self.jogador.movendo_baixo = False
        else:
            # Atualiza o jogador SOMENTE SE NÃO HOUVER UM EVENTO CONTROLANDO
            self.jogador.update(dt, self.obstaculos_caminho, self.caminhos)

            # Lógica de clamping do jogador para não sair dos limites do mundo (movimento normal)
            largura_mundo_atual = self.mapa_fundo_imagem.get_width()
            altura_mundo_atual = self.mapa_fundo_imagem.get_height()

            if self.jogador.rect.left < 0:
                self.jogador.rect.left = 0
            if self.jogador.rect.right > largura_mundo_atual:
                self.jogador.rect.right = largura_mundo_atual
            if self.jogador.rect.top < 0:
                self.jogador.rect.top = 0
            if self.jogador.rect.bottom > altura_mundo_atual:
                self.jogador.rect.bottom = altura_mundo_atual

            self.jogador.mundo_x = self.jogador.rect.x
            self.jogador.mundo_y = self.jogador.rect.y


        # Atualiza a visibilidade do ícone de interação
        self.areas_interacao_colididas = pygame.sprite.spritecollide(self.jogador, self.areas_interacao, False)
        self.jogador.mostrar_icone_interacao = len(self.areas_interacao_colididas) > 0

        # Atualiza os NPCs, passando a posição do jogador para a orientação
        for npc in self.npcs:
            npc.atualizar(dt, self.jogador.rect)

        self.camera.update(dt, self.jogador.rect)

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
                    jogador_olhando_direita=self.jogador.orientacao,
                    mapa_atual_id=self.dados_da_area.identificador_area,
                    personagem=self.jogador.nome
                )
                return # Termina o update aqui para não processar mais nada após a transição
            
        if self.exibicao_nome_ilha:
            self.exibicao_nome_ilha.update()
        
        # Se o diálogo for controlado pela TelaJogo (não pela missão), atualiza aqui
        if self.dialogo_ativo and self.caixa_dialogo and not self.gerenciador_missoes.dialogo_controlado_ativo:
            self.caixa_dialogo.atualizar()
        
        # Se o menu de viagem estiver ativo, ele tem prioridade no update
        if self.menu_viagem_ativo and self.menu_viagem:
            # Não faz nada aqui no update, pois ele é controlado por handle_input
            pass

        return None



    def draw(self, tela):
        # Desenha a imagem de fundo
        tela.blit(self.mapa_fundo_imagem, (self.mapa_fundo_imagem.get_rect(topleft=(-self.camera.rect.x, -self.camera.rect.y))))
        
        # --- NOVO: Desenha a cena estática SE estiver ativa ---
        if self.cena_estatica_ativa and self.imagem_cena_estatica:
            tela.blit(self.imagem_cena_estatica, (0, 0)) # Desenha a cena cobrindo toda a tela
        else: # Só desenha os elementos do jogo se a cena estática não estiver ativa
            # Desenha os NPCs
            for npc in self.npcs:
                npc.desenhar(tela, self.camera.rect.x, self.camera.rect.y) # NOVO: Desenha NPCs

            for area in self.areas_interacao:
                area.desenhar(tela, self.camera.rect.x)

            # Desenha o jogador
            self.jogador.draw(tela, self.camera.rect.x, self.camera.rect.y)

            # Desenha os inimigos
            for inimigo in self.inimigos:
                inimigo.draw(tela, self.camera.rect.x)

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

                # DEBUG para NPCs
                for npc in self.npcs:
                    debug_rect_npc = pygame.Rect(
                        npc.rect.x - self.camera.rect.x,
                        npc.rect.y - self.camera.rect.y,
                        npc.rect.width,
                        npc.rect.height
                    )
                    pygame.draw.rect(tela, VERDE, debug_rect_npc, 1) # Cor verde para NPCs


            # --- Desenha o nome da ilha com fade ---
            if self.exibicao_nome_ilha:
                self.exibicao_nome_ilha.draw(tela)
            
            # --- Desenha o menu de viagem se estiver ativo ---
            if self.menu_viagem_ativo and self.menu_viagem:
                self.menu_viagem.draw(tela)

            # --- Desenha a caixa de diálogo se estiver ativa ---
            if self.dialogo_ativo and self.caixa_dialogo:
                self.caixa_dialogo.desenhar(tela)

        # NOVO: Se o gerenciador de missões estiver ativo e tiver um diálogo para exibir, ele desenha
        if self.gerenciador_missoes.dialogo_controlado_ativo and self.gerenciador_missoes.caixa_dialogo:
             self.gerenciador_missoes.caixa_dialogo.desenhar(tela)

    

    # --- NOVOS MÉTODOS PARA CENA ESTÁTICA ---
    def ativar_cena_estatica(self, chave_imagem):
        """Ativa a exibição de uma imagem de cena estática (tela cheia)."""
        self.imagem_cena_estatica = self.gerenciador_recursos.obter_imagem(chave_imagem)
        if self.imagem_cena_estatica:
            # Redimensiona a imagem para caber na tela se necessário
            self.imagem_cena_estatica = pygame.transform.scale(self.imagem_cena_estatica, (LARGURA_TELA, ALTURA_TELA))
            self.cena_estatica_ativa = True
            print(f"Cena estática '{chave_imagem}' ativada.")
        else:
            self.cena_estatica_ativa = False
            print(f"AVISO: Imagem da cena estática '{chave_imagem}' não encontrada.")



    def desativar_cena_estatica(self):
        """Desativa a exibição da imagem de cena estática."""
        self.cena_estatica_ativa = False
        self.imagem_cena_estatica = None
        print("Cena estática desativada.")




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
