# main.py

import pygame
import sys
from utilidades.constantes import *
from recursos.gerenciador_de_recursos import GerenciadorDeRecursos
# Importa a função que obtém os dados do mapa (necessário para saber quais mapas existem)
from mapa_dados import mapas_data

# Importa as classes das telas
from telas.tela_inicial import TelaInicial
from telas.tela_salvamento import TelaSalvamento
from telas.tela_de_jogo import TelaJogo
from telas.tela_selecao_personagem import TelaSelecaoPersonagem # <-- Importa a nova tela

# Inicializa o Pygame
pygame.init()
pygame.font.init()

# Configurações da tela principal
tela_principal = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Marventura")

# --- Gerenciador de Recursos ---
gerenciador_recursos = GerenciadorDeRecursos()

# --- Carregar Recursos usando o gerenciador ---
# Carregar Fontes
caminho_arquivo_fonte = 'recursos/fontes/Tagesschrift-Regular.ttf'
gerenciador_recursos.load_font('titulo', caminho_arquivo_fonte, 70)       # Fonte para títulos grandes
gerenciador_recursos.load_font('botao', caminho_arquivo_fonte, 48)     # Fonte para botões de menu
gerenciador_recursos.load_font('nome_cartaz', caminho_arquivo_fonte, 20)  # Fonte para o texto principal dos slots de save
gerenciador_recursos.load_font('data_cartaz', caminho_arquivo_fonte, 12)   # Fonte para data/hora nos slots de save

# --- Carregar Imagens ---
# Imagem de fundo comum (para menu inicial e tela de arquivos de progresso salvos)
gerenciador_recursos.load_image('fundo_inicial', 'recursos/imagens/tela_inicial.png', escalar_para_tamanho=(LARGURA_TELA, ALTURA_TELA))
# Imagem do logo (para a tela inicial), redimensionada proporcionalmente com base na altura da tela
gerenciador_recursos.load_image('logo', 'recursos/imagens/logo.png')
# Imagem para os slots de save (cartaz procurado), redimensionada proporcionalmente
gerenciador_recursos.load_image('cartaz_de_procurada', 'recursos/imagens/cartaz_de_procurado_menina.png')
gerenciador_recursos.load_image('cartaz_de_procurado', 'recursos/imagens/cartaz_de_procurado_menino.png')
gerenciador_recursos.load_image('cartaz_de_procurado_vazio', 'recursos/imagens/cartaz_de_procurado_vazio.png')
# Imagem de fundo da tela de jogo (Ilha_1.png), redimensionada proporcionalmente para a altura da tela
gerenciador_recursos.load_image('cenario_ilha_1', 'recursos/imagens/ilha_1.png', escalar_para_altura=ALTURA_TELA)
# Imagem de fundo do interior da loja
gerenciador_recursos.load_image('loja_interior', 'recursos/imagens/loja_interior.png', escalar_para_altura=ALTURA_TELA)

# --- Carregar Imagens do Jogador para Animação ---
gerenciador_recursos.load_image('protagonista_menino_em_repouso', 'recursos/imagens/jogador_parado.png', escalar_para_altura=120)
gerenciador_recursos.load_image('protagonista_menino_caminhando_1', 'recursos/imagens/jogador_caminhando_1.png', escalar_para_altura=120)
gerenciador_recursos.load_image('protagonista_menino_caminhando_2', 'recursos/imagens/jogador_caminhando_2.png', escalar_para_altura=120)
gerenciador_recursos.load_image('protagonista_menina_em_repouso', 'recursos/imagens/jogadora_parada.png', escalar_para_altura=120)
gerenciador_recursos.load_image('protagonista_menina_caminhando_1', 'recursos/imagens/jogadora_caminhando_1.png', escalar_para_altura=120)
gerenciador_recursos.load_image('protagonista_menina_caminhando_2', 'recursos/imagens/jogadora_caminhando_2.png', escalar_para_altura=120)

# --- Carregar Ícone de Interação ---
gerenciador_recursos.load_image(ICONE_INTERACAO_KEY, 'recursos/imagens/icone_interacao.png', escalar_para_altura=48)

# Verifica se todos os recursos críticos foram carregados com sucesso
# Em um jogo real, você poderia exibir uma tela de erro e sair graciosamente.
if not gerenciador_recursos.all_loaded_successfully():
    print("Recursos críticos falharam ao carregar. Saindo.")
    pygame.quit() # Sai do Pygame
    sys.exit() # Sai do script Python


# --- Gerenciamento de Telas ---
# Função para criar instâncias de tela com base no estado atual do jogo
def criar_tela(estado, gr, **kwargs): # <-- Adiciona **kwargs para aceitar argumentos adicionais (como map_id)
    """
    Cria e retorna uma nova instância de tela baseada no estado do jogo.
    :param estado: O ID do estado do jogo (uma constante).
    :param gr: A instância do GerenciadorDeRecursos.
    :param kwargs: Argumentos adicionais para o construtor da tela (ex: map_id='...', character_type='...').
    :return: Uma instância de TelaModelo ou uma de suas subclasses, ou None.
    """
    if estado == ESTADO_MENU_INICIAL:
        return TelaInicial(gr)
    elif estado == ESTADO_MENU_SALVAR:
        return TelaSalvamento(gr)
    elif estado == ESTADO_SELECAO_PERSONAGEM:
        return TelaSelecaoPersonagem(gr)
    elif estado == ESTADO_JOGO:
        # Para a Tela de Jogo, esperamos o map_id e o character_type nos kwargs
        map_id_a_carregar = kwargs.get('map_id')
        character_type = kwargs.get('character_type') # <-- Obtém o tipo de personagem

        if map_id_a_carregar and character_type:
             # Passa o gerenciador, o ID do mapa E o tipo de personagem para a TelaJogo
             return TelaJogo(gr, map_id_a_carregar, character_type) # <-- Passa character_type
        else:
             print(f"ERRO: Tentativa de criar TelaJogo sem fornecer 'map_id' ({map_id_a_carregar}) e/ou 'character_type' ({character_type}).") # Print de erro mais detalhado
             return None # Não cria a tela de jogo se dados essenciais faltarem


    else:
        print(f"AVISO: Estado de jogo desconhecido: {estado}. Retornando None.")
        return None # Retorna None para estados desconhecidos ou não implementados

