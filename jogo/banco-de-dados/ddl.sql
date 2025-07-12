CREATE TABLE tipo_item (
    identificador_item ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('ace', 'arm', 'fru', 'con', 'ncn'))
);

CREATE TRIGGER atribui_id_tipo_item
BEFORE INSERT ON tipo_item
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();



CREATE TABLE arma (
    identificador_arma ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    tipo_arma CHAR(3) NOT NULL CHECK (tipo_arma IN ('esp', 'est', 'arc')),
    local_encontrado CHAR(27) NOT NULL CHECK (local_encontrado IN ('Loja de Espadas', 'Loja de Estilingues e Arcos')),
    preco_de_compra SMALLINT NOT NULL CHECK (preco_de_compra BETWEEN 1 AND 999)
);

CREATE TRIGGER atribui_id_arma
BEFORE INSERT ON arma
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_item();



CREATE TABLE fruta (
    identificador_fruta ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(222) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Missão', 'Evento')),
    preco_de_venda SMALLINT CHECK (preco_de_venda IS NULL OR preco_de_venda BETWEEN 1 AND 999)
);

CREATE TRIGGER atribui_id_fruta
BEFORE INSERT ON fruta
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_item();



CREATE TABLE acessorio (
    identificador_acessorio ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(18) NOT NULL CHECK (local_encontrado IN ('Loja de Acessórios')),
    preco_de_compra SMALLINT NOT NULL CHECK (preco_de_compra BETWEEN 1 AND 999)
);

CREATE TRIGGER atribui_id_acessorio
BEFORE INSERT ON acessorio
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_item();



CREATE TABLE consumivel (
    identificador_consumivel ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(200) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57', 'Cozinha')),
    preco_de_compra SMALLINT CHECK (preco_de_compra IS NULL OR preco_de_compra BETWEEN 1 AND 999),
    preco_de_venda SMALLINT NOT NULL CHECK (preco_de_venda BETWEEN 1 AND 999),
    e_fabricavel BOOLEAN DEFAULT FALSE CHECK (e_fabricavel IN (TRUE, FALSE)),
    e_coletado BOOLEAN 
);

CREATE TRIGGER atribui_id_consumivel
BEFORE INSERT ON consumivel
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_item();



CREATE TABLE nao_consumivel (
    identificador_nao_consumivel ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57')),
    preco_de_compra SMALLINT CHECK (preco_de_compra IS NULL OR preco_de_compra BETWEEN 1 AND 999),
    preco_de_venda SMALLINT NOT NULL CHECK (preco_de_venda BETWEEN 1 AND 999),
    e_coletado BOOLEAN 
);

CREATE TRIGGER atribui_id_nao_consumivel
BEFORE INSERT ON nao_consumivel
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_item();



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
    nome CHAR(15) NOT NULL CHECK (nome IN ('Cura', 'Energia', 'Vida Máxima', 'Energia Máxima', 'Ataque', 'Sorte', 'Eletrificado', 'Congelado', 'Molhado', 'Envenenado', 'Sangramento', 'Queimadura', 'Tontura', 'Cegueira', 'Purificação')),
    valor SMALLINT CHECK (valor BETWEEN 1 AND 20)
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



CREATE TABLE habilidade (
    identificador_habilidade ID PRIMARY KEY,
    identificador_efeito ID REFERENCES efeito(identificador_efeito),
    nome CHAR(50) NOT NULL,
    descricao CHAR(200) NOT NULL,
    tipo_de_ataque CHAR(10) NOT NULL CHECK (tipo_de_ataque IN ('soco', 'espada', 'estilingue', 'arco', 'fruta')),
    tipo_de_alvo CHAR(15) NOT NULL CHECK (tipo_de_alvo IN ('fila', 'alvo_terrestre', 'terrestre', 'alvo_livre', 'area')),
    dano SMALLINT NOT NULL,
    custo SMALLINT DEFAULT 0
);

CREATE TRIGGER atribui_id_habilidade
BEFORE INSERT ON habilidade
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();



CREATE TABLE habilidade_arma (
    identificador_habilidade ID NOT NULL REFERENCES habilidade(identificador_habilidade),
    identificador_arma ID NOT NULL REFERENCES arma (identificador_arma),
    PRIMARY KEY (identificador_habilidade, identificador_arma)
);

CREATE TABLE habilidade_fruta (
    identificador_habilidade ID NOT NULL REFERENCES habilidade(identificador_habilidade),
    identificador_fruta ID NOT NULL REFERENCES fruta (identificador_fruta),
    PRIMARY KEY (identificador_habilidade, identificador_fruta)
);



