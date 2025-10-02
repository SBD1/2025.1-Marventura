# gerenciador_de_recursos.py

import pygame
import sys
from utilidades.constantes import *
from utilidades import caminho_absoluto
TAMANHO_TITULO = int(ALTURA_TELA * 0.06)    # por ex: 64px em 1080p
TAMANHO_BOTAO = int(ALTURA_TELA * 0.045)    # por ex: 48px
TAMANHO_TEXTO = int(ALTURA_TELA * 0.028)    # por ex: 30px
TAMANHO_TEXTO_PEQUENO = int(ALTURA_TELA * 0.02)  # por ex: 20px
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
        self._sons = {}
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
            #print(f"Recurso carregado: Imagem '{chave}' de '{caminho}'")

        except pygame.error as e:
            # Em caso de erro no carregamento ou redimensionamento
            print(f"ERRO ao carregar imagem '{chave}' de '{caminho}': {e}")
            self._imagens[chave] = None # Armazena None para indicar falha, ou pode criar uma imagem de placeholder de erro
            self._carregado_com_sucesso = False # Marca que houve falha no carregamento de um recurso

    def obter_imagem(self, chave) -> pygame.surface.Surface:
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
        try:
            # Esta chamada agora vai funcionar perfeitamente!
            caminho_final = caminho_absoluto(caminho)
            #print(f"Tentando carregar fonte de: {caminho_final}") # Linha de debug
            fonte = pygame.font.Font(caminho_final, tamanho)
            self._fontes[chave] = fonte

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

    def _carregar_som(self, chave, caminho):
        """Carrega um arquivo de som e o armazena sob uma chave."""
        try:
            som = pygame.mixer.Sound(caminho_absoluto(caminho))
            self._sons[chave] = som
            #print(f"Recurso carregado: Som '{chave}' de '{caminho}'")
        except pygame.error as e:
            print(f"ERRO ao carregar som '{chave}' de '{caminho}': {e}")
            self._sons[chave] = None
            # Não marcamos como falha crítica, o jogo pode rodar sem som
    
    def obter_som(self, chave) -> pygame.mixer.Sound:
        """Retorna um som carregado anteriormente."""
        if chave in self._sons:
            return self._sons[chave]
        else:
            print(f"AVISO: Som '{chave}' não encontrado.")
            return None
    
    def obter_fonte(self, chave) -> pygame.font.Font:
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
        #print("Iniciando carregamento de todos os recursos...")
        
        # --- Carregar Fontes ---
        #caminho_arquivo_fonte_coliner = 'recursos/fontes/Coliner-Regular.ttf'
        caminho_arquivo_fonte_coliner = 'recursos/fontes/Coliner-Bold.ttf'
        caminho_arquivo_fonte_always = 'recursos/fontes/Always In My Heart.ttf'
        caminho_arquivo_fonte_playfair = 'recursos/fontes/PlayfairDisplay-Regular.ttf'
        fonte_cherry = 'recursos/fontes/CherryBombOne-Regular.ttf'
        self._carregar_fonte(CHAVE_FONTE_COLINER_TITULO, caminho_arquivo_fonte_coliner, TAMANHO_TITULO)       # Fonte para títulos grandes
        self._carregar_fonte(CHAVE_FONTE_COLINER_BOTAO, caminho_arquivo_fonte_coliner, TAMANHO_BOTAO)     # Fonte para botões
        self._carregar_fonte(CHAVE_FONTE_COLINER_TEXTO, caminho_arquivo_fonte_coliner, TAMANHO_TEXTO)     # Fonte para botões
        self._carregar_fonte(CHAVE_FONTE_PAYFAIR_TEXTO, caminho_arquivo_fonte_playfair, TAMANHO_TEXTO)  # Fonte para nome no cartaz
        self._carregar_fonte(CHAVE_FONTE_HEART_TEXTO, caminho_arquivo_fonte_always, 15)   # Fonte para data/dados no cartaz
        self._carregar_fonte(CHAVE_FONTE_CHERRY_TITULO, fonte_cherry, 48)          # Fonte para barra de estado
        self._carregar_fonte(CHAVE_FONTE_CHERRY_SUBTITULO, fonte_cherry, 32)       # Fonte para barra de estado
        self._carregar_fonte(CHAVE_FONTE_CHERRY_TEXTO, fonte_cherry, 24)           # Fonte para textos gerais
        fonte_hachi_maru_texto = 'recursos/fontes/HachiMaruPop-Regular.ttf'
        self._carregar_fonte(CHAVE_FONTE_HACHI_MARU_TEXTO, fonte_hachi_maru_texto, 20)           # Fonte para textos gerais

        # --- Carregar Imagens de Interface e Fundos ---
        self._carregar_imagem(CHAVE_TELA_INICIAL, 'recursos/imagens/cenario/tela_inicial.png', escalar_para_tamanho=(LARGURA_TELA, ALTURA_TELA))
        self._carregar_imagem(CHAVE_LOGO, 'recursos/imagens/interface/logo.png')
        self._carregar_imagem(CHAVE_CARTAZ_PROCURADA, 'recursos/imagens/interface/cartaz_de_procurado_menina.png')
        self._carregar_imagem(CHAVE_CARTAZ_PROCURADO, 'recursos/imagens/interface/cartaz_de_procurado_menino.png')
        self._carregar_imagem(CHAVE_CARTAZ_VAZIO, 'recursos/imagens/interface/cartaz_de_procurado_vazio.png')
        self._carregar_imagem(CHAVE_CAIXA_DIALOGO, 'recursos/imagens/interface/caixa_de_dialogo.png')
        self._carregar_imagem(CHAVE_BARRA_DE_ESTADO, 'recursos/imagens/interface/barra_de_estado.png')
        self._carregar_imagem(CHAVE_CAIXA_DE_TEXTO, 'recursos/imagens/interface/caixa_de_texto.png')
        self._carregar_imagem(CHAVE_MENU_ESTRATEGIAS, 'recursos/imagens/interface/menu_estrategias.png')
        self._carregar_imagem(CHAVE_MENU_ITENS, 'recursos/imagens/interface/menu_itens.png')
        self._carregar_imagem(CHAVE_MENU_SELECAO_HABILIDADE, 'recursos/imagens/interface/caixa_de_habilidades.png')
        self._carregar_imagem(ABA_LATERAL_COZINHAR, 'recursos/imagens/interface/cozinha.png')
        self._carregar_imagem(ABA_LATERAL_COZINHAR_ATIVO, 'recursos/imagens/interface/cozinha_ativo.png')
        self._carregar_imagem(ABA_LATERAL_RECEITAS, 'recursos/imagens/interface/receitas.png')
        self._carregar_imagem(ABA_LATERAL_RECEITAS_ATIVO, 'recursos/imagens/interface/receitas_ativo.png')
        self._carregar_imagem(PAINEL_RECEITAS, 'recursos/imagens/interface/painel_receitas.png')
        self._carregar_imagem(ITEM_GENERICO, 'recursos/imagens/itens/item_generico.png')
        self._carregar_imagem(ETIQUETA, 'recursos/imagens/interface/etiqueta.png')
        self._carregar_imagem(SLOT_INGREDIENTE_VAZIO, 'recursos/imagens/interface/espaco_ingrediente.png')
        self._carregar_imagem(BOTAO_COZINHAR_ATIVO, 'recursos/imagens/interface/panela.png')
        self._carregar_imagem(BOTAO_COZINHAR_INATIVO, 'recursos/imagens/interface/panela_inativo.png')
        
        # --- Carregar planos de fundo para os mapas do jogo ---
        self._carregar_imagem(CHAVE_CENARIO_CAMPO_COSTA_OESTE, 'recursos/imagens/cenario/ilha_campo_costa_oeste.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CAMPO_COSTA_LESTE, 'recursos/imagens/cenario/ilha_campo_costa_leste.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CAMPO_COSTA_OESTE_CAMADA_SUPERIOR, 'recursos/imagens/cenario/ilha_campo_costa_oeste-camada_superior.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_CENARIO_CAMPO_COSTA_LESTE_CAMADA_SUPERIOR, 'recursos/imagens/cenario/ilha_campo_costa_leste-camada_superior.png', escalar_para_altura=ALTURA_TELA)
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
        self._carregar_imagem(CHAVE_BARRACA, 'recursos/imagens/cenario/barraca.png')
        self._carregar_imagem(CHAVE_LOJA_INTERIOR, 'recursos/imagens/cenario/loja_interior.png')
        self._carregar_imagem(CHAVE_LOJA_ARMAS_E_ACESSORIOS_INTERIOR, 'recursos/imagens/cenario/loja_armas_e_acessorios_interior.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CHAVE_COZINHA_INTERIOR, 'recursos/imagens/cenario/cozinha_interior.png')
        self._carregar_imagem(CHAVE_CENARIO_OCEANO, 'recursos/imagens/cenario/oceano.png')

        # --- Carregar Imagens de Componentes do Inventário ---
        self._carregar_imagem(INV_PAINEL_FUNDO, 'recursos/imagens/mochila/painel_fundo.png')
        self._carregar_imagem(INV_BOTAO_FECHAR, 'recursos/imagens/mochila/fechar.png')
        self._carregar_imagem(INV_LATERAL_ESTADO, 'recursos/imagens/mochila/estado.png')
        self._carregar_imagem(INV_LATERAL_ESTADO_ATIVO, 'recursos/imagens/mochila/estado_ativo.png')
        self._carregar_imagem(INV_LATERAL_ARMA, 'recursos/imagens/mochila/arma.png')
        self._carregar_imagem(INV_LATERAL_ARMA_ATIVO, 'recursos/imagens/mochila/arma_ativo.png')
        self._carregar_imagem(INV_LATERAL_ACESSORIO, 'recursos/imagens/mochila/acessorio.png')
        self._carregar_imagem(INV_LATERAL_ACESSORIO_ATIVO, 'recursos/imagens/mochila/acessorio_ativo.png')
        self._carregar_imagem(INV_LATERAL_CONSUMIVEL, 'recursos/imagens/mochila/consumivel.png')
        self._carregar_imagem(INV_LATERAL_CONSUMIVEL_ATIVO, 'recursos/imagens/mochila/consumivel_ativo.png')
        self._carregar_imagem(INV_LATERAL_ESPECIAL, 'recursos/imagens/mochila/especiais.png')
        self._carregar_imagem(INV_LATERAL_ESPECIAL_ATIVO, 'recursos/imagens/mochila/especiais_ativo.png')
        self._carregar_imagem(INV_PAINEL_ITENS, 'recursos/imagens/mochila/painel_itens.png')
        self._carregar_imagem(INV_VAZIO, 'recursos/imagens/mochila/vazio.png')
        self._carregar_imagem(FILTRO_ESPADA, 'recursos/imagens/mochila/filtro_espadas.png')
        self._carregar_imagem(FILTRO_PROJETIL, 'recursos/imagens/mochila/filtro_projeteis.png')
        self._carregar_imagem(FILTRO_CONSUMIVEL, 'recursos/imagens/mochila/filtro_consumiveis.png')
        self._carregar_imagem(FILTRO_NAO_CONSUMIVEL, 'recursos/imagens/mochila/filtro_nao_consumiveis.png')
        self._carregar_imagem(FILTRO_ESPECIAL, 'recursos/imagens/mochila/filtro_especiais.png')
        self._carregar_imagem(FILTRO_ACESSORIO, 'recursos/imagens/mochila/filtro_acessorios.png')
        self._carregar_imagem(ESTATISTICA_SILVIE, 'recursos/imagens/mochila/estatistica_silvie.png')
        self._carregar_imagem(ESTATISTICA_SHUAN, 'recursos/imagens/mochila/estatistica_shuan.png')
        self._carregar_imagem(MENU_INFO, 'recursos/imagens/mochila/menu_info.png')
        self._carregar_imagem(INV_BOTAO_USAR, 'recursos/imagens/mochila/botao.png')

        # --- Carregar imagens de Componetes de Mapa ---
        self._carregar_imagem(CHAVE_MARCADOR_MAPA_SILVIE, 'recursos/imagens/icones/marcador_mapa_silvie.png', escalar_para_altura=48)
        self._carregar_imagem(CHAVE_MARCADOR_MAPA_SHUAN, 'recursos/imagens/icones/marcador_mapa_shuan.png', escalar_para_altura=48)
        self._carregar_imagem(ICONE_ILHA_ASSOMBRADA, 'recursos/imagens/mapa/assombrada.png')
        self._carregar_imagem(ICONE_ILHA_CAMPOS, 'recursos/imagens/mapa/campos.png')
        self._carregar_imagem(ICONE_ILHA_CIDADE, 'recursos/imagens/mapa/cidade.png')
        self._carregar_imagem(ICONE_ILHA_DESERTO, 'recursos/imagens/mapa/deserto.png')
        self._carregar_imagem(ICONE_ILHA_FORTALEZA, 'recursos/imagens/mapa/fortaleza.png')
        self._carregar_imagem(ICONE_ILHA_NEVE, 'recursos/imagens/mapa/neve.png')
        self._carregar_imagem(CHAVE_IMAGEM_MAPA_FUNDO, 'recursos/imagens/mapa/mapa.png')
        self._carregar_imagem(ICONE_NUVEM_ASSOMBRADA, 'recursos/imagens/mapa/nuvem_assombrada.png')
        self._carregar_imagem(ICONE_NUVEM_CIDADE, 'recursos/imagens/mapa/nuvem_cidade.png')
        self._carregar_imagem(ICONE_NUVEM_DESERTO, 'recursos/imagens/mapa/nuvem_deserto.png')
        self._carregar_imagem(ICONE_NUVEM_FORTALEZA, 'recursos/imagens/mapa/nuvem_fortaleza.png')
        self._carregar_imagem(ICONE_NUVEM_NEVE, 'recursos/imagens/mapa/nuvem_neve.png')
        self._carregar_imagem(ROTA_ASSOMBRADA_FORTALEZA, 'recursos/imagens/mapa/rota_assombrada-fortaleza.png')
        self._carregar_imagem(ROTA_CAMPOS_CIDADE, 'recursos/imagens/mapa/rota_campos-cidade.png')
        self._carregar_imagem(ROTA_CAMPOS_DESERTO, 'recursos/imagens/mapa/rota_campos-deserto.png')
        self._carregar_imagem(ROTA_CIDADE_FORTALEZA, 'recursos/imagens/mapa/rota_cidade-fortaleza.png')
        self._carregar_imagem(ROTA_CIDADE_NEVE, 'recursos/imagens/mapa/rota_cidade-neve.png')
        self._carregar_imagem(ROTA_NEVE_DESERTO, 'recursos/imagens/mapa/rota_neve-deserto.png')
        self._carregar_imagem(ROTA_NEVE_ASSOMBRADA, 'recursos/imagens/mapa/rota_neve-assombrada.png')

        

        self._carregar_som(SOM_COMPRA_SUCESSO, 'recursos/audio/compra_sucesso.mp3') 
        self._carregar_som(SOM_COMPRA_FALHA, 'recursos/audio/compra_falha.mp3')
     
        self._carregar_imagem(CENA_SILVIE_NO_CAMPO, 'recursos/imagens/cenas/cena_silvie_no_campo.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CENA_SHUAN_NO_CAMPO, 'recursos/imagens/cenas/cena_shuan_no_campo.png', escalar_para_altura=ALTURA_TELA)
        self._carregar_imagem(CENA_JANTAR_COMUNITARIO, 'recursos/imagens/cenas/cena_jantar_comunitario.png', escalar_para_altura=ALTURA_TELA)
        
        # --- Carregar Imagens de Campos de Batalha ---
        self._carregar_imagem(CHAVE_CAMPO_DE_BATALHA_CAMPOS, 'recursos/imagens/cenario/campo_de_batalha_campos.png')
        self._carregar_imagem(CHAVE_CAMPO_DE_BATALHA_CIDADE, 'recursos/imagens/cenario/campo_de_batalha_cidade.png')
        self._carregar_imagem(CHAVE_CAMPO_DE_BATALHA_NEVE, 'recursos/imagens/cenario/campo_de_batalha_neve.png')

        # --- Carregar Imagens de Ações em Batalhas ---
        self._carregar_imagem(CHAVE_ACAO_ESTRATEGIAS, 'recursos/imagens/interface/balao_de_estrategias.png', escalar_para_altura=100)
        self._carregar_imagem(CHAVE_ACAO_MOCHILA, 'recursos/imagens/interface/balao_de_inventario.png', escalar_para_altura=100)
        self._carregar_imagem(CHAVE_ACAO_FRUTA, 'recursos/imagens/interface/balao_de_fruta.png', escalar_para_altura=100)
        self._carregar_imagem(CHAVE_ACAO_SOCO_SILVIE, 'recursos/imagens/interface/balao_de_soco_silvie.png', escalar_para_altura=100)
        self._carregar_imagem(CHAVE_ACAO_SOCO_SHUAN, 'recursos/imagens/interface/balao_de_soco_shuan.png', escalar_para_altura=100)
        self._carregar_imagem(CHAVE_ACAO_ESPADA, 'recursos/imagens/interface/balao_de_espadas.png', escalar_para_altura=100)
        self._carregar_imagem(CHAVE_ACAO_PROJETIL, 'recursos/imagens/interface/balao_de_projeteis.png', escalar_para_altura=100)

        # --- Carregar Imagens de Ícones ---
        self._carregar_imagem(CHAVE_ICONE_CORACAO, 'recursos/imagens/icones/coracao.png', escalar_para_altura=48)
        self._carregar_imagem(CHAVE_ICONE_ENERGIA, 'recursos/imagens/icones/energia.png', escalar_para_altura=48)
        self._carregar_imagem(CHAVE_ICONE_MOEDA, 'recursos/imagens/icones/moeda.png', escalar_para_altura=48)
        self._carregar_imagem(CHAVE_ICONE_CEGUEIRA, 'recursos/imagens/icones/efeito_cegueira.png')
        self._carregar_imagem(CHAVE_ICONE_CONGELADO, 'recursos/imagens/icones/efeito_congelado.png')
        self._carregar_imagem(CHAVE_ICONE_ELETRIFICADO, 'recursos/imagens/icones/efeito_eletrificado.png')
        self._carregar_imagem(CHAVE_ICONE_ENVENENADO, 'recursos/imagens/icones/efeito_envenenado.png')
        self._carregar_imagem(CHAVE_ICONE_MOLHADO, 'recursos/imagens/icones/efeito_molhado.png')
        self._carregar_imagem(CHAVE_ICONE_QUEIMADURA, 'recursos/imagens/icones/efeito_queimadura.png')
        self._carregar_imagem(CHAVE_ICONE_SANGRAMENTO, 'recursos/imagens/icones/efeito_sangramento.png')
        self._carregar_imagem(CHAVE_ICONE_TONTURA, 'recursos/imagens/icones/efeito_tontura.png')

        # --- Carregar Imagens do Jogador para Animação ---
        self._carregar_imagem(SHUAN, 'recursos/imagens/jogador/Shuan_pose-descanso.png', escalar_para_altura=300)
        self._carregar_imagem(SILVIE, 'recursos/imagens/jogador/Silvie_pose-descanso.png', escalar_para_altura=300)
        self._carregar_imagem(f'{SHUAN}_em_repouso', 'recursos/imagens/jogador/Shuan_pose-descanso.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SHUAN}_caminhando_1', 'recursos/imagens/jogador/Shuan_pose-caminhada-direito.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SHUAN}_caminhando_2', 'recursos/imagens/jogador/Shuan_pose-caminhada.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SHUAN}_caminhando_3', 'recursos/imagens/jogador/Shuan_pose-caminhada-esquerdo.png', escalar_para_altura=120)
        
        self._carregar_imagem(f'{SHUAN}_em_repouso_ampliada', 'recursos/imagens/jogador/Shuan_pose-descanso.png', escalar_para_altura=300)
        self._carregar_imagem(f'{SHUAN}_caminhando_1_ampliada', 'recursos/imagens/jogador/Shuan_pose-caminhada-direito.png', escalar_para_altura=300)
        self._carregar_imagem(f'{SHUAN}_caminhando_2_ampliada', 'recursos/imagens/jogador/Shuan_pose-caminhada.png', escalar_para_altura=300)
        self._carregar_imagem(f'{SHUAN}_caminhando_3_ampliada', 'recursos/imagens/jogador/Shuan_pose-caminhada-esquerdo.png', escalar_para_altura=300)

        self._carregar_imagem(f'{SILVIE}_em_repouso', 'recursos/imagens/jogador/Silvie_pose-descanso.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SILVIE}_caminhando_1', 'recursos/imagens/jogador/Silvie_pose-caminhada-direito.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SILVIE}_caminhando_2', 'recursos/imagens/jogador/Silvie_pose-caminhada.png', escalar_para_altura=120)
        self._carregar_imagem(f'{SILVIE}_caminhando_3', 'recursos/imagens/jogador/Silvie_pose-caminhada-esquerdo.png', escalar_para_altura=120)
       
        self._carregar_imagem(f'{SILVIE}_em_repouso_ampliada', 'recursos/imagens/jogador/Silvie_pose-descanso.png', escalar_para_altura=300)
        self._carregar_imagem(f'{SILVIE}_caminhando_1_ampliada', 'recursos/imagens/jogador/Silvie_pose-caminhada-direito.png', escalar_para_altura=300)
        self._carregar_imagem(f'{SILVIE}_caminhando_2_ampliada', 'recursos/imagens/jogador/Silvie_pose-caminhada.png', escalar_para_altura=300)
        self._carregar_imagem(f'{SILVIE}_caminhando_3_ampliada', 'recursos/imagens/jogador/Silvie_pose-caminhada-esquerdo.png', escalar_para_altura=300)

        # --- Carregar Imagens dos Inimigos ---
        self._carregar_imagem(f"{INIMIGO_LOBO}_0", 'recursos/imagens/inimigos/Lobo_0.png', escalar_para_altura=80)
        self._carregar_imagem(f"{INIMIGO_LOBO}_1", 'recursos/imagens/inimigos/Lobo_1.png', escalar_para_altura=80)
        self._carregar_imagem(f"{INIMIGO_LOBO}_2", 'recursos/imagens/inimigos/Lobo_2.png', escalar_para_altura=80)
        self._carregar_imagem(f"{INIMIGO_CORVO}_0", 'recursos/imagens/inimigos/Corvo_0.png', escalar_para_altura=60)
        self._carregar_imagem(f"{INIMIGO_CORVO}_1", 'recursos/imagens/inimigos/Corvo_1.png', escalar_para_altura=60)
        self._carregar_imagem(f"{INIMIGO_BRUTAMONTES}_0", 'recursos/imagens/inimigos/Brutamontes_0.png')
        self._carregar_imagem(f"{INIMIGO_MARINHEIRO_CORRUPTO}_0", 'recursos/imagens/inimigos/Marinheiro_corrupto_0.png')
        self._carregar_imagem(f"{CHEFE_JAVALI}_0", 'recursos/imagens/inimigos/Javali.png')

        # --- Carregar Imagens dos Habitantes ---
        self._carregar_imagem('VENDEDOR_JOAO', 'recursos/imagens/jogador/vendedor.png', escalar_para_altura=200)
        self._carregar_imagem(BIGODINI, 'recursos/imagens/habitantes/campones_b.png')
        self._carregar_imagem(TIAO_PALHA, 'recursos/imagens/habitantes/campones_a.png')
        self._carregar_imagem(LINA_PANELA, 'recursos/imagens/habitantes/camponesa_a.png')
        self._carregar_imagem(TIA_COTINHA, 'recursos/imagens/habitantes/camponesa_b.png')
        self._carregar_imagem(SR_LEE, 'recursos/imagens/habitantes/lee.png')
        self._carregar_imagem(SR_LEE_LOGISTA, 'recursos/imagens/habitantes/lee-busto.png')

        self._carregar_imagem(CANOA, 'recursos/imagens/barcos/canoa.png')
        self._carregar_imagem(f'{CANOA}_fundo', 'recursos/imagens/barcos/canoa_fundo.png')
        self._carregar_imagem(VELEIRO, 'recursos/imagens/barcos/veleiro.png')
        self._carregar_imagem(f'{VELEIRO}_fundo', 'recursos/imagens/barcos/veleiro_fundo.png')

        # --- Carregar Ícone de Interação ---
        self._carregar_imagem(CHAVE_ICONE_INTERACAO, 'recursos/imagens/icones/icone_interacao.png', escalar_para_altura=48)
        self._carregar_imagem(CHAVE_ICONE_ALERTA, 'recursos/imagens/icones/alerta.png', escalar_para_altura=48)
        self._carregar_imagem(CHAVE_ICONE_INTERROGACAO, 'recursos/imagens/icones/interrogacao.png', escalar_para_altura=48)
        self._carregar_imagem(f'{SHUAN}_inventario', 'recursos/imagens/jogador/Shuan_pose-descanso.png', escalar_para_altura=160)
        self._carregar_imagem(f'{SILVIE}_inventario', 'recursos/imagens/jogador/Silvie_pose-descanso.png', escalar_para_altura=160)
        
        self._carregar_imagem(ARBUSTO, 'recursos/imagens/itens/arbusto.png')
        self._carregar_imagem(CHAVE_CERCA, 'recursos/imagens/cenario/cerca.png')
        self._carregar_imagem(CHAVE_CERCA_DANIFICADA, 'recursos/imagens/cenario/cerca_danificada.png')

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
