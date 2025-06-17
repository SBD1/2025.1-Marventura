CREATE TABLE efeito (
    identificador_efeito SMALLINT SERIAL PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    valor SMALLINT NOT NULL
);

CREATE TABLE consumivel (
    identificador_consumivel SMALLINT PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('con')),
    nome CHAR(100) NOT NULL,
    descricao CHAR(100) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL CHECK (Raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(100) NOT NULL CHECK (local_encontrado IN ('Campos', 'Cidade', 'Neve', 'Deserto', 'Ilha Assombrada', 'Fortaleza da Marinha')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL,
    e_fabricavel BOOLEAN
);

CREATE TABLE nao_consumivel (
    identificador_nao_consumivel SMALLINT PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('ncn')),
    nome CHAR(100) NOT NULL,
    descricao CHAR(100) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL CHECK (Raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(100) NOT NULL CHECK (local_encontrado IN ('Campos', 'Cidade', 'Neve', 'Deserto', 'Ilha Assombrada', 'Fortaleza da Marinha')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL,
);

CREATE TABLE efeito_consumivel (
    identificador_consumivel SMALLINT,
    identificador_efeito SMALLINT,
    PRIMARY KEY (identificador_consumivel, identificador_efeito),
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel),
    FOREIGN KEY (identificador_efeito) REFERENCES efeito(identificador_efeito)
);

CREATE TABLE receita (
    identificador_receita SMALLINT PRIMARY KEY,
    consumivel_produzido SMALLINT,
    FOREIGN KEY (consumivel_roduzido) REFERENCES consumivel(identificador_consumivel)
);

CREATE TABLE ingrediente_consumivel (
    identificador_receita SMALLINT,
    identificador_consumivel SMALLINT,
    PRIMARY KEY (identificador_receita, identificador_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel)
);

CREATE TABLE ingrediente_nao_consumivel (
    identificador_receita SMALLINT,
    identificador_nao_consumivel SMALLINT,
    PRIMARY KEY (identificador_receita, identificador_nao_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_nao_consumivel) REFERENCES nao_consumivel(identificador_nao_consumivel)
);