# gerenciadores/gerenciador_missoes.py

import pygame
import json # Ou outro formato para carregar seus scripts
from utilidades.constantes import * # Importa as constantes

class GerenciadorDeMissoes:
    def __init__(self, banco_de_dados, gerenciador_recursos, camera, jogador, caixa_dialogo, npcs, gerenciador_telas, tela_jogo):
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


    def _carregar_scripts_missoes(self, nome_jogador):
        """
        Carrega os scripts das missões de um arquivo JSON (ou pode ser um dicionário direto aqui).
        Este é um exemplo. Em um jogo real, você carregaria de um arquivo.
        """
        # Exemplo de dicionário de scripts (pode ser carregado de um JSON)
        return {
            'mis001': [ # Sua primeira missão
                {'tipo': 'cena_dialogo_missao', 'missao_id': 'mis001', 'chave_imagem_cena': CENA_SILVIE_NO_CAMPO if nome_jogador == SILVIE else CENA_SHUAN_NO_CAMPO},
                # Os passos para focar no jogador e finalizar a missão serão executados
                # automaticamente após o diálogo da cena terminar.
            ],
            'mis002': [
                {'tipo': 'focar_em_ponto', 'x': 500, 'y': 100},
                {'tipo': 'dialogo', 'textos': ["Encontrei o baú perdido!", "Mas está trancado...", "Preciso da chave sagrada."]},
                {'tipo': 'retornar_para_jogador'}
            ]
            # ... outras missões
        }

    def iniciar_missao(self, identificador_missao):
        """Inicia a execução do script de uma missão."""
        if identificador_missao in self.scripts_missoes:
            self.missao_ativa_id = identificador_missao
            self.script_em_execucao = self.scripts_missoes[identificador_missao]
            self.indice_passo_atual = 0
            self.esta_pausado = False
            self.dialogo_controlado_ativo = False
            print(f"Missão '{identificador_missao}' iniciada.")
            # Você pode querer atualizar o estado_missao no banco de dados para 'aceita'
            # self.banco_de_dados.atualizar_estado_missao(identificador_missao, self.jogador.identificador_progresso, 'aceita')
        else:
            print(f"Erro: Missão '{identificador_missao}' não encontrada nos scripts.")

    def atualizar(self, dt_ms):
        """
        Atualiza o estado do gerenciador de missões e avança no script.
        :param dt_ms: Delta time em milissegundos.
        """
        if self.missao_ativa_id is None or self.esta_pausado:
            if self.dialogo_controlado_ativo and self.caixa_dialogo:
                self.caixa_dialogo.atualizar() # Garante que o diálogo continue a ser atualizado
            return

        # Se há um diálogo controlado ativo, a execução do script está pausada
        if self.dialogo_controlado_ativo:
            self.caixa_dialogo.atualizar()
            return # A lógica de avanço do diálogo está no processar_eventos

        # Se o movimento da câmera estiver em andamento, pausa o script
        if self.camera.modo == 'movimento_suave' and not self.camera.is_movimento_suave_completo():
            self.camera.update(dt_ms) # A câmera se atualiza
            return # Pausa o avanço do script até o movimento terminar

        # Executa o passo atual do script
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
            # Pode ativar a próxima missão, dar recompensas, etc.
            self.camera.retornar_para_jogador() # Retorna a câmera para o jogador ao fim da missão

    def _executar_passo(self, passo, dt_ms):
        """Executa uma única ação do script da missão."""
        tipo_passo = passo['tipo']

        if tipo_passo == 'focar_em_ponto':
            self.camera.focar_em_ponto(passo['x'], passo['y'])
            self._avancar_passo() # Este é instantâneo, então avança imediatamente

        elif tipo_passo == 'dialogo':
            self.iniciar_dialogo_controlado(passo['textos'])
            # O avanço do passo acontecerá após o diálogo terminar,
            # em processar_eventos quando o usuário pressionar espaço no último texto.
            self.proximo_passo_apos_dialogo_controlado = True # Sinaliza para avançar o passo do script depois

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
            print(f"Recompensa: XP={passo.get('xp', 0)}, Item={passo.get('item_id', 'Nenhum')}")
            # Lógica para adicionar XP e itens ao jogador
            self._avancar_passo()
        
        elif tipo_passo == 'finalizar_missao':
            print(f"Missão '{self.missao_ativa_id}' marcada como finalizada.")
            # Atualizar estado_missao no banco de dados para 'concluida'
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
            
            dialogos_da_missao = self.banco_de_dados.buscar_dialogos_da_missao(missao_id, genero)
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


    def processar_eventos(self, evento):
        """
        Processa inputs relevantes para eventos de missão, como avançar diálogos.
        """
        if self.dialogo_controlado_ativo and self.caixa_dialogo:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if self.caixa_dialogo.esta_digitando:
                        print("DEBUG: Pressionado ESPAÇO - pulando digitação do diálogo.")
                        self.caixa_dialogo.pular_digitacao()
                    elif self.caixa_dialogo.esta_finalizado():
                        print("DEBUG: Pressionado ESPAÇO - diálogo atual finalizado.")
                        self.indice_dialogo_controlado += 1
                        if self.indice_dialogo_controlado < len(self.dialogos_controlados_atuais):
                            print(f"DEBUG: Avançando para o diálogo {self.indice_dialogo_controlado + 1}/{len(self.dialogos_controlados_atuais)}.")
                            self.caixa_dialogo.definir_texto(self.dialogos_controlados_atuais[self.indice_dialogo_controlado].dialogo, self.dialogos_controlados_atuais[self.indice_dialogo_controlado].nome_personagem)
                        else:
                            print(f"DEBUG: Avançando para o diálogo {self.indice_dialogo_controlado + 1}/{len(self.dialogos_controlados_atuais)}.")
                            self._finalizar_dialogo_controlado()
                            if self.proximo_passo_apos_dialogo_controlado == 'finalizar_cena_e_missao':
                                print("DEBUG: Condição 'finalizar_cena_e_missao' ATENDIDA.")
                                print("Diálogo da cena de missão terminado. Finalizando cena e missão.")
                                self.tela_jogo.desativar_cena_estatica()
                                self.camera.retornar_para_jogador()
                                #self.banco_de_dados.atualizar_estado_missao(self.missao_ativa_id, self.jogador.identificador_progresso, 'concluida')
                                self._avancar_passo() # Avança o script da missão
                                self.proximo_passo_apos_dialogo_controlado = None # Reseta a flag
                            elif self.proximo_passo_apos_dialogo_controlado:
                                print(f"DEBUG: Condição {self.proximo_passo_apos_dialogo_controlado} ATENDIDA. Avançando passo do script.")
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