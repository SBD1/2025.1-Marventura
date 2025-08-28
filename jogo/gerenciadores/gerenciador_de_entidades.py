# entidades/gerenciador_entidades.py

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Literal
if TYPE_CHECKING:
    from entidades import Jogador

@dataclass
class ProgressoDoJogo:
    identificador_progresso: str
    numero_do_slot: int
    data_ultimo_salvamento: int
    ocupado: bool
    nome_jogador: str
    identificador_jogador: str
    percentual_concluido: float

@dataclass
class Area:
    identificador_area: str
    identificador_ilha: str
    nome: str
    tipo_area: Literal['Área de combate', 'Área neutra', 'Vila', 'Porto', 'Loja', 'Yomotsu Hirasaka']
    chave_imagem_fundo: str
    chave_imagem_frente: str
    visitada: bool

@dataclass
class Ilha:
    identificador_ilha: str
    nome: str
    visitada: bool



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
        self._entidade_jogador:"Jogador" = None
        self._mochila_jogador = None
        self._kit_jogador = None
        self._iniciar_missao = None


        self._ilha_atual: Ilha = None
        self._area_atual: Area = None
        self._ponto_de_renascimento = (360, 410)    # Coordenadas da praia

        self._entidade_inimigos = None
        # Adicione outros atributos para entidades globais persistentes aqui
        # self._inventario_global = None
        self._dados_salvos: list[ProgressoDoJogo] = [] # Dados de todos os slots
        self._progresso_do_jogo: Optional[ProgressoDoJogo] = None # Dados de um slot específico



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
    def ilha_atual(self) -> Ilha:
        """Retorna a ilha atual do jogador principal."""
        return self._ilha_atual

    @ilha_atual.setter
    def ilha_atual(self, ilha_atual: Ilha):
        """Define a ilha atual do jogador principal."""
        self._ilha_atual = ilha_atual



    @property
    def iniciar_missao(self):
        """Missão atual em andamento do jogador principal."""
        return self._iniciar_missao

    @iniciar_missao.setter
    def iniciar_missao(self, iniciar_missao):
        """Define a missão atual em andamento do jogador principal."""
        self._iniciar_missao = iniciar_missao
 
 
 
    @property
    def area_atual(self) -> Area:
        """Retorna a área atual do jogador principal."""
        return self._area_atual

    @area_atual.setter
    def area_atual(self, area_atual: Area):
        """Define a área atual do jogador principal."""
        if area_atual.tipo_area == 'Loja':
            self._entidade_jogador.aplicar_fator_de_escala(2.5)
        else:
            if self._entidade_jogador.fator_de_escala != 1.0:
                self._entidade_jogador.aplicar_fator_de_escala(1.0)
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
    def progresso_do_jogo(self) -> Optional[ProgressoDoJogo]:
        """Retorna os dados do slot selecionado."""
        return self._progresso_do_jogo

    @progresso_do_jogo.setter
    def progresso_do_jogo(self, progresso: ProgressoDoJogo):
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