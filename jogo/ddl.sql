-- =========== Tabela de Tipos ===========
CREATE TABLE tipo_item (
    identificador_item SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL UNIQUE
);

-- =========== Tabela de Efeitos ===========
CREATE TABLE efeito (
    identificador_efeito SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    bravura TEXT
);

-- =========== Tabela de Habilidades (MOVIDO PARA CIMA para resolver dependências) ===========
CREATE TABLE habilidade (
    id_habilidade SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    dano INT,
    custo INT
);

-- =========== Tabela de Consumíveis ===========
CREATE TABLE consumivel (
    identificador_consumivel SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50),
    preco_compra DECIMAL(10, 2),
    preco_venda DECIMAL(10, 2),
    efabricavel BOOLEAN,
    FOREIGN KEY (tipo) REFERENCES tipo_item(tipo)
);

-- =========== Tabela de Não-Consumíveis ===========
CREATE TABLE nao_consumivel (
    identificador_nao_consumivel SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50),
    preco_compra DECIMAL(10, 2),
    preco_venda DECIMAL(10, 2),
    FOREIGN KEY (tipo) REFERENCES tipo_item(tipo)
);

-- =========== Tabela de Acessórios ===========
CREATE TABLE acessorio (
    identificador_acessorio INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50),
    preco_compra DECIMAL(10,2),
    preco_venda DECIMAL(10,2),
    FOREIGN KEY (identificador_acessorio) REFERENCES nao_consumivel(identificador_nao_consumivel)
);

-- =========== Tabela de Armas ===========
CREATE TABLE arma (
    identificador_arma INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50),
    preco_compra DECIMAL(10,2),
    preco_venda DECIMAL(10,2),
    identificador_habilidade INT,
    FOREIGN KEY (identificador_arma) REFERENCES nao_consumivel(identificador_nao_consumivel),
    FOREIGN KEY (identificador_habilidade) REFERENCES habilidade(id_habilidade) -- Agora 'habilidade' já existirá
);

-- =========== Tabela de Frutas ===========
CREATE TABLE fruta (
    identificador_fruta INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50),
    preco_compra DECIMAL(10,2),
    preco_venda DECIMAL(10,2),
    identificador_habilidade INT,
    FOREIGN KEY (identificador_fruta) REFERENCES nao_consumivel(identificador_nao_consumivel),
    FOREIGN KEY (identificador_habilidade) REFERENCES efeito(identificador_efeito) -- Nota: Aqui a FK para 'efeito' está mantida como no seu último script.
);

-- =========== Tabela de Relação Efeito x Consumível ===========
CREATE TABLE efeito_consumivel (
    identificador_efeito INT,
    identificador_consumivel INT,
    PRIMARY KEY (identificador_efeito, identificador_consumivel),
    FOREIGN KEY (identificador_efeito) REFERENCES efeito(identificador_efeito),
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel)
);

-- =========== Tabela de Relação Efeito x Acessório ===========
CREATE TABLE efeito_acessorio (
    identificador_efeito INT,
    identificador_acessorio INT,
    PRIMARY KEY (identificador_efeito, identificador_acessorio),
    FOREIGN KEY (identificador_efeito) REFERENCES efeito(identificador_efeito),
    FOREIGN KEY (identificador_acessorio) REFERENCES acessorio(identificador_acessorio)
);


-- =========== Tabelas de Personagens e Mundo ===========
CREATE TABLE tipo_personagem (
    id_personagem SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE mapa (
    id_mapa SERIAL PRIMARY KEY,
    total_ilhas INT,
    total_item_chave INT
);

CREATE TABLE jogador (
    id_jogador SERIAL PRIMARY KEY,
    id_personagem INT,
    id_habilidade INT,
    id_mapa INT,
    nome VARCHAR(100) NOT NULL,
    energia INT,
    vida INT,
    nivel INT,
    sorte INT,
    vida_atual INT,
    dano_base INT,
    experiencia_atual INT,
    coordenada_x DECIMAL(10,2),
    coordenada_y DECIMAL(10,2),
    FOREIGN KEY (id_personagem) REFERENCES tipo_personagem(id_personagem),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade), -- Agora 'habilidade' já existirá
    FOREIGN KEY (id_mapa) REFERENCES mapa(id_mapa)
);

-- =========== Tabela de Receitas ===========
CREATE TABLE receita (
    identificador_receita SERIAL PRIMARY KEY,
    consumivel_produzido INT,
    id_jogador INT,
    FOREIGN KEY (consumivel_produzido) REFERENCES consumivel(identificador_consumivel)
);