CREATE TABLE progresso (
    identificador_progresso ID PRIMARY KEY,
    numero_do_slot SMALLINT NOT NULL UNIQUE CHECK (numero_do_slot BETWEEN 1 AND 3),
    data_ultimo_salvamento TIMESTAMP DEFAULT now(),
    ocupado BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TRIGGER atribui_id_progresso
BEFORE INSERT ON progresso
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();



CREATE TABLE ilha (
    identificador_ilha ID PRIMARY KEY,
    nome CHAR(30) CHECK (nome IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57'))
);

CREATE TRIGGER atribui_id_ilha
BEFORE INSERT ON ilha
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();




CREATE TABLE area (
    identificador_area ID PRIMARY KEY,
    identificador_ilha ID REFERENCES ilha(identificador_ilha),
    nome CHAR(30),
    tipo_area CHAR(25) NOT NULL CHECK (tipo_area IN ('Área de combate', 'Área neutra', 'Vila', 'Porto', 'Loja', 'Yomotsu Hirasaka')),
    chave_imagem_fundo CHAR(50) CHECK (chave_imagem_fundo ~ '^[a-z _]+$'),
    chave_imagem_frente CHAR(50) CHECK (chave_imagem_frente ~ '^[a-z _]+$'),

    -- Se NÃO for 'Yomotsu Hirasaka', então identificador_ilha é obrigatório
    CHECK (
        tipo_area = 'Yomotsu Hirasaka' OR identificador_ilha IS NOT NULL
    )
);

CREATE TRIGGER atribui_id_area
BEFORE INSERT ON area
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();



CREATE TABLE conexao_entre_areas (
    identificador_area_origem ID NOT NULL REFERENCES area(identificador_area),
    identificador_area_destino ID NOT NULL REFERENCES area(identificador_area),
    ponto_geracao_x SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    ponto_geracao_y SMALLINT CHECK (ponto_geracao_y BETWEEN 0 AND 5000),
    orientacao CHAR(8) CHECK (orientacao IN ('esquerda', 'direita')),
    PRIMARY KEY (identificador_area_origem, identificador_area_destino)
);



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
    identificador_progresso ID UNIQUE REFERENCES progresso(identificador_progresso),
    nome char(6) NOT NULL CHECK (nome IN ('Silvie', 'Shuan')),
    descricao CHAR(300),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    energia SMALLINT CHECK (energia BETWEEN 5 AND 35),
    energia_atual SMALLINT DEFAULT 5 CHECK (energia_atual BETWEEN 0 AND energia),
    vida SMALLINT CHECK (vida BETWEEN 10 AND 70),
    nivel SMALLINT CHECK (nivel BETWEEN 1 AND 60),
    sorte SMALLINT CHECK (sorte BETWEEN 1 AND 10), -- chance_de_esquiva = 1 - (0.95 ^ sorte)
    vida_atual SMALLINT CHECK (vida_atual BETWEEN 0 AND vida),
    experiencia_atual SMALLINT CHECK (experiencia_atual BETWEEN 0 AND 6000),
    moedas_totais SMALLINT NOT NULL CHECK (moedas_totais BETWEEN 0 AND 999)
);

CREATE TRIGGER atribui_id_jogador
BEFORE INSERT ON jogador
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();



CREATE TABLE aliado (
    identificador_aliado ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    identificador_progresso ID UNIQUE REFERENCES progresso(identificador_progresso),
    nome char(6) NOT NULL CHECK (nome IN ('Silvie', 'Shuan')),
    descricao CHAR(300),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida SMALLINT  CHECK (vida BETWEEN 10 AND 70),
    nivel SMALLINT CHECK (nivel BETWEEN 0 AND 60),
    vida_atual SMALLINT CHECK (vida_atual BETWEEN 0 AND vida)
);

CREATE TRIGGER atribui_id_aliado
BEFORE INSERT ON aliado
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();



CREATE TABLE chefe (
    identificador_chefe ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    nome CHAR(28),
    descricao CHAR(100),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 10 AND 60),
    experiencia SMALLINT,
    moedas_totais SMALLINT NOT NULL CHECK (moedas_totais BETWEEN 0 AND 999)
);

CREATE TRIGGER atribui_id_chefe
BEFORE INSERT ON chefe
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();



CREATE TABLE lacaio (
    identificador_lacaio ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    nome CHAR(20),
    descricao CHAR(100),
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 0 AND 60),
    experiencia SMALLINT,
    tempo_reacao SMALLINT
);

CREATE TRIGGER atribui_id_lacaio
BEFORE INSERT ON lacaio
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();



