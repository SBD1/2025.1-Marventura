import pygame
import sys
from utilidades.constantes import *
from recursos import GerenciadorDeRecursos
from utilidades import db_manager
from telas import TelaLoja
# Inicializa o Pygame
pygame.init()
pygame.font.init()

# Configurações da tela
tela_principal = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Teste Loja")

# Gerenciadores
gerenciador_recursos = GerenciadorDeRecursos()
gerenciador_banco_de_dados = db_manager.DBManager()
gerenciador_recursos.carregar_recursos()

# Mock do gerenciador de telas
class MockGerenciadorTelas:
    def __init__(self):
        self.gerenciador_banco_de_dados = gerenciador_banco_de_dados

# Testa a tela de loja
mock_gerenciador = MockGerenciadorTelas()
tela_loja = TelaLoja(mock_gerenciador, gerenciador_recursos, 'jog001', 'ven001', 'Teste Vendedor')

# Loop de teste
relogio = pygame.time.Clock()
rodando = True

while rodando:
    dt = relogio.tick(60) / 1000.0
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        else:
            resultado = tela_loja.handle_input(evento)
            if resultado:
                print(f"Transição: {resultado}")
    
    tela_loja.update(dt)
    
    tela_principal.fill((0, 0, 0))
    tela_loja.draw(tela_principal)
    pygame.display.flip()

pygame.quit()
sys.exit()