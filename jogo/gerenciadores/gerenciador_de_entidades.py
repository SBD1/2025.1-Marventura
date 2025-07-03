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
        self._jogador_principal = None
        # Adicione outros atributos para entidades globais persistentes aqui
        # self._inventario_global = None
        # self._progresso_do_jogo = None

    @property
    def jogador_principal(self):
        """Retorna a instância do jogador principal."""
        return self._jogador_principal

    @jogador_principal.setter
    def jogador_principal(self, jogador):
        """Define a instância do jogador principal."""
        self._jogador_principal = jogador

    # Você pode adicionar métodos para gerenciar outras entidades aqui, por exemplo:
    # def obter_inventario_global(self):
    #     return self._inventario_global
    #
    # def definir_inventario_global(self, inventario):
    #     self._inventario_global = inventario
    #
    # def obter_progresso_do_jogo(self):
    #     return self._progresso_do_jogo
    #
    # def definir_progresso_do_jogo(self, progresso):
    #     self._progresso_do_jogo = progresso