-- =========== Ingredientes ===========
CREATE TABLE ingrediente_consumivel (
    identificador_receita INT,
    identificador_consumivel INT,
    PRIMARY KEY (identificador_receita, identificador_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel)
);

CREATE TABLE ingrediente_nao_consumivel (
    identificador_receita INT,
    identificador_nao_consumivel INT,
    PRIMARY KEY (identificador_receita, identificador_nao_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_nao_consumivel) REFERENCES nao_consumivel(identificador_nao_consumivel)
);

CREATE TABLE chefe (
    id_chefe SERIAL PRIMARY KEY,
    id_habilidade INT,
    id_mapa INT,
    nome VARCHAR(100),
    dano INT,
    vida INT,
    nivel INT,
    experiencia INT,
    coordenada_x DECIMAL(10,2),
    coordenada_y DECIMAL(10,2),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade), -- Agora 'habilidade' já existirá
    FOREIGN KEY (id_mapa) REFERENCES mapa(id_mapa)
);

CREATE TABLE lacaio (
    id_lacaio SERIAL PRIMARY KEY,
    id_habilidade INT,
    id_mapa INT,
    nome VARCHAR(100),
    dano INT,
    vida INT,
    nivel INT,
    experiencia INT,
    coordenada_x DECIMAL(10,2),
    coordenada_y DECIMAL(10,2),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade), -- Agora 'habilidade' já existirá
    FOREIGN KEY (id_mapa) REFERENCES mapa(id_mapa)
);

CREATE TABLE instancia_lacaio (
    id_instancia_lacaio SERIAL PRIMARY KEY,
    id_lacaio INT,
    vida_atual INT,
    FOREIGN KEY (id_lacaio) REFERENCES lacaio(id_lacaio)
);

CREATE TABLE aliado (
    id_aliado SERIAL PRIMARY KEY,
    id_mapa INT,
    nome VARCHAR(100),
    vida INT,
    nivel INT,
    vida_atual INT,
    dano_base INT,
    coordenada_x DECIMAL(10,2),
    coordenada_y DECIMAL(10,2),
    FOREIGN KEY (id_mapa) REFERENCES mapa(id_mapa)
);

CREATE TABLE habitante (
    id_habitante SERIAL PRIMARY KEY,
    id_mapa INT,
    nome VARCHAR(100),
    tipo VARCHAR(50),
    especialidade VARCHAR(100),
    coordenada_x DECIMAL(10,2),
    coordenada_y DECIMAL(10,2),
    FOREIGN KEY (id_mapa) REFERENCES mapa(id_mapa)
);

-- =========== Relacionamentos ===========
CREATE TABLE habilidade_aliado (
    id_aliado INT,
    id_habilidade INT,
    PRIMARY KEY (id_aliado, id_habilidade),
    FOREIGN KEY (id_aliado) REFERENCES aliado(id_aliado),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade) -- Agora 'habilidade' já existirá
);

CREATE TABLE batalha (
    id_batalha SERIAL PRIMARY KEY,
    id_jogador INT,
    id_aliado INT,
    id_chefe INT,
    id_instancia_lacaio INT,
    experiencia_ganha INT,
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
    FOREIGN KEY (id_aliado) REFERENCES aliado(id_aliado),
    FOREIGN KEY (id_chefe) REFERENCES chefe(id_chefe),
    FOREIGN KEY (id_instancia_lacaio) REFERENCES instancia_lacaio(id_instancia_lacaio)
);

CREATE TABLE batalha_instancia_lacaio (
    id_batalha INT,
    id_instancia_lacaio INT,
    PRIMARY KEY (id_batalha, id_instancia_lacaio),
    FOREIGN KEY (id_batalha) REFERENCES batalha(id_batalha),
    FOREIGN KEY (id_instancia_lacaio) REFERENCES instancia_lacaio(id_instancia_lacaio)
);

CREATE TABLE negociacao (
    id_negociacao SERIAL PRIMARY KEY,
    identificador_item INT,
    id_jogador INT,
    id_vendedor INT,
    quantidade INT,
    preco_final DECIMAL(10,2),
    tipo VARCHAR(20),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item),
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
    FOREIGN KEY (id_vendedor) REFERENCES habitante(id_habitante)
);

-- Subclasses de Sala
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

