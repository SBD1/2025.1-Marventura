# gerenciador_de_recursos.py

import pygame
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

    def load_image(self, chave, caminho, escalar_para_tamanho=None, escalar_para_altura=None):
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

    def get_image(self, chave):
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

    def load_font(self, chave, caminho, tamanho):
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


    def get_font(self, chave):
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
            # Fallback genérico caso a fonte não tenha sido carregada, a key esteja errada, ou o fallback original falhou
            try:
                return pygame.font.SysFont("Arial", 30) # Tenta um fallback genérico com Arial tamanho 30
            except pygame.error as generic_fallback_e:
                 print(f"ERRO: Falha no fallback genérico para fonte: {generic_fallback_e}")
                 # Retorna None ou levanta um erro crítico se nenhum fallback funcionar
                 return None # Retorna None como último recurso


    def all_loaded_successfully(self):
        """
        Verifica se todos os recursos carregados marcaram sucesso.
        (Nesta versão simples, apenas verifica se a flag _carregado_com_sucesso é True).
        Em um gerenciador mais complexo, poderia verificar recursos marcados como "críticos".

        :return: True se não houve erros durante o carregamento, False caso contrário.
        """
        return self._carregado_com_sucesso
