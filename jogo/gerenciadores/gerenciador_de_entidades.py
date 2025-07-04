# entidades/gerenciador_entidades.py

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
        self._entidade_inimigos = None
        # Adicione outros atributos para entidades globais persistentes aqui
        # self._inventario_global = None
        self._progresso_do_jogo = None

    @property
    def jogador(self):
        """Retorna a instância do jogador principal."""
        return self._entidade_jogador

    @jogador.setter
    def jogador(self, jogador):
        """Define a instância do jogador principal."""
        self._entidade_jogador = jogador

    # Você pode adicionar métodos para gerenciar outras entidades aqui, por exemplo:
    # def obter_inventario_global(self):
    #     return self._inventario_global
    #
    # def definir_inventario_global(self, inventario):
    #     self._inventario_global = inventario
    #
    @property
    def progresso_do_jogo(self):
        return self._progresso_do_jogo

    @progresso_do_jogo.setter
    def progresso_do_jogo(self, progresso):
        self._progresso_do_jogo = progresso