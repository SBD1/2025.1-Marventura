CREATE EXTENSION IF NOT EXISTS btree_gist;

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
    ponto_geracao_x SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    ponto_geracao_y SMALLINT CHECK (ponto_geracao_y BETWEEN 0 AND 5000),
    orientacao CHAR(8) CHECK (orientacao IN ('esquerda', 'direita')),
    chance_sucesso DECIMAL CHECK (chance_sucesso BETWEEN 0.0 AND 1.0),
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
    x SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000)
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
    x SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000)
);

CREATE TRIGGER atribui_id_areainterativa
BEFORE INSERT ON AreaInterativa
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE RecompensaDeExploracao (
    id_recompensa ID PRIMARY KEY,
    id_area_interativa ID NOT NULL REFERENCES AreaInterativa(id_area_interativa),
    data_da_tentativa TIMESTAMPTZ NOT NULL DEFAULT now(),
    EXCLUDE USING GIST (
        id_area_interativa WITH =,
        tstzrange(data_da_tentativa, data_da_tentativa + interval '5 minutes') WITH &&
    )
);

CREATE TRIGGER atribui_id_recompensadeexploracao
BEFORE INSERT ON RecompensaDeExploracao
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE TipoPersonagem (
    id_personagem ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('hbt', 'rct', 'coz', 'ven', 'ali', 'jog', 'lac', 'che'))
);

CREATE TRIGGER atribui_id_tipopersonagem
BEFORE INSERT ON TipoPersonagem
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Jogador (
    id_jogador ID PRIMARY KEY,
    id_area ID NOT NULL REFERENCES Area(id_area),
    nome char(6) NOT NULL CHECK (nome IN ('Silvie', 'Shuan')),
    descricao CHAR(100),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    energia SMALLINT,
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 0 AND 60),
    sorte SMALLINT,
    vida_atual SMALLINT CHECK (vida_atual BETWEEN 0 AND vida),
    experiencia_atual SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 600)
);

CREATE TRIGGER atribui_id_jogador
BEFORE INSERT ON Jogador
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Aliado (
    id_aliado ID PRIMARY KEY,
    id_area ID NOT NULL REFERENCES Area(id_area),
    nome char(6) NOT NULL CHECK (nome IN ('Silvie', 'Shuan')),
    descricao CHAR(100),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 0 AND 60),
    vida_atual SMALLINT CHECK (vida_atual BETWEEN 0 AND vida)
);

CREATE TRIGGER atribui_id_aliado
BEFORE INSERT ON Aliado
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Chefe (
    id_chefe ID PRIMARY KEY,
    id_habilidade ID NOT NULL REFERENCES Habilidade(identificador_habilidade),
    id_area ID NOT NULL REFERENCES Area(id_area),
    nome CHAR(28),
    descricao CHAR(100),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 10 AND 60),
    experiencia SMALLINT
);

CREATE TRIGGER atribui_id_chefe
BEFORE INSERT ON Chefe
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Lacaio (
    id_lacaio ID PRIMARY KEY,
    id_habilidade ID NOT NULL REFERENCES Habilidade(identificador_habilidade),
    id_area ID NOT NULL REFERENCES Area(id_area),
    nome CHAR(15),
    descricao CHAR(100),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida SMALLINT,
    nivel SMALLINT CHECK ( nivel BETWEEN 0 AND 60),
    experiencia SMALLINT
);

CREATE TRIGGER atribui_id_lacaio
BEFORE INSERT ON Lacaio
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Habitante (
    id_habitante ID PRIMARY KEY,
    id_area ID NOT NULL REFERENCES Area(id_area),
    nome CHAR(15),
    descricao CHAR(100),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    especialidade char(3) NOT NULL CHECK (especialidade IN ('arm', 'ace', 'com')),
);

CREATE TRIGGER atribui_id_habitante
BEFORE INSERT ON Habitante
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE InstanciaLacaio (
    id_instancia_lacaio ID PRIMARY KEY,
    id_lacaio ID NOT NULL REFERENCES Lacaio(id_lacaio),
    id_area ID NOT NULL,
    vida_atual SMALLINT
);

CREATE TRIGGER atribui_id_instancialacaio
BEFORE INSERT ON InstanciaLacaio
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE Batalha (
    id_batalha ID PRIMARY KEY,
    id_jogador ID NOT NULL REFERENCES Jogador(id_jogador),
    id_aliado ID NOT NULL REFERENCES Aliado(id_aliado),
    id_chefe ID NOT NULL REFERENCES Chefe(id_chefe)
);

CREATE TRIGGER atribui_id_batalha
BEFORE INSERT ON Batalha
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE BatalhaInstanciaLacaio (
    id_batalha ID NOT NULL REFERENCES Batalha(id_batalha),
    id_instancia_lacaio ID NOT NULL REFERENCES InstanciaLacaio(id_instancia_lacaio),
    PRIMARY KEY (id_batalha, id_instancia_lacaio)
);

CREATE TABLE HabilidadeJogador (
    id_jogador ID NOT NULL REFERENCES Jogador(id_jogador),
    id_habilidade ID NOT NULL REFERENCES Habilidade(identificador_habilidade),
    PRIMARY KEY (id_jogador, id_habilidade)
);

CREATE TABLE HabilidadeAliado (
    id_aliado ID NOT NULL REFERENCES Aliado(id_aliado),
    id_habilidade ID NOT NULL REFERENCES Habilidade(identificador_habilidade),
    PRIMARY KEY (id_aliado, id_habilidade)
);

CREATE TABLE ReceitasConhecidas (
    id_jogador ID NOT NULL REFERENCES Jogador(id_jogador),
    id_receita ID NOT NULL REFERENCES receita(identificador_receita),
    PRIMARY KEY (id_jogador, id_receita)
);

CREATE TABLE Inventario (
    id_inventario ID PRIMARY KEY,
    id_personagem ID NOT NULL REFERENCES TipoPersonagem(id_personagem),
    tipo_inventario CHAR(3) NOT NULL CHECK (tipo_inventario IN ('ger', 'kit'))
);

CREATE TRIGGER atribui_id_inventario
BEFORE INSERT ON Inventario
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE ItemInventario (
    id_inventario ID NOT NULL REFERENCES Inventario(id_inventario),
    id_item ID NOT NULL REFERENCES tipo_item(identificador_item),
    PRIMARY KEY (id_inventario, id_item)
);

CREATE TABLE Negociacao (
    id_negociacao ID PRIMARY KEY,
    id_item ID NOT NULL REFERENCES tipo_item(identificador_item),
    id_jogador ID NOT NULL REFERENCES Jogador(id_jogador),
    id_vendedor ID NOT NULL REFERENCES Habitante(id_habitante),
    quantidade SMALLINT CHECK (quantidade BETWEEN 0 AND 99),
    preco_final SMALLINT,
    tipo_negociacao CHAR(6) NOT NULL CHECK (tipo_negociacao IN ('compra', 'venda'))
);

CREATE TRIGGER atribui_id_negociacao
BEFORE INSERT ON Negociacao
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();
