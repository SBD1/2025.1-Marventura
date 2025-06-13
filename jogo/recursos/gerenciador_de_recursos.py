# gerenciador_de_recursos.py

# import pygame # Comentado: Não é necessário para o DB
# import sys    # Comentado: Não é necessário para o DB
# from utilidades.constantes import * # Comentado: Não é necessário para o DB
# from utilidades import caminho_absoluto # Comentado: Não é necessário para o DB

# import psycopg2 # Mantido: Para conexão com o banco
# import os       # Mantido: Para conexão com o banco

# ===============================================
# A parte de gerenciamento de recursos gráficos/áudio do Pygame foi comentada
# para focar apenas na conexão com o banco de dados.
# ===============================================

class GerenciadorDeRecursos:
    """
    Gerencia o carregamento e acesso de recursos do jogo.
    Nesta versão focada apenas no DB, a funcionalidade Pygame está desabilitada.
    """
    def __init__(self):
        # self._imagens = {} # Comentado
        # self._fontes = {}  # Comentado
        self._carregado_com_sucesso = True # Mantido como um placeholder

    # def _carregar_imagem(self, chave, caminho, escalar_para_tamanho=None, escalar_para_altura=None):
    #     pass # Implementação comentada

    # def obter_imagem(self, chave):
    #     return None # Implementação comentada

    # def _carregar_fonte(self, chave, caminho, tamanho):
    #     pass # Implementação comentada

    # def obter_fonte(self, chave):
    #     return None # Implementação comentada

    def carregar_recursos(self):
        """
        Nesta versão, este método apenas imprime uma mensagem,
        pois o carregamento real de recursos gráficos/áudio está desativado.
        """
        print("Iniciando carregamento de recursos (funções Pygame desativadas para teste de DB)...")
        # if not self._tudo_carregado_com_sucesso(): # Comentado
        #     print("Recursos críticos falharam ao carregar. Saindo.") # Comentado
        #     pygame.quit() # Comentado
        #     sys.exit() # Comentado

    def _tudo_carregado_com_sucesso(self):
        return self._carregado_com_sucesso

# A parte de conexão direta com o banco de dados que estava aqui foi movida
# ou será tratada pelo DBManager, conforme a sua nova estrutura.
# Vou remover o bloco original de conexão direta daqui para evitar duplicação
# com o DBManager.