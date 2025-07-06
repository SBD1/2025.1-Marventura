class ItemInventario:
    def __init__(self, id_item, nome, descricao, tipo, raridade, quantidade, efeitos=None):
        self.id = id_item
        self.nome = nome
        self.descricao = descricao
        self.tipo = tipo  # Ex: 'fruta', 'consumivel', etc.
        self.raridade = raridade.strip() if raridade else "★"
        self.quantidade = quantidade
        self.efeitos = efeitos or []  # Lista de dicionários: [{"nome": "Cura", "valor": 2}, ...]

    def adicionar_efeito(self, nome, valor):
        self.efeitos.append({"nome": nome, "valor": valor})

    def aplicar_efeitos(self, jogador):
        """
        Aplica os efeitos do item ao jogador. A quantidade deve ser controlada fora.
        """
        for efeito in self.efeitos:
            tipo = efeito["nome"]
            valor = efeito["valor"]

            match tipo:
                case "Cura":  # Cura de vida
                    jogador.vida_atual += valor
                    jogador.vida_atual = min(jogador.vida_atual, jogador.vida_maxima)

                case "Energia":  # Recupera de energia
                    jogador.energia_atual += valor
                    jogador.energia_atual = min(jogador.energia_atual, jogador.energia_maxima)

                case "Vida Máxima":  # Aumenta a vida máxima
                    jogador.vida_maxima += valor

                case "Energia Máxima":  # Aumenta a energia máxima
                    jogador.energia_maxima += valor

                case "Ataque":  # Aumenta o ataque
                    jogador.ataque += valor

                case "Sorte":  # Aumenta a sorte
                    jogador.sorte += valor

                case "Eletrificado":  # Aplica o status eletrificado
                    jogador.status.append("Eletrificado")

                case "Congelado":  # Aplica o status congelado
                    jogador.status.append("Congelado")

                case "Molhado":  # Aplica o status molhado
                    jogador.status.append("Molhado")

                case "Envenenado":  # Aplica o status envenenado
                    jogador.status.append("Envenenado")

                case "Sangramento":  # Aplica o status sangramento
                    jogador.status.append("Sangramento")

                case "Queimadura":  # Aplica o status queimadura
                    jogador.status.append("Queimadura")

                case "Tontura":  # Aplica o status tontura
                    jogador.status.append("Tontura")

                case "Cegueira":  # Aplica o status cegueira
                    jogador.status.append("Cegueira")

                case "Purificação":  # Remove todos os status negativos
                    jogador.status = [status for status in jogador.status if status not in [
                        "Eletrificado", "Congelado", "Molhado", "Envenenado", "Sangramento", "Queimadura", "Tontura", "Cegueira"]]

                case _:  # Caso o efeito não seja reconhecido
                    print(f"Efeito desconhecido: {tipo}")

            # Você pode adicionar suporte a outros tipos de efeito aqui futuramente

    def resumir_efeitos(self):
        return ", ".join(
            f"+{e['valor']} {e['nome']}" if e.get('valor') is not None else e['nome']
            for e in self.efeitos
        )
