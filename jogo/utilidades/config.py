import os
import sys

def caminho_absoluto(caminho_relativo):
    """
    Gera um caminho absoluto para um recurso, funcionando de forma confiável
    independente de onde o script foi executado.
    """
    # Encontra o caminho para o diretório raiz do projeto (a pasta 'jogo')
    # __file__ é o caminho para este arquivo de configuração.
    # Usamos dirname() para subir na hierarquia de pastas.
    # Assumindo que este arquivo está em 'jogo/utilidades/', subimos um nível.
    diretorio_raiz_do_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Junta o caminho raiz do projeto com o caminho relativo do recurso.
    return os.path.join(diretorio_raiz_do_projeto, caminho_relativo)
