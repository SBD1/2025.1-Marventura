-- Tabela Mapa
CREATE TABLE mapa (
    id SERIAL PRIMARY KEY,
    qtd_salas SMALLINT,
    total_itenas SMALLINT,
    total_itenas_chave SMALLINT
);

-- Tabela Ilhas
CREATE TABLE ilhas (
    id SERIAL PRIMARY KEY,
    tipo CHAR(50),
    nome CHAR(50),
    tamanho SMALLINT,
    quantidade_sala SMALLINT
);

-- Tabela Mar
CREATE TABLE mar (
    id SERIAL PRIMARY KEY,
    tipo CHAR(50), -- 'Monstro' ou 'Obstaculo'
    ilha_id SMALLINT REFERENCES ilhas(id)
);

-- Tabela Corredor Marítimo
CREATE TABLE corredor_maritmo (
    id SERIAL PRIMARY KEY,
    ilha_a SMALLINT REFERENCES ilhas(id),
    ilha_b SMALLINT REFERENCES ilhas(id),
    sentido CHAR(10)
);

-- Tabela Campo de Batalha
CREATE TABLE campo_batalha (
    sala_id SMALLINT PRIMARY KEY REFERENCES sala(sala_id),
    tipo_terreno CHAR(100),
    qtd_pessoas SMALLINT,
    tamanho SMALLINT
);

-- Tabela Porto
CREATE TABLE porto (
    id SERIAL PRIMARY KEY,
    sentidoilha CHAR(50),
    capacidade SMALLINT,
    qtde_barcos SMALLINT,
    campo_batalha_id SMALLINT REFERENCES campo_batalha(id)
);

-- Tabela Barco
CREATE TABLE barco (
    id SERIAL PRIMARY KEY,
    tipo CHAR(50),
    nome CHAR(50),
    melhoria CHAR(100),
    porto_id SMALLINT REFERENCES porto(id)
);
