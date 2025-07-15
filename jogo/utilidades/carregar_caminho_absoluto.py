# utilidades/carregar_caminho_absoluto.py

import os
import sys

def caminho_absoluto(caminho_relativo):
    """
    Gera um caminho absoluto para um recurso, funcionando de forma confiável
    seja no desenvolvimento ou em um executável congelado (com PyInstaller).
    """
    # Encontra o diretório base (onde o executável ou o script principal está)
    if getattr(sys, 'frozen', False):
        # Se o aplicativo for um executável congelado ('frozen')
        base_path = sys._MEIPASS
    else:
        # Se estiver rodando como um script .py normal
        # __file__ aponta para este arquivo (carregar_caminho_absoluto.py)
        # dirname() pega o diretório (utilidades)
        # dirname() de novo sobe um nível para a pasta raiz do projeto (Marventura)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Junta o caminho base com o caminho relativo do recurso
    return os.path.join(base_path, caminho_relativo)