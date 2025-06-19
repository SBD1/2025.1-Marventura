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
