
CREATE SEQUENCE global_numeric_id_sequence START WITH 1 INCREMENT BY 1 NO CYCLE;

CREATE TABLE habilidade (
    id_habilidade SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    dano INT CHECK (dano >= 0 AND dano <= 20) NOT NULL,
    custo INT CHECK (custo >= 0 AND custo <= 4) NOT NULL
);

CREATE TABLE tipo_item (
    identificador_item SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE tipo_personagem (
    id_personagem SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE efeito (
    identificador_efeito SMALLINT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    valor SMALLINT NOT NULL
);

CREATE TABLE consumivel (
    identificador_consumivel SMALLINT PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('con')),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL,
    local_encontrado VARCHAR(100) NOT NULL CHECK (local_encontrado IN ('Campos', 'Cidade', 'Neve', 'Deserto', 'Ilha Assombrada', 'Fortaleza da Marinha')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL,
    e_fabricavel BOOLEAN
);

CREATE TABLE nao_consumivel (
    identificador_nao_consumivel SMALLINT PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('ncn')),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL,
    local_encontrado VARCHAR(100) NOT NULL CHECK (local_encontrado IN ('Campos', 'Cidade', 'Neve', 'Deserto', 'Ilha Assombrada', 'Fortaleza da Marinha')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL
);

CREATE TABLE efeito_consumivel (
    identificador_consumivel SMALLINT REFERENCES consumivel(identificador_consumivel) ON DELETE CASCADE,
    identificador_efeito SMALLINT REFERENCES efeito(identificador_efeito) ON DELETE CASCADE,
    PRIMARY KEY (identificador_consumivel, identificador_efeito)
);

CREATE TABLE receita (
    identificador_receita SMALLINT PRIMARY KEY,
    consumivel_produzido SMALLINT REFERENCES consumivel(identificador_consumivel) ON DELETE CASCADE
);

CREATE TABLE ingrediente_consumivel (
    identificador_receita SMALLINT REFERENCES receita(identificador_receita) ON DELETE CASCADE,
    identificador_consumivel SMALLINT REFERENCES consumivel(identificador_consumivel) ON DELETE CASCADE,
    PRIMARY KEY (identificador_receita, identificador_consumivel)
);

CREATE TABLE ingrediente_nao_consumivel (
    identificador_receita SMALLINT REFERENCES receita(identificador_receita) ON DELETE CASCADE,
    identificador_nao_consumivel SMALLINT REFERENCES nao_consumivel(identificador_nao_consumivel) ON DELETE CASCADE,
    PRIMARY KEY (identificador_receita, identificador_nao_consumivel)
);

CREATE TABLE campo_batalha (
    sala_id SERIAL PRIMARY KEY,
    tipo_terreno VARCHAR(50),
    qtd_de_pessoas INT,
    tamanho VARCHAR(50)
);

CREATE TABLE porto (
    sala_id SERIAL PRIMARY KEY,
    qtd_barcos INT,
    capacidade INT,
    sendo_ilha BOOLEAN
);

CREATE TABLE vila (
    sala_id SERIAL PRIMARY KEY,
    total_salas INT,
    informacoes TEXT
);

CREATE TABLE ilha (
    id SERIAL PRIMARY KEY,
    sala_id INT UNIQUE NOT NULL
);

CREATE TABLE mapa (
    id_mapa_pk SERIAL PRIMARY KEY,
    id_mapa INT NOT NULL,
    id_ilha INT NOT NULL REFERENCES ilha(id),
    UNIQUE (id_mapa, id_ilha)
);

CREATE TABLE jogador (
    id_jogador SERIAL PRIMARY KEY,
    id_personagem INT REFERENCES tipo_personagem(id_personagem),
    id_habilidade INT REFERENCES habilidade(id_habilidade),
    id_mapa_pk INT NOT NULL REFERENCES mapa(id_mapa_pk),
    nome VARCHAR(100) NOT NULL,
    energia INT DEFAULT 100,
    vida INT DEFAULT 100,
    nivel INT DEFAULT 1,
    sorte INT DEFAULT 0,
    vida_atual INT DEFAULT 100,
    dano_base INT NOT NULL,
    experiencia_atual INT DEFAULT 0,
    coordenada_x DECIMAL(10,2) NOT NULL,
    coordenada_y DECIMAL(10,2) NOT NULL
);

CREATE TABLE chefe (
    id_chefe SERIAL PRIMARY KEY,
    id_habilidade INT REFERENCES habilidade(id_habilidade),
    id_mapa_pk INT NOT NULL REFERENCES mapa(id_mapa_pk),
    nome VARCHAR(28) NOT NULL UNIQUE,
    dano INT,
    vida INT DEFAULT 100,
    nivel INT DEFAULT 1,
    experiencia INT NOT NULL,
    coordenada_x DECIMAL(10,2) NOT NULL,
    coordenada_y DECIMAL(10,2) NOT NULL
);

CREATE TABLE lacaio (
    id_lacaio SERIAL PRIMARY KEY,
    id_habilidade INT REFERENCES habilidade(id_habilidade),
    id_mapa_pk INT NOT NULL REFERENCES mapa(id_mapa_pk),
    nome VARCHAR(15) NOT NULL,
    dano INT,
    vida INT DEFAULT 100,
    nivel INT DEFAULT 1,
    experiencia INT NOT NULL,
    coordenada_x DECIMAL(10,2) NOT NULL,
    coordenada_y DECIMAL(10,2) NOT NULL
);

CREATE TABLE instancia_lacaio (
    id_instancia_lacaio SERIAL PRIMARY KEY,
    identificador_lacaio INT NOT NULL REFERENCES lacaio(id_lacaio),
    vida_atual INT DEFAULT 100
);

CREATE TABLE aliado (
    id_aliado SERIAL PRIMARY KEY,
    id_mapa_pk INT NOT NULL REFERENCES mapa(id_mapa_pk),
    nome VARCHAR(6) NOT NULL UNIQUE,
    descricao VARCHAR(100) NOT NULL,
    vida INT DEFAULT 100,
    nivel INT DEFAULT 1,
    vida_atual INT DEFAULT 100,
    dano_base INT
);

CREATE TABLE habitante (
    identificador_habitante SERIAL PRIMARY KEY,
    id_mapa_pk INT NOT NULL REFERENCES mapa(id_mapa_pk),
    nome VARCHAR(15) NOT NULL,
    tipo VARCHAR(3) NOT NULL CHECK (tipo IN ('hbt', 'rec', 'coz', 'ven')),
    descricao VARCHAR(100) NOT NULL,
    especialidade VARCHAR(3) CHECK (especialidade IN ('arm', 'ace', 'com')),
    coordenada_x DECIMAL(10,2) NOT NULL,
    coordenada_y DECIMAL(10,2) NOT NULL
);

CREATE TABLE habilidade_aliado (
    id_aliado INT REFERENCES aliado(id_aliado),
    id_habilidade INT REFERENCES habilidade(id_habilidade),
    PRIMARY KEY (id_aliado, id_habilidade)
);

CREATE TABLE batalha (
    identificador_batalha SERIAL PRIMARY KEY,
    identificador_jogador INT REFERENCES jogador(id_jogador),
    identificador_aliado INT REFERENCES aliado(id_aliado),
    identificador_chefe INT REFERENCES chefe(id_chefe)
);

CREATE TABLE batalha_instancia_lacaio (
    identificador_batalha INT REFERENCES batalha(identificador_batalha) ON DELETE CASCADE,
    identificador_instancia_lacaio INT REFERENCES instancia_lacaio(id_instancia_lacaio) ON DELETE CASCADE,
    PRIMARY KEY (identificador_batalha, identificador_instancia_lacaio)
);

CREATE TABLE negociacao (
    identificador_negociacao SERIAL PRIMARY KEY,
    identificador_item INT NOT NULL REFERENCES tipo_item(identificador_item),
    identificador_jogador INT NOT NULL REFERENCES jogador(id_jogador),
    identificador_vendedor INT NOT NULL REFERENCES habitante(identificador_habitante),
    quantidade INT NOT NULL DEFAULT 0,
    preco_final DECIMAL(10,2) NOT NULL DEFAULT 1,
    tipo VARCHAR(6) NOT NULL CHECK (tipo IN ('compra', 'venda'))
);

CREATE TABLE missao (
    missao_id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    id_mapa_pk INT NOT NULL REFERENCES mapa(id_mapa_pk),
    id_jogador INT REFERENCES jogador(id_jogador),
    id_recrutador INT,
    tipo_sala VARCHAR(50) NOT NULL,
    sala_id INT NOT NULL
);

CREATE TABLE ItemMissao (
    missao_id INT NOT NULL REFERENCES missao(missao_id),
    identificador_item INT NOT NULL REFERENCES tipo_item(identificador_item),
    PRIMARY KEY (missao_id, identificador_item)
);

CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_jogador INT NOT NULL REFERENCES jogador(id_jogador),
    nome VARCHAR(100)
);

CREATE TABLE ItemInventario (
    id_inventario INT NOT NULL REFERENCES Inventario(id_inventario),
    identificador_item INT NOT NULL REFERENCES tipo_item(identificador_item),
    PRIMARY KEY (id_inventario, identificador_item)
);

CREATE TABLE mar (
    mar_id SERIAL PRIMARY KEY,
    monstro VARCHAR(100),
    obstaculo VARCHAR(100)
);

CREATE TABLE mapa_mar (
    id_mapa_pk INT NOT NULL REFERENCES mapa(id_mapa_pk),
    mar_id INT NOT NULL REFERENCES mar(mar_id),
    PRIMARY KEY (id_mapa_pk, mar_id)
);

CREATE TABLE corredor_maritimo (
    maritimo_id SERIAL PRIMARY KEY,
    ilha_a INT NOT NULL REFERENCES ilha(id),
    ilha_b INT NOT NULL REFERENCES ilha(id)
);

CREATE TABLE controlador_mar (
    maritimo_id INT NOT NULL REFERENCES corredor_maritimo(maritimo_id),
    mar_id INT NOT NULL REFERENCES mar(mar_id),
    PRIMARY KEY (maritimo_id, mar_id)
);

CREATE TABLE barco (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    nome VARCHAR(100),
    melhoria TEXT,
    porto_id INT REFERENCES porto(sala_id)
);

CREATE TABLE barco_porto (
    barco_id INT NOT NULL REFERENCES barco(id),
    sala_id INT NOT NULL REFERENCES porto(sala_id),
    PRIMARY KEY (barco_id, sala_id)
);

CREATE TABLE controlador_barco (
    barco_id INT NOT NULL REFERENCES barco(id),
    maritimo_id INT NOT NULL REFERENCES corredor_maritimo(maritimo_id),
    PRIMARY KEY (barco_id, maritimo_id)
);

CREATE TABLE marco (
    mar_id INT PRIMARY KEY REFERENCES mar(mar_id),
    monstro VARCHAR(100),
    obstaculo VARCHAR(100)
);