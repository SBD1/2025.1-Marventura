CREATE TABLE tipo_item (
    identificador_item ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('ace', 'arm', 'fru', 'con', 'ncn'))
);

CREATE TABLE habilidade (
    identificador_habilidade ID PRIMARY KEY,
    nome CHAR(50) NOT NULL CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    descricao CHAR(150) NOT NULL CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    tipo_de_ataque CHAR(10) NOT NULL CHECK (tipo_de_ataque IN ('soco', 'espada', 'estilingue', 'fruta')),
    dano SMALLINT NOT NULL,
    custo SMALLINT NOT NULL
);

CREATE TRIGGER atribui_id_habilidade
BEFORE INSERT ON habilidade
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE arma (
    identificador_arma ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    identificador_habilidade ID NOT NULL REFERENCES habilidade(identificador_habilidade),
    nome CHAR(50) NOT NULL CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    descricao CHAR(150) NOT NULL CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(4) NOT NULL CHECK (local_encontrado IN ('Loja')),
    preco_de_compra SMALLINT NOT NULL
);

CREATE TABLE fruta (
    identificador_fruta ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    identificador_habilidade ID NOT NULL REFERENCES habilidade(identificador_habilidade),
    nome CHAR(50) NOT NULL CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    descricao CHAR(150) NOT NULL CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Missão', 'Evento')),
    preco_de_venda SMALLINT NOT NULL
);

CREATE TABLE acessorio (
    identificador_acessorio ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    descricao CHAR(150) NOT NULL CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57')),
    preco_de_compra SMALLINT NOT NULL
);

CREATE TABLE consumivel (
    identificador_consumivel ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    descricao CHAR(150) NOT NULL CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57')),
    preco_de_compra SMALLINT,
    preco_de_venda SMALLINT NOT NULL,
    e_fabricavel BOOLEAN DEFAULT FALSE CHECK (e_fabricavel IN (TRUE, FALSE))
);

CREATE TABLE nao_consumivel (
    identificador_nao_consumivel ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    descricao CHAR(150) NOT NULL CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57')),
    preco_de_compra SMALLINT,
    preco_de_venda SMALLINT NOT NULL
);

CREATE TABLE receita (
    identificador_receita ID PRIMARY KEY,
    consumivel_produzido ID NOT NULL REFERENCES consumivel(identificador_consumivel)
);

CREATE TRIGGER atribui_id_receita
BEFORE INSERT ON receita
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE ingrediente_consumivel (
    identificador_receita ID NOT NULL REFERENCES receita(identificador_receita),
    identificador_consumivel ID NOT NULL REFERENCES consumivel(identificador_consumivel),
    PRIMARY KEY (identificador_receita, identificador_consumivel)
);

CREATE TABLE ingrediente_nao_consumivel (
    identificador_receita ID NOT NULL REFERENCES receita(identificador_receita),
    identificador_nao_consumivel ID NOT NULL REFERENCES nao_consumivel(identificador_nao_consumivel),
    PRIMARY KEY (identificador_receita, identificador_nao_consumivel)
);

CREATE TABLE efeito (
    identificador_efeito ID PRIMARY KEY,
    nome CHAR(25) NOT NULL CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    valor SMALLINT NOT NULL
);

CREATE TRIGGER atribui_id_efeito
BEFORE INSERT ON efeito
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE efeito_acessorio (
    identificador_efeito ID NOT NULL REFERENCES efeito(identificador_efeito),
    identificador_acessorio ID NOT NULL REFERENCES acessorio(identificador_acessorio),
    PRIMARY KEY (identificador_efeito, identificador_acessorio)
);

CREATE TABLE efeito_consumivel (
    identificador_efeito ID NOT NULL REFERENCES efeito(identificador_efeito),
    identificador_consumivel ID NOT NULL REFERENCES consumivel(identificador_consumivel),
    PRIMARY KEY (identificador_efeito, identificador_consumivel)
);

CREATE TABLE tipo_mapa (
    identificador_mapa ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('ilh', 'mar'))
);

