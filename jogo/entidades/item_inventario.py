class ItemInventario:
    def __init__(self, id_item, nome, descricao, tipo, raridade, quantidade, efeitos=None):
        self.id = id_item
        self.nome = nome
        self.descricao = descricao
        self.tipo = tipo  # Ex: 'con', 'ncn', etc.
        self.raridade = raridade
        self.quantidade = quantidade
        self.efeitos = efeitos or []  # Lista de dicionários: [{"nome": "Cura", "valor": 2}, ...]

    def adicionar_efeito(self, nome, valor):
        self.efeitos.append({"nome": nome, "valor": valor})

    def resumir_efeitos(self):
        return ", ".join(
            f"+{e['valor']} {e['nome']}" if e.get('valor') is not None else e['nome']
            for e in self.efeitos
        )
