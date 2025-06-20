CREATE TABLE tipo_item (
    identificador_item ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('ace', 'arm', 'fru', 'con', 'ncn'))
);

CREATE TABLE acessorio (
    identificador_acessorio ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('ace')),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL CHECK (Raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL
);

CREATE TRIGGER atribui_id_acessorio
BEFORE INSERT ON acessorio
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE arma (
    identificador_arma ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    identificador_habilidade ID REFERENCES habilidade(identificador_habilidade),
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('arm')),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL CHECK (Raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(4) NOT NULL CHECK (local_encontrado IN ('Loja')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL
);

CREATE TRIGGER atribui_id_arma
BEFORE INSERT ON arma
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE fruta (
    identificador_fruta ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    identificador_habilidade ID REFERENCES habilidade(identificador_habilidade),
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('fru')),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL CHECK (Raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Missão', 'Evento')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL
);

CREATE TRIGGER atribui_id_fruta
BEFORE INSERT ON fruta
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE consumivel (
    identificador_consumivel ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('con')),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL CHECK (Raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL,
    e_fabricavel BOOLEAN
);

CREATE TRIGGER atribui_id_consumivel
BEFORE INSERT ON consumivel
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE nao_consumivel (
    identificador_nao_consumivel ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('ncn')),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL CHECK (Raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL
);

CREATE TRIGGER atribui_id_nao_consumivel
BEFORE INSERT ON nao_consumivel
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE receita (
    identificador_receita ID PRIMARY KEY,
    consumivel_produzido ID REFERENCES consumivel(identificador_consumivel)
);

CREATE TRIGGER atribui_id_receita
BEFORE INSERT ON receita
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE ingrediente_consumivel (
    identificador_receita ID,
    identificador_consumivel ID,
    PRIMARY KEY (identificador_receita, identificador_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel)
);

CREATE TABLE ingrediente_nao_consumivel (
    identificador_receita ID,
    identificador_nao_consumivel ID,
    PRIMARY KEY (identificador_receita, identificador_nao_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_nao_consumivel) REFERENCES nao_consumivel(identificador_nao_consumivel)
);

CREATE TABLE efeito (
    identificador_efeito ID PRIMARY KEY,
    nome CHAR(25) NOT NULL,
    valor SMALLINT NOT NULL
);

CREATE TRIGGER atribui_id_efeito
BEFORE INSERT ON efeito
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE efeito_acessorio (
    identificador_efeito ID,
    identificador_acessorio ID,
    PRIMARY KEY (identificador_efeito, identificador_acessorio),
    FOREIGN KEY (identificador_efeito) REFERENCES efeito(identificador_efeito),
    FOREIGN KEY (identificador_acessorio) REFERENCES acessorio(identificador_acessorio)
);

CREATE TABLE efeito_consumivel (
    identificador_efeito ID,
    identificador_consumivel ID,
    PRIMARY KEY (identificador_efeito, identificador_consumivel),
    FOREIGN KEY (identificador_efeito) REFERENCES efeito(identificador_efeito)
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel),
);

CREATE TABLE habilidade (
    identificador_habilidade ID PRIMARY KEY,
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    tipo_de_ataque CHAR(10) NOT NULL CHECK (Tipo IN ('soco', 'espada', 'estilingue', 'fruta')),
    dano SMALLINT NOT NULL,
    custo SMALLINT NOT NULL
);

CREATE TRIGGER atribui_id_habilidade
BEFORE INSERT ON habilidade
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE TipoMapa (
    id_mapa ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('ilh', 'mar'))
);

CREATE TRIGGER atribui_id_tipomapa
BEFORE INSERT ON TipoMapa
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Mar (
    id_mar ID PRIMARY KEY,
    chave_imagem CHAR(15) NOT NULL
);

CREATE TRIGGER atribui_id_mar
BEFORE INSERT ON Mar
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Barco (
    id_barco ID PRIMARY KEY,
    id_mar ID NOT NULL REFERENCES Mar(id_mar),
    tipo CHAR(10) NOT NULL CHECK (tipo IN ('Canoa', 'Veleiro', 'Navio'))
);

