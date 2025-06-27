from utilidades import DBManager

def carregar_dados_do_progresso(id_jogador: str, db: DBManager):
    """
    Retorna uma tupla com os dados do jogador, da área atual e dos inimigos na área (se houver arena).
    :return: (jogador, area, inimigos ou None)
    """
    #print(f"\n--- Carregando dados do jogador '{id_jogador}' ---\n")

    jogador = db.buscar_jogador(id_jogador)
    if not jogador:
        #print(f"Jogador com ID '{id_jogador}' não encontrado.")
        return None, None, None

    #print(f"Jogador encontrado: {jogador}")

    area = db.buscar_info_area(jogador.identificador_area)
    #print(f"\nInformações da área atual: {area}")

    ilha = db.buscar_info_ilha(area.identificador_ilha)

    return jogador, ilha, area
