# telas/tela_jogo.py

import pygame
from utilidades.constantes import *
from entidades.item_inventario import ItemInventario
from entidades import Inimigo
from entidades import Chefe
from entidades import Habitante
from entidades import Obstaculo
from entidades import Caminho
from entidades import AreaInteracao
from entidades.habilidades import Habilidade
from utilidades import Camera
from componentes import CaixaDeDialogo
from .tela_modelo import TelaModelo
from telas.tela_inventario import TelaInventario
from telas.tela_cozinha import TelaCozinha
from telas.tela_mapa import Mapa
from gerenciadores import GerenciadorDeEntidades
from gerenciadores import GerenciadorNotificacoesItem
from componentes import BarraDeEstado
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import DBManager
    from gerenciadores import GerenciadorDeRecursos
    from gerenciadores import GerenciadorDeTelas
    from gerenciadores import GerenciadorDeMissoes

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
    def __init__(self, gerenciador_telas: 'GerenciadorDeTelas', gerenciador_recursos: 'GerenciadorDeRecursos', gerenciador_banco_de_dados: 'DBManager', gerenciador_missoes: 'GerenciadorDeMissoes'):
        super().__init__(gerenciador_telas, gerenciador_recursos) # Chama o construtor da TelaModelo
        self.gerenciador_entidades = GerenciadorDeEntidades()
        self.gerenciador_recursos = gerenciador_recursos

        self.dados_da_area = self.gerenciador_entidades.area_atual
        self.dados_da_ilha = self.gerenciador_entidades.ilha_atual
        self.dados_do_progresso = self.gerenciador_entidades.progresso_do_jogo
        self.banco_de_dados = gerenciador_banco_de_dados

        # --- Atributos para o menu de viagem ---
        self.menu_mapa = None
        self.menu_mapa_ativo = False
        self.menu_inventario = None
        self.menu_inventario_ativo = False
        self.menu_cozinha = None
        self.menu_cozinha_ativo = False
        self.menu_pausa = None
        self.menu_pausa_ativo = False

        self.barra_de_estado = BarraDeEstado(gerenciador_recursos, self.gerenciador_entidades.jogador)
        self.tempo_ocioso = 0  # Tempo que o jogador está ocioso
        self.limite_ocioso = 5  # Tempo limite em segundos para exibir a barra de estado
        self.barra_de_estado_visivel = False  # Controla a visibilidade da barra de estado
        self.posicao_anterior_jogador = self.gerenciador_entidades.jogador.rect.topleft

        # --- Atributo para exibição do nome da ilha ---
        self.exibicao_nome_ilha = None

        self._marcar_ilha_visitada_e_exibir_nome()

        self.mapa_fundo_imagem = self.gerenciador_recursos.obter_imagem(self.dados_da_area.chave_imagem_fundo)

        if not self.mapa_fundo_imagem:
            print(f"ERRO: Imagem de fundo '{self.dados_da_area.chave_imagem_fundo}' não encontrada.")
            self.mapa_fundo_imagem = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
            self.mapa_fundo_imagem.fill(CINZA)  # Cor de fallback

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

        self.chefe = None  # Inicializa como None, será definido se houver um chefe

        # Inicialize TODOS os seus grupos de sprites aqui
        self.todos_os_sprites = pygame.sprite.Group() # <-- LINHA ADICIONADA
        self.obstaculos_caminho: pygame.sprite.Group['Obstaculo'] = pygame.sprite.Group()
        self.obstaculos_visao: pygame.sprite.Group['Obstaculo'] = pygame.sprite.Group()
        self.inimigos: pygame.sprite.Group['Inimigo'] = pygame.sprite.Group()
        self.areas_interacao: pygame.sprite.Group['AreaInteracao'] = pygame.sprite.Group()
        self.areas_interacao_missao: pygame.sprite.Group['AreaInteracao'] = pygame.sprite.Group()
        self.npcs: pygame.sprite.Group['Habitante'] = pygame.sprite.Group()
        
        # Adicione o jogador ao grupo de todos os sprites para facilitar a renderização
        self.todos_os_sprites.add(self.jogador)
        
        self.areas_interacao_colididas = []
        self.caminhos: list['Caminho'] = []

        self._carregar_entidades_dos_dados_do_mapa()

        self.efeitos_visuais = []
        self.sprites_efeito_ataque = [
            pygame.image.load(f"recursos/efeitos/slash_{i}.png").convert_alpha()
            for i in range(5)
        ]
        # print("Sprites de ataque carregadas:", len(self.sprites_efeito_ataque))
        # --- Atributos da Caixa de Diálogo ---
        self.caixa_dialogo = CaixaDeDialogo(self.gerenciador_recursos) # Garante que a caixa de diálogo seja sempre criada
        self.dialogos_atuais = []
        self.indice_dialogo_atual = 0
        self.dialogo_ativo = False
        
        # --- NOVO: Atributos para cena estática ---
        self.cena_estatica_ativa = False
        self.imagem_cena_estatica = None # Imagem da cena (tela cheia)

        # --- NOVO: Gerenciador de Missões ---
        self.gerenciador_missoes = gerenciador_missoes
        self.gerenciador_missoes.vincular_nova_tela_jogo(self)  # Vincula a tela de jogo ao gerenciador de missões
        self.gerenciador_entidades.jogador.gerenciador_missoes = self.gerenciador_missoes
        fonte_notificacoes = self.gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_TEXTO)
        self.notificador = GerenciadorNotificacoesItem(fonte_notificacoes, posicao_base=(LARGURA_TELA - 20, 20))

        self.gerenciador_missoes.notificar_mudanca_de_area(self.dados_da_area.identificador_area)



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
                caminho_arena = caminho
            self.caminhos.append(caminho)
        
        if not caminho_arena:
            print("AVISO: Nenhum caminho do tipo 'arena' foi encontrado no mapa. Os inimigos não serão carregados.")
        else:
            inimigos = self.banco_de_dados.buscar_lacaios_por_area(self.dados_do_progresso.identificador_progresso, id_area_atual)
            
            # Carrega os inimigos, agora passando o caminho da arena
            for dado_do_inimigo in inimigos:
                #print(f"[DEBUG] Carregando inimigo: {dado_do_inimigo.nome_lacaio} ({dado_do_inimigo.identificador_instancia_lacaio})")
                habilidades = self.banco_de_dados.buscar_habilidades_por_personagem(dado_do_inimigo.identificador_lacaio)
                itens = self.banco_de_dados.buscar_inventario(dado_do_inimigo.identificador_instancia_lacaio, 'moc', self.dados_do_progresso.identificador_progresso)
                #print(f"[DEBUG] Habilidades encontradas para o inimigo {dado_do_inimigo.nome_lacaio}: {habilidades}")
                habilidades_obj = [
                    Habilidade(
                        id=h.identificador_habilidade,
                        nome=h.nome,
                        descricao=h.descricao,
                        tipo_de_ataque=h.tipo_de_ataque,
                        tipo_de_alvo=h.tipo_de_alvo,
                        dano=h.dano,
                        custo=h.custo,
                        efeito=(
                            {"nome": h.efeito_nome, "valor": h.efeito_valor}
                            if h.efeito_nome else None
                        )
                    )
                    for h in habilidades
                ]
                print(f"[DEBUG] Habilidades_obj encontradas para o inimigo {dado_do_inimigo.nome_lacaio}: {habilidades_obj}")

                novo_inimigo = Inimigo(
                    self.gerenciador_recursos,
                    dado_do_inimigo.x, dado_do_inimigo.y,
                    self.dados_da_area.identificador_area,
                    dado_do_inimigo.identificador_lacaio,
                    dado_do_inimigo.identificador_instancia_lacaio,
                    dado_do_inimigo.nome_lacaio,
                    dado_do_inimigo.descricao_lacaio,
                    dado_do_inimigo.vida_atual,
                    dado_do_inimigo.vida_total,
                    dado_do_inimigo.nivel,
                    dado_do_inimigo.experiencia,
                    habilidade=habilidades_obj,
                    inventario=itens,
                    caminho_container=caminho_arena, # Passa o caminho encontrado
                )
                self.inimigos.add(novo_inimigo)
                if hasattr(self, 'todos_os_sprites'):
                    self.todos_os_sprites.add(novo_inimigo)

        chefe = self.banco_de_dados.buscar_chefe_por_area(id_area_atual, self.dados_do_progresso.identificador_progresso)

        if chefe:
            habilidades = self.banco_de_dados.buscar_habilidades_por_personagem(chefe.identificador_chefe)
            itens = self.banco_de_dados.buscar_inventario(chefe.identificador_chefe, 'moc', self.dados_do_progresso.identificador_progresso)
            habilidades_obj = [
                Habilidade(
                    id=h.identificador_habilidade,
                    nome=h.nome,
                    descricao=h.descricao,
                    tipo_de_ataque=h.tipo_de_ataque,
                    tipo_de_alvo=h.tipo_de_alvo,
                    dano=h.dano,
                    custo=h.custo,
                    efeito=(
                        {"nome": h.efeito_nome, "valor": h.efeito_valor}
                        if h.efeito_nome else None
                    )
                )
                for h in habilidades
            ]
            novo_chefe = Chefe(
                self.gerenciador_recursos,
                chefe.identificador_chefe,
                self.dados_da_area.identificador_area,
                chefe.coordenada_x, chefe.coordenada_y,
                chefe.nome,
                chefe.descricao,
                chefe.vida_total,
                chefe.vida_atual,
                chefe.nivel,
                chefe.experiencia,
                habilidades_obj,
                itens,
            )
            self.chefe = novo_chefe
            self.todos_os_sprites.add(novo_chefe)

        areas_interativas = self.banco_de_dados.buscar_areas_interativas_da_area(id_area_atual, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)
        for area_data in areas_interativas:
            # Inicializa a área como None para garantir que ela seja criada dentro de um if
            area = None
            
            if area_data.tipo_evento == 'mudar_area':
                area = AreaInteracao(
                    identificador=area_data.identificador,
                    x=area_data.x, y=area_data.y,
                    largura=area_data.largura, altura=area_data.altura,
                    tipo_evento=area_data.tipo_evento,
                    metodo_ativacao=area_data.metodo_ativacao,
                    ativa=area_data.ativa,
                    area_destino=area_data.area_destino
                )
            
            elif area_data.tipo_evento == 'embarcar':
                area = AreaInteracao(
                    identificador=area_data.identificador,
                    x=area_data.x, y=area_data.y,
                    largura=area_data.largura, altura=area_data.altura,
                    tipo_evento=area_data.tipo_evento,
                    metodo_ativacao=area_data.metodo_ativacao,
                    ativa=area_data.ativa,
                    area_destino=area_data.area_destino
                )
            
            elif area_data.tipo_evento == 'investigar':
                area = AreaInteracao(
                    identificador=area_data.identificador,
                    x=area_data.x, y=area_data.y,
                    largura=area_data.largura, altura=area_data.altura,
                    tipo_evento=area_data.tipo_evento,
                    chance_sucesso=area_data.chance_sucesso,
                    metodo_ativacao=area_data.metodo_ativacao,
                    ativa=area_data.ativa,
                    chave_imagem=area_data.chave_imagem,
                    gererenciador_recursos=self.gerenciador_recursos
                )

            elif area_data.tipo_evento == 'missao':
                area = AreaInteracao(
                    identificador=area_data.identificador,
                    x=area_data.x, y=area_data.y,
                    largura=area_data.largura, altura=area_data.altura,
                    tipo_evento=area_data.tipo_evento,
                    metodo_ativacao=area_data.metodo_ativacao,
                    ativa=area_data.ativa,
                    identificador_missao=area_data.identificador_missao,
                    chave_imagem=area_data.chave_imagem,
                    gererenciador_recursos=self.gerenciador_recursos if area_data.chave_imagem else None
                )

            elif area_data.tipo_evento == 'abrir_loja':
                # Para uma loja, não precisamos de dados extras do evento,
                # apenas saber que este é o tipo.
                # A lógica para encontrar o vendedor será feita no handle_input.
                area = AreaInteracao(identificador=area_data.identificador,
                                     x=area_data.x, y=area_data.y,
                                     largura=area_data.largura, altura=area_data.altura,
                                     tipo_evento=area_data.tipo_evento,
                                     chave_imagem=area_data.chave_imagem,
                                     gererenciador_recursos=self.gerenciador_recursos,
                                     metodo_ativacao=area_data.metodo_ativacao,
                                     ativa=area_data.ativa)
            
            # Adiciona a área criada ao grupo de sprites
            if area:
                if area_data.tipo_evento == 'missao':
                    self.areas_interacao_missao.add(area)
                else:
                    self.areas_interacao.add(area)

        # --- NOVO: Carregar NPCs ---
        dados_habitantes = self.banco_de_dados.buscar_habitante_por_area(id_area_atual, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)
        for habitante in dados_habitantes:
            genero = 'F' if self.gerenciador_entidades.jogador.nome == SILVIE else 'M'
            dialogos = self.banco_de_dados.buscar_dialogos_sem_missao(habitante.identificador_habitante, genero)

            # Filtra a saudação
            saudacao = list(filter(lambda d: d.sequencia_local < 10, dialogos))

            # Agora sobrescreve dialogos com apenas as missões
            dialogos = list(filter(lambda d: d.sequencia_local >= 10, dialogos))

            missoes = []

            if habitante.tipo_habitante == 'rct':
                missoes = self.banco_de_dados.buscar_missoes_de_habitante_nao_concluidas(habitante.identificador_habitante, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

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
                saudacao,
                dialogos,
                missoes,
                habitante.conhecido
            )
            self.npcs.add(novo_npc)
            self.todos_os_sprites.add(novo_npc)  # Adiciona o NPC ao grupo de todos os sprites



    def atualizar_areas_interativas_de_missao(self):
        id_area_atual = self.dados_da_area.identificador_area
        areas_interativas = self.banco_de_dados.buscar_areas_interativas_da_area(id_area_atual, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

        self.areas_interacao_missao.empty()

        for area_data in areas_interativas:
            if area_data.tipo_evento == 'missao':
                print("Atualizar area interativa de missão:", area_data, '\n')
                area = AreaInteracao(
                    identificador=area_data.identificador,
                    x=area_data.x, y=area_data.y,
                    largura=area_data.largura, altura=area_data.altura,
                    tipo_evento=area_data.tipo_evento,
                    metodo_ativacao=area_data.metodo_ativacao,
                    ativa=area_data.ativa,
                    chave_imagem=area_data.chave_imagem,
                    identificador_missao=area_data.identificador_missao,
                    gererenciador_recursos=self.gerenciador_recursos if area_data.chave_imagem else None
                )
                
                self.areas_interacao_missao.add(area)



    def iniciar_dialogo(self, lista_de_textos):
        """Inicia uma sequência de diálogos."""
        self.dialogos_atuais = lista_de_textos
        self.indice_dialogo_atual = 0
        self.dialogo_ativo = True
        
        self.caixa_dialogo.definir_texto(self.dialogos_atuais[self.indice_dialogo_atual].fala, self.dialogos_atuais[self.indice_dialogo_atual].nome_personagem)



    def adicionar_inimigo_em_missao(self, nome_inimigo, id_instancia, x, y):
        """
        Cria e adiciona um inimigo específico para uma missão.
        Diferente do carregamento normal do mapa.
        """
        print(f"Adicionando inimigo de missão: {nome_inimigo} em ({x}, {y})")
        # Você precisará buscar os dados base do inimigo (vida, nível etc.) do DB
        # Aqui, vamos usar valores de exemplo.
        dados_base_inimigo = self.banco_de_dados.buscar_lacaio_por_nome_com_habilidades(nome_inimigo)[0] # Supondo que você tenha essa função

        habilidade = [
            Habilidade(
                id=dados_base_inimigo.identificador_habilidade,
                nome=dados_base_inimigo.nome_habilidade,
                descricao=dados_base_inimigo.descricao_habilidade,
                tipo_de_ataque=dados_base_inimigo.tipo_de_ataque,
                tipo_de_alvo=dados_base_inimigo.tipo_de_alvo,
                dano=dados_base_inimigo.dano,
                efeito=(
                    {"nome": dados_base_inimigo.nome_efeito, "valor": dados_base_inimigo.valor_efeito}
                    if dados_base_inimigo.nome_efeito else None
                )
            )
        ]

        novo_inimigo = Inimigo(
            gerenciador_recursos=self.gerenciador_recursos,
            coordenada_x=x,
            coordenada_y=y,
            area=self.dados_da_area.identificador_area,
            id_inimigo=dados_base_inimigo.identificador_lacaio,
            identificador_instancia_lacaio=id_instancia,
            nome=dados_base_inimigo.nome_lacaio, # ou a chave_inimigo
            descricao=dados_base_inimigo.descricao,
            vida_atual=dados_base_inimigo.vida,
            vida_total=dados_base_inimigo.vida,
            nivel=dados_base_inimigo.nivel,
            experiencia=dados_base_inimigo.experiencia,
            habilidade=habilidade,
            inventario=[], # Busque se necessário
            caminho_container=None
        )
        # Adiciona um identificador único para podermos encontrá-lo depois

        self.inimigos.add(novo_inimigo)
        self.todos_os_sprites.add(novo_inimigo)  # Adiciona o novo inimigo ao grupo de todos os sprites



    def definir_coordenada_de_habitante_especifico(self, nome_habitante, nova_coordenada_x, nova_coordenada_y):
        """
        Define a coordenada de um Habitante pelo nome dentro do grupo de NPCs.
        """
        for npc in self.npcs:
            if npc.nome == nome_habitante:
                npc.coordenada_x = nova_coordenada_x
                npc.coordenada_y = nova_coordenada_y
                npc.rect.x = int(nova_coordenada_x)  # Atualiza a posição do rect também
                npc.rect.y = int(nova_coordenada_y)
                # print(f"Coordenadas do habitante '{nome_habitante}' atualizadas para ({nova_coordenada_x}, {nova_coordenada_y}).")
                return  # Encontrou e atualizou, pode sair da função

        print(f"AVISO: Habitante com o nome '{nome_habitante}' não encontrado.")



    def inserir_habitante_em_missao(self, identificador_habitante, x, y):
        """
        Cria e adiciona um habitante específico para uma missão.
        Diferente do carregamento normal do mapa.
        """
        print(f"Adicionando habitante de missão: {identificador_habitante} em ({x}, {y})")
        dados_habitante = self.banco_de_dados.buscar_habitante(identificador_habitante, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)
        if not dados_habitante:
            print(f"ERRO: Habitante com o ID '{identificador_habitante}' não encontrado no banco de dados.")
            return

        genero = 'F' if self.gerenciador_entidades.jogador.nome == SILVIE else 'M'
        dialogos = self.banco_de_dados.buscar_dialogos_sem_missao(dados_habitante.identificador_habitante, genero)

        # Filtra a saudação
        saudacao = list(filter(lambda d: d.sequencia_local < 10, dialogos))

        # Agora sobrescreve dialogos com apenas as missões
        dialogos = list(filter(lambda d: d.sequencia_local >= 10, dialogos))

        missoes = []

        if dados_habitante.tipo_habitante == 'rct':
            missoes = self.banco_de_dados.buscar_missoes_de_habitante_nao_concluidas(dados_habitante.identificador_habitante, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

        novo_npc = Habitante(
            self.gerenciador_recursos,
            dados_habitante.identificador_habitante,
            self.dados_da_area.identificador_area,
            x,
            y,
            dados_habitante.nome,
            dados_habitante.descricao,
            dados_habitante.tipo_habitante,
            dados_habitante.moedas_totais,
            dados_habitante.especialidade,
            dados_habitante.chave_imagem,
            saudacao,
            dialogos,
            missoes,
            conhecido=dados_habitante.conhecido
        )
        self.npcs.add(novo_npc)
        self.todos_os_sprites.add(novo_npc)  # Adiciona o NPC ao grupo de todos os sprites



    def _marcar_ilha_visitada_e_exibir_nome(self):
        """
        Marca a ilha atual como visitada e inicializa a exibição do nome da ilha e da área.
        """
        if not self.dados_da_ilha.visitada:
            self.banco_de_dados.marcar_ilha_como_visitada(self.dados_da_ilha.identificador_ilha, self.dados_do_progresso.identificador_progresso)
            self.dados_da_ilha = self.banco_de_dados.buscar_info_ilha(self.dados_da_ilha.identificador_ilha, self.dados_do_progresso.identificador_progresso)

        if self.dados_da_ilha.nome or self.dados_da_area.nome: # Só cria a exibição se houver algo para mostrar
            self.exibicao_nome_ilha = _ExibicaoNomeIlha(self.dados_da_ilha.nome, self.dados_da_area.nome, self.gerenciador_recursos)
        else:
            self.exibicao_nome_ilha = None
            print(f"AVISO: Nenhuma informação de ilha ou área para exibir para o mapa ID: {self.dados_da_area.identificador_area}")



    def _detectar_inimigos_acertados(self) -> list['Inimigo']:
        """Verifica quais inimigos foram atingidos pelo ataque do jogador."""
        atingidos = []

        # Define a área de ataque (você pode ter isso em outro lugar)
        area_ataque = self.jogador.get_area_de_ataque()  # Ex: um retângulo na frente

        for inimigo in self.inimigos:
            if inimigo.rect.colliderect(area_ataque):
                #print(f"[DEBUG] Inimigo {inimigo.tipo} atingido!")
                atingidos.append(inimigo)

        return atingidos



    def _ataque_no_mapa(self):
        print("[DEBUG] Jogador atacou no mapa!")
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

        # Pega inimigos atingidos
        inimigos_acertados = self._detectar_inimigos_acertados()

        if inimigos_acertados:
            print("Ataque no mapa acertou inimigo!")

            # Pega todos os inimigos da área (visão ou perseguição)
            inimigos_reagindo = [
                inimigo for inimigo in self.inimigos
                if inimigo.estado in (ESTADO_INIMIGO_ALERTA, ESTADO_INIMIGO_PERSEGUINDO)
            ]

            # Junta os dois sem repetir
            inimigos_para_batalha = list({i for i in inimigos_acertados + inimigos_reagindo})

            self.gerenciador_telas.mudar_tela(
                CHAVE_TRANSICAO_BATALHA,
                inimigos_na_batalha = inimigos_para_batalha,
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



    def processar_eventos(self, evento):
        transicao_info = super().processar_eventos(evento)
        if transicao_info:
            return transicao_info
        
        # --- NOVO: Priorizar o gerenciador de missões/eventos para inputs ---
        # Se o gerenciador de missões estiver em um estado de "cutscene"
        # ou esperando um input específico que ele controla, ele deve ter prioridade.
        if self.gerenciador_missoes.esta_em_evento_controlado():
            self.gerenciador_missoes.processar_eventos(evento)
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
                            self.caixa_dialogo.definir_texto(self.dialogos_atuais[self.indice_dialogo_atual].fala, self.dialogos_atuais[self.indice_dialogo_atual].nome_personagem)
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
        
        if self.menu_pausa_ativo and self.menu_pausa:
            resultado = self.menu_pausa.processar_eventos(evento)
            if resultado:
                if resultado == "continuar":
                    self.menu_pausa_ativo = False
                    self.menu_pausa = None
                elif resultado == "sair":
                    # Supondo que CHAVE_TRANSICAO_MENU_PRINCIPAL te leve para o menu principal
                    return {'estado': CHAVE_TRANSICAO_MENU_PRINCIPAL}
                elif resultado == "enciclopédia":
                    # Crie esta chave em suas constantes se ainda não existir
                    # return {'estado': CHAVE_TRANSICAO_ENCICLOPEDIA}
                    print("INFO: Transição para Enciclopédia ainda não implementada.")
                    # Por enquanto, apenas fechamos o menu
                    self.menu_pausa_ativo = False
                    self.menu_pausa = None

            return None # Consome o evento para não fazer mais nada


        if self.menu_inventario_ativo and self.menu_inventario:
            self.menu_inventario.processar_eventos(evento)
            return None

        if self.menu_cozinha_ativo and self.menu_cozinha:
            self.menu_cozinha.processar_eventos(evento)
            return None # Consome o evento, não processa o input do jogador normal

        # --- Lógica do Menu de Viagem (se estiver ativo) ---
        if self.menu_mapa_ativo and self.menu_mapa:
            resultado_menu = self.menu_mapa.processar_eventos(evento)
            if resultado_menu is not None:
                if resultado_menu == "cancelar":
                    self.menu_mapa_ativo = False
                    self.menu_mapa = None # Limpa a instância do menu
                    return None # Consome o evento
                else: # Uma ilha foi selecionada
                    ilha_selecionada = resultado_menu
                    print(f"Viajando para: {ilha_selecionada.identificador_ilha}")

                    if ilha_selecionada:
                        porto_destino = self.banco_de_dados.buscar_porto_da_ilha(ilha_selecionada.identificador_ilha, self.dados_do_progresso.identificador_progresso)
                        print(f"porto_destino: {porto_destino}")
                        if porto_destino:
                            self.menu_mapa_ativo = False
                            self.menu_mapa = None
                            
                            id_area_destino = porto_destino.identificador_area

                            # 1. Prepara os Gerenciadores para o estado *após* a viagem
                            self.gerenciador_entidades.ilha_atual = ilha_selecionada
                            self.gerenciador_entidades.area_atual = porto_destino
                            
                            informacoes_de_destino = self.banco_de_dados.buscar_conexao_entre_areas(self.dados_da_area.identificador_area, id_area_destino)
                            
                            self.gerenciador_entidades.ponto_de_renascimento = (
                                informacoes_de_destino.ponto_geracao_x,
                                informacoes_de_destino.ponto_geracao_y
                            )
                            
                            # 2. Define os dados para a transição final (depois da animação)
                            dados_para_tela_final = {
                                'coordenada_x': informacoes_de_destino.ponto_geracao_x,
                                'coordenada_y': informacoes_de_destino.ponto_geracao_y,
                                'orientacao': informacoes_de_destino.orientacao,
                            }

                            # 3. Inicia a tela de transição, passando os dados do destino final
                            return {
                                'estado': CHAVE_TRANSICAO_VIAGEM,
                                'dados_destino': dados_para_tela_final
                            }
                        else:
                            print(f"AVISO: Não foi possível determinar o mapa de destino para a ilha '{ilha_selecionada.nome}'.")
                    else:
                        print(f"AVISO: ID da ilha não encontrado para o nome '{ilha_selecionada.nome}'.")
            return None # Consome o evento, não processa o input do jogador normal

        # --- Lógica de Interação com Áreas de Interação (Eventos KEYDOWN) ---
        # SOMENTE reage a um evento KEYDOWN, não ao estado contínuo da tecla.
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e:
                areas_colidindo_agora: list[AreaInteracao] = pygame.sprite.spritecollide(self.jogador, self.areas_interacao, False)
                
                if not areas_colidindo_agora:
                    print("DEBUG: Tecla 'E' pressionada, mas o jogador NÃO está colidindo com uma área de interação.")
                else:
                    # Se houver colisão, vamos inspecionar cada área
                    for area in areas_colidindo_agora:
                        # ESTA É A LINHA MAIS IMPORTANTE PARA A DEPURAÇÃO:
                        print(f"DEBUG: Interagindo com uma área. O tipo do evento é: '{area.tipo_evento}'")

                        # O código abaixo só será executado se o print acima mostrar 'mudar_area'
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
                                self.gerenciador_entidades.jogador.identificador,
                                area.area_destino,
                                informacoes_de_destino.ponto_geracao_x,
                                informacoes_de_destino.ponto_geracao_y,
                            )

                            self.gerenciador_entidades.ponto_de_renascimento = (
                                informacoes_de_destino.ponto_geracao_x,
                                informacoes_de_destino.ponto_geracao_y
                            )

                            return {'estado': CHAVE_TRANSICAO_MAPA}
                        
                        elif area.tipo_evento == 'abrir_loja':
                            vendedores = self.banco_de_dados.buscar_vendedor_por_area(self.dados_da_area.identificador_area, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)
                            if vendedores:
                                vendedor = vendedores[0]  # Assume o primeiro vendedor da área
                                return {
                                    'estado': CHAVE_TRANSICAO_LOJA,
                                    'vendedor_id': vendedor.identificador_habitante,
                                    'nome_vendedor': vendedor.nome.strip(),
                                }
                            
                        elif area.tipo_evento == 'embarcar':
                            if not self.menu_mapa_ativo:
                                print('Embarcando na viagem...')
                                self.ilhas_vizinhas = self.banco_de_dados.buscar_conexoes_ilha(self.dados_da_area.identificador_ilha, self.dados_do_progresso.identificador_progresso)

                                self.menu_mapa = Mapa(self.gerenciador_telas, self.gerenciador_recursos, self.banco_de_dados, self.gerenciador_entidades, modo='Navegar', opcoes_destino=self.ilhas_vizinhas)
                                self.menu_mapa_ativo = True
                                return None # Consome o evento
                        
                        
                        elif area.tipo_evento == 'investigar' and not area.animando:
                            area.iniciar_animacao_chacoalhar()
                            resultado = self.banco_de_dados.tentar_coletar_item_no_mapa(self.jogador.identificador, area.identificador, self.notificador)
                            if resultado['sucesso']:
                                self.gerenciador_entidades.jogador.mochila = self.banco_de_dados.carregar_mochila_do_jogador(self.gerenciador_entidades.jogador.identificador, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

                                self.gerenciador_entidades.jogador.experiencia_atual += 3
                                self.banco_de_dados.atualizar_atributos_de_batalha_do_jogador(
                                    self.gerenciador_entidades.jogador.identificador,
                                    self.gerenciador_entidades.jogador.energia_maxima,
                                    self.gerenciador_entidades.jogador.vida_maxima,
                                    self.gerenciador_entidades.jogador.nivel,
                                    self.gerenciador_entidades.jogador.sorte,
                                    self.gerenciador_entidades.jogador.energia_atual,
                                    self.gerenciador_entidades.jogador.vida_atual,
                                    self.gerenciador_entidades.jogador.experiencia_atual,
                                    self.gerenciador_entidades.jogador.moedas
                                )
                            print(resultado['mensagem'])


                        # Adicione outros tipos de interação aqui (ex: diálogo com NPC)
                        # elif area.tipo_evento == 'dialogo_npc':
                        #     return {'estado': CHAVE_TRANSICAO_DIALOGO, 'npc_id': area.dados_evento['npc_id']}

                 # --- Lógica de Interação com áreas de missão ---
                areas_de_missao_colidindo_agora: list[AreaInteracao] = pygame.sprite.spritecollide(self.jogador, self.areas_interacao_missao, False)

                for area in areas_de_missao_colidindo_agora:
                    if area.tipo_evento == 'missao' and area.metodo_ativacao == 'ativo':
                        print('Notificando interação com área de missão...')
                        self.gerenciador_missoes.notificar_interacao_area(area.identificador)

                # --- Lógica de Interação com NPCs ---
                npcs_colidindo_agora: list[Habitante] = pygame.sprite.spritecollide(self.jogador, self.npcs, False)
                for npc in npcs_colidindo_agora:
                    # Prioridade: Saudação > Missões > Diálogos Sem Missão
                    # 1. Primeiro tenta iniciar um diálogo de saudação
                    if not npc.conhecido:
                        self.banco_de_dados.marcar_habitante_como_conhecido(npc.identificador, self.dados_do_progresso.identificador_progresso)
                        npc.conhecido = True
                        
                        if not self.dialogo_ativo and npc.saudacao:
                            self.iniciar_dialogo(npc.saudacao)
                            return None # Consome o evento, o diálogo foi iniciado

                    # 1. Tenta iniciar uma missão
                    if npc.missoes_pendentes:
                        missao_iniciada = self.gerenciador_missoes.iniciar_missao(npc.missoes_pendentes[0].identificador_missao)
                        if missao_iniciada:
                            # Se a missão foi iniciada com sucesso, remove-a da lista do NPC
                            # Isso garante que a próxima interação com o mesmo NPC inicie a próxima missão
                            # Ou inicie os diálogos gerais se as missões acabarem.
                            npc.missoes_pendentes.pop(0) # Remove a primeira missão da lista
                            # Atualiza a flag do ícone de interação do NPC
                            npc._atualizar_icone_interacao()
                            return None # Consome o evento, o GerenciadorDeMissoes agora controla
                    
                    # 2. Se não houver missões ou se a missão falhou ao iniciar (já ativa, etc.), tenta iniciar diálogo sem missão
                    if not self.dialogo_ativo and npc.dialogos:
                        self.iniciar_dialogo(npc.dialogos)
                        return None # Consome o evento
                    
                # --- Lógica de Interação com Chefes ---
                chefe_colidindo = False
                if self.chefe:
                    chefe_colidindo = pygame.sprite.collide_rect(self.jogador, self.chefe)

                if chefe_colidindo and self.chefe is not None:
                    self.gerenciador_telas.mudar_tela(
                        CHAVE_TRANSICAO_BATALHA,
                        inimigos_na_batalha=[self.chefe],
                        numero_inimigos=1
                    )

            elif evento.key == pygame.K_k:
                self._ataque_no_mapa()

            # --- Abrir Inventário ---
            elif evento.key == pygame.K_i:
                self.menu_inventario = TelaInventario(
                    self.gerenciador_telas,
                    self.gerenciador_recursos,
                    self.banco_de_dados,
                    self.gerenciador_entidades)
                self.menu_inventario_ativo = True

            # --- Abrir Cozinha ---
            elif evento.key == pygame.K_c:
                self.menu_cozinha = TelaCozinha(
                    self.gerenciador_telas,
                    self.gerenciador_recursos,
                    self.banco_de_dados,
                    self.gerenciador_entidades)
                self.menu_cozinha_ativo = True

            # --- Abrir Mapa ---
            elif evento.key == pygame.K_m:
                self.menu_mapa = Mapa(
                    self.gerenciador_telas,
                    self.gerenciador_recursos,
                    self.banco_de_dados,
                    self.gerenciador_entidades,
                    modo='Exibir'
                )
                self.menu_mapa_ativo = True

            # --- ABRIR/FECHAR MENU DE PAUSA ---
            elif evento.key == pygame.K_ESCAPE:
                # Condição: só abre o menu de pausa se nenhum outro menu estiver ativo
                if not self.menu_mapa_ativo and not self.menu_inventario_ativo and not self.dialogo_ativo:
                    if not self.menu_pausa_ativo:
                        self.menu_pausa_ativo = True
                        self.menu_pausa = _MenuPausa(self.gerenciador_recursos)
                    else:
                        # Se já estiver ativo, o evento é capturado no topo do método
                        # para fechar o menu, então essa parte não é necessária.
                        pass




    def atualizar(self, dt):
        if self.menu_pausa_ativo:
            return
        
        super().atualizar(dt)
        dt_ms = dt * 1000 # Converte dt para milissegundos para a câmera e eventos

        # --- NOVO: Atualiza o Gerenciador de Missões PRIMEIRO ---
        # Se um evento de missão estiver ativo, ele pode controlar o jogador, a câmera, etc.
        self.gerenciador_missoes.atualizar(dt_ms) # Passa dt em milissegundos

        # Verifica se o gerenciador está controlando o jogo
        if self.gerenciador_missoes.esta_em_evento_controlado() or self.cena_estatica_ativa:
            self.jogador.movimento_bloqueado = True # Bloqueia o movimento do jogador
        elif self.menu_inventario_ativo and self.menu_inventario:
            if self.exibicao_nome_ilha:
                self.exibicao_nome_ilha.atualizar()
            # Não faz nada aqui no atualizar, pois ele é controlado por processar_eventos
            return
        elif self.menu_cozinha_ativo and self.menu_cozinha:
            self.menu_cozinha.atualizar(dt)
            
            if self.exibicao_nome_ilha:
                self.exibicao_nome_ilha.atualizar()
            # Não faz nada aqui no atualizar, pois ele é controlado por processar_eventos
            return
        elif self.menu_mapa_ativo and self.menu_mapa:
            if self.exibicao_nome_ilha:
                self.exibicao_nome_ilha.atualizar()
            # Não faz nada aqui no atualizar, pois ele é controlado por processar_eventos
            return
        else:
            self.jogador.movimento_bloqueado = False # Libera o movimento do jogador

        # Lógica de clamping do jogador para não sair dos limites do mundo (movimento normal)
        largura_mundo_atual = self.mapa_fundo_imagem.get_width()
        altura_mundo_atual = self.mapa_fundo_imagem.get_height()
        self.jogador.atualizar(dt, self.obstaculos_caminho, self.caminhos, largura_mundo_atual, altura_mundo_atual)

        # NOVO: Esta lógica toda só deve rodar quando o jogador está no controle
        if not self.gerenciador_missoes.esta_em_evento_controlado() or not self.cena_estatica_ativa:

            # --- Controle de tempo ocioso ---
            if self.jogador.rect.topleft == self.posicao_anterior_jogador:
                self.tempo_ocioso += dt
            else:
                self.tempo_ocioso = 0
                self.barra_de_estado_visivel = False

            self.posicao_anterior_jogador = self.jogador.rect.topleft

            if self.tempo_ocioso >= self.limite_ocioso:
                self.barra_de_estado_visivel = True

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

            # Sincroniza as coordenadas de mundo com o rect após o clamp
            self.jogador.coordenada_x = self.jogador.rect.x
            self.jogador.coordenada_y = self.jogador.rect.y

            # Obtém as áreas de interação que estão colidindo com o jogador
            areas_colidindo_agora = pygame.sprite.spritecollide(self.jogador, self.areas_interacao_missao, False)
            
            for area in areas_colidindo_agora:
                # Áreas de interação que ativam uma missão quando o jogador entra em uma área específica
                if area.metodo_ativacao == 'passivo':
                    self.gerenciador_missoes.iniciar_missao(area.identificador_missao)



        # Atualiza a visibilidade do ícone de interação
        self.areas_interacao_colididas = pygame.sprite.spritecollide(self.jogador, self.areas_interacao, False)
        colidindo_com_chefe = pygame.sprite.collide_rect(self.jogador, self.chefe) if self.chefe else False
        self.jogador.mostrar_icone_interacao = len(self.areas_interacao_colididas) > 0 or colidindo_com_chefe

        # Atualiza os NPCs, passando a posição do jogador para a orientação
        for npc in self.npcs:
            npc.atualizar(dt, self.jogador.rect)

        if self.chefe:
            self.chefe.atualizar(dt, self.jogador.rect)

        for area in self.areas_interacao:
            area.atualizar()
        self.notificador.atualizar(dt)

        self.camera.atualizar(dt, self.jogador.rect)

        # 3. ATUALIZAÇÃO CORRIGIDA: Atualiza SOMENTE os inimigos (com IA)
        # O vendedor, que está em outro grupo (self.npcs), não é afetado por este loop.
        for inimigo in self.inimigos:
            #print(f"[DEBUG] Atualizando inimigo: {inimigo.nome}, estado: {inimigo.estado}")
            inimigo.atualizar(dt, self.jogador, self.obstaculos_caminho, self.obstaculos_visao)
            if inimigo.atingiu_jogador:
                # Pega todos os inimigos da área (visão ou perseguição)
                print(f"[DEBUG] Inimigo {inimigo.nome} atingiu o jogador!")
                inimigos_reagindo = [
                    inimigo for inimigo in self.inimigos
                    if inimigo.estado in (ESTADO_INIMIGO_ALERTA, ESTADO_INIMIGO_PERSEGUINDO, ESTADO_INIMIGO_ATACANDO)
                ]
                print(inimigos_reagindo)
                print(f"[DEBUG] Inimigos reagindo: {[i.nome for i in inimigos_reagindo]}")
                # Se ninguém está alerta ainda, adiciona ao menos o atacante
                if not inimigos_reagindo:
                    inimigos_reagindo = [inimigo]

                # Sinaliza para o gerenciador de telas que uma batalha deve começar
                self.gerenciador_telas.mudar_tela(
                    CHAVE_TRANSICAO_BATALHA,
                    inimigos_na_batalha = inimigos_reagindo
                )
                return # Termina o atualizar aqui para não processar mais nada após a transição
            
        # 5. Atualiza a animação de fade-in/out do nome da ilha
        if self.exibicao_nome_ilha:
            self.exibicao_nome_ilha.atualizar()
        
        # Se o diálogo for controlado pela TelaJogo (não pela missão), atualiza aqui
        if self.dialogo_ativo and self.caixa_dialogo and not self.gerenciador_missoes.dialogo_controlado_ativo:
            self.caixa_dialogo.atualizar()
        
        # Se o menu de viagem estiver ativo, ele tem prioridade no atualizar
        if self.menu_mapa_ativo and self.menu_mapa:
            # Não faz nada aqui no atualizar, pois ele é controlado por processar_eventos
            pass

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


    def salvar_progresso(self):
        """
        Coleta os dados atuais do jogo (posição, status do jogador) e os salva no banco de dados.
        Este método centraliza a lógica de salvamento para esta tela.
        """
        print(f"Iniciando salvamento para o jogador: {self.jogador.identificador}")

        moedas_atuais = self.banco_de_dados.buscar_jogador(self.jogador.identificador).moedas_totais

        # Chama o método do DBManager para salvar os dados
        self.banco_de_dados.salvar_progresso_jogador(
            id_jogador=self.jogador.identificador,
            vida=self.jogador.vida_maxima_base,
            vida_atual=self.jogador.vida_atual,
            energia=self.jogador.energia_maxima_base,
            energia_atual=self.jogador.energia_atual,
            experiencia_atual=self.jogador.experiencia_atual,
            nivel=self.jogador.nivel,
            moedas_totais=moedas_atuais,  # Use a variável com o valor correto
            coordenada_x=int(self.jogador.coordenada_x),
            coordenada_y=int(self.jogador.coordenada_y),
            orientacao=self.jogador.orientacao,
            identificador_area=self.dados_da_area.identificador_area
        )
        
        print("Progresso salvo com sucesso.")
    


    def desenhar(self, tela: pygame.surface.Surface):
        # Desenha a imagem de fundo
        tela.blit(self.mapa_fundo_imagem, (self.mapa_fundo_imagem.get_rect(topleft=(-self.camera.rect.x, -self.camera.rect.y))))
        
        # --- NOVO: Desenha a cena estática SE estiver ativa ---
        if self.cena_estatica_ativa and self.imagem_cena_estatica:
            tela.blit(self.imagem_cena_estatica, (0, 0)) # Desenha a cena cobrindo toda a tela
        else: # Só desenha os elementos do jogo se a cena estática não estiver ativa

            for area in self.areas_interacao:
                area.desenhar(tela, self.camera.rect.x)

            sprites_ordenados = sorted(self.todos_os_sprites, key=lambda sprite: sprite.rect.bottom)

            for sprite in sprites_ordenados:
                sprite.desenhar(tela, self.camera.rect.x, self.camera.rect.y)

            # Desenha o efeito do ataque no mapa
            for efeito in self.efeitos_visuais:
                # print(f"Desenhando efeito: {efeito['frame']}, Tempo restante: {efeito['tempo_restante']:.2f}s")
                sprite = efeito["sprites"][efeito["frame"]]
                sprite = pygame.transform.scale(sprite, (60, 60))
                if self.jogador.orientacao == "direita":
                    sprite = pygame.transform.flip(sprite, True, False)
                pos = efeito["pos"]
                tela.blit(sprite, (pos[0]-self.camera.rect.x, pos[1]-self.camera.rect.y))

            for area in self.areas_interacao_missao:
                area.desenhar(tela, self.camera.rect.x)

            # --- Desenhar a camada superior (se existir) ---
            if self.camada_superior_imagem:
                tela.blit(self.camada_superior_imagem, (self.camada_superior_imagem.get_rect(topleft=(-self.camera.rect.x, -self.camera.rect.y))))

            for caminho in self.caminhos:
                caminho.desenhar(tela, self.camera.rect.x)

            if DEBUG_DESENHAR_CAIXAS_COLISAO:
                for area in list(self.areas_interacao) + list(self.areas_interacao_missao):
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

            self.notificador.desenhar(tela)
            # --- Desenha o nome da ilha com fade ---
            if self.exibicao_nome_ilha:
                self.exibicao_nome_ilha.desenhar(tela)

            # --- Desenha a barra de estado se estiver visível ---
            if self.barra_de_estado_visivel:
                self.barra_de_estado.desenhar(tela)

            # --- DESENHA O MENU DE PAUSA E ESMAECIMENTO ---
            if self.menu_pausa_ativo and self.menu_pausa:
                # Cria uma superfície para escurecer a tela
                esmaecer_superficie = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
                esmaecer_superficie.fill((0, 0, 0, 150))  # Preto com 150 de alpha (0-255)
                tela.blit(esmaecer_superficie, (0, 0))
                # Desenha o menu por cima
                self.menu_pausa.desenhar(tela)

            # --- Desenha o menu de inventário se estiver ativo ---
            if self.menu_inventario_ativo and self.menu_inventario:
                self.menu_inventario.desenhar(tela)

            # --- Desenha o menu de cozinha se estiver ativo ---
            if self.menu_cozinha_ativo and self.menu_cozinha:
                self.menu_cozinha.desenhar(tela)

            # --- Desenha o menu de viagem se estiver ativo ---
            if self.menu_mapa_ativo and self.menu_mapa:
                self.menu_mapa.desenhar(tela)

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



class _MenuPausa:
    def __init__(self, gerenciador_recursos):
        self.opcoes = ["Continuar", "Enciclopédia", "Sair"]
        self.indice_selecionado = 0
        self.fonte_menu = gerenciador_recursos.obter_fonte(CHAVE_FONTE_COLINER_BOTAO)
        self.cor_texto_normal = (255, 255, 255)
        self.cor_texto_selecionado = (255, 255, 0)
        self.cor_fundo_menu = (10, 10, 20, 220) # Fundo azul escuro, bem opaco
        self.cor_borda_menu = (200, 200, 200)



    def processar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)
            elif evento.key == pygame.K_DOWN:
                self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)
            elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                # Retorna a opção selecionada em minúsculas para facilitar a verificação
                return self.opcoes[self.indice_selecionado].lower()
            elif evento.key == pygame.K_ESCAPE:
                # Apertar ESC de novo fecha o menu
                return "continuar"
        return None



    def desenhar(self, tela):
        largura_menu = 400
        altura_linha = self.fonte_menu.get_height() + 20
        altura_menu = (len(self.opcoes) * altura_linha) + 40

        pos_x_menu = (LARGURA_TELA - largura_menu) // 2
        pos_y_menu = (ALTURA_TELA - altura_menu) // 2

        retangulo_menu = pygame.Rect(pos_x_menu, pos_y_menu, largura_menu, altura_menu)

        # Desenha o fundo do menu
        s = pygame.Surface((largura_menu, altura_menu), pygame.SRCALPHA)
        s.fill(self.cor_fundo_menu)
        tela.blit(s, retangulo_menu.topleft)

        # Desenha a borda
        pygame.draw.rect(tela, self.cor_borda_menu, retangulo_menu, 3)

        # Desenha as opções
        y_offset = pos_y_menu + 30
        for i, opcao in enumerate(self.opcoes):
            cor_texto = self.cor_texto_selecionado if i == self.indice_selecionado else self.cor_texto_normal
            texto_renderizado = self.fonte_menu.render(opcao, True, cor_texto)

            pos_x_texto = pos_x_menu + (largura_menu - texto_renderizado.get_width()) // 2
            tela.blit(texto_renderizado, (pos_x_texto, y_offset))
            y_offset += altura_linha



class _MenuViagemFlutuante:
    def __init__(self, opcoes_viagem):
        self.opcoes = opcoes_viagem  # Lista de objetos Row com id, nome_ilha, visitada
        self.indice_selecionado = 0
        self.fonte_menu = pygame.font.Font(None, 36)
        self.cor_texto_normal = (255, 255, 255)
        self.cor_texto_selecionado = (255, 255, 0)
        self.cor_fundo_menu = (50, 50, 50, 200)
        self.cor_borda_menu = (200, 200, 200)

    def processar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)
            elif evento.key == pygame.K_DOWN:
                self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)
            elif evento.key == pygame.K_RETURN:
                if self.opcoes and self.opcoes[self.indice_selecionado].bloqueada is False:
                    return self.opcoes[self.indice_selecionado]  # Retorna o ID da ilha
                return None
            elif evento.key == pygame.K_ESCAPE:
                return "cancelar"
        return None

    def desenhar(self, tela):
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

    def atualizar(self):
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

    def desenhar(self, tela):
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