CREATE TABLE missao (
    missao_id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    mapa_id INT,
    id_jogador INT,
    id_recrutador INT,
    tipo_sala VARCHAR(50) NOT NULL CHECK (tipo_sala IN ('campo_batalha', 'porto', 'vila')),
    sala_id INT NOT NULL,
    FOREIGN KEY (mapa_id) REFERENCES mapa(id_mapa),
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
    FOREIGN KEY (id_recrutador) REFERENCES habitante(id_habitante)
);

CREATE TABLE ilha (
    id SERIAL PRIMARY KEY,
    sala_id INT UNIQUE NOT NULL,
    tipo VARCHAR(50),
    tamanho VARCHAR(50),
    nome VARCHAR(100),
    quantidade_sala INT,
    FOREIGN KEY (sala_id) REFERENCES campo_batalha(sala_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE mar (
    mar_id SERIAL PRIMARY KEY,
    monstro VARCHAR(100),
    obstaculo VARCHAR(100)
);

CREATE TABLE mapa_mar (
    mapa_id INT NOT NULL,
    mar_id INT NOT NULL,
    PRIMARY KEY (mapa_id, mar_id),
    FOREIGN KEY (mapa_id) REFERENCES mapa(id_mapa),
    FOREIGN KEY (mar_id) REFERENCES mar(mar_id)
);

CREATE TABLE corredor_maritimo (
    maritimo_id SERIAL PRIMARY KEY,
    ilha_a INT NOT NULL,
    ilha_b INT NOT NULL,
    FOREIGN KEY (ilha_a) REFERENCES ilha(id),
    FOREIGN KEY (ilha_b) REFERENCES ilha(id)
);

CREATE TABLE controlador_mar (
    maritimo_id INT NOT NULL,
    mar_id INT NOT NULL,
    PRIMARY KEY (maritimo_id, mar_id),
    FOREIGN KEY (maritimo_id) REFERENCES corredor_maritimo(maritimo_id),
    FOREIGN KEY (mar_id) REFERENCES mar(mar_id)
);

-- =========== Tabela de Barco (NOVO FORMATO) ===========
CREATE TABLE barco (
    id SERIAL PRIMARY KEY,       -- Mudou de tipo_barco para id (SERIAL)
    tipo VARCHAR(50),            -- Era o antigo tipo_barco
    nome VARCHAR(100),
    melhoria TEXT,               -- Mudou de VARCHAR(255) para TEXT
    porto_id INT,                -- Nova coluna
    FOREIGN KEY (porto_id) REFERENCES porto(sala_id) -- FK para porto(sala_id)
);

-- =========== Tabelas que dependem de Barco ===========
CREATE TABLE barco_porto (
    barco_id INT NOT NULL, -- Renomeado de tipo_barco para barco_id
    sala_id INT NOT NULL,
    PRIMARY KEY (barco_id, sala_id),
    FOREIGN KEY (barco_id) REFERENCES barco(id), -- Deve referenciar barco(id)
    FOREIGN KEY (sala_id) REFERENCES porto(sala_id)
);

CREATE TABLE controlador_barco (
    barco_id INT NOT NULL, -- Renomeado de tipo_barco para barco_id
    maritimo_id INT NOT NULL,
    PRIMARY KEY (barco_id, maritimo_id),
    FOREIGN KEY (barco_id) REFERENCES barco(id), -- Deve referenciar barco(id)
    FOREIGN KEY (maritimo_id) REFERENCES corredor_maritimo(maritimo_id)
);

CREATE TABLE marco (
    mar_id INT PRIMARY KEY,
    monstro VARCHAR(100),
    obstaculo VARCHAR(100),
    FOREIGN KEY (mar_id) REFERENCES mar(mar_id)
);

-- Inventario and Item Tables
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_jogador INT NOT NULL,
    nome VARCHAR(100),
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador)
);

CREATE TABLE ItemInventario (
    id_inventario INT NOT NULL,
    identificador_item INT NOT NULL,
    PRIMARY KEY (id_inventario, identificador_item),
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item)
);

CREATE TABLE ItemMissao (
    missao_id INT NOT NULL,
    identificador_item INT NOT NULL,
    PRIMARY KEY (missao_id, identificador_item),
    FOREIGN KEY (missao_id) REFERENCES missao(missao_id),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item)
);

-- Finalmente, adicione as FKs restantes que dependem de tabelas criadas anteriormente
ALTER TABLE receita
ADD CONSTRAINT fk_receita_jogador FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador);