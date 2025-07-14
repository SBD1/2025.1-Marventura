# entidades/gerenciador_entidades.py

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entidades import Jogador

class GerenciadorDeEntidades:
    _instance = None # Atributo para armazenar a única instância

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GerenciadorDeEntidades, cls).__new__(cls)
            # Inicialize os atributos da instância aqui, uma única vez
            cls._instance._inicializar()
        return cls._instance

    def _inicializar(self):
        """
        Método de inicialização real da instância.
        Chamado apenas uma vez quando a instância é criada.
        """
        self._entidade_jogador = None
        self._mochila_jogador = None
        self._kit_jogador = None

        self._ilha_atual = None
        self._area_atual = None
        self._ponto_de_renascimento = (360, 410)    # Coordenadas da praia

        self._entidade_inimigos = None
        # Adicione outros atributos para entidades globais persistentes aqui
        # self._inventario_global = None
        self._dados_salvos = None # Dados de todos os slots
        self._progresso_do_jogo = None # Dados de um slot específico



    @property
    def jogador(self) -> "Jogador":
        """Retorna a instância do jogador principal."""
        return self._entidade_jogador

    @jogador.setter
    def jogador(self, jogador: "Jogador"):
        """Define a instância do jogador principal."""
        self._entidade_jogador = jogador



    @property
    def mochila_jogador(self):
        """Retorna a mochila do jogador principal."""
        return self._mochila_jogador

    @mochila_jogador.setter
    def mochila_jogador(self, mochila):
        """Define a mochila do jogador principal."""
        self._mochila_jogador = mochila



    @property
    def kit_jogador(self):
        """Retorna o kit do jogador principal."""
        return self._kit_jogador

    @kit_jogador.setter
    def kit_jogador(self, kit):
        """Define o kit do jogador principal."""
        self._kit_jogador = kit



    @property
    def ilha_atual(self):
        """Retorna a ilha atual do jogador principal."""
        return self._ilha_atual

    @ilha_atual.setter
    def ilha_atual(self, ilha_atual):
        """Define a ilha atual do jogador principal."""
        self._ilha_atual = ilha_atual



    @property
    def area_atual(self):
        """Retorna a área atual do jogador principal."""
        return self._area_atual

    @area_atual.setter
    def area_atual(self, area_atual):
        """Define a área atual do jogador principal."""
        self._area_atual = area_atual



    @property
    def ponto_de_renascimento(self):
        return self._ponto_de_renascimento
    
    @ponto_de_renascimento.setter
    def ponto_de_renascimento(self, ponto_de_renascimento):
        self._ponto_de_renascimento = ponto_de_renascimento

    # Você pode adicionar métodos para gerenciar outras entidades aqui, por exemplo:
    # def obter_inventario_global(self):
    #     return self._inventario_global
    #
    # def definir_inventario_global(self, inventario):
    #     self._inventario_global = inventario
    #
    @property
    def progresso_do_jogo(self):
        """Retorna os dados do slot selecionado."""
        return self._progresso_do_jogo

    @progresso_do_jogo.setter
    def progresso_do_jogo(self, progresso):
        """Define os dados do slot selecionado."""
        self._progresso_do_jogo = progresso
    
    
    
    @property
    def dados_salvos(self):
        """Retorna os dados de todos os slots."""
        return self._dados_salvos

    @dados_salvos.setter
    def dados_salvos(self, dados_salvos):
        """Define os dados de todos os slots."""
        self._dados_salvos = dados_salvos