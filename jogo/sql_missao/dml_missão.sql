-- INSERÇÕES NA TABELA: JOGADOR
INSERT INTO Jogador (idJogador, idHabilidade, idMapa, Energia, Vida, Nivel, Sorte, VidaAtual, DanoBase, ExperienciaAtual, CoordenadaX, CoordenadaY) VALUES
(NEXTVAL('global_numeric_id_sequence'), 100, 1, 100, 100, 1, 0, 100, 10, 0, 0, 0);

-- INSERÇÕES NA TABELA: HABITANTE
INSERT INTO Habitante (idHabitante, idMapa, Tipo, Especialidade, CoordenadaX, CoordenadaY) VALUES
(NEXTVAL('global_numeric_id_sequence'), 101, 'Aldeao', 'Nenhum', 10, 5);

INSERT INTO Habitante (idHabitante, idMapa, Tipo, Especialidade, CoordenadaX, CoordenadaY) VALUES
(NEXTVAL('global_numeric_id_sequence'), 601, 'Medico', 'Curandeira', 15, 10);

INSERT INTO Habitante (idHabitante, idMapa, Tipo, Especialidade, CoordenadaX, CoordenadaY) VALUES
(NEXTVAL('global_numeric_id_sequence'), 701, 'Morador Secreto', 'Tecnicas Secretas', 50, 50);

