class Habilidade:
    def __init__(self, id, nome, descricao, tipo_de_ataque, tipo_de_alvo, dano, custo, efeito=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.tipo_de_ataque = tipo_de_ataque
        self.tipo_de_alvo = tipo_de_alvo
        self.dano = dano
        self.custo = custo
        self.efeito = efeito  # pode ser um dicionário, tipo {'nome': 'Envenenado', 'valor': 1}



    def calcular_dano_final(self, nivel_jogador, raridade="★", escala=60):
        multiplicador_area = 1.0
        if self.tipo_de_alvo in ["area", "terrestre"]:
            multiplicador_area = 0.65  # médio para ataques em área

        multiplicadores_raridade = {
            "★": 1.0,
            "★★": 1.25,
            "★★★": 1.5
        }
        multiplicador_raridade = multiplicadores_raridade.get(raridade, 1.0)

        dano_final = self.dano * (1 + (nivel_jogador / escala)) * multiplicador_area * multiplicador_raridade
        print(f"Dano base: {self.dano}, Nível do Jogador: {nivel_jogador}, Raridade: {raridade}, Dano Final: {dano_final}")
        return int(round(dano_final))