CREATE TABLE habitante (
    identificador_habitante ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    nome CHAR(27),
    descricao CHAR(500),
    chave_imagem CHAR(50) CHECK (chave_imagem ~ '^[a-z _]+$'),
    tipo_habitante CHAR(3) NOT NULL CHECK (tipo_habitante IN ('hbt', 'ven', 'coz', 'rct')),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    especialidade char(3) CHECK (especialidade IN ('arm', 'ace', 'com')),
    moedas_totais SMALLINT NOT NULL CHECK (moedas_totais BETWEEN 0 AND 999)
);

CREATE TRIGGER atribui_id_habitante
BEFORE INSERT ON habitante
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_personagem();



CREATE TABLE instancia_lacaio (
    identificador_instancia_lacaio ID PRIMARY KEY,
    identificador_lacaio ID NOT NULL REFERENCES lacaio(identificador_lacaio),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    moedas_totais SMALLINT NOT NULL CHECK (moedas_totais BETWEEN 0 AND 999)
);

CREATE TRIGGER atribui_id_instancia_lacaio
BEFORE INSERT ON instancia_lacaio
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();



CREATE TABLE barco (
    identificador_barco ID PRIMARY KEY,
    identificador_progresso ID NOT NULL REFERENCES progresso(identificador_progresso),
    tipo_barco CHAR(3) NOT NULL CHECK (tipo_barco IN ('can', 'vel', 'nav')),
    nome CHAR(30) NOT NULL,
    descricao CHAR (150) NOT NULL,
    estado CHAR (9) NOT NULL CHECK (estado IN ('bloquedo', 'adquirido', 'destruido'))
);

CREATE TRIGGER atribui_id_barco
BEFORE INSERT ON barco
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();



CREATE TABLE habilidade_personagem (
    identificador_personagem ID,
    identificador_habilidade ID,
    PRIMARY KEY (identificador_personagem, identificador_habilidade),
    FOREIGN KEY (identificador_personagem) REFERENCES tipo_personagem(identificador_personagem),
    FOREIGN KEY (identificador_habilidade) REFERENCES habilidade(identificador_habilidade)
);



CREATE TABLE receitas_conhecidas (
    identificador_progresso ID,
    identificador_receita ID,
    PRIMARY KEY (identificador_progresso, identificador_receita),
    FOREIGN KEY (identificador_progresso) REFERENCES progresso(identificador_progresso),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita)
);



CREATE TABLE inventario (
    identificador_inventario ID PRIMARY KEY,
    identificador_personagem ID NOT NULL REFERENCES tipo_personagem(identificador_personagem),
    identificador_progresso ID NOT NULL REFERENCES progresso(identificador_progresso),
    tipo_inventario CHAR(3) DEFAULT 'moc' NOT NULL CHECK (tipo_inventario IN ('moc', 'kit'))
);

CREATE TRIGGER atribui_id_inventario
BEFORE INSERT ON inventario
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();



CREATE TABLE item_inventario (
    identificador_inventario ID,
    identificador_item ID,
    quantidade SMALLINT DEFAULT 0 CHECK (quantidade BETWEEN 0 AND 99),
    PRIMARY KEY (identificador_inventario, identificador_item),
    FOREIGN KEY (identificador_inventario) REFERENCES inventario(identificador_inventario),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item)
);



CREATE TABLE ilha_visitada (
    identificador_progresso ID REFERENCES progresso(identificador_progresso),
    identificador_ilha ID REFERENCES ilha(identificador_ilha),
    PRIMARY KEY (identificador_progresso, identificador_ilha),
    visitada BOOLEAN NOT NULL DEFAULT FALSE
);



CREATE TABLE conexao_entre_ilhas (
    identificador_ilha_a ID NOT NULL REFERENCES ilha(identificador_ilha),
    identificador_ilha_b ID NOT NULL REFERENCES ilha(identificador_ilha),
    identificador_progresso ID NOT NULL REFERENCES progresso(identificador_progresso),
    bloqueada BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (identificador_ilha_a, identificador_ilha_b, identificador_progresso)
);



CREATE TABLE area_visitada (
    identificador_progresso ID REFERENCES progresso(identificador_progresso),
    identificador_area ID REFERENCES area(identificador_area),
    PRIMARY KEY (identificador_progresso, identificador_area),
    visitada BOOLEAN NOT NULL DEFAULT FALSE
);



CREATE TABLE estado_instancia_lacaio (
    identificador_progresso ID REFERENCES progresso(identificador_progresso),
    identificador_instancia_lacaio ID REFERENCES instancia_lacaio(identificador_instancia_lacaio),
    identificador_area_atual ID REFERENCES area(identificador_area),
    vida_atual SMALLINT,
    data_da_morte TIMESTAMP DEFAULT NULL,
    PRIMARY KEY (identificador_progresso, identificador_instancia_lacaio)
);



