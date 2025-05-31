import os
import sys

def caminho_absoluto(relativo):
    """Retorna o caminho absoluto para um recurso, seja no desenvolvimento ou no executável."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relativo)