# Inicializa a primeira tela do jogo (Menu Inicial), passando o gerenciador
tela_atual = criar_tela(ESTADO_MENU_INICIAL, gerenciador_recursos)

# Verifica se a tela inicial foi criada com sucesso
if tela_atual is None:
    print("ERRO FATAL: Não foi possível criar a tela inicial. Verifique create_screen.")
    pygame.quit() # Sai do Pygame
    sys.exit() # Sai do script Python

# Relógio para controlar a taxa de quadros (FPS)
relogio = pygame.time.Clock()

# --- Loop principal do jogo ---
# Esta função contém o loop que mantém o jogo rodando
def executar_jogo():
    global tela_atual

    running = True
    while running:
        # --- Tratamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            proximo_estado_result = tela_atual.handle_event(event) # <-- Variável traduzida

            # --- Verifica o valor retornado para gerenciar a transição de tela ou sair ---
            # next_state_result pode ser:
            # - None (continua na tela atual)
            # - sys.exit (sair do jogo)
            # - Um ID de estado (inteiro, ex: ESTADO_MENU_INICIAL)
            # - Um dicionário (ex: {'estado': ESTADO_JOGO, 'map_id': 'outra_ilha'}) para transições complexas

            if proximo_estado_result is not None:
                 if proximo_estado_result is sys.exit:
                     running = False
                 elif isinstance(proximo_estado_result, int):
                     # Retornou um ID de estado simples (sem mudar de mapa dentro do ESTADO_JOGO)
                     nova_tela = criar_tela(proximo_estado_result, gerenciador_recursos) # Cria a nova tela sem map_id nos kwargs
                     if nova_tela:
                         tela_atual = nova_tela
                     else:
                         print(f"ERRO: Não foi possível criar tela para o estado ID: {proximo_estado_result}")

                 elif isinstance(proximo_estado_result, dict):
                     # Retornou um dicionário (esperamos {'estado': ..., 'map_id': ...})
                     estado_desejado = proximo_estado_result.get('estado')
                     
                     # Verifica se o estado desejado é ESTADO_JOGO (precisa de map_id e character_type)
                     if estado_desejado == ESTADO_JOGO:
                          map_id_desejado = proximo_estado_result.get('map_id')
                          character_type_desejado = proximo_estado_result.get('character_type') # <-- Obtém o tipo de personagem do dicionário

                          if map_id_desejado and character_type_desejado:
                               # Cria a TELA DE JOGO com o novo ID do mapa E o tipo de personagem
                               nova_tela = criar_tela(ESTADO_JOGO, gerenciador_recursos, map_id=map_id_desejado, character_type=character_type_desejado) # <--- Passa map_id E character_type como kwargs
                               if nova_tela:
                                   tela_atual = nova_tela
                               else:
                                   print(f"ERRO: Não foi possível criar TelaJogo para o map_id: {map_id_desejado} e character_type: {character_type_desejado}")
                          else:
                               print(f"ERRO: Dicionário de transição para ESTADO_JOGO inválido (faltando map_id ou character_type): {proximo_estado_result}")
                     # Trata outras transições de estado baseadas em dicionário, se houver (ex: de diálogo retornando escolha)
                     # elif estado_desejado == ESTADO_OUTRO_ESTADO:
                     #    # Passa o dicionário completo como kwargs para a função criar_tela
                     #    nova_tela = criar_tela(estado_desejado, gerenciador_recursos, **proximo_estado_result)
                     #    if nova_tela:
                     #        tela_atual = nova_tela
                     #    else:
                     #       print(f"ERRO: Não foi possível criar tela para o estado retornado em dicionário: {estado_desejado}")

                     else:
                          # Se o dicionário retornado não corresponde a um caso conhecido (como ESTADO_JOGO),
                          # você pode adicionar um tratamento de erro ou um comportamento padrão.
                          print(f"AVISO: Dicionário de transição de estado retornado, mas estado desconhecido ou inválido: {proximo_estado_result}")


                 # else: o resultado é None, a tela atual continua.


        # --- Atualização do Estado dos Elementos ---
        if hasattr(tela_atual, 'update'):
             tela_atual.update()

        # --- Desenho ---
        tela_atual.draw(tela_principal)

        # --- Atualização da Tela e Controle de FPS ---
        pygame.display.flip()
        relogio.tick(FPS)

    # --- Fim do Jogo ---
    pygame.quit()
    sys.exit()
    
# Inicia o jogo chamando a função principal (se o script for executado diretamente)
if __name__ == "__main__":
    executar_jogo()