CREATE TABLE estado_chefe (
    identificador_progresso ID REFERENCES progresso(identificador_progresso),
    identificador_chefe ID REFERENCES chefe(identificador_chefe),
    identificador_area_atual ID REFERENCES area(identificador_area),
    vida_atual SMALLINT,
    data_da_morte TIMESTAMP DEFAULT NULL,
    PRIMARY KEY (identificador_progresso, identificador_chefe)
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



CREATE TABLE missao (
    identificador_missao ID PRIMARY KEY,
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    identificador_recrutador ID REFERENCES habitante(identificador_habitante), 
    identificador_missao_dependente ID REFERENCES missao(identificador_missao), 
    descricao CHAR(100),
    nome CHAR(50) NOT NULL,
    nivel_de_desbloqueio SMALLINT NOT NULL CHECK (nivel_de_desbloqueio BETWEEN 0 AND 60)
);

CREATE TRIGGER atribui_id_missao
BEFORE INSERT ON missao
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();



CREATE TABLE dialogo (
    identificador_dialogo ID PRIMARY KEY,
    identificador_personagem ID REFERENCES tipo_personagem(identificador_personagem),
    identificador_missao ID REFERENCES missao(identificador_missao),
    sequencia_local SMALLINT CHECK (sequencia_local > 0),
    genero CHAR(1) CHECK (genero IN ('M', 'F')),
    dialogo CHAR(500)
);

CREATE TRIGGER atribui_id_dialogo
BEFORE INSERT ON dialogo
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id();



CREATE TABLE estado_missao (
    identificador_missao ID REFERENCES missao(identificador_missao), 
    identificador_progresso ID REFERENCES progresso(identificador_progresso), 
    estado CHAR(9) NOT NULL DEFAULT 'pendente' CHECK (estado IN ('concluida', 'aceita', 'pendente')),
    PRIMARY KEY (identificador_missao, identificador_progresso)
);



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
    chave_imagem CHAR(50) CHECK (chave_imagem ~ '^[a-z _]+$'),
    x SMALLINT CHECK (x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (y BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (largura BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (altura BETWEEN 0 AND 5000)
);

CREATE TRIGGER atribui_id_obstaculo
BEFORE INSERT ON obstaculo
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



CREATE TABLE area_interativa (
    identificador_area_interativa ID PRIMARY KEY REFERENCES tipo_elemento_espacial(identificador_elemento_espacial),
    identificador_area_origem ID NOT NULL REFERENCES area(identificador_area),
    identificador_area_destino ID REFERENCES area(identificador_area),
    identificador_missao ID REFERENCES missao(identificador_missao),
    chave_imagem CHAR(50) CHECK (chave_imagem ~ '^[a-z _]+$'),
    x SMALLINT CHECK (x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (y BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (largura BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (altura BETWEEN 0 AND 5000),
    chance_sucesso DECIMAL DEFAULT 1.0 CHECK (chance_sucesso BETWEEN 0.0 AND 1.0),
    tipo_evento CHAR(10) NOT NULL CHECK (
        tipo_evento IN ('embarcar', 'investigar', 'mudar_area', 'missao')
    ),
    metodo_ativacao CHAR(7) NOT NULL CHECK (metodo_ativacao IN ('ativo', 'passivo')),
    ativa BOOLEAN NOT NULL DEFAULT TRUE

    CHECK (
        -- Se for 'mudar_area', identificador_area_destino é obrigatório
        (tipo_evento <> 'mudar_area' OR identificador_area_destino IS NOT NULL)
        AND
        -- Se for 'missao', identificador_missao é obrigatório
        (tipo_evento <> 'missao' OR identificador_missao IS NOT NULL)
    )
);

CREATE TRIGGER atribui_id_area_interativa
BEFORE INSERT ON area_interativa
FOR EACH ROW
EXECUTE FUNCTION public.gerar_id_tabelas_elemento_espacial();



CREATE TABLE recompensa_de_exploracao (
    identificador_area_interativa ID REFERENCES area_interativa(identificador_area_interativa),
    identificador_jogador ID REFERENCES tipo_personagem(identificador_personagem),
    data_da_tentativa TIMESTAMP NOT NULL DEFAULT now(),
    PRIMARY KEY (identificador_area_interativa, identificador_jogador)
);

CREATE TRIGGER trigger_registrar_interacao
BEFORE INSERT ON recompensa_de_exploracao
FOR EACH ROW
EXECUTE FUNCTION tentar_coletar_item();



CREATE TABLE item_missao (
    identificador_missao ID,
    identificador_item ID,
    quantidade SMALLINT DEFAULT 1 CHECK (quantidade BETWEEN 1 AND 99),
    PRIMARY KEY (identificador_missao, identificador_item),
    FOREIGN KEY (identificador_missao) REFERENCES missao(identificador_missao),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item)
);
