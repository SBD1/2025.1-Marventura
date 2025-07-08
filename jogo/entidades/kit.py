class KitDoExplorador:
    def __init__(self, kit):
        self.arma = None  # dict com dados da arma (já carregado do banco)
        self.fruta = None
        self.acessorio = None

        self.equipar(kit)
       

    def equipar(self, kit):
        for item in kit:
            match item.tipo_item:
                case "ace":
                    self.acessorio = item
                case "fru":
                    self.fruta = item
                case "arm":
                    self.arma = item
                    print(f"Arma equipada: {self.arma.nome_item} (ID: {self.arma.identificador_item}) (Tipo: {self.arma.tipo_arma}) (Raridade: {self.arma.raridade})")

    def obter_ids_do_equipamento(self):
        return {
            "id_arma": self.arma.identificador_item if self.arma else None,
            "id_fruta": self.fruta.identificador_item if self.fruta else None,
            "id_acessorio": self.acessorio.identificador_item if self.acessorio else None
        }
