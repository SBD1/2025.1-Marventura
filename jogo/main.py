# main.py

import pygame
import sys
from utilidades.constantes import *
from recursos import GerenciadorDeRecursos

# Importa as classes das telas
from telas import TelaInicial
from telas import TelaSalvamento
from telas import TelaJogo
from telas import TelaSelecaoPersonagem

# Inicializa o Pygame (DEVE VIR ANTES DE CARREGAR FONTES/IMAGENS)
pygame.init()
# Inicializa apenas o módulo de fonte explicitamente (importante para o carregamento de fontes no gerenciador)
pygame.font.init()

# Configurações da tela principal
tela_principal = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Marventura") # Título da janela do jogo

# --- Gerenciador de Recursos ---
# Cria uma única instância do gerenciador de recursos
gerenciador_recursos = GerenciadorDeRecursos()

# --- Carregar Recursos usando o gerenciador ---
# Carregar Fontes usando o gerenciador
caminho_arquivo_fonte = 'recursos/fontes/Tagesschrift-Regular.ttf'
gerenciador_recursos.load_font(CHAVE_FONTE_TITULO, caminho_arquivo_fonte, 70)       # Fonte para títulos grandes
gerenciador_recursos.load_font(CHAVE_FONTE_BOTAO, caminho_arquivo_fonte, 48)     # Fonte para botões
gerenciador_recursos.load_font(CHAVE_FONTE_NOME_CARTAZ, caminho_arquivo_fonte, 20)  # Fonte para nome no cartaz
gerenciador_recursos.load_font(CHAVE_FONTE_DATA_CARTAZ, caminho_arquivo_fonte, 12)   # Fonte para data/dados no cartaz

# --- Carregar Imagens usando o gerenciador ---
# Imagem de fundo comum (para menu inicial e tela de arquivos de progresso salvos)
gerenciador_recursos.load_image(CHAVE_TELA_INICIAL, 'recursos/imagens/tela_inicial.png', escalar_para_tamanho=(LARGURA_TELA, ALTURA_TELA))
# Imagem do logo (para a tela inicial)
gerenciador_recursos.load_image(CHAVE_LOGO, 'recursos/imagens/logo.png')

# --- Carregar Imagens dos Cartazes de Procurado para Slots de Save (Por Tipo de Personagem) ---
gerenciador_recursos.load_image(CHAVE_CARTAZ_PROCURADA, 'recursos/imagens/cartaz_de_procurado_menina.png')
gerenciador_recursos.load_image(CHAVE_CARTAZ_PROCURADO, 'recursos/imagens/cartaz_de_procurado_menino.png')
gerenciador_recursos.load_image(CHAVE_CARTAZ_VAZIO, 'recursos/imagens/cartaz_de_procurado_vazio.png')

# Carregar backgrounds para os mapas do jogo
# Use as chaves que você definiu para os backgrounds dos mapas em mapa_dados.py
gerenciador_recursos.load_image(CHAVE_CENARIO_CAMPO_VILA, 'recursos/imagens/ilha_campo_vila.png', escalar_para_altura=ALTURA_TELA)
gerenciador_recursos.load_image(CHAVE_CENARIO_NEVE_VILA, 'recursos/imagens/ilha_neve_vila.png', escalar_para_altura=ALTURA_TELA)
# Imagem de fundo do interior da loja
gerenciador_recursos.load_image(CHAVE_LOJA_INTERIOR, 'recursos/imagens/loja_interior.png')
gerenciador_recursos.load_image(CHAVE_COZINHA_INTERIOR, 'recursos/imagens/cozinha_interior.png')
# Certifique-se de carregar os fundos de TODOS os mapas que você definiu em mapa_dados.py aqui.


# --- Carregar Imagens do Jogador para Animação (Para Ambos os Tipos) ---
# Usa as constantes PERSONAGEM_MENINO/MENINA e as chaves que você definiu
gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINO}_em_repouso', 'recursos/imagens/jogador_parado.png', escalar_para_altura=120)
gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINO}_caminhando_1', 'recursos/imagens/jogador_caminhando_1.png', escalar_para_altura=120)
gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINO}_caminhando_2', 'recursos/imagens/jogador_caminhando_2.png', escalar_para_altura=120)

gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINA}_em_repouso', 'recursos/imagens/jogadora_parada.png', escalar_para_altura=120)
gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINA}_caminhando_1', 'recursos/imagens/jogadora_caminhando_1.png', escalar_para_altura=120)
gerenciador_recursos.load_image(f'protagonista_{PERSONAGEM_MENINA}_caminhando_2', 'recursos/imagens/jogadora_caminhando_2.png', escalar_para_altura=120)


# --- Carregar Ícone de Interação ---
# Usa a chave constante
gerenciador_recursos.load_image(CHAVE_ICONE_INTERACAO, 'recursos/imagens/icone_interacao.png', escalar_para_altura=48)


# Verifica se todos os recursos críticos foram carregados com sucesso
# Em um jogo real, você poderia exibir uma tela de erro e sair graciosamente.
if not gerenciador_recursos.all_loaded_successfully():
    print("Recursos críticos falharam ao carregar. Saindo.") # Print traduzido
    pygame.quit() # Sai do Pygame
    sys.exit() # Sai do script Python


# --- Gerenciamento de Telas ---
# Função para criar instâncias de tela com base no estado atual do jogo
# Aceita argumentos adicionais (kwargs) que podem incluir id_mapa, tipo_personagem,
# id_entrada_alvo OU coordenada_x, coordenada_y, olhando_para_direita.
def criar_tela(estado, gr, **kwargs): # <-- Mantém **kwargs para flexibilidade
    """
    Cria e retorna uma nova instância de tela baseada no estado do jogo e dados adicionais.
    :param estado: O ID do estado do jogo (uma constante).
    :param gr: A instância do GerenciadorDeRecursos.
    :param kwargs: Dicionário de argumentos adicionais para o construtor da tela (ex: id_mapa='...', tipo_personagem='...', id_entrada_alvo='...', coordenada_x=..., coordenada_y=...).
    :return: Uma instância de TelaModelo ou uma de suas subclasses, ou None se a tela não puder ser criada.
    """
    if estado == ESTADO_MENU_INICIAL:
        print("Criando Tela Inicial") # Print de debug
        # A TelaInicial só precisa do gerenciador de recursos
        return TelaInicial(gr)
    elif estado == ESTADO_MENU_SALVAR:
        print("Criando Tela Salvamento") # Print de debug
        # A TelaSalvamento só precisa do gerenciador de recursos
        return TelaSalvamento(gr)
    elif estado == ESTADO_SELECAO_PERSONAGEM:
        print("Criando Tela Seleção Personagem") # Print de debug
        # A TelaSelecaoPersonagem só precisa do gerenciador de recursos
        return TelaSelecaoPersonagem(gr)
    elif estado == ESTADO_JOGO:
        print("Criando Tela Jogo") # Print de debug
        # Para a Tela de Jogo, precisamos extrair dados essenciais dos kwargs
        id_mapa_a_carregar = kwargs.get('id_mapa')
        tipo_personagem = kwargs.get('tipo_personagem')
        # Também extraímos o ID do ponto de entrada E os dados salvos (eles podem ser None)
        id_entrada_alvo = kwargs.get('ponto_entrada_destino_id') # <-- A chave deve ser 'ponto_entrada_destino_id' conforme retornado pelas outras telas
        coordenada_x = kwargs.get('coordenada_x') # <-- Extrai a posição X salva dos kwargs
        coordenada_y = kwargs.get('coordenada_y') # <-- Extrai a posição Y salva dos kwargs
        olhando_para_direita = kwargs.get('olhando_para_direita') # <-- Extrai a orientação salva dos kwargs


        # A TelaJogo precisa pelo menos do id_mapa e tipo_personagem para ser criada
        if id_mapa_a_carregar and tipo_personagem:
             # Cria a instância da TelaJogo, passando todos os dados que ela pode precisar
             # Passamos o gerenciador, ID do mapa, tipo de personagem,
             # E os dados opcionais de ponto de entrada ou dados salvos como keyword arguments.
             # A lógica dentro de TelaJogo.__init__ decidirá qual usar.
             return TelaJogo(gr, id_mapa_a_carregar, tipo_personagem,
                              id_entrada_alvo=id_entrada_alvo, # Passa o ID do ponto de entrada (pode ser None)
                              coordenada_x=coordenada_x, # Passa a posição X salva (pode ser None)
                              coordenada_y=coordenada_y, # Passa a posição Y salva (pode ser None)
                              olhando_para_direita=olhando_para_direita) # Passa a orientação salva (pode ser None)

        else:
             # Erro se faltarem dados essenciais para criar a TelaJogo
             print(f"ERRO: Tentativa de criar TelaJogo sem fornecer dados essenciais (id_mapa={id_mapa_a_carregar}, tipo_personagem={tipo_personagem}).") # Print de erro mais detalhado
             return None # Retorna None, indicando falha na criação da tela


    else:
        # Estado desconhecido
        print(f"AVISO: Estado de jogo desconhecido: {estado}. Retornando None.") # Print de aviso
        return None # Retorna None para estados desconhecidos ou não implementados

