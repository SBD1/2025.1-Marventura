from entidades.item_inventario import ItemInventario

class Mochila:
    def __init__(self, itens=None):
        self.itens = itens or []  # Lista de objetos ItemInventario

    def adicionar(self, item: ItemInventario):
        existente = self.encontrar_item_por_id(item.id)
        if existente:
            existente.quantidade += item.quantidade
        else:
            self.itens.append(item)

    def remover(self, id_item):
        self.itens = [i for i in self.itens if i.id != id_item]

    def buscar_por_tipo(self, tipo):
        return [i for i in self.itens if i.tipo == tipo]

    def encontrar_item_por_id(self, id_item):
        return next((i for i in self.itens if i.id == id_item), None)

    def usar_item(self, id_item, jogador):
        item = self.encontrar_item_por_id(id_item)
        if item:
            jogador.aplicar_efeitos(item.efeitos)
            item.quantidade -= 1
            if item.quantidade <= 0:
                self.remover(id_item)
            return True
        return False