-- INSERÇÕES NA TABELA: CHEFE
INSERT INTO Chefe (idChefe, idHabilidade, idMapa, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(NEXTVAL('global_numeric_id_sequence'), 200, 202, 'A Fera', 'Animal selvagem que ataca plantacoes.', 10, 10, 150, 5, 20, 50, 'Animal');

INSERT INTO Chefe (idChefe, idHabilidade, idMapa, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(NEXTVAL('global_numeric_id_sequence'), 201, 303, 'Comandante da Marinha', 'Lider corrupto da Marinha na cidade.', 25, 25, 200, 10, 30, 100, 'Humanoide');

INSERT INTO Chefe (idChefe, idHabilidade, idMapa, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(NEXTVAL('global_numeric_id_sequence'), 204, 301, 'Lider Rebelde', 'Lider de um grupo de rebeldes que conhece a irma do protagonista.', 20, 15, 120, 8, 15, 80, 'Humanoide');

INSERT INTO Chefe (idChefe, idHabilidade, idMapa, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(NEXTVAL('global_numeric_id_sequence'), 202, 503, 'Lider Pirata do Deserto', 'Chefao dos piratas no deserto.', 5, 5, 250, 15, 40, 150, 'Humanoide');

INSERT INTO Chefe (idChefe, idHabilidade, idMapa, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(NEXTVAL('global_numeric_id_sequence'), 203, 801, 'Marinheiro Nobre - Forma Final', 'Vilao final com dupla personalidade.', 40, 40, 300, 20, 50, 200, 'Humanoide');

-- INSERÇÕES NA TABELA: ITEM
INSERT INTO Item (ItemID, Nome, Descricao, Tipo) VALUES
(NEXTVAL('global_numeric_id_sequence'), 'Fruta Estranha', 'Fruta de gosto horrivel que concede poderes de eco.', 'Fruta');

-- INSERÇÕES NA TABELA: CAMPO_DE_BATALHA
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(201, 'Campo de Batalha', 'Clareira Selvagem', 1, 'Pequeno', 'Floresta', 1);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(202, 'Campo de Batalha', 'Bosque Assombrado', 1, 'Medio', 'Floresta', 1);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(302, 'Campo de Batalha', 'Setor de Registros', 1, 'Pequeno', 'Urbano', 5);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(303, 'Campo de Batalha', 'Praça Central', 1, 'Medio', 'Urbano', 1);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(402, 'Campo de Batalha', 'Trilha Congelada', 1, 'Pequeno', 'Neve', 3);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(403, 'Campo de Batalha', 'Litoral Norte', 1, 'Medio', 'Costa', 10);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(501, 'Campo de Batalha', 'Dunas Arenosas', 1, 'Grande', 'Deserto', 1);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(502, 'Campo de Batalha', 'Ruínas Antigas', 1, 'Pequeno', 'Deserto', 0);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(503, 'Campo de Batalha', 'Oásis da Batalha', 1, 'Medio', 'Deserto', 1);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(701, 'Campo de Batalha', 'Ilha Fantasma', 1, 'Medio', 'Misterioso', 0);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(801, 'Campo de Batalha', 'Fortaleza da Marinha', 1, 'Grande', 'Militar', 10);

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(802, 'Campo de Batalha', 'Águas Tempestuosas', 1, 'Enorme', 'Aquatico', 1);

-- INSERÇÕES NA TABELA: VILA
INSERT INTO Vila (SalaID, TipoSala, Nome, TotalSalas, Informacoes) VALUES
(101, 'Vila', 'Vila Inicial', 1, 'Primeira vila encontrada, amigavel.');

INSERT INTO Vila (SalaID, TipoSala, Nome, TotalSalas, Informacoes) VALUES
(401, 'Vila', 'Vilarejo do Norte', 1, 'Vila fria, moradores desconfiados.');

INSERT INTO Vila (SalaID, TipoSala, Nome, TotalSalas, Informacoes) VALUES
(601, 'Vila', 'Vila da Neve', 1, 'Vila com medica famosa.');

-- INSERÇÕES NA TABELA: PORTO
INSERT INTO Porto (SalaID, TipoSala, Nome, TotalSalas, QtdBarcos, Capacidade, SentidoIlha) VALUES
(301, 'Porto', 'Porto da Cidade', 1, 5, 100, 'Leste');

-- INSERÇÕES NA TABELA: MISSÃO
INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 1, 1, 201, 'Campo de Batalha', 2, 'Derrotar o animal selvagem que atacou o protagonista no caminho para a vila.', 'Animal Selvagem');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 101, 1, 202, 'Campo de Batalha', 2, 'Enfrentar a fera que esta atacando camponeses e destruindo plantacoes perto da vila.', 'A Fera da Vila');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 301, 1, 301, 'Porto', 2, 'Salvar o velho vendedor de frutas sendo agredido no porto da cidade.', 'Vendedor Agressao');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 301, 1, 302, 'Campo de Batalha', 7, 'Invadir os registros da prisao para libertar inocentes e buscar pistas sobre a irma do protagonista.', 'Infiltracao Prisao');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 301, 1, 303, 'Campo de Batalha', 7, 'Lutar e derrotar o comandante da Marinha na cidade.', 'Comandante da Marinha');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 401, 1, 402, 'Campo de Batalha', 1, 'Lutar contra lobos no caminho para o vilarejo do norte.', 'Ataque de Lobos');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 401, 1, 403, 'Campo de Batalha', 1, 'Defender o vilarejo do norte de um ataque de piratas.', 'Defesa do Vilarejo');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 501, 1, 501, 'Campo de Batalha', 1, 'Lutar contra o verme de areia que destruiu o barco no deserto.', 'Verme da Areia');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 501, 1, 502, 'Campo de Batalha', 1, 'Destruir suprimentos e usar ilusoes para diminuir o numero de piratas no deserto.', 'Estrategia do Deserto');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 501, 1, 503, 'Campo de Batalha', 1, 'Lutar e derrotar o lider dos piratas no deserto.', 'Lider Pirata do Deserto');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 701, 1, 701, 'Campo de Batalha', 4, 'Passar por treinamento e coletar materiais para aprender tecnica secreta.', 'Treinamento Secreto');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 801, 1, 801, 'Campo de Batalha', 1, 'Realizar favores para os marinheiros enquanto espera o marinheiro nobre.', 'Favores na Fortaleza');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 802, 1, 802, 'Campo de Batalha', 1, 'Derrotar uma besta marinha no caminho para a fortaleza.', 'Besta Marinha');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 801, 1, 801, 'Campo de Batalha', 9, 'Lutar contra o marinheiro nobre em sua forma hibrida.', 'Marinheiro Nobre - Hibrido');

INSERT INTO Missão (MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(NEXTVAL('global_numeric_id_sequence'), 801, 1, 801, 'Campo de Batalha', 9, 'Luta final contra o marinheiro nobre em sua forma completa.', 'Marinheiro Nobre - Final');

-- INSERÇÕES NA TABELA: ITEMMISSÃO
INSERT INTO ItemMissão (MissaoID, IdentificadorItem) VALUES
(11, 10);