# Inicializa a primeira tela do jogo (Menu Inicial), passando o gerenciador
tela_atual = criar_tela(ESTADO_MENU_INICIAL, gerenciador_recursos)

# Verifica se a tela inicial foi criada com sucesso
if tela_atual is None:
    print("ERRO FATAL: Não foi possível criar a tela inicial. Verifique create_screen.") # Print de erro fatal
    pygame.quit() # Sai do Pygame
    sys.exit() # Sai do script Python

# Relógio para controlar a taxa de quadros (FPS)
relogio = pygame.time.Clock() # Variável traduzida

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

            proximo_estado_result = tela_atual.handle_event(event)

            # --- Verifica o valor retornado para gerenciar a transição de tela ou sair ---
            if proximo_estado_result is not None:
                 if proximo_estado_result is sys.exit:
                     running = False
                 elif isinstance(proximo_estado_result, int):
                     # Retornou um ID de estado simples (sem dados adicionais no dicionário)
                     # Ex: TelaInicial -> ESTADO_MENU_SALVAR
                     # Ex: TelaSalvamento -> ESTADO_MENU_INITIAL
                     # Ex: TelaSalvamento -> ESTADO_SELECAO_PERSONAGEM (se o slot for vazio)
                     # Cria a nova tela usando o ID de estado retornado.
                     # Para ESTADO_JOGO retornado assim, criart_ela usará os padrões (id_entrada_alvo=None, coordenada_x=None...).
                     nova_tela = criar_tela(proximo_estado_result, gerenciador_recursos)
                     if nova_tela:
                         tela_atual = nova_tela
                     else:
                         print(f"ERRO: Não foi possível criar tela para o estado ID: {proximo_estado_result}")

                 elif isinstance(proximo_estado_result, dict):
                     # Retornou um dicionário (esperamos {'estado': ..., ...})
                     # EXTRAI o estado do dicionário antes de passá-lo para criar_tela
                     estado_desejado = proximo_estado_result.pop('estado', None) # <-- Extrai 'estado' e remove do dicionário

                     if estado_desejado is not None:
                         # Cria a nova tela usando o estado extraído como o primeiro argumento posicional,
                         # e o RESTANTE do dicionário (SEM a chave 'estado') como kwargs.
                         nova_tela = criar_tela(estado_desejado, gerenciador_recursos, **proximo_estado_result) # <-- Passa o estado extraído, depois desempacota o resto do dicionário

                         if nova_tela:
                             tela_atual = nova_tela # Atualiza a tela atual
                         else:
                             # Se criar_tela retornou None, o erro detalhado já foi impresso
                             pass # A tela_atual permanece a mesma que causou o retorno do dicionário inválido
                     else:
                         # Se o dicionário retornado não tinha a chave 'estado'
                         print(f"ERRO: Dicionário de transição retornado sem a chave 'estado': {proximo_estado_result}")


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
    executar_jogo() # <-- Chama a função principal do jogo