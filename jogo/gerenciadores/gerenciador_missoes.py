# gerenciadores/gerenciador_missoes.py

import pygame
import json # Ou outro formato para carregar seus scripts
from utilidades.constantes import * # Importa as constantes
from entidades.item_inventario import ItemInventario
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Dict
if TYPE_CHECKING:
    from gerenciadores import DBManager, GerenciadorDeRecursos, GerenciadorDeTelas, GerenciadorDeEntidades
    from entidades import Jogador
    from telas import TelaJogo



@dataclass
class EstadoMissao:
    """Armazena o estado individual de uma missão ativa."""
    id_missao: str
    script: list
    indice_passo: int = 0
    esta_pausado: bool = False
    lista_ids_areas_aguardadas: List[str] = field(default_factory=list)



class GerenciadorDeMissoes:
    _instancia = None

    def __new__(cls, banco_de_dados: "DBManager" = None, gerenciador_recursos: "GerenciadorDeRecursos" = None, gerenciador_telas: "GerenciadorDeTelas" = None, gerenciador_entidades: "GerenciadorDeEntidades" = None):
        if cls._instancia is None:
            if banco_de_dados is None or gerenciador_recursos is None or gerenciador_telas is None or gerenciador_entidades is None:
                raise ValueError("GerenciadorDeMissoes deve ser inicializado com banco_de_dados, gerenciador_recursos, gerenciador_telas e gerenciador_entidades.")
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar(banco_de_dados, gerenciador_recursos, gerenciador_telas, gerenciador_entidades)
        return cls._instancia



    def _inicializar(self, banco_de_dados: "DBManager", gerenciador_recursos: "GerenciadorDeRecursos", gerenciador_telas: "GerenciadorDeTelas", gerenciador_entidades: "GerenciadorDeEntidades"):
        self.banco_de_dados = banco_de_dados
        self.gerenciador_recursos = gerenciador_recursos
        self.gerenciador_entidades = gerenciador_entidades
        self.gerenciador_telas = gerenciador_telas # Para mudar de tela se necessário

        self.scripts_missoes = self._carregar_scripts_missoes() # Carrega os scripts do JSON/dicionário
        self.missoes_ativas: Dict[str, EstadoMissao] = {}
        self.pausa_geral = False
        self.dialogo_controlado_ativo = False # Flag para indicar que o diálogo está sendo controlado por aqui
        self.missao_que_ativou_dialogo: EstadoMissao = None # ID da missão que ativou o diálogo controlado
        self.dialogos_controlados_atuais = []
        self.indice_dialogo_controlado = 0
        
        # NOVO: Atributos para controle de movimento
        self.entidade_em_movimento = None
        self.destino_movimento = None
        self.missao_que_ativou_movimento: EstadoMissao = None
        self.velocidade_movimento_controlado = VELOCIDADE_JOGADOR * 0.8 # Um pouco mais lento para cutscenes



    def vincular_nova_tela_jogo(self, tela_jogo: "TelaJogo"):
        """
        Atualiza as referências para os componentes da tela de jogo atual.
        Isso evita a necessidade de recriar o GerenciadorDeMissoes.
        """
        print("GerenciadorDeMissoes vinculado à nova TelaJogo.")
        self.tela_jogo = tela_jogo
        self.camera = tela_jogo.camera
        self.caixa_dialogo = tela_jogo.caixa_dialogo
        self.npcs = tela_jogo.npcs



    def limpar_estados_das_missoes(self):
        """
        Limpa os estados das missões ativas no progresso atual.
        Usado ao alternar entre progressos.
        """
        self.missoes_ativas.clear()
        self.scripts_missoes = self._carregar_scripts_missoes()

        self.pausa_geral = False
        self.dialogo_controlado_ativo = False # Flag para indicar que o diálogo está sendo controlado por aqui
        self.missao_que_ativou_dialogo: EstadoMissao = None # ID da missão que ativou o diálogo controlado
        self.dialogos_controlados_atuais = []
        self.indice_dialogo_controlado = 0
        
        self.entidade_em_movimento = None
        self.destino_movimento = None
        self.missao_que_ativou_movimento: EstadoMissao = None



    def notificar_vitoria_em_batalha(self, inimigo_derrotado):
        """
        Método chamado quando uma batalha é vencida.
        Verifica se alguma das missões ativas está esperando por essa vitória.
        """
        for missao_id, estado_missao in self.missoes_ativas.items():
            if estado_missao.script:
                passo_atual = estado_missao.script[estado_missao.indice_passo]
                if passo_atual['tipo'] == 'aguardar_batalha':
                    if 'inimigo' in passo_atual and passo_atual['inimigo'] == inimigo_derrotado:
                        print(f"Batalha vencida na missão {missao_id}. Avançando no script.")
                        estado_missao.esta_pausado = False
                        self._avancar_passo(estado_missao)

                if passo_atual['tipo'] == 'batalha':
                    print(f"Batalha vencida na missão {missao_id}. Avançando no script.")
                    estado_missao.esta_pausado = False
                    self._avancar_passo(estado_missao)


    def notificar_mudanca_de_area(self, id_area):
        """
        Método chamado quando o jogador muda de área.
        Verifica se alguma das missões ativas está aguardando essa mudança.
        """
        print("Notificando mudança de área...")
        for missao_id, estado_missao in self.missoes_ativas.items():
            passo_atual = estado_missao.script[estado_missao.indice_passo]
            print(f"passo_atual['tipo']: {passo_atual['tipo']}\tid_area in estado_missao.lista_ids_areas_aguardadas: {id_area in estado_missao.lista_ids_areas_aguardadas}")
            if passo_atual['tipo'] == 'aguardar_mudanca_de_area' and id_area in estado_missao.lista_ids_areas_aguardadas:
                print(f"Mudança de área detectada na missão {missao_id}. Avançando no script.")
                estado_missao.lista_ids_areas_aguardadas.remove(id_area)
                if not estado_missao.lista_ids_areas_aguardadas:
                    estado_missao.esta_pausado = False
                    self._avancar_passo(estado_missao)



    def notificar_interacao_area(self, id_area_interativa):
        """
        Método chamado quando o jogador interage com uma área interativa.
        Verifica se alguma das missões ativas está aguardando essa interação.
        """
        for missao_id, estado_missao in self.missoes_ativas.items():
            if estado_missao.esta_pausado and estado_missao.script:
                passo_atual = estado_missao.script[estado_missao.indice_passo]

                if passo_atual['tipo'] == 'aguardar_interacao' and estado_missao.lista_ids_areas_aguardadas:
                    if id_area_interativa in estado_missao.lista_ids_areas_aguardadas:

                        print(f"Interação na área {id_area_interativa} detectada na missão {missao_id}. Avançando no script.")

                        estado_missao.lista_ids_areas_aguardadas.remove(id_area_interativa)

                        resposta = passo_atual.get('resposta_da_interacao')

                        if resposta == 'remover_area':
                            print('Removendo área...')
                            resultado = self.banco_de_dados.remover_area_interativa(id_area_interativa, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

                            if resultado['sucesso']:
                                print('Área interativa removida')
                            else:
                                print(resultado['erro'])

                        elif resposta == 'atualizar_area':
                            print('Atualizando área...')
                            resultado = self.banco_de_dados.desativar_area_interativa(id_area_interativa, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

                            if resultado['sucesso']:
                                print('Área interativa desativada')
                            else:
                                print(resultado['erro'])

                        self.tela_jogo.atualizar_areas_interativas_de_missao()


                    # Se todas as áreas já foram interagidas, avança na missão.
                    if not estado_missao.lista_ids_areas_aguardadas:
                        estado_missao.esta_pausado = False
                        self._avancar_passo(estado_missao)



    def _carregar_scripts_missoes(self):
        """
        Carrega os scripts das missões de um arquivo JSON (ou pode ser um dicionário direto aqui).
        Este é um exemplo. Em um jogo real, você carregaria de um arquivo.
        """
        # Exemplo de dicionário de scripts (pode ser carregado de um JSON)
        return {
            'mis001': [ # Sua primeira missão
                {'tipo': 'aguardar_mudanca_de_area', 'id_area': 'are001'},
                {'tipo': 'cena_dialogo_missao', 'missao_id': 'mis001', 'chave_imagem_cena': CENA_SILVIE_NO_CAMPO if self.gerenciador_entidades.jogador.nome == SILVIE else CENA_SHUAN_NO_CAMPO},
                {'tipo': 'finalizar_cena'},
                {'tipo': 'inserir_gatilho_de_missao', 'id_area': 'are001', 'id_missao': 'mis003', 'x': 2560, 'y': 220, 'largura': 180, 'altura': 133},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'ativar_proxima_missao', 'id_missao': 'mis002'}
            ],
            'mis002': [
                {'tipo': 'aguardar_mudanca_de_area', 'id_area': 'are002'},
                {'tipo': 'posicionar_jogador', 'x': 100, 'y': 370, 'orientacao': 'direita'},
                {'tipo': 'mover_jogador_para', 'x': 1485, 'y': 370},
                {'tipo': 'dialogo', 'missao_id': 'mis002'},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'recompensa'}
            ],
            'mis003': [
                {'tipo': 'remover_inimigos_da_area', 'area_id': 'are001'},
                {'tipo': 'carregar_inimigo_na_posicao', 'chave_inimigo': 'Lobo', 'x': 2980, 'y': 290, 'id_instancia': 'lobo_missao_003'},
                {'tipo': 'mover_jogador_para', 'x': 2780, 'y': 170},
                {'tipo': 'mover_inimigo_para', 'id_instancia': 'lobo_missao_003', 'x': 2900, 'y': 210},
                {'tipo': 'dialogo', 'missao_id': 'mis003'}, # Precisamos do ID para buscar os diálogos
                {'tipo': 'remover_gatilho_de_missao', 'id_area': 'are001', 'id_missao': 'mis003', 'x': 2560, 'y': 220, 'largura': 180, 'altura': 133},
                {'tipo': 'batalha', 'inimigos_batalha': ['lobo_missao_003'], 'fuga_habilitada': False},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'recompensa', 'xp': 50}
            ],
            'mis004': [
                {'tipo': 'dialogo', 'missao_id': 'mis004'},
                {'tipo': 'inserir_area_interativa_de_missao', 'id_area': 'are001', 'x': 1430, 'y': 327, 'largura': 60, 'altura': 60, 'chave_imagem': 'Corvo_0', 'metodo_ativacao': 'ativo'},
                {'tipo': 'inserir_area_interativa_de_missao', 'id_area': 'are001', 'x': 2247, 'y': 282, 'largura': 60, 'altura': 60, 'chave_imagem': 'Corvo_0', 'metodo_ativacao': 'ativo'},
                {'tipo': 'inserir_area_interativa_de_missao', 'id_area': 'are001', 'x': 2698, 'y': 276, 'largura': 60, 'altura': 60, 'chave_imagem': 'Corvo_0', 'metodo_ativacao': 'ativo'},
                {'tipo': 'aguardar_interacao', 'resposta_da_interacao': 'remover_area'},
                {'tipo': 'carregar_inimigo_na_posicao', 'chave_inimigo': 'Corvo', 'x': 2043, 'y': 363, 'id_instancia': 'corvo_missao_004'},
                {'tipo': 'batalha', 'inimigos_batalha': ['corvo_missao_004']},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'recompensa', 'xp': 50}
            ],
            'mis005': [
                {'tipo': 'dialogo', 'missao_id': 'mis005'},
                {'tipo': 'buscar_areas_interativas_de_missao', 'id_area': 'are003'},
                {'tipo': 'aguardar_interacao', 'resposta_da_interacao': 'atualizar_area'},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'recompensa', 'xp': 25}
            ],
            'mis006': [
                {'tipo': 'dialogo', 'missao_id': 'mis006'},
                {'tipo': 'aguardar_batalha', 'inimigo': 'Lobo'},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'recompensa', 'xp': 25}
            ],
            'mis007': [
                {'tipo': 'dialogo', 'missao_id': 'mis007'},
                {'tipo': 'inserir_area_interativa_de_missao', 'id_area': 'are003', 'x': 556, 'y': 105, 'largura': 150, 'altura': 127, 'metodo_ativacao': 'ativo'},
                {'tipo': 'aguardar_interacao', 'resposta_da_interacao': 'remover_area'},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'recompensa', 'xp': 25}
            ],
            'mis008': [
                {'tipo': 'dialogo', 'missao_id': 'mis008'},
                {'tipo': 'inserir_area_interativa_de_missao', 'id_area': 'are001', 'x': 1480, 'y': 336, 'largura': 1400, 'altura': 75, 'metodo_ativacao': 'ativo'},
                {'tipo': 'aguardar_interacao', 'resposta_da_interacao': 'remover_area'},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'recompensa', 'xp': 25}
            ],
            'mis009': [
                {'tipo': 'dialogo', 'missao_id': 'mis009'},
                {'tipo': 'inserir_area_interativa_de_missao', 'id_area': 'are002', 'x': 2513, 'y': 351, 'largura': 346, 'altura': 97, 'metodo_ativacao': 'ativo'},
                {'tipo': 'aguardar_interacao', 'resposta_da_interacao': 'remover_area'},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'recompensa', 'xp': 25}
            ],
            'mis010': [
                {'tipo': 'entregar_itens', 'itens': ['ncn022', 'ncn023', 'ncn024']},
                {'tipo': 'dialogo', 'missao_id': 'mis010'},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'aprender_receita', 'receita_id': 'rec014'},
                {'tipo': 'recompensa', 'xp': 25}
            ],
            'mis011': [
                {'tipo': 'cena_dialogo_missao', 'missao_id': 'mis011', 'chave_imagem_cena': CENA_JANTAR_COMUNITARIO},
                {'tipo': 'carregar_chefe', 'chefe': 'Javali', 'id_chefe': 'che001'},
                {'tipo': 'aguardar_batalha', 'inimigo': 'Javali'},
                {'tipo': 'finalizar_missao'},
                {'tipo': 'recompensa', 'xp': 50}
            ],
            'mis012': [
                {'tipo': 'aguardar_mudanca_de_area', 'id_area': 'are002'},
                {'tipo': 'dialogo', 'missao_id': 'mis012'},
                {'tipo': 'finalizar_missao'},
            ]


            # ... outras missões
        }



    def iniciar_missao(self, identificador_missao):
        #print(f"Tentando iniciar a missão: {identificador_missao} no progresso {self.gerenciador_entidades.progresso_do_jogo.identificador_progresso}")
        estado_missao = self.banco_de_dados.buscar_estado_da_missao(identificador_missao, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)
        #print(f"Estado da missão: {estado_missao}")


        if estado_missao == 'concluida' or identificador_missao in self.missoes_ativas:
            return False

        """Inicia a execução do script de uma missão."""
        if identificador_missao in self.scripts_missoes:
            print(f"Missão '{identificador_missao}' iniciada.")
            self.banco_de_dados.atualizar_estado_missao(identificador_missao, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso, 'aceita')
            self.missoes_ativas[identificador_missao] = EstadoMissao(identificador_missao, self.scripts_missoes[identificador_missao])
            return True
        else:
            print(f"Erro: Missão '{identificador_missao}' não encontrada nos scripts.")
            return False



    def atualizar(self, dt_ms):
        """
        Atualiza o estado do gerenciador de missões e avança no script.
        :param dt_ms: Delta time em milissegundos.
        """

        # =====================================================================
        #  PRIMEIRO: Verifique e execute o movimento controlado, se houver.
        #  Esta lógica precisa rodar MESMO SE o script estiver "pausado".
        # =====================================================================
        if self.entidade_em_movimento and self.destino_movimento:
            self._atualizar_movimento()
            # Como o movimento está acontecendo, paramos o resto do atualizar deste frame
            return 

        # =====================================================================
        #  SEGUNDO: Agora, verifique as condições de pausa geral (diálogo, etc.)
        # =====================================================================
        if not self.missoes_ativas or self.pausa_geral:
            if self.dialogo_controlado_ativo and self.caixa_dialogo:
                self.caixa_dialogo.atualizar()
            return

        # Se o movimento da câmera estiver em andamento, pausa o script
        if self.camera.modo == 'movimento_suave':
            if not self.camera.movimento_suave_completo():
                self.camera.atualizar(dt_ms)
            else:
                # Movimento suave completo, despausa a missão que estava em movimento
                if self.missao_que_ativou_movimento:
                    self.missao_que_ativou_movimento.esta_pausado = False
                    self.missao_que_ativou_movimento = None
                self.pausa_geral = False
            return

        # =====================================================================
        #  TERCEIRO: Se não há movimento nem pausa, execute o próximo passo
        # =====================================================================
        for missao_id, estado in list(self.missoes_ativas.items()):
            # Se a missão específica não estiver pausada, executa seu próximo passo
            if not estado.esta_pausado:
                if estado.indice_passo < len(estado.script):
                    self._executar_passo(estado) # Passa o objeto de estado inteiro
                else:
                    # Script da missão concluído (mas a missão só é finalizada com o passo 'finalizar_missao')
                    print(f"Script da missão '{missao_id}' concluído.")
                    del self.missoes_ativas[missao_id]
                    pass



    def _atualizar_movimento(self):
        entidade = self.entidade_em_movimento
        destino = self.destino_movimento
        
        direcao = destino - pygame.math.Vector2(entidade.coordenada_x, entidade.coordenada_y)

        # Checa se a entidade chegou ao destino
        if direcao.length() < 5: # Usamos uma pequena margem de erro
            entidade.coordenada_x, entidade.coordenada_y = destino.x, destino.y
            entidade.estado = 'parado' # Para a animação
            self.entidade_em_movimento = None
            self.destino_movimento = None
            # IMPORTANTE: O próprio movimento, ao terminar, avança o script
            self._avancar_passo(self.missao_que_ativou_movimento)
            self.missao_que_ativou_movimento.esta_pausado = False # Despausa a missão que estava em movimento
            self.missao_que_ativou_movimento = None # Limpa a referência após
            self.pausa_geral = False # Despausa o script
        else:
            # Move a entidade
            direcao.normalize_ip()
            entidade.coordenada_x += direcao.x * self.velocidade_movimento_controlado
            entidade.coordenada_y += direcao.y * self.velocidade_movimento_controlado
            entidade.estado = 'caminhando' # Ativa a animação de caminhada

            # NOVO E CRUCIAL: Sincronize o rect com as coordenadas de mundo
            entidade.rect.x = int(entidade.coordenada_x)
            entidade.rect.y = int(entidade.coordenada_y)
            
            # Atualiza a orientação visual da entidade
            if hasattr(entidade, 'orientacao'):
                entidade.orientacao = 'direita' if direcao.x >= 0 else 'esquerda'
            


    def _executar_passo(self, estado: EstadoMissao):
        """Executa uma única ação do script da missão."""
        passo = estado.script[estado.indice_passo]
        tipo_passo = passo['tipo']

        print(f"Executando passo da missão: {tipo_passo}") # Ótimo para debug

        if tipo_passo == 'focar_em_ponto':
            self.camera.focar_em_ponto(passo['x'], passo['y'])
            self._avancar_passo(estado) # Este é instantâneo, então avança imediatamente

        elif tipo_passo == 'aguardar_interacao':
            # Este passo é uma espera, não faz nada por enquanto
            print("Aguardando interação do jogador...")
            estado.esta_pausado = True # Pausa a missão até que a interação ocorra

        elif tipo_passo == 'aguardar_batalha':
            # Este passo é uma espera, não faz nada por enquanto
            print("Aguardando batalha...")
            estado.esta_pausado = True # Pausa a missão até que a batalha ocorra

        elif tipo_passo == 'aguardar_mudanca_de_area':
            id_area_alvo = passo['id_area']

            # Garante que a tela de jogo já foi vinculada antes de tentar acessá-la
            if not hasattr(self, 'tela_jogo'):
                # Isso pode acontecer se uma missão for iniciada antes da tela de jogo existir.
                # A lógica de repetição no próximo frame vai lidar com isso.
                print(f"AVISO: Tentando checar 'aguardar_mudanca_de_area' antes da tela de jogo ser vinculada.")
                estado.esta_pausado = True # Pausa temporariamente para tentar de novo
                return

            id_area_atual = self.tela_jogo.dados_da_area.identificador_area

            # CHECAGEM IMEDIATA: Verifica se o jogador JÁ ESTÁ na área alvo.
            if id_area_alvo == id_area_atual:
                print(f"Condição 'aguardar_mudanca_de_area' para '{id_area_alvo}' já satisfeita na execução. Avançando imediatamente.")
                self._avancar_passo(estado)
            else:
                # Se não estiver, configura o estado de espera normal.
                print(f"Aguardando mudança de área para '{id_area_alvo}'...")
                if id_area_alvo not in estado.lista_ids_areas_aguardadas:
                    estado.lista_ids_areas_aguardadas.append(id_area_alvo)
                estado.esta_pausado = True

        elif tipo_passo == 'aprender_receita':
            self.banco_de_dados.aprender_receita(passo.get('receita_id'), self.gerenciador_entidades.jogador.identificador)
            self._avancar_passo(estado)

        elif tipo_passo == 'buscar_areas_interativas_de_missao':
            resultado = self.banco_de_dados.buscar_areas_interativas_de_missao_por_area(passo.get('id_area'), self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

            if resultado:
                for area in resultado:
                    if area.identificador_missao == estado.id_missao:
                        estado.lista_ids_areas_aguardadas.append(area.identificador)

            self._avancar_passo(estado)

        elif tipo_passo == 'carregar_chefe':
            self.banco_de_dados.reviver_chefe(passo['id_chefe'], self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

            self._avancar_passo(estado)

        elif tipo_passo == 'remover_inimigos_da_area':
            # Remove inimigos existentes para garantir um cenário limpo
            # A melhor forma é fazer isso na TelaJogo, que controla o grupo de inimigos
            self.tela_jogo.inimigos.empty()
            self._avancar_passo(estado)

        elif tipo_passo == 'carregar_inimigo_na_posicao':
            # Pede para a TelaJogo criar e adicionar o inimigo da missão
            self.tela_jogo.adicionar_inimigo_em_missao(
                passo['chave_inimigo'],
                passo['id_instancia'],
                passo['x'],
                passo['y']
            )
            self._avancar_passo(estado)

        elif tipo_passo == 'posicionar_jogador':
            self.gerenciador_entidades.jogador.coordenada_x = passo['x']
            self.gerenciador_entidades.jogador.coordenada_y = passo['y']
            self.gerenciador_entidades.jogador.orientacao = passo['orientacao']
            self._avancar_passo(estado)

        elif tipo_passo == 'mover_jogador_para':
            if self.pausa_geral:
                print(f"AVISO [Missão {estado.id_missao}]: Tentou iniciar movimento enquanto uma ação global já estava em curso. O passo será tentado novamente no próximo frame.")
                return # Não faz nada neste frame, a missão tentará executar o passo novamente no próximo.

            self.entidade_em_movimento = self.gerenciador_entidades.jogador
            self.destino_movimento = pygame.math.Vector2(passo['x'], passo['y'])
            self.missao_que_ativou_movimento = estado
            estado.esta_pausado = True # Pausa a missão até o movimento terminar
            self.pausa_geral = True # Pausa o script até o movimento terminar

        elif tipo_passo == 'mover_inimigo_para':
            if self.pausa_geral:
                print(f"AVISO [Missão {estado.id_missao}]: Tentou iniciar movimento enquanto uma ação global já estava em curso. O passo será tentado novamente no próximo frame.")
                return # Não faz nada neste frame, a missão tentará executar o passo novamente no próximo.

            # Encontra o inimigo pelo ID de instância que demos a ele
            inimigo_alvo = None
            for inimigo in self.tela_jogo.inimigos:
                if hasattr(inimigo, 'identificador_instancia_lacaio') and inimigo.identificador_instancia_lacaio == passo['id_instancia']:
                    inimigo_alvo = inimigo
                    break
            
            if inimigo_alvo:
                self.entidade_em_movimento = inimigo_alvo
                self.destino_movimento = pygame.math.Vector2(passo['x'], passo['y'])
                self.missao_que_ativou_movimento = estado
                estado.esta_pausado = True # Pausa a missão até o movimento terminar
                self.pausa_geral = True # Pausa o script
            else:
                print(f"ERRO: Inimigo com ID '{passo['id_instancia']}' não encontrado para mover.")
                self._avancar_passo(estado) # Pula o passo se não encontrar

        elif tipo_passo == 'dialogo':
            if self.pausa_geral:
                print(f"AVISO [Missão {estado.id_missao}]: Tentou iniciar diálogo enquanto uma ação global já estava em curso. O passo será tentado novamente no próximo frame.")
                return
            id_missao = passo['missao_id']
            genero = 'F' if self.gerenciador_entidades.jogador.nome == SILVIE else 'M'
            dialogos = self.banco_de_dados.buscar_dialogos_da_missao(id_missao, genero, self.gerenciador_entidades.jogador.identificador)
            if dialogos:
                self.missao_que_ativou_dialogo = estado
                estado.esta_pausado = True # Pausa a missão até o diálogo terminar
                self.iniciar_dialogo_controlado(dialogos)
            else:
                print(f"AVISO: Nenhum diálogo encontrado para a missão '{id_missao}'. Pulando.")
                self._avancar_passo(estado)
                
        elif tipo_passo == 'batalha':
            # Usa o sistema de transição de tela que você já tem
            print("Iniciando transição para batalha...")
            
            # Encontra os inimigos da batalha na lista de inimigos da tela de jogo
            inimigos_para_batalha = []
            for id_inimigo in passo['inimigos_batalha']:
                for inimigo_sprite in self.tela_jogo.inimigos:
                    if hasattr(inimigo_sprite, 'identificador_instancia_lacaio') and inimigo_sprite.identificador_instancia_lacaio == id_inimigo:
                        inimigos_para_batalha.append(inimigo_sprite)
                        print(inimigos_para_batalha)

            if inimigos_para_batalha:
                self.gerenciador_telas.mudar_tela(
                    CHAVE_TRANSICAO_BATALHA,
                    inimigos_na_batalha=inimigos_para_batalha,
                    modo_batalha='chefe',
                    fuga_habilitada=passo.get('fuga_habilitada', True)
                    # Adicione quaisquer outros dados que sua tela de batalha precise
                )
                # A missão será finalizada quando a batalha terminar (ver Passo 3)
                estado.esta_pausado = True # Pausa a missão até o retorno da batalha
            else:
                print("ERRO: Inimigos para a batalha não foram encontrados.")
                self._avancar_passo(estado)

        elif tipo_passo == 'movimento_camera_suave':
            if self.pausa_geral:
                print(f"AVISO [Missão {estado.id_missao}]: Tentou iniciar movimento enquanto uma ação global já estava em curso. O passo será tentado novamente no próximo frame.")
                return # Não faz nada neste frame, a missão tentará executar o passo novamente no próximo.

            self.missao_que_ativou_movimento = estado

            self.camera.iniciar_movimento_suave(
                self.camera.rect.centerx, self.camera.rect.centery, # Começa da posição atual da câmera
                passo['fim_x'], passo['fim_y'],
                passo['duracao_ms']
            )
            estado.esta_pausado = True # Pausa a missão até o movimento terminar
            self.pausa_geral = True # Pausa o script até o movimento terminar (será despausado no update)
            # O avanço do passo acontecerá no próximo update, quando o movimento for completo.

        elif tipo_passo == 'focar_jogador':
            self.camera.retornar_para_jogador()
            self._avancar_passo(estado)

        elif tipo_passo == 'entregar_itens':
            for item in passo.get('itens'):
                self.banco_de_dados.remover_item_do_inventario(self.gerenciador_entidades.jogador.id_mochila, item)
            self._avancar_passo(estado)

        elif tipo_passo == 'recompensa':
            print(f"Recompensa: XP={passo.get('xp', 50)}, Item={passo.get('item_id', 'Nenhum')}")
            # Lógica para adicionar XP e itens ao jogador
            self.gerenciador_entidades.jogador.experiencia_atual += passo.get('xp', 50)
            self.gerenciador_entidades.jogador.atualizar_atributos_por_nivel()
    
            dados_do_item = self.banco_de_dados.buscar_item_recompensa_missao(estado.id_missao)
            if dados_do_item:
                efeitos = self.banco_de_dados.buscar_efeitos_por_item(dados_do_item.identificador_item)
            
                item = ItemInventario(
                    dados_do_item.identificador_item,
                    dados_do_item.nome_item,
                    dados_do_item.descricao_item,
                    dados_do_item.tipo,
                    dados_do_item.raridade,
                    dados_do_item.quantidade
                )
                for efeito in efeitos:
                    item.adicionar_efeito(efeito.efeito_nome, efeito.efeito_valor)
    
                self.gerenciador_entidades.jogador.inserir_item_na_mochila(item, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)
                self.gerenciador_entidades.jogador.moedas += passo.get('moedas', 0)
    
                self.tela_jogo.notificador.adicionar_item(dados_do_item.nome_item, dados_do_item.quantidade)

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
            self._avancar_passo(estado)

        elif tipo_passo == 'inserir_gatilho_de_missao':
            resultado = self.banco_de_dados.inserir_gatilho_de_missao(passo.get('id_area'), passo.get('id_missao'), passo.get('x'), passo.get('y'), passo.get('largura'), passo.get('altura'), self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)
            print(resultado)
            if resultado:
                print(f"Gatilho de missão inserido na área '{passo.get('id_area')}' para a missão '{passo.get('id_missao')}'.")
            self.tela_jogo.atualizar_areas_interativas_de_missao()

            self._avancar_passo(estado)

        elif tipo_passo == 'remover_gatilho_de_missao':
            self.banco_de_dados.remover_gatilho_de_missao(passo.get('id_area'), passo.get('id_missao'), passo.get('x'), passo.get('y'), passo.get('largura'), passo.get('altura'), self.gerenciador_entidades.progresso_do_jogo.identificador_progresso)

            self.tela_jogo.atualizar_areas_interativas_de_missao()

            self._avancar_passo(estado)

        elif tipo_passo == 'inserir_area_interativa_de_missao':
            resultado = self.banco_de_dados.inserir_area_interativa_de_missao(
                passo.get('id_area'),
                estado.id_missao,
                passo.get('x'),
                passo.get('y'),
                passo.get('largura'),
                passo.get('altura'),
                self.gerenciador_entidades.progresso_do_jogo.identificador_progresso,
                passo.get('metodo_ativacao'),
                passo.get('chave_imagem')
            )
            if resultado['sucesso']:
                estado.lista_ids_areas_aguardadas.append(resultado['id_area_interativa'])

                self.tela_jogo.atualizar_areas_interativas_de_missao()
            else:
                print(f"ERRO: {resultado['erro']}")

            self._avancar_passo(estado)
        
        elif tipo_passo == 'ativar_proxima_missao':
            
            self.banco_de_dados.atualizar_estado_missao(passo.get('id_missao'), self.gerenciador_entidades.progresso_do_jogo.identificador_progresso, 'aceita')
            self.iniciar_missao(passo.get('id_missao'))
            self._avancar_passo(estado)

        elif tipo_passo == 'finalizar_cena':
            print("Finalizando cena estática.")
            self.tela_jogo.desativar_cena_estatica()
            self.camera.retornar_para_jogador()
            self._avancar_passo(estado)

        elif tipo_passo == 'finalizar_missao':
            print(f"Missão '{estado.id_missao}' marcada como finalizada.")
            
            self.banco_de_dados.atualizar_estado_missao(estado.id_missao, self.gerenciador_entidades.progresso_do_jogo.identificador_progresso, 'concluida')
            self.gerenciador_entidades.iniciar_missao = None
            self._avancar_passo(estado)

        # NOVO TIPO DE PASSO: Cena estática com diálogo
        elif tipo_passo == 'cena_dialogo_missao':
            if self.pausa_geral:
                print(f"AVISO [Missão {estado.id_missao}]: Tentou iniciar diálogo enquanto uma ação global já estava em curso. O passo será tentado novamente no próximo frame.")
                return
            missao_id = passo['missao_id']
            chave_imagem_cena = passo['chave_imagem_cena']
            print(f"DEBUG: Executando passo 'cena_dialogo_missao' para a missão '{missao_id}'.")

            # 1. Exibir a cena estática
            self.tela_jogo.ativar_cena_estatica(chave_imagem_cena)

            # 2. Carregar e exibir os diálogos da missão
            genero = 'F' if self.gerenciador_entidades.jogador.nome == SILVIE else 'M'
            
            dialogos_da_missao = self.banco_de_dados.buscar_dialogos_da_missao(missao_id, genero, self.gerenciador_entidades.jogador.identificador)
            if dialogos_da_missao:
                print(f"DEBUG: Diálogos encontrados para a missão '{missao_id}': {len(dialogos_da_missao)}.")
                self.missao_que_ativou_dialogo = estado
                estado.esta_pausado = True # Pausa a missão até o diálogo terminar
                self.iniciar_dialogo_controlado(dialogos_da_missao)
            else:
                print(f"AVISO: Nenhun diálogo encontrado para a missão '{missao_id}'.")
                
                # Se não houver diálogos, finalizar a cena imediatamente
                self.tela_jogo.desativar_cena_estatica()
                self.camera.retornar_para_jogador()
                self._avancar_passo(estado) # Avança para o próximo passo no script (se houver)



    def _avancar_passo(self, estado: EstadoMissao):
        """Avança para o próximo passo do script."""
        estado.indice_passo += 1
        estado.esta_pausado = False # Garante que o script não esteja mais pausado após o avanço



    def iniciar_dialogo_controlado(self, lista_de_textos):
        """Inicia uma sequência de diálogos controlada pelo gerenciador de missões."""
        self.dialogos_controlados_atuais = lista_de_textos
        self.indice_dialogo_controlado = 0
        self.dialogo_controlado_ativo = True
        self.pausa_geral = True # Pausa o script da missão enquanto o diálogo está ativo
        
        # Garante que a caixa de diálogo esteja pronta
        if not self.caixa_dialogo:
            # Isso não deveria acontecer se a TelaJogo já passou uma instância
            print("AVISO: CaixaDeDialogo não está disponível no GerenciadorDeMissoes. Criando uma nova.")
            # self.caixa_dialogo = CaixaDeDialogo(self.gerenciador_recursos) # Descomente se precisar criar aqui

        if self.dialogos_controlados_atuais:
            self.caixa_dialogo.definir_texto(self.dialogos_controlados_atuais[self.indice_dialogo_controlado].fala, self.dialogos_controlados_atuais[self.indice_dialogo_controlado].nome_personagem)
        else:
            print("Nenhum texto para o diálogo controlado.")
            self._finalizar_dialogo_controlado() # Finaliza imediatamente se não houver textos



    def processar_eventos(self, evento):
        """
        Processa inputs relevantes para eventos de missão, como avançar diálogos.
        """
        if self.dialogo_controlado_ativo and self.caixa_dialogo:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if self.caixa_dialogo.esta_digitando:
                        self.caixa_dialogo.pular_digitacao()
                    elif self.caixa_dialogo.esta_finalizado():
                        self.indice_dialogo_controlado += 1
                        if self.indice_dialogo_controlado < len(self.dialogos_controlados_atuais):
                            self.caixa_dialogo.definir_texto(self.dialogos_controlados_atuais[self.indice_dialogo_controlado].fala, self.dialogos_controlados_atuais[self.indice_dialogo_controlado].nome_personagem)
                        else:
                            self._finalizar_dialogo_controlado()
                            self._avancar_passo(self.missao_que_ativou_dialogo) # Avança o script da missão
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if self.caixa_dialogo.aguardando_input and not self.caixa_dialogo.esta_digitando:
                    if evento.button == 4:
                        self.caixa_dialogo.rolar(-1)
                    elif evento.button == 5:
                        self.caixa_dialogo.rolar(1)



    def _finalizar_dialogo_controlado(self):
        self.dialogo_controlado_ativo = False
        self.pausa_geral = False # Libera o script da missão
        self.caixa_dialogo.limpar_dialogo()



    def esta_em_evento_controlado(self):
        """Retorna True se o gerenciador de missões estiver controlando o fluxo (ex: cutscene, diálogo)."""
        return self.missoes_ativas and self.pausa_geral