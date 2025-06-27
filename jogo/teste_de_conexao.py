# main.py

from utilidades import DBManager


# --- Gerenciador de Banco de Dados ---
db_manager = DBManager() # Isso vai tentar conectar ao banco de dados

# --- Bloco de Teste de Banco de Dados ---
def testar_db_operacoes():
    print("\n--- INICIANDO TESTES DO BANCO DE DADOS ---")
    db = DBManager() # Pega a instância Singleton (que já tentou conectar)

    jogador = 'jog001'
    # 1. Testar buscar jogador
    print(f"\n--- Teste: Buscar Jogador (ID {jogador}) ---")
    jogador_data = db.buscar_jogador(jogador)
    if jogador_data:
        print(f"Jogador encontrado: {jogador_data}")
    else:
        print("Jogador com ID jog001 não encontrado.")

    print(f"\n--- Teste: Buscar informações básicas da área '{jogador_data.identificador_area}' ---\n")
    area_atual = db.buscar_info_area(jogador_data.identificador_area)
    print(f"Informações da área: {area_atual}\n")

    print(f"\n--- Teste: Buscar caminhos da área '{jogador_data.identificador_area}' ---\n")
    caminhos = db.buscar_caminhos_da_area(jogador_data.identificador_area)
    print(f"Caminhos encontrados: {caminhos}\n")

    print(f"\n--- Teste: Buscar inimigos na área '{jogador_data.identificador_area}' ---\n")

    if any(caminho.tipo_terreno == 'arena' for caminho in caminhos):
        inimigos = db.buscar_lacaios_por_area(jogador_data.identificador_area)
    else:
        inimigos = []

    print(f"Inimigos encontrados: {inimigos}\n")

    
    """
    # 2. Testar atualizar jogador
    print("\n--- Teste: Atualizar Jogador (ID 1) ---")
    if jogador_data:
        nova_experiencia = jogador_data[8] + 100
        novo_nivel = jogador_data[4]
        if db.atualizar_jogador(1, jogador_data[2], jogador_data[6], novo_nivel, nova_experiencia, jogador_data[9], jogador_data[10], jogador_data[5]):
            print(f"Jogador ID 1 atualizado. Nova EXP: {nova_experiencia}")
            jogador_atualizado = db.buscar_jogador(1)
            if jogador_atualizado:
                print(f"EXP após atualização: {jogador_atualizado[8]}")
        else:
            print("Falha ao atualizar jogador ID 1.")
    else:
        print("Não foi possível atualizar: Jogador ID 1 não encontrado.")

    # 3. Testar inserir um novo jogador
    print("\n--- Teste: Inserir Novo Jogador ---")
    # Para evitar erro de chave duplicada, vamos inserir com um nome diferente
    # e deixar o SERIAL ID gerenciar o ID.
    novo_jogador_id = db.salvar_novo_jogador("Aventureiro Novato", 1, 1, 1, 10, 20, 1, 5, 20, 2, 0, 10.5, 15.0)
    if novo_jogador_id:
        print(f"Novo jogador 'Aventureiro Novato' inserido com ID: {novo_jogador_id}")
    else:
        print("Falha ao inserir novo jogador.")

    # 4. Testar inventário: buscar inventário do jogador 1
    print("\n--- Teste: Buscar Inventário do Jogador 1 ---")
    inventario_jogador1 = db.buscar_inventario_jogador(1)
    if inventario_jogador1:
        print(f"Inventário do Jogador 1 encontrado: ID={inventario_jogador1[0]}, Nome='{inventario_jogador1[1]}'")
        id_inventario_jogador1 = inventario_jogador1[0]

        # 5. Testar buscar itens no inventário
        print("\n--- Teste: Buscar Itens no Inventário do Jogador 1 (tipos) ---")
        itens_inventario = db.buscar_itens_no_inventario(id_inventario_jogador1)
        if itens_inventario:
            print("Tipos de Itens no inventário:")
            for item in itens_inventario:
                # Ajustado para imprimir apenas Tipo ID e Tipo Geral,
                # pois Nome Detalhado é 'None' com a modelagem atual
                print(f"  - Tipo ID: {item[0]}, Tipo Geral: {item[1]}")
        else:
            print("Nenhum item encontrado no inventário do Jogador 1.")
        
        # 6. Testar adicionar item ao inventário (usando TipoItem ID 5 = 'Fruta')
        print("\n--- Teste: Adicionar item 'Fruta' (TipoItem ID 5) ao Inventário do Jogador 1 ---")
        if db.adicionar_item_ao_inventario(id_inventario_jogador1, 5):
            print("Item 'Fruta' (TipoItem ID 5) adicionado com sucesso.")
            itens_apos_adicao = db.buscar_itens_no_inventario(id_inventario_jogador1)
            print("Itens no inventário após adição:")
            for item in itens_apos_adicao:
                print(f"  - Tipo ID: {item[0]}, Tipo Geral: {item[1]}")
        else:
            print("Falha ao adicionar item 'Fruta'.")

        # 7. Testar remover item do inventário (remover 'Fruta' novamente)
        print("\n--- Teste: Remover item 'Fruta' (TipoItem ID 5) do Inventário do Jogador 1 ---")
        if db.remover_item_do_inventario(id_inventario_jogador1, 5):
            print("Item 'Fruta' (TipoItem ID 5) removido com sucesso.")
            itens_apos_remocao = db.buscar_itens_no_inventario(id_inventario_jogador1)
            print("Itens no inventário após remoção:")
            for item in itens_apos_remocao:
                print(f"  - Tipo ID: {item[0]}, Tipo Geral: {item[1]}")
        else:
            print("Falha ao remover item 'Fruta'.")

    else:
        print("Inventário do Jogador 1 não encontrado. Tentando criar um...")
        novo_inventario_id = db.criar_inventario(1, "Inventário do Protagonista")
        if novo_inventario_id:
            print(f"Inventário criado para Jogador 1 com ID: {novo_inventario_id}")
        else:
            print("Falha ao criar inventário.")


    # 8. Testar buscar missões de um jogador
    print("\n--- Teste: Buscar Missões do Jogador 1 ---")
    missoes_jogador1 = db.buscar_missoes_jogador(1)
    if missoes_jogador1:
        print("Missões do Jogador 1:")
        for missao in missoes_jogador1:
            print(f"  - Nome: {missao[0]}, Descrição: {missao[1]}")
    else:
        print("Nenhuma missão encontrada para o Jogador 1.")

    # 9. Testar buscar habitante
    print("\n--- Teste: Buscar Habitante (ID 1) ---")
    habitante_data = db.buscar_habitante(1)
    if habitante_data:
        print(f"Habitante encontrado: Nome={habitante_data[0]}, Tipo={habitante_data[1]}")
    else:
        print("Habitante com ID 1 não encontrado.")

    # 10. Testar buscar conexões de ilha
    print("\n--- Teste: Buscar Conexões da Ilha 1 ---")
    conexoes = db.buscar_conexoes_ilha(1)
    if conexoes:
        print("Conexões da Ilha 1:")
        for conexao in conexoes:
            print(f"  - De: {conexao[1]}, Para: {conexao[2]}")
    else:
        print("Nenhuma conexão encontrada para a Ilha 1.")

    # ===============================================
    # NOVOS TESTES (Baseados nos seus exemplos)
    # ===============================================

    # Teste: Ver o tipo de uma pessoa (Personagem) - usando TipoPersonagem
    print("\n--- Teste: Buscar Tipo de Personagem (ID 1) ---")
    tipo_personagem_data = db.buscar_tipo_personagem(1)
    if tipo_personagem_data:
        print(f"Tipo de Personagem encontrado: {tipo_personagem_data[0]}")
    else:
        print("Tipo de Personagem com ID 1 não encontrado.")

    # Teste: Ver atributos de um lacaio específico
    print("\n--- Teste: Buscar Lacaio (ID 1) ---")
    lacaio_data = db.buscar_lacaio(1)
    if lacaio_data:
        print(f"Lacaio encontrado: Nome={lacaio_data[0]}, Dano={lacaio_data[1]}, Vida={lacaio_data[2]}, Nível={lacaio_data[3]}")
    else:
        print("Lacaio com ID 1 não encontrado.")

    # Teste: Ver atributos de um chefe específico
    print("\n--- Teste: Buscar Chefe (ID 1) ---")
    chefe_data = db.buscar_chefe(1)
    if chefe_data:
        print(f"Chefe encontrado: Nome={chefe_data[0]}, Dano={chefe_data[1]}, Vida={chefe_data[2]}, Nível={chefe_data[3]}")
    else:
        print("Chefe com ID 1 não encontrado.")

    # Teste: Ver atributos de um aliado específico
    print("\n--- Teste: Buscar Aliado (ID 1) ---")
    aliado_data = db.buscar_aliado(1)
    if aliado_data:
        print(f"Aliado encontrado: Nome={aliado_data[0]}, Vida={aliado_data[1]}, Nível={aliado_data[2]}")
    else:
        print("Aliado com ID 1 não encontrado.")

    # Teste: Ver informações de um mapa (adaptação de "prisão")
    print("\n--- Teste: Buscar Informações do Mapa (ID 1) ---")
    mapa_data = db.buscar_info_mapa(1)
    if mapa_data:
        print(f"Mapa encontrado: ID={mapa_data[0]}, Total Ilhas={mapa_data[1]}, Total Item Chave={mapa_data[2]}")
    else:
        print("Mapa com ID 1 não encontrado.")

    # Teste: Ver quais pessoas estão em um local (mapa)
    print("\n--- Teste: Buscar Pessoas no Mapa (ID 1) ---")
    pessoas_no_mapa = db.buscar_pessoas_em_local(1)
    if pessoas_no_mapa:
        print("Pessoas no Mapa 1:")
        for pessoa in pessoas_no_mapa:
            # A tupla de retorno é (id, nome, tipo_entidade, coord_x, coord_y)
            print(f"  - {pessoa[2]}: {pessoa[1]} (ID: {pessoa[0]}) em ({pessoa[3]}, {pessoa[4]})")
    else:
        print("Nenhuma pessoa encontrada no Mapa 1.")
    
    # Teste: Ver quais itens estão em um local (mapa) - adaptação para itens chave do mapa
    print("\n--- Teste: Buscar Itens em Local (Mapa ID 1) ---")
    itens_no_mapa = db.buscar_itens_em_local(1)
    if itens_no_mapa:
        print("Itens Chave no Mapa 1:")
        for item in itens_no_mapa:
            print(f"  - Mapa ID: {item[0]}, Total Itens Chave: {item[1]}")
    else:
        print("Nenhum item chave encontrado para o Mapa 1.")

    # Teste: Buscar fabricação específica (Receita ID 1)
    print("\n--- Teste: Buscar Fabricação Específica (Receita ID 1) ---")
    receita_data = db.buscar_fabricacao_especifica(1)
    if receita_data:
        print(f"Detalhes da Receita ID 1 (Produz: {receita_data[0][1]}):")
        for item_receita in receita_data:
            print(f"  - Ingrediente: {item_receita[4]} (Tipo: {item_receita[2]}, ID: {item_receita[3]})")
    else:
        print("Receita com ID 1 não encontrada ou sem ingredientes.")

    # Teste: Ver fabricações possíveis com um item específico (consumível ID 106)
    print("\n--- Teste: Buscar Fabricações por Ingrediente (Consumível ID 106 - 'Alga Fresca') ---")
    fab_por_ingrediente = db.buscar_fabricacoes_por_ingrediente(106, 'consumivel')
    if fab_por_ingrediente:
        print("Receitas que usam 'Alga Fresca':")
        for receita_item in fab_por_ingrediente:
            print(f"  - Receita ID: {receita_item[0]}, Produz: {receita_item[1]} (ID: {receita_item[2]})")
    else:
        print("Nenhuma receita encontrada usando 'Alga Fresca'.")

    # Teste: Ver todas as fabricações de um jogador (ID 1)
    print("\n--- Teste: Buscar Fabricações por Jogador (ID 1) ---")
    fab_por_jogador = db.buscar_fabricacoes_por_jogador(1)
    if fab_por_jogador:
        print("Receitas do Jogador 1:")
        for receita_jogador in fab_por_jogador:
            print(f"  - Receita ID: {receita_jogador[0]}, Produz: {receita_jogador[1]}")
    else:
        print("Nenhuma receita encontrada para o Jogador 1.")

    # Teste: Ver o item que uma missão X vai dar (Missão ID 1)
    print("\n--- Teste: Buscar Item Recompensa Missão (Missão ID 1) ---")
    item_recompensa = db.buscar_item_recompensa_missao(1)
    if item_recompensa:
        print(f"Itens recompensa da Missão 1:")
        for item_r in item_recompensa:
            print(f"  - Tipo ID: {item_r[0]}, Tipo Geral: {item_r[1]}")
    else:
        print("Nenhum item recompensa encontrado para a Missão 1.")

    # Teste: Ver o lugar que uma missão X está (Missão ID 1)
    print("\n--- Teste: Buscar Local da Missão (Missão ID 1) ---")
    local_missao = db.buscar_local_missao(1)
    if local_missao:
        print(f"Local da Missão 1: Nome da Missão: '{local_missao[0]}', Tipo de Sala: '{local_missao[1]}', ID da Sala: {local_missao[2]}, Detalhes: {local_missao[3]}")
    else:
        print("Local da Missão 1 não encontrado.")

    # Teste: Ver (nome, descrição) de uma missão específica (Missão ID 2)
    print("\n--- Teste: Buscar Detalhes da Missão (ID 2) ---")
    detalhes_missao = db.buscar_detalhes_missao(2)
    if detalhes_missao:
        print(f"Detalhes da Missão 2: Nome: '{detalhes_missao[0]}', Descrição: '{detalhes_missao[1]}'")
    else:
        print("Missão com ID 2 não encontrada.")

    # Teste: Ver o tipo de um item específico (TipoItem ID 1)
    print("\n--- Teste: Buscar Tipo de Item (TipoItem ID 1) ---")
    tipo_item_data = db.buscar_item_por_tipo_id(1)
    if tipo_item_data:
        print(f"Tipo de Item ID 1: {tipo_item_data[0]}")
    else:
        print("Tipo de Item com ID 1 não encontrado.")

    # Teste: Ver os atributos de uma arma específica (Arma ID 401)
    print("\n--- Teste: Buscar Atributos da Arma (ID 401) ---")
    arma_data = db.buscar_arma_atributos(401)
    if arma_data:
        print(f"Arma 401: Nome='{arma_data[0]}', Raridade='{arma_data[1]}', Preço Compra={arma_data[2]}, Habilidade='{arma_data[4]}' (Dano: {arma_data[5]})")
    else:
        print("Arma com ID 401 não encontrada.")

    # Teste: Ver os atributos de um consumível específico (Consumível ID 101)
    print("\n--- Teste: Buscar Atributos do Consumível (ID 101) ---")
    consumivel_data = db.buscar_consumivel_atributos(101)
    if consumivel_data:
        print(f"Consumível 101: Nome='{consumivel_data[0]}', Tipo='{consumivel_data[1]}', Raridade='{consumivel_data[2]}', Fabricável={consumivel_data[6]}")
    else:
        print("Consumível com ID 101 não encontrado.")
    
    # Teste: Ver os atributos de um acessório específico (Acessório ID 301)
    print("\n--- Teste: Buscar Atributos do Acessório (ID 301) ---")
    acessorio_data = db.buscar_acessorio_atributos(301)
    if acessorio_data:
        print(f"Acessório 301: Nome='{acessorio_data[0]}', Tipo='{acessorio_data[1]}', Raridade='{acessorio_data[2]}', Preço Compra={acessorio_data[3]}")
    else:
        print("Acessório com ID 301 não encontrado.")

    # Teste: Ver os atributos de um não-consumível específico (Não-Consumível ID 201)
    print("\n--- Teste: Buscar Atributos do Não-Consumível (ID 201) ---")
    nao_consumivel_data = db.buscar_nao_consumivel_atributos(201)
    if nao_consumivel_data:
        print(f"Não-Consumível 201: Nome='{nao_consumivel_data[0]}', Tipo='{nao_consumivel_data[1]}', Raridade='{nao_consumivel_data[2]}'")
    else:
        print("Não-Consumível com ID 201 não encontrado.")

    # Teste: Ver os atributos de uma fruta específica (Fruta ID 501)
    print("\n--- Teste: Buscar Atributos da Fruta (ID 501) ---")
    fruta_data = db.buscar_fruta_atributos(501)
    if fruta_data:
        print(f"Fruta 501: Nome='{fruta_data[0]}', Tipo='{fruta_data[1]}', Raridade='{fruta_data[2]}', Habilidade='{fruta_data[5]}' (Bravura: '{fruta_data[6]}')")
    else:
        print("Fruta com ID 501 não encontrada.")

    # Teste: Verificar inconsistências no inventário (sem inconsistências esperadas nos dados de exemplo)
    print("\n--- Teste: Verificar Inconsistências no Inventário ---")
    inconsistencias = db.verificar_inconsistencia_inventario()
    if inconsistencias:
        print("Inconsistências encontradas no Inventário:")
        for inc in inconsistencias:
            print(f"  - Inventário ID: {inc[0]}, Item Tipo ID: {inc[1]} (Sem tipo correspondente)")
    else:
        print("Nenhuma inconsistência encontrada no Inventário.")
"""

    print("\n--- TESTES DO BANCO DE DADOS CONCLUÍDOS ---")
    db.fechar_conexao() # Fechar a conexão com o banco de dados


# Inicia o bloco de teste de banco de dados
if __name__ == "__main__":
    testar_db_operacoes()