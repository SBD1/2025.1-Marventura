class KitDoExplorador:
    def __init__(self, id):
        self.id_kit = id
        self.arma = None  # dict com dados da arma (já carregado do banco)
        self.fruta = None
        self.acessorio = None

       

    def equipar(self, kit):
        match kit.tipo:
            case "ace":
                self.acessorio = kit
            case "fru":
                self.fruta = kit
            case "arm":
                self.arma = kit

    def obter_ids_do_equipamento(self):
        return {
            "id_arma": self.arma.identificador_item if self.arma else None,
            "id_fruta": self.fruta.identificador_item if self.fruta else None,
            "id_acessorio": self.acessorio.identificador_item if self.acessorio else None
        }
