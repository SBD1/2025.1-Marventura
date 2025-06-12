-- Tabela Mapa
CREATE TABLE mapa (
    id SERIAL PRIMARY KEY,
    qtd_salas INT,
    total_itenas INT,
    total_itenas_chave INT
);

-- Tabela Sala
CREATE TABLE sala (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    total_salas INT,
    mapa_id INT REFERENCES mapa(id)
);

-- Tabela Ilhas
CREATE TABLE ilhas (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    nome VARCHAR(100),
    tamanho INT,
    quantidade_sala INT
);

-- Tabela Mar
CREATE TABLE mar (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50), -- 'Monstro' ou 'Obstaculo'
    ilha_id INT REFERENCES ilhas(id)
);

-- Tabela Corredor_maritmo
CREATE TABLE corredor_maritmo (
    id SERIAL PRIMARY KEY,
    ilha_a INT REFERENCES ilhas(id),
    ilha_b INT REFERENCES ilhas(id),
    sentido VARCHAR(10)
);

-- Tabela CampoBatalha
CREATE TABLE campo_batalha (
    id SERIAL PRIMARY KEY,
    tipo_terreno VARCHAR(100),
    qtd_pessoas INT,
    tamanho INT,
    sala_id INT REFERENCES sala(id)
);

-- Tabela Porto
CREATE TABLE porto (
    id SERIAL PRIMARY KEY,
    sentidoilha VARCHAR(50),
    capacidade INT,
    qtde_barcos INT,
    campo_batalha_id INT REFERENCES campo_batalha(id)
);

-- Tabela Barco
CREATE TABLE barco (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    nome VARCHAR(100),
    melhoria TEXT,
    porto_id INT REFERENCES porto(id)
);