CREATE TRIGGER atribui_id_barco
BEFORE INSERT ON Barco
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Ilha (
    id_ilha ID PRIMARY KEY,
    id_mapa ID NOT NULL REFERENCES TipoMapa(id_mapa),
    nome CHAR(30),
    visitada BOOLEAN
);

CREATE TRIGGER atribui_id_ilha
BEFORE INSERT ON Ilha
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE ConexaoEntreIlhas (
    id_ilha_origem ID NOT NULL REFERENCES Ilha(id_ilha),
    id_ilha_destino ID NOT NULL REFERENCES Ilha(id_ilha),
    bloqueada BOOLEAN,
    PRIMARY KEY (id_ilha_origem, id_ilha_destino)
);

CREATE TABLE Area (
    id_area ID PRIMARY KEY,
    id_ilha ID NOT NULL REFERENCES Ilha(id_ilha),
    nome CHAR(30),
    tipo_area CHAR(25) NOT NULL CHECK (tipo_area IN ('Área de combate', 'Área neutra', 'Vila', 'Porto', 'Loja', 'Yomotsu Hirasaka')),
    chave_imagem_fundo CHAR(50),
    chave_imagem_frente CHAR(50),
    visitada BOOLEAN
);

CREATE TRIGGER atribui_id_area
BEFORE INSERT ON Area
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE ConexaoEntreAreas (
    id_area_origem ID NOT NULL REFERENCES Area(id_area),
    id_area_destino ID NOT NULL REFERENCES Area(id_area),
    PRIMARY KEY (id_area_origem, id_area_destino)
);

CREATE TABLE Evento (
    id_evento ID PRIMARY KEY,
    id_ilha_origem ID,
    id_ilha_destino ID,
    id_area_origem ID,
    id_area_destino ID,
    tipo_evento CHAR(12) NOT NULL CHECK (tipo_evento IN ('embarcar', 'investigar', 'mudar_area')),
    ponto_geracao_x SMALLINT,
    ponto_geracao_y SMALLINT,
    orientacao CHAR(8) CHECK (orientacao IN ('esquerda', 'direita')),
    chance_sucesso DECIMAL,
    FOREIGN KEY (id_ilha_origem, id_ilha_destino) REFERENCES ConexaoEntreIlhas(id_ilha_origem, id_ilha_destino),
    FOREIGN KEY (id_area_origem, id_area_destino) REFERENCES ConexaoEntreAreas(id_area_origem, id_area_destino)
);

CREATE TRIGGER atribui_id_evento
BEFORE INSERT ON Evento
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE TipoElementoEspacial (
    id_elemento_espacial ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('are', 'obs'))
);

CREATE TRIGGER atribui_id_tipoelementoespacial
BEFORE INSERT ON TipoElementoEspacial
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Obstaculo (
    id_obstaculo ID PRIMARY KEY,
    id_area ID NOT NULL REFERENCES Area(id_area),
    chave_imagem CHAR(50),
    x SMALLINT,
    y SMALLINT,
    largura SMALLINT,
    altura SMALLINT
);

CREATE TRIGGER atribui_id_obstaculo
BEFORE INSERT ON Obstaculo
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE AreaInterativa (
    id_area_interativa ID PRIMARY KEY,
    id_area ID NOT NULL REFERENCES Area(id_area),
    id_evento ID NOT NULL REFERENCES Evento(id_evento),
    chave_imagem CHAR(50),
    x SMALLINT,
    y SMALLINT,
    largura SMALLINT,
    altura SMALLINT
);

CREATE TRIGGER atribui_id_areainterativa
BEFORE INSERT ON AreaInterativa
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE RecompensaDeExploracao (
    id_recompensa ID PRIMARY KEY,
    id_area_interativa ID NOT NULL REFERENCES AreaInterativa(id_area_interativa),
    data_da_tentativa TIMESTAMP
);

CREATE TRIGGER atribui_id_recompensadeexploracao
BEFORE INSERT ON RecompensaDeExploracao
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();
