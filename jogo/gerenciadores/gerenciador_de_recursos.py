# gerenciador_de_recursos.py

import pygame
import sys
from utilidades.constantes import *
from utilidades import caminho_absoluto

class GerenciadorDeRecursos:
    """
    Gerencia o carregamento e acesso de recursos do jogo (imagens, fontes, etc.).
    Carrega recursos do disco uma única vez durante a inicialização e os fornece para outras partes do jogo sob demanda.
    Isso centraliza o gerenciamento de assets e melhora o desempenho ao evitar recarregar.
    """
    def __init__(self):
        """Inicializa o gerenciador criando dicionários vazios para armazenar recursos."""
        self._imagens = {} # Dicionário para armazenar imagens carregadas
        self._fontes = {}   # Dicionário para armazenar fontes carregadas
        # Adicionar outros dicionários aqui para outros tipos de recursos (sons, músicas, dados, etc.)

        # Flag para rastrear se todos os recursos marcados como essenciais foram carregados sem erros fatais
        self._carregado_com_sucesso = True

    def _carregar_imagem(self, chave, caminho, escalar_para_tamanho=None, escalar_para_altura=None):
        """
        Carrega uma imagem de um caminho, opcionalmente a redimensiona e a armazena
        sob uma chave identificadora.

        :param chave: Uma string única para identificar esta imagem (ex: 'player_idle', 'fundo_menu').
        :param caminho: O caminho do arquivo da imagem no disco (ex: 'assets/images/player.png').
        :param escalar_para_tamanho: Uma tupla (largura, altura) para redimensionar a imagem para um tamanho fixo.
        :param escalar_para_altura: Um número inteiro para redimensionar a imagem proporcionalmente com base em uma nova altura.
        """
        try:
            imagem = pygame.image.load(caminho_absoluto(caminho)).convert_alpha()

            # Aplicar redimensionamento se especificado
            if escalar_para_tamanho:
                imagem = pygame.transform.scale(imagem, escalar_para_tamanho)
            elif escalar_para_altura is not None and imagem.get_height() > 0:
                 # Redimensionamento proporcional baseado na altura desejada
                 largura_original = imagem.get_width()
                 altura_original = imagem.get_height()
                 # Calcula a nova largura mantendo a proporção (evita divisão por zero)
                 fator_escala = escalar_para_altura / altura_original if altura_original > 0 else 0
                 largura_calculada = int(largura_original * fator_escala)
                 novo_tamanho = (largura_calculada, escalar_para_altura)
                 imagem = pygame.transform.scale(imagem, novo_tamanho)

            # Armazena a imagem carregada (ou redimensionada) no dicionário interno
            self._imagens[chave] = imagem
            print(f"Recurso carregado: Imagem '{chave}' de '{caminho}'")

        except pygame.error as e:
            # Em caso de erro no carregamento ou redimensionamento
            print(f"ERRO ao carregar imagem '{chave}' de '{caminho}': {e}")
            self._imagens[chave] = None # Armazena None para indicar falha, ou pode criar uma imagem de placeholder de erro
            self._carregado_com_sucesso = False # Marca que houve falha no carregamento de um recurso

    def obter_imagem(self, chave):
        """
        Retorna uma imagem carregada anteriormente pelo seu identificador (chave).

        :param chave: A string identificadora da imagem.
        :return: O objeto pygame.Surface da imagem, ou None se a chave não existir
                 ou se o carregamento falhou anteriormente.
        """
        # Retorna a imagem associada à chave, ou None se a chave não estiver no dicionário
        if chave in self._imagens:
            return self._imagens[chave]
        else:
            print(f"AVISO: Imagem '{chave}' não encontrada no gerenciador de recursos. Verifique se foi carregada.")
            return None # Retorna None se a imagem não foi carregada ou a chave está errada

    def _carregar_fonte(self, chave, caminho, tamanho):
        """
        Carrega uma fonte de um caminho com um tamanho específico e a armazena
        sob uma chave identificadora.

        :param chave: Uma string única para identificar esta fonte (ex: 'fonte_botao', 'fonte_titulo').
        :param caminho: O caminho do arquivo da fonte (ex: 'assets/fonts/minha_fonte.ttf').
        :param tamanho: O tamanho da fonte.
        """
        try:
            fonte = pygame.font.Font(caminho_absoluto(caminho), tamanho)

            self._fontes[chave] = fonte
            print(f"Recurso carregado: Fonte '{chave}' de '{caminho}' (tamanho {tamanho})")

        except pygame.error as e:
            # Em caso de erro no carregamento da fonte
            print(f"ERRO ao carregar fonte '{chave}' de '{caminho}' (tamanho {tamanho}): {e}")
            # Fallback para uma fonte do sistema em caso de falha no carregamento da fonte específica
            try:
                 fonte_fallback = pygame.font.SysFont("Arial", tamanho) # Tenta Arial com o tamanho desejado
                 self._fontes[chave] = fonte_fallback
                 print(f"Usando fonte de sistema 'Arial' como fallback para '{chave}'.")
            except pygame.error as fallback_e:
                 print(f"ERRO: Falha no fallback para fonte 'Arial' para '{chave}': {fallback_e}")
                 self._fontes[chave] = None # Último recurso: armazena None se nem o fallback funcionar
                 self._carregado_com_sucesso = False # Marca falha grave


    def obter_fonte(self, chave):
        """
        Retorna uma fonte carregada anteriormente pelo seu identificador (chave).

        :param chave: A string identificadora da fonte.
        :return: O objeto pygame.font.Font da fonte, ou um fallback genérico
                 se a chave não existir ou se o carregamento falhou.
        """
        # Retorna a fonte associada à chave, ou um fallback genérico se a chave não existir ou o carregamento falhou
        if chave in self._fontes and self._fontes[chave] is not None:
            return self._fontes[chave]
        else:
            print(f"AVISO: Fonte '{chave}' não encontrada ou falhou no carregamento. Usando fallback genérico.")
            return pygame.font.Font(None, 30)
            
    def carregar_recursos(self):
        """
        Carrega todos os recursos do jogo (fontes, imagens, etc.).
        Este método centraliza todas as chamadas de carregamento.
        """
        print("Iniciando carregamento de todos os recursos...")

        # --- Carregar Fontes ---
        #caminho_arquivo_fonte_coliner = 'recursos/fontes/Coliner-Regular.ttf'
        caminho_arquivo_fonte_coliner = 'recursos/fontes/Coliner-Bold.ttf'
        caminho_arquivo_fonte_always = 'recursos/fontes/Always In My Heart.ttf'
        caminho_arquivo_fonte_playfair = 'recursos/fontes/PlayfairDisplay-Regular.ttf'
        self._carregar_fonte(CHAVE_FONTE_COLINER_TITULO, caminho_arquivo_fonte_coliner, 70)       # Fonte para títulos grandes
        self._carregar_fonte(CHAVE_FONTE_COLINER_BOTAO, caminho_arquivo_fonte_coliner, 48)     # Fonte para botões
        self._carregar_fonte(CHAVE_FONTE_COLINER_TEXTO, caminho_arquivo_fonte_coliner, 20)     # Fonte para botões
        self._carregar_fonte(CHAVE_FONTE_PAYFAIR_TEXTO, caminho_arquivo_fonte_playfair, 20)  # Fonte para nome no cartaz
        self._carregar_fonte(CHAVE_FONTE_HEART_TEXTO, caminho_arquivo_fonte_always, 15)   # Fonte para data/dados no cartaz

        # --- Carregar Imagens de Interface e Fundos ---
        self._carregar_imagem(CHAVE_TELA_INICIAL, 'recursos/imagens/cenario/tela_inicial.png', escalar_para_tamanho=(LARGURA_TELA, ALTURA_TELA))
        self._carregar_imagem(CHAVE_LOGO, 'recursos/imagens/interface/logo.png')
        self._carregar_imagem(CHAVE_CARTAZ_PROCURADA, 'recursos/imagens/interface/cartaz_de_procurado_menina.png')
        self._carregar_imagem(CHAVE_CARTAZ_PROCURADO, 'recursos/imagens/interface/cartaz_de_procurado_menino.png')
        self._carregar_imagem(CHAVE_CARTAZ_VAZIO, 'recursos/imagens/interface/cartaz_de_procurado_vazio.png')
        #self._carregar_imagem('mapa_mundi', 'recursos/imagens/interface/mapa_mundi.jpg')

        # --- Carregar planos de fundo para os mapas do jogo ---
        self._carregar_imagem(CHAVE_CENARIO_CAMPO_COSTA_OESTE, 'recursos/imagens/cenario/ilha_campo_costa_oeste.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CAMPO_COSTA_LESTE, 'recursos/imagens/cenario/ilha_campo_costa_leste.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CAMPO_COSTA_OESTE_CAMADA_SUPERIOR, 'recursos/imagens/cenario/ilha_campo_costa_oeste-camada_superior.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CAMPO_VILA, 'recursos/imagens/cenario/ilha_campo_vila.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CIDADE_PORTO, 'recursos/imagens/cenario/ilha_cidade_porto.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CIDADE_PORTO_CAMADA_SUPERIOR, 'recursos/imagens/cenario/ilha_cidade_porto-camada_superior.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CIDADE_CENTRO, 'recursos/imagens/cenario/ilha_cidade_centro.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CIDADE_PRACA, 'recursos/imagens/cenario/ilha_cidade_praça.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CIDADE_PRACA_CAMADA_SUPERIOR, 'recursos/imagens/cenario/ilha_cidade_praça-camada_superior.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_NEVE_COSTA, 'recursos/imagens/cenario/ilha_neve_costa.png')
        self._carregar_imagem(CHAVE_CENARIO_NEVE_VILA, 'recursos/imagens/cenario/ilha_neve_vila.png')
        self._carregar_imagem(CHAVE_CENARIO_NEVE_FLORESTA, 'recursos/imagens/cenario/ilha_neve_floresta.png')
        self._carregar_imagem(CHAVE_CENARIO_NEVE_FLORESTA_CAMADA_SUPERIOR, 'recursos/imagens/cenario/ilha_neve_floresta-camada_superior.png')
        self._carregar_imagem(CHAVE_CENARIO_NEVE_MONTANHA, 'recursos/imagens/cenario/ilha_neve_montanha.png')
        self._carregar_imagem(CHAVE_LOJA_INTERIOR, 'recursos/imagens/cenario/loja_interior.png')
        self._carregar_imagem(CHAVE_COZINHA_INTERIOR, 'recursos/imagens/cenario/cozinha_interior.png')


        # --- Carregar Imagens do Jogador para Animação ---
        self._carregar_imagem(SHUAN, 'recursos/imagens/jogador/Shuan_pose-descanso.png', escalar_para_altura=300)
        self._carregar_imagem(SILVIE, 'recursos/imagens/jogador/Silvie_pose-descanso.png', escalar_para_altura=300)

        self._carregar_imagem(f'{SHUAN}_em_repouso', 'recursos/imagens/jogador/Shuan_pose-descanso.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SHUAN}_caminhando_1', 'recursos/imagens/jogador/Shuan_pose-caminhada-direito.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SHUAN}_caminhando_2', 'recursos/imagens/jogador/Shuan_pose-caminhada.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SHUAN}_caminhando_3', 'recursos/imagens/jogador/Shuan_pose-caminhada-esquerdo.png', escalar_para_altura=120)

        self._carregar_imagem(f'{SILVIE}_em_repouso', 'recursos/imagens/jogador/Silvie_pose-descanso.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SILVIE}_caminhando_1', 'recursos/imagens/jogador/Silvie_pose-caminhada-direito.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SILVIE}_caminhando_2', 'recursos/imagens/jogador/Silvie_pose-caminhada.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SILVIE}_caminhando_3', 'recursos/imagens/jogador/Silvie_pose-caminhada-esquerdo.png', escalar_para_altura=120)

        # --- Carregar Imagens dos Inimigos ---
        self._carregar_imagem(f"{INIMIGO_LOBO}_0", 'recursos/imagens/inimigos/Lobo_0.png', escalar_para_altura=80)
        self._carregar_imagem(f"{INIMIGO_LOBO}_1", 'recursos/imagens/inimigos/Lobo_1.png', escalar_para_altura=80)
        self._carregar_imagem(f"{INIMIGO_LOBO}_2", 'recursos/imagens/inimigos/Lobo_2.png', escalar_para_altura=80)
        self._carregar_imagem(f"{INIMIGO_CORVO}_0", 'recursos/imagens/inimigos/Corvo_0.png', escalar_para_altura=60)
        self._carregar_imagem(f"{INIMIGO_CORVO}_1", 'recursos/imagens/inimigos/Corvo_1.png', escalar_para_altura=60)

        # --- Carregar Ícone de Interação ---
        self._carregar_imagem(CHAVE_ICONE_INTERACAO, 'recursos/imagens/icones/icone_interacao.png', escalar_para_altura=48)
        self._carregar_imagem(CHAVE_ICONE_ALERTA, 'recursos/imagens/icones/alerta.png', escalar_para_altura=48)
        self._carregar_imagem(CHAVE_ICONE_INTERROGACAO, 'recursos/imagens/icones/interrogacao.png', escalar_para_altura=48)
        self._carregar_imagem(CHAVE_MARCADOR_MAPA_SILVIE, 'recursos/imagens/icones/marcador_mapa_silvie.png', escalar_para_altura=48)

        if not self._tudo_carregado_com_sucesso():
            print("Recursos críticos falharam ao carregar. Saindo.")
            pygame.quit()
            sys.exit()

    def _tudo_carregado_com_sucesso(self):
        """
        Verifica se todos os recursos carregados marcaram sucesso.
        (Nesta versão simples, apenas verifica se a flag _carregado_com_sucesso é True).
        Em um gerenciador mais complexo, poderia verificar recursos marcados como "críticos".

        :return: True se não houve erros durante o carregamento, False caso contrário.
        """
        return self._carregado_com_sucesso