CREATE TRIGGER atribui_id_tipo_mapa
BEFORE INSERT ON tipo_mapa
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE mar (
    identificador_mar ID PRIMARY KEY REFERENCES tipo_mapa(identificador_mapa),
    chave_imagem CHAR(15) NOT NULL CHECK (chave_imagem ~ '^[a-z_]+$')
);

CREATE TRIGGER atribui_id_mar
BEFORE INSERT ON mar
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_mapa();

CREATE TABLE barco (
    identificador_barco ID PRIMARY KEY,
    identificador_mar ID NOT NULL REFERENCES mar(identificador_mar),
    tipo CHAR(10) NOT NULL CHECK (tipo IN ('Canoa', 'Veleiro', 'Navio'))
);

CREATE TRIGGER atribui_id_barco
BEFORE INSERT ON barco
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE ilha (
    identificador_ilha ID PRIMARY KEY REFERENCES tipo_mapa(identificador_mapa),
    nome CHAR(30) CHECK (nome ~ '^[0-9a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    visitada BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TRIGGER atribui_id_ilha
BEFORE INSERT ON ilha
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_mapa();

CREATE TABLE conexao_entre_ilhas (
    identificador_ilha_origem ID NOT NULL REFERENCES ilha(identificador_ilha),
    identificador_ilha_destino ID NOT NULL REFERENCES ilha(identificador_ilha),
    bloqueada BOOLEAN,
    PRIMARY KEY (identificador_ilha_origem, identificador_ilha_destino)
);

CREATE TABLE area (
    identificador_area ID PRIMARY KEY,
    identificador_ilha ID NOT NULL REFERENCES ilha(identificador_ilha),
    nome CHAR(30) CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    tipo_area CHAR(25) NOT NULL CHECK (tipo_area IN ('Área de combate', 'Área neutra', 'Vila', 'Porto', 'Loja', 'Yomotsu Hirasaka')),
    chave_imagem_fundo CHAR(50) CHECK (BTRIM(chave_imagem_fundo) ~ '^[a-z_]+$'),
    chave_imagem_frente CHAR(50) CHECK (BTRIM(chave_imagem_frente) ~ '^[a-z_]+$'),
    visitada BOOLEAN
);

CREATE TRIGGER atribui_id_area
BEFORE INSERT ON area
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE conexao_entre_areas (
    identificador_area_origem ID NOT NULL REFERENCES area(identificador_area),
    identificador_area_destino ID NOT NULL REFERENCES area(identificador_area),
    PRIMARY KEY (identificador_area_origem, identificador_area_destino)
);

CREATE TABLE evento (
    identificador_evento ID PRIMARY KEY,
    identificador_ilha_origem ID,
    identificador_ilha_destino ID,
    identificador_area_origem ID,
    identificador_area_destino ID,
    tipo_evento CHAR(12) NOT NULL CHECK (tipo_evento IN ('embarcar', 'investigar', 'mudar_area')),
    ponto_geracao_x SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    ponto_geracao_y SMALLINT CHECK (ponto_geracao_y BETWEEN 0 AND 5000),
    orientacao CHAR(8) CHECK (orientacao IN ('esquerda', 'direita')),
    chance_sucesso DECIMAL CHECK (chance_sucesso BETWEEN 0.0 AND 1.0),
    FOREIGN KEY (identificador_ilha_origem, identificador_ilha_destino) REFERENCES conexao_entre_ilhas(identificador_ilha_origem, identificador_ilha_destino),
    FOREIGN KEY (identificador_area_origem, identificador_area_destino) REFERENCES conexao_entre_areas(identificador_area_origem, identificador_area_destino)
);

CREATE TRIGGER atribui_id_evento
BEFORE INSERT ON evento
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE tipo_elemento_espacial (
    identificador_elemento_espacial ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('ari', 'obs', 'cam'))
);

CREATE TRIGGER atribui_id_tipo_elemento_espacial
BEFORE INSERT ON tipo_elemento_espacial
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE obstaculo (
    identificador_obstaculo ID PRIMARY KEY REFERENCES tipo_elemento_espacial(identificador_elemento_espacial),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    chave_imagem CHAR(50) CHECK (chave_imagem ~ '^[a-z_]+$'),
    x SMALLINT CHECK (x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (y BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (largura BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (altura BETWEEN 0 AND 5000)
);

CREATE TRIGGER atribui_id_obstaculo
BEFORE INSERT ON obstaculo
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_elemento_espacial();

CREATE TABLE area_interativa (
    identificador_area_interativa ID PRIMARY KEY REFERENCES tipo_elemento_espacial(identificador_elemento_espacial),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    identificador_evento ID NOT NULL REFERENCES evento(identificador_evento),
    chave_imagem CHAR(50) CHECK (chave_imagem ~ '^[a-z_]+$'),
    x SMALLINT CHECK (x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (y BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (largura BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (altura BETWEEN 0 AND 5000)
);

CREATE TRIGGER atribui_id_area_interativa
BEFORE INSERT ON area_interativa
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_elemento_espacial();

CREATE TABLE caminho (
    identificador_caminho ID PRIMARY KEY REFERENCES tipo_elemento_espacial(identificador_elemento_espacial),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    tipo_terreno CHAR(6) DEFAULT 'normal' CHECK (tipo_terreno IN ('normal', 'neve', 'arena')),
    x SMALLINT CHECK (x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (y BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (largura BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (altura BETWEEN 0 AND 5000)
);

CREATE TRIGGER atribui_id_caminho
BEFORE INSERT ON caminho
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_elemento_espacial();

CREATE TABLE recompensa_de_exploracao (
    identificador_recompensa ID PRIMARY KEY,
    identificador_area_interativa ID NOT NULL REFERENCES area_interativa(identificador_area_interativa),
    data_da_tentativa TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TRIGGER atribui_id_recompensa_de_exploracao
BEFORE INSERT ON recompensa_de_exploracao
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE tipo_personagem (
    identificador_personagem ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('hbt', 'rct', 'coz', 'ven', 'ali', 'jog', 'lac', 'che'))
);

CREATE TRIGGER atribui_id_tipo_personagem
BEFORE INSERT ON tipo_personagem
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE jogador (
    identificador_jogador ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    nome char(6) NOT NULL CHECK (nome IN ('Silvie', 'Shuan')),
    descricao CHAR(100) CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-!?,.]+$'),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    energia SMALLINT,
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 0 AND 60),
    sorte SMALLINT,
    vida_atual SMALLINT CHECK (vida_atual BETWEEN 0 AND vida),
    experiencia_atual SMALLINT CHECK (experiencia_atual BETWEEN 0 AND 600)
);

CREATE TRIGGER atribui_id_jogador
BEFORE INSERT ON jogador
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();

CREATE TABLE aliado (
    identificador_aliado ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    nome char(6) NOT NULL CHECK (nome IN ('Silvie', 'Shuan')),
    descricao CHAR(100) CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-!?,.]+$'),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 0 AND 60),
    vida_atual SMALLINT CHECK (vida_atual BETWEEN 0 AND vida)
);

CREATE TRIGGER atribui_id_aliado
BEFORE INSERT ON aliado
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();

CREATE TABLE chefe (
    identificador_chefe ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_habilidade ID NOT NULL REFERENCES habilidade(identificador_habilidade),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    nome CHAR(28) CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    descricao CHAR(100) CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-!?,.]+$'),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 10 AND 60),
    experiencia SMALLINT
);

CREATE TRIGGER atribui_id_chefe
BEFORE INSERT ON chefe
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();

CREATE TABLE lacaio (
    identificador_lacaio ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_habilidade ID NOT NULL REFERENCES habilidade(identificador_habilidade),
    nome CHAR(15) CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    descricao CHAR(100) CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-!?,.]+$'),
    vida SMALLINT,
    nivel SMALLINT CHECK ( nivel BETWEEN 0 AND 60),
    experiencia SMALLINT
);

CREATE TRIGGER atribui_id_lacaio
BEFORE INSERT ON lacaio
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();

CREATE TABLE habitante (
    identificador_habitante ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    nome CHAR(15) CHECK (nome ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-]+$'),
    descricao CHAR(100) CHECK (descricao ~ '^[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ \\-!?,.]+$'),
    tipo_habitante CHAR(3) NOT NULL CHECK (tipo_habitante IN ('hbt', 'ven', 'coz', 'rct')),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    especialidade char(3) CHECK (especialidade IN ('arm', 'ace', 'com'))
);

CREATE TRIGGER atribui_id_habitante
BEFORE INSERT ON aliado
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();

CREATE TABLE instancia_lacaio (
    identificador_instancia_lacaio ID PRIMARY KEY,
    identificador_lacaio ID NOT NULL REFERENCES lacaio(identificador_lacaio),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida_atual SMALLINT
);

CREATE TRIGGER atribui_id_instancia_lacaio
BEFORE INSERT ON instancia_lacaio
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE batalha (
    identificador_batalha ID PRIMARY KEY,
    identificador_jogador ID NOT NULL REFERENCES jogador(identificador_jogador),
    identificador_aliado ID NOT NULL REFERENCES aliado(identificador_aliado),
    identificador_chefe ID NOT NULL REFERENCES chefe(identificador_chefe)
);

CREATE TRIGGER atribui_id_batalha
BEFORE INSERT ON batalha
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE batalha_instancia_lacaio (
    identificador_batalha ID,
    identificador_instancia_lacaio ID,
    PRIMARY KEY (identificador_batalha, identificador_instancia_lacaio),
    FOREIGN KEY (identificador_batalha) REFERENCES batalha(identificador_batalha),
    FOREIGN KEY (identificador_instancia_lacaio) REFERENCES instancia_lacaio(identificador_instancia_lacaio)
);

CREATE TABLE habilidade_jogador (
    identificador_jogador ID,
    identificador_habilidade ID,
    PRIMARY KEY (identificador_jogador, identificador_habilidade),
    FOREIGN KEY (identificador_jogador) REFERENCES jogador(identificador_jogador),
    FOREIGN KEY (identificador_habilidade) REFERENCES habilidade(identificador_habilidade)
);

CREATE TABLE habilidade_aliado (
    identificador_aliado ID,
    identificador_habilidade ID,
    PRIMARY KEY (identificador_aliado, identificador_habilidade),
    FOREIGN KEY (identificador_aliado) REFERENCES aliado(identificador_aliado),
    FOREIGN KEY (identificador_habilidade) REFERENCES habilidade(identificador_habilidade)
);

CREATE TABLE receitas_conhecidas (
    identificador_jogador ID,
    identificador_receita ID,
    PRIMARY KEY (identificador_jogador, identificador_receita),
    FOREIGN KEY (identificador_jogador) REFERENCES jogador(identificador_jogador),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita)
);

CREATE TABLE inventario (
    identificador_inventario ID PRIMARY KEY,
    identificador_personagem ID NOT NULL REFERENCES tipo_personagem(identificador_personagem),
    tipo_inventario CHAR(3) NOT NULL CHECK (tipo_inventario IN ('ger', 'kit'))
);

CREATE TRIGGER atribui_id_inventario
BEFORE INSERT ON inventario
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();

CREATE TABLE item_inventario (
    identificador_inventario ID,
    identificador_item ID,
    PRIMARY KEY (identificador_inventario, identificador_item),
    FOREIGN KEY (identificador_inventario) REFERENCES inventario(identificador_inventario),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item)
);

CREATE TABLE negociacao (
    identificador_negociacao ID PRIMARY KEY,
    identificador_item ID NOT NULL REFERENCES tipo_item(identificador_item),
    identificador_jogador ID NOT NULL REFERENCES jogador(identificador_jogador),
    identificador_vendedor ID NOT NULL REFERENCES habitante(identificador_habitante),
    quantidade SMALLINT CHECK (quantidade BETWEEN 0 AND 99),
    preco_final SMALLINT,
    tipo_negociacao CHAR(6) NOT NULL CHECK (tipo_negociacao IN ('compra', 'venda'))
);

CREATE TRIGGER atribui_id_negociacao
BEFORE INSERT ON negociacao
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();
