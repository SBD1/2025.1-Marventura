# gerenciadores/gerenciador_missoes.py

import pygame
import json # Ou outro formato para carregar seus scripts
from utilidades.constantes import * # Importa as constantes
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gerenciadores import DBManager, GerenciadorDeRecursos, GerenciadorDeTelas
    from entidades import Jogador
    from utilidades import Camera
    from telas import TelaJogo
    from componentes import CaixaDeDialogo

class GerenciadorDeMissoes:
    def __init__(self, banco_de_dados: "DBManager", gerenciador_recursos: "GerenciadorDeRecursos", camera: "Camera", jogador: "Jogador", caixa_dialogo: "CaixaDeDialogo", npcs, gerenciador_telas: "GerenciadorDeTelas", tela_jogo: "TelaJogo"):
        self.banco_de_dados = banco_de_dados
        self.gerenciador_recursos = gerenciador_recursos
        self.camera = camera
        self.jogador = jogador
        self.caixa_dialogo = caixa_dialogo # A mesma instância da TelaJogo
        self.npcs = npcs # O grupo de NPCs da TelaJogo
        self.gerenciador_telas = gerenciador_telas # Para mudar de tela se necessário
        self.tela_jogo = tela_jogo # NOVO: Referência à instância da TelaJogo

        self.scripts_missoes = self._carregar_scripts_missoes(self.jogador.nome) # Carrega os scripts do JSON/dicionário
        self.missao_ativa_id = None
        self.script_em_execucao = None
        self.indice_passo_atual = 0
        self.esta_pausado = False # Para pausar o script enquanto um evento (diálogo, movimento) está em andamento

        self.dialogo_controlado_ativo = False # Flag para indicar que o diálogo está sendo controlado por aqui
        self.dialogos_controlados_atuais = []
        self.indice_dialogo_controlado = 0
        
        self.proximo_passo_apos_dialogo_controlado = None # O que fazer depois que o diálogo controlado terminar

        # NOVO: Atributos para controle de movimento
        self.entidade_em_movimento = None
        self.destino_movimento = None
        self.velocidade_movimento_controlado = VELOCIDADE_JOGADOR * 0.8 # Um pouco mais lento para cutscenes


    def _carregar_scripts_missoes(self, nome_jogador):
        """
        Carrega os scripts das missões de um arquivo JSON (ou pode ser um dicionário direto aqui).
        Este é um exemplo. Em um jogo real, você carregaria de um arquivo.
        """
        # Exemplo de dicionário de scripts (pode ser carregado de um JSON)
        return {
            'mis001': [ # Sua primeira missão
                {'tipo': 'cena_dialogo_missao', 'missao_id': 'mis001', 'chave_imagem_cena': CENA_SILVIE_NO_CAMPO if nome_jogador == SILVIE else CENA_SHUAN_NO_CAMPO},
                {'tipo': 'inserir_gatilho_de_missao', 'id_area': 'are001', 'id_missao': 'mis002', 'x': 2560, 'y': 220, 'largura': 180, 'altura': 133}
                # Os passos para focar no jogador e finalizar a missão serão executados
                # automaticamente após o diálogo da cena terminar.
            ],
            'mis002': [
                {'tipo': 'remover_inimigos_da_area', 'area_id': 'are001'},
                {'tipo': 'carregar_inimigo_na_posicao', 'chave_inimigo': 'Lobo', 'x': 2980, 'y': 290, 'id_instancia': 'lobo_missao_002'},
                {'tipo': 'mover_jogador_para', 'x': 2780, 'y': 170},
                {'tipo': 'mover_inimigo_para', 'id_instancia': 'lobo_missao_002', 'x': 2900, 'y': 210},
                {'tipo': 'dialogo', 'missao_id': 'mis002'}, # Precisamos do ID para buscar os diálogos
                {'tipo': 'finalizar_missao'},
                {'tipo': 'remover_gatilho_de_missao', 'id_area': 'are001', 'id_missao': 'mis002', 'x': 2560, 'y': 220, 'largura': 180, 'altura': 133},
                {'tipo': 'inserir_gatilho_de_missao', 'id_area': 'are002', 'id_missao': 'mis003', 'x': 0, 'y': 0, 'largura': 150, 'altura': 600},
                {'tipo': 'batalha', 'inimigos_batalha': ['lobo_missao_002']},
            ],
            'mis003': [
                {'tipo': 'mover_jogador_para', 'x': 1485, 'y': 370},
                {'tipo': 'dialogo', 'missao_id': 'mis003'},
                {'tipo': 'remover_gatilho_de_missao', 'id_area': 'are002', 'id_missao': 'mis003', 'x': 0, 'y': 0, 'largura': 150, 'altura': 600},
                {'tipo': 'finalizar_missao'},
            ]
            # ... outras missões
        }

    def iniciar_missao(self, identificador_missao):
        estado_missao = self.banco_de_dados.buscar_estado_da_missao(identificador_missao, self.jogador.identificador_progresso)

        if estado_missao == 'concluida':
            return

        """Inicia a execução do script de uma missão."""
        if identificador_missao in self.scripts_missoes:
            self.missao_ativa_id = identificador_missao
            self.script_em_execucao = self.scripts_missoes[identificador_missao]
            self.indice_passo_atual = 0
            self.esta_pausado = False
            self.dialogo_controlado_ativo = False
            print(f"Missão '{identificador_missao}' iniciada.")
            # Você pode querer atualizar o estado_missao no banco de dados para 'aceita'
            self.banco_de_dados.atualizar_estado_missao(identificador_missao, self.jogador.identificador_progresso, 'aceita')
        else:
            print(f"Erro: Missão '{identificador_missao}' não encontrada nos scripts.")



    def update(self, dt_ms):
        """
        Atualiza o estado do gerenciador de missões e avança no script.
        :param dt_ms: Delta time em milissegundos.
        """

        # =====================================================================
        #  PRIMEIRO: Verifique e execute o movimento controlado, se houver.
        #  Esta lógica precisa rodar MESMO SE o script estiver "pausado".
        # =====================================================================
        if self.entidade_em_movimento and self.destino_movimento:
            entidade = self.entidade_em_movimento
            destino = self.destino_movimento
            
            direcao = destino - pygame.math.Vector2(entidade.mundo_x, entidade.mundo_y)

            # Checa se a entidade chegou ao destino
            if direcao.length() < 5: # Usamos uma pequena margem de erro
                entidade.mundo_x, entidade.mundo_y = destino.x, destino.y
                entidade.estado = 'parado' # Para a animação
                self.entidade_em_movimento = None
                self.destino_movimento = None
                # IMPORTANTE: O próprio movimento, ao terminar, avança o script
                self._avancar_passo() 
            else:
                # Move a entidade
                direcao.normalize_ip()
                entidade.mundo_x += direcao.x * self.velocidade_movimento_controlado
                entidade.mundo_y += direcao.y * self.velocidade_movimento_controlado
                entidade.estado = 'caminhando' # Ativa a animação de caminhada

                # NOVO E CRUCIAL: Sincronize o rect com as coordenadas de mundo
                entidade.rect.x = int(entidade.mundo_x)
                entidade.rect.y = int(entidade.mundo_y)
                
                # Atualiza a orientação visual da entidade
                if hasattr(entidade, 'orientacao'):
                    entidade.orientacao = 'direita' if direcao.x >= 0 else 'esquerda'
                elif hasattr(entidade, 'olhando_direita'):
                    entidade.olhando_direita = direcao.x >= 0
            
            # Como o movimento está acontecendo, paramos o resto do update desta frame
            return 

        # =====================================================================
        #  SEGUNDO: Agora, verifique as condições de pausa geral (diálogo, etc.)
        # =====================================================================
        if self.missao_ativa_id is None or self.esta_pausado:
            if self.dialogo_controlado_ativo and self.caixa_dialogo:
                self.caixa_dialogo.atualizar()
            return

        # Se há um diálogo controlado ativo, a execução do script está pausada
        if self.dialogo_controlado_ativo:
            self.caixa_dialogo.atualizar()
            return

        # Se o movimento da câmera estiver em andamento, pausa o script
        if self.camera.modo == 'movimento_suave' and not self.camera.is_movimento_suave_completo():
            self.camera.update(dt_ms)
            return

        # =====================================================================
        #  TERCEIRO: Se não há movimento nem pausa, execute o próximo passo
        # =====================================================================
        if self.indice_passo_atual < len(self.script_em_execucao):
            passo = self.script_em_execucao[self.indice_passo_atual]
            self._executar_passo(passo, dt_ms)
        else:
            # Script da missão concluído
            print(f"Script da missão '{self.missao_ativa_id}' concluído.")
            self.missao_ativa_id = None
            self.script_em_execucao = None
            self.indice_passo_atual = 0
            self.esta_pausado = False
            self.camera.retornar_para_jogador()



    def _executar_passo(self, passo, dt_ms):
        """Executa uma única ação do script da missão."""
        tipo_passo = passo['tipo']

        print(f"Executando passo da missão: {tipo_passo}") # Ótimo para debug

        if tipo_passo == 'focar_em_ponto':
            self.camera.focar_em_ponto(passo['x'], passo['y'])
            self._avancar_passo() # Este é instantâneo, então avança imediatamente

        elif tipo_passo == 'remover_inimigos_da_area':
            # Remove inimigos existentes para garantir um cenário limpo
            # A melhor forma é fazer isso na TelaJogo, que controla o grupo de inimigos
            self.tela_jogo.inimigos.empty()
            self._avancar_passo()

        elif tipo_passo == 'carregar_inimigo_na_posicao':
            # Pede para a TelaJogo criar e adicionar o inimigo da missão
            self.tela_jogo.adicionar_inimigo_em_missao(
                passo['chave_inimigo'],
                passo['id_instancia'],
                passo['x'],
                passo['y']
            )
            self._avancar_passo()

        elif tipo_passo == 'mover_jogador_para':
            self.entidade_em_movimento = self.jogador
            self.destino_movimento = pygame.math.Vector2(passo['x'], passo['y'])
            self.esta_pausado = True # Pausa o script até o movimento terminar

        elif tipo_passo == 'mover_inimigo_para':
            # Encontra o inimigo pelo ID de instância que demos a ele
            inimigo_alvo = None
            for inimigo in self.tela_jogo.inimigos:
                if hasattr(inimigo, 'id_instancia') and inimigo.id_instancia == passo['id_instancia']:
                    inimigo_alvo = inimigo
                    break
            
            if inimigo_alvo:
                self.entidade_em_movimento = inimigo_alvo
                self.destino_movimento = pygame.math.Vector2(passo['x'], passo['y'])
                self.esta_pausado = True # Pausa o script
            else:
                print(f"ERRO: Inimigo com ID '{passo['id_instancia']}' não encontrado para mover.")
                self._avancar_passo() # Pula o passo se não encontrar

        elif tipo_passo == 'dialogo':
            # Seu código de diálogo estava quase certo, só precisa do ID da missão
            id_missao = passo['missao_id']
            genero = 'F' if self.jogador.nome == SILVIE else 'M'
            dialogos = self.banco_de_dados.buscar_dialogos_da_missao(id_missao, genero, self.jogador.identificador_jogador)
            if dialogos:
                self.iniciar_dialogo_controlado(dialogos)
                self.proximo_passo_apos_dialogo_controlado = True
            else:
                print(f"AVISO: Nenhum diálogo encontrado para a missão '{id_missao}'. Pulando.")
                self._avancar_passo()
                
        elif tipo_passo == 'batalha':
            # Usa o sistema de transição de tela que você já tem
            print("Iniciando transição para batalha...")
            
            # Encontra os inimigos da batalha na lista de inimigos da tela de jogo
            inimigos_para_batalha = []
            for id_inimigo in passo['inimigos_batalha']:
                for inimigo_sprite in self.tela_jogo.inimigos:
                    if hasattr(inimigo_sprite, 'id_instancia') and inimigo_sprite.id_instancia == id_inimigo:
                        inimigos_para_batalha.append(inimigo_sprite)

            if inimigos_para_batalha:
                self.gerenciador_telas.mudar_tela(
                    CHAVE_TRANSICAO_BATALHA,
                    inimigos_batalha=inimigos_para_batalha,
                    # Adicione quaisquer outros dados que sua tela de batalha precise
                )
                # A missão será finalizada quando a batalha terminar (ver Passo 3)
                self.esta_pausado = True # Pausa a missão até o retorno da batalha
            else:
                print("ERRO: Inimigos para a batalha não foram encontrados.")
                self._avancar_passo()

        elif tipo_passo == 'movimento_camera_suave':
            self.camera.iniciar_movimento_suave(
                self.camera.rect.centerx, self.camera.rect.centery, # Começa da posição atual da câmera
                passo['fim_x'], passo['fim_y'],
                passo['duracao_ms']
            )
            self.esta_pausado = True # Pausa o script até o movimento terminar (será despausado no update)
            # O avanço do passo acontecerá no próximo update, quando o movimento for completo.

        elif tipo_passo == 'focar_jogador':
            self.camera.retornar_para_jogador()
            self._avancar_passo()

        elif tipo_passo == 'recompensa':
            print(f"Recompensa: XP={passo.get('xp', 50)}, Item={passo.get('item_id', 'Nenhum')}")
            # Lógica para adicionar XP e itens ao jogador
            self._avancar_passo()

        elif tipo_passo == 'inserir_gatilho_de_missao':
            self.banco_de_dados.inserir_gatilho_de_missao(passo.get('id_area'), passo.get('id_missao'), passo.get('x'), passo.get('y'), passo.get('largura'), passo.get('altura'))

            self.tela_jogo.atualizar_areas_interativas_passivas()

            self._avancar_passo()

        elif tipo_passo == 'remover_gatilho_de_missao':
            self.banco_de_dados.remover_gatilho_de_missao(passo.get('id_area'), passo.get('id_missao'), passo.get('x'), passo.get('y'), passo.get('largura'), passo.get('altura'))

            self.tela_jogo.atualizar_areas_interativas_passivas()

            self._avancar_passo()
        
        elif tipo_passo == 'ativar_proxima_missao':
            
            self.banco_de_dados.atualizar_estado_missao(passo.get('id_missao'), self.jogador.identificador_progresso, 'aceita')
            self.tela_jogo.gerenciador_entidades.iniciar_missao = self.banco_de_dados.buscar_missoes_aceitas_pelo_jogador(self.jogador.identificador_jogador)[0]
            self._avancar_passo()

        elif tipo_passo == 'finalizar_missao':
            print(f"Missão '{self.missao_ativa_id}' marcada como finalizada.")
            
            self.banco_de_dados.atualizar_estado_missao(self.missao_ativa_id, self.jogador.identificador_progresso, 'concluida')
            self.tela_jogo.gerenciador_entidades.iniciar_missao = None
            self._avancar_passo()

        # NOVO TIPO DE PASSO: Cena estática com diálogo
        elif tipo_passo == 'cena_dialogo_missao':
            missao_id = passo['missao_id']
            chave_imagem_cena = passo['chave_imagem_cena']
            print(f"DEBUG: Executando passo 'cena_dialogo_missao' para a missão '{missao_id}'.")

            # 1. Exibir a cena estática
            self.tela_jogo.ativar_cena_estatica(chave_imagem_cena)

            # 2. Carregar e exibir os diálogos da missão
            genero = 'F' if self.jogador.nome == SILVIE else 'M'
            
            dialogos_da_missao = self.banco_de_dados.buscar_dialogos_da_missao(missao_id, genero, self.jogador.identificador_jogador)
            if dialogos_da_missao:
                print(f"DEBUG: Diálogos encontrados para a missão '{missao_id}': {len(dialogos_da_missao)}.")
                self.iniciar_dialogo_controlado(dialogos_da_missao)
                self.proximo_passo_apos_dialogo_controlado = 'finalizar_cena_e_missao' # Sinaliza a ação a ser feita após o diálogo
                print(f"DEBUG: proximo_passo_apos_dialogo_controlado definido como '{self.proximo_passo_apos_dialogo_controlado}'.")
            else:
                print(f"AVISO: Nenhun diálogo encontrado para a missão '{missao_id}'.")
                
                # Se não houver diálogos, finalizar a cena imediatamente
                self.tela_jogo.desativar_cena_estatica()
                self.camera.retornar_para_jogador()
                self.banco_de_dados.atualizar_estado_missao(self.missao_ativa_id, self.jogador.identificador_progresso, 'concluida')
                self.tela_jogo.gerenciador_entidades.iniciar_missao = None
                self._avancar_passo() # Avança para o próximo passo no script (se houver)


        # Adicione mais tipos de passos conforme necessário:
        # 'mostrar_cena_video', 'spawn_inimigo', 'ativar_area_interacao', etc.


    def _avancar_passo(self):
        """Avança para o próximo passo do script."""
        self.indice_passo_atual += 1
        self.esta_pausado = False # Garante que o script não esteja mais pausado após o avanço
        self.dialogo_controlado_ativo = False # Se avançou, o diálogo anterior terminou
        self.proximo_passo_apos_dialogo_controlado = None

    def iniciar_dialogo_controlado(self, lista_de_textos):
        """Inicia uma sequência de diálogos controlada pelo gerenciador de missões."""
        self.dialogos_controlados_atuais = lista_de_textos
        self.indice_dialogo_controlado = 0
        self.dialogo_controlado_ativo = True
        self.esta_pausado = True # Pausa o script da missão enquanto o diálogo está ativo
        
        # Garante que a caixa de diálogo esteja pronta
        if not self.caixa_dialogo:
            # Isso não deveria acontecer se a TelaJogo já passou uma instância
            print("AVISO: CaixaDeDialogo não está disponível no GerenciadorDeMissoes. Criando uma nova.")
            # self.caixa_dialogo = CaixaDeDialogo(self.gerenciador_recursos) # Descomente se precisar criar aqui

        if self.dialogos_controlados_atuais:
            self.caixa_dialogo.definir_texto(self.dialogos_controlados_atuais[self.indice_dialogo_controlado].dialogo, self.dialogos_controlados_atuais[self.indice_dialogo_controlado].nome_personagem)
        else:
            print("Nenhum texto para o diálogo controlado.")
            self._finalizar_dialogo_controlado() # Finaliza imediatamente se não houver textos


    def handle_input(self, evento):
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
                            self.caixa_dialogo.definir_texto(self.dialogos_controlados_atuais[self.indice_dialogo_controlado].dialogo, self.dialogos_controlados_atuais[self.indice_dialogo_controlado].nome_personagem)
                        else:
                            self._finalizar_dialogo_controlado()
                            if self.proximo_passo_apos_dialogo_controlado == 'finalizar_cena_e_missao':
                                self.tela_jogo.desativar_cena_estatica()
                                self.camera.retornar_para_jogador()
                                self.banco_de_dados.atualizar_estado_missao(self.missao_ativa_id, self.jogador.identificador_progresso, 'concluida')
                                self.tela_jogo.gerenciador_entidades.iniciar_missao = None
                                self._avancar_passo() # Avança o script da missão
                                self.proximo_passo_apos_dialogo_controlado = None # Reseta a flag
                            elif self.proximo_passo_apos_dialogo_controlado:
                                self._avancar_passo() # Avança o script da missão
                                self.proximo_passo_apos_dialogo_controlado = None
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if self.caixa_dialogo.aguardando_input and not self.caixa_dialogo.esta_digitando:
                    if evento.button == 4:
                        self.caixa_dialogo.rolar(-1)
                    elif evento.button == 5:
                        self.caixa_dialogo.rolar(1)

    def _finalizar_dialogo_controlado(self):
        self.dialogo_controlado_ativo = False
        self.esta_pausado = False # Libera o script da missão
        self.caixa_dialogo.limpar_dialogo()

    def esta_em_evento_controlado(self):
        """Retorna True se o gerenciador de missões estiver controlando o fluxo (ex: cutscene, diálogo)."""
        return self.missao_ativa_id is not None and self.esta_pausado