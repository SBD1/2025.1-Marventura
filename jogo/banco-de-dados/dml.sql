INSERT INTO efeito (nome, valor) VALUES
('Restaura PE', 2),
('Restaura PV', 2),
('Restaura PV', 1),
('Restaura PE', 1),
('Restaura PV', 1),
('Restaura PE', 2),
('Restaura PV', 1),
('Aumenta Ataque', 2),
('Restaura PV', 1),
('Restaura PE', 2),
('Restaura PV', 3),
('Restaura PE', 3),
('Aumenta Ataque', 3),
('Restaura PV', -1),
('Aumenta Ataque', 2),
('Restaura PV', 2),
('Restaura PE', 2),
('Restaura PV', 4),
('Restaura PE', 1),
('Aumenta Ataque', 2),
('Restaura PE', 3),
('Restaura PV', 2),
('Aumenta Ataque', 3),
('Restaura PV', 2),
('Restaura PE', 3),
('Restaura PV', 1),
('Restaura PV', -2),
('Aumenta Ataque', 3),
('Restaura PV', 2),
('Restaura PE', 3),
('Restaura PE', 5),
('Restaura PV', 4),
('Restaura PE', 2),
('Restaura PV', 5),
('Restaura PE', 5),
('Restaura PV', 3),
('Aumenta Ataque', 3),
('Restaura PV', 7),
('Restaura PE', 1),
('Restaura PV', 3),
('Reduz Ataque', -2),
('Restaura PV', 5),
('Restaura PE', 3),
('Aumenta Ataque', 5),
('Aumenta Sorte', 2),
('Aumenta Sorte', 1),
('Aumenta Sorte', 4),
('Aumenta Sorte', 1),
('Aumenta Sorte', 3),
('Aumenta Sorte', 2),
('Restaura PE', 6),
('Restaura PV', 6),
('Restaura PV', 4),
('Aumenta Ataque', 4),
('Restaura PV', 2),
('Aumenta Ataque', 4),
('Restaura PE', 4),
('Restaura PV', 1),
('Restaura PE', 5),
('Restaura PV', 1),
('Restaura PE', 5),
('Restaura PV', 3),
('Restaura PE', 1),
('Aumenta Ataque', 3),
('Restaura PE', -1),
('Aumenta Ataque', 3),
('Restaura PE', 3),
('Aumenta Ataque', 1),
('Aumenta Sorte', 3),
('Aumenta Sorte', 1),
('Restaura PV', 2),
('Restaura PV', 1);



INSERT INTO nao_consumivel (identificador_nao_consumivel, nome, tipo, quantidade, raridade, preco_de_compra, preco_de_venda) VALUES
(8, 'Presa de Lobo', 'ncn', NULL, '★★', NULL, 15),
(12, 'Farinha Misteriosa', 'ncn', NULL, '★', 10, 5),
(13, 'ButterCream de Fuligem', 'ncn', NULL, '★★', 20, 8),
(16, 'Medalha de Marinheiro', 'ncn', NULL, '★★', NULL, 20),
(20, 'Pérola Cantante', 'ncn', NULL, '★★', 30, 17),
(23, 'Pedaço de Tecido Rasgado', 'ncn', NULL, '★', NULL, 8),
(31, 'Faixa de Pirata Estorricado', 'ncn', NULL, '★', NULL, 10),
(35, 'Sombra Engarrafada', 'ncn', NULL, '★★', NULL, 17),
(36, 'Açúcar Estranho', 'ncn', NULL, '★', 5, 2),
(38, 'Essência de Névoa Doce', 'ncn', NULL, '★★', 10, 4),
(42, 'Peixe Saltitante', 'ncn', NULL, '★', NULL, 11),
(48, 'Chapéu de Marinheiro', 'ncn', NULL, '★★', NULL, 15);



INSERT INTO consumivel
    (identificador_consumivel, nome, tipo, quantidade, raridade,
     preco_de_compra, preco_de_venda, e_fabricavel)
VALUES
(1,   'Fruta do Mar Azul',              'con', NULL, '★',  NULL,  5, 0),
(2,   'Fruta do Mar Vermelha',          'con', NULL, '★',  NULL,  5, 0),
(3,   'Folha de Hortelã',               'con', NULL, '★',  NULL,  5, 0),
(4,   'Abóbora Redonduda',              'con', NULL, '★',     15,  6, 0),
(5,   'Arroz do Planalto',              'con', NULL, '★',     10,  5, 0),
(6,   'Ovo dos Campos',                 'con', NULL, '★',     10,  5, 0),
(7,   'Carne de Ave Brava',             'con', NULL, '★',  NULL,  7, 0),
(9,   'Maçã Lustrosa',                  'con', NULL, '★',  NULL,  7, 0),
(10,  'Repolho Redondo',                'con', NULL, '★',  NULL,  5, 0),
(11,  'Alga Fresca',                    'con', NULL, '★',  NULL,  6, 0),
(14,  'Chá Enlatado',                   'con', NULL, '★',     15,  6, 0),
(15,  'Doce Amassado',                  'con', NULL, '★',  NULL,  2, 0),
(17,  'Noz Crocante',                   'con', NULL, '★',  NULL,  2, 0),
(18,  'Ervas Aromáticas',               'con', NULL, '★',  NULL,  3, 0),
(19,  'Neve Mágica',                    'con', NULL, '★★', NULL, 12, 0),
(21,  'Leite de Cabra Alpina',          'con', NULL, '★',     10,  6, 0),
(22,  'Chocolate Amargo',               'con', NULL, '★',     15,  8, 0),
(24,  'Lamento Gelado',                 'con', NULL, '★★', NULL, 12, 0),
(25,  'Fruta Cítrica do Oeste',         'con', NULL, '★',  NULL,  4, 0),
(26,  'Côco do Oásis',                  'con', NULL, '★',  NULL,  7, 0),
(27,  'Areia Mineral',                  'con', NULL, '★★', NULL, 10, 0),
(28,  'Carne do Deserto',               'con', NULL, '★★',    20,  8, 0),
(29,  'Geleia de Cacto Doce',           'con', NULL, '★★',    11,  6, 0),
(30,  'Suco Refrescante Solar',         'con', NULL, '★',      7,  4, 0),
(32,  'Fragmento de Miragem',           'con', NULL, '★★', NULL, 12, 0),
(33,  'Cogumelo Risonho',               'con', NULL, '★',  NULL,  9, 0),
(34,  'Fruta Fluorescente',             'con', NULL, '★',  NULL,  7, 0),
(37,  'Doce Fantasmal',                 'con', NULL, '★',     13,  5, 0),
(39,  'Asa de Morcego Noturno',         'con', NULL, '★',  NULL,  9, 0),
(40,  'Presa Venenosa',                 'con', NULL, '★',  NULL,  7, 0),
(41,  'Amendoim Crocante',              'con', NULL, '★',  NULL,  3, 0),
(43,  'Pepino de Salmoura',             'con', NULL, '★',  NULL,  5, 0),
(44,  'Ração de Soldado',               'con', NULL, '★★',    10,  4, 0),
(45,  'Café Turbinado',                 'con', NULL, '★',      8,  3, 0),
(46,  'Carne de Rei dos Mares',         'con', NULL, '★★★',   40, 19, 0),
(47,  'Rosquinha Mordida',              'con', NULL, '★',  NULL,  3, 0),
(101, 'Sushi Enrolado',                 'con', NULL, '★★', NULL, 15, 1),
(102, 'Chá de Algas',                   'con', NULL, '★',  NULL, 10, 1),
(103, 'Pastel de Fruta do Diabo',       'con', NULL, '★★', NULL, 18, 1),
(104, 'Caldo da Vovó Yuba',             'con', NULL, '★★', NULL, 22, 1),
(105, 'Tônico de Areia',                'con', NULL, '★★', NULL, 16, 1),
(106, 'Chá Gelado de Neve',             'con', NULL, '★★', NULL, 15, 1),
(107, 'Receita Secreta do Capitão',     'con', NULL, '★★★', NULL, 27, 1),
(108, 'Carne Grelhada',                 'con', NULL, '★★', NULL, 18, 1),
(109, 'Pérola Caramelizada',            'con', NULL, '★★', NULL, 13, 1),
(110, 'Pérola da Lua de Inverno',       'con', NULL, '★★★', NULL, 24, 1),
(111, 'Pérola do Sol Escaldante',       'con', NULL, '★★★', NULL, 24, 1),
(112, 'Gelado de Algas',                'con', NULL, '★',  NULL, 15, 1),
(113, 'Omurice de Arroz',               'con', NULL, '★★', NULL, 15, 1),
(114, 'Bolo do Campo',                  'con', NULL, '★★', NULL, 14, 1),
(115, 'Bombom Nebuloso',                'con', NULL, '★★', NULL, 12, 1),
(116, 'Arroz dos Sete Mares',           'con', NULL, '★',  NULL,  9, 1),
(117, 'Doce da Ilha',                   'con', NULL, '★★', NULL, 12, 1),
(118, 'Omelete dos 4 Ventos',           'con', NULL, '★★', NULL, 13, 1),
(119, 'Frango Assado Estaladiço',       'con', NULL, '★',  NULL, 10, 1),
(120, 'Sopa da Guarda Noturna',         'con', NULL, '★',  NULL,  6, 1),
(121, 'Doce de Duna Dourada',           'con', NULL, '★★', NULL, 16, 1),
(122, 'Bife do Abismo',                 'con', NULL, '★★★', NULL, 35, 1),
(123, 'Sashimi do Fim do Mundo',        'con', NULL, '★★★', NULL, 35, 1),
(124, 'Torta do Marujo Feliz',          'con', NULL, '★',  NULL, 10, 1),
(125, 'Doce Assombrado',                'con', NULL, '★★', NULL, 12, 1),
(126, 'Curry do Capitão Covarde',       'con', NULL, '★★', NULL, 13, 1),
(127, 'Elixir Sombrio',                 'con', NULL, '★★', NULL, 18, 1),
(128, 'Poção do Dente Torto',           'con', NULL, '★★', NULL, 18, 1),
(129, 'Cookie de Chocolate',            'con', NULL, '★',  NULL, 14, 1),
(130, 'Leite Condensado Alpino',        'con', NULL, '★',  NULL, 11, 1),
(131, 'Doce do Silêncio Eterno',        'con', NULL, '★★', NULL, 17, 1),
(132, 'Cacto‑Pop Geladinho',            'con', NULL, '★★', NULL, 16, 1),
(133, 'Esfera da Miragem',              'con', NULL, '★★', NULL, 17, 1),
(134, 'Amendoins Torrados',             'con', NULL, '★',  NULL,  5, 1),
(135, 'Pickles Pirata',                 'con', NULL, '★',  NULL, 10, 1),
(136, 'Frankenprato',                   'con', NULL, '★',  NULL,  5, 1);



INSERT INTO efeito_consumivel (identificador_consumivel, identificador_efeito) VALUES
(1, 1), (2, 2), (3, 3), (9, 4), (10, 5), (11, 6), (14, 7), (15, 8), (17, 2), (18, 9), (19, 10), (21, 11), (22, 12), (24, NULL),
(25, 13), (26, 14), (27, 11), (28, 15), (29, 16), (30, 17), (32, NULL),
(33, 18), (34, 19), (37, 20), (39, NULL), (40, NULL), (41, 21), (43, 22), (44, 23), (45, 24), (46, 25), (47, 56),
(101, 26), (102, 27), (103, 28), (104, 29), (105, 30), (106, 31), (107, 32), (108, 33), (109, 34), (110, 35), (111, 36), (112, 37), (113, 38), (114, 39), (115, 40), (116, 41), (117, 42), (118, 43), (119, 33), (120, 44), (121, 45), (122, 46), (123, 47), (124, 39), (125, 12), (126, 31), (127, 48), (128, 49), (129, 50), (130, 51), (131, 52), (132, 53), (133, 54), (134, 55), (135, 40), (136, 8);

INSERT INTO receita (identificador_receita, consumivel_produzido) VALUES
(1, 101), (2, 102), (3, 103), (4, 104), (5, 104), (6, 105), (7, 106), (8, 107), (9, 108), (10, 109),
(11, 110), (12, 111), (13, 112), (14, 113), (15, 114), (16, 115), (17, 115), (18, 116), (19, 116), (20, 116),
(21, 116), (22, 117), (23, 118), (24, 118), (25, 119), (26, 120), (27, 120), (28, 121), (29, 122), (30, 123),
(31, 124), (32, 125), (33, 126), (34, 127), (35, 128), (36, 129), (37, 130), (38, 131), (39, 132), (40, 133),
(41, 134), (42, 135), (43, 136);

INSERT INTO ingrediente_consumivel (identificador_receita, identificador_consumivel) VALUES
(1, 11), (2, 11), (3, 2), (3, 28), (4, 28), (4, 18), (5, 28), (5, 3), (6, 27), (7, 19), (7, 3), (8, 101), (8, 104), (9, 28),
(11, 109), (11, 19), (12, 109), (12, 19), (13, 11), (13, 19), (14, 5), (14, 6), (15, 6), (17, 22), (18, 5), (18, 1), (19, 5), (19, 2),
(20, 5), (20, 25), (21, 5), (21, 34), (22, 26), (22, 25), (23, 6), (23, 3), (24, 6), (24, 18), (25, 7), (25, 18),
(26, 10), (26, 11), (27, 10), (27, 7), (28, 27), (28, 26), (29, 46), (29, 24), (30, 46), (31, 4), (32, 4),
(33, 4), (33, 28), (34, 39), (35, 40), (35, 30), (36, 17), (36, 22), (37, 21), (38, 24), (38, 19),
(39, 29), (39, 25), (40, 32), (40, 27), (41, 41), (42, 43), (42, 28);

INSERT INTO ingrediente_nao_consumivel (identificador_receita, identificador_nao_consumivel) VALUES
(1, 42), (6, 38), (10, 20), (10, 36), (15, 12), (16, 35), (16, 38), (17, 35), (30, 35), (31, 12), (32, 38), (34, 35), (37, 36);

INSERT INTO ilha
	(nome, visitada)
VALUES
	('Ilha de Borabóia', FALSE), -- → ilh001
	('Cidade de Lurien', FALSE), -- → ilh002
	('Ilha Glacial de Frimora', FALSE), -- → ilh003
	('Cactuaraquara', FALSE), -- → ilh004
	('Nublária', FALSE), -- → ilh005
	('Quartel Naval D-57', FALSE); -- → ilh006

INSERT INTO conexao_entre_ilhas
    (ilha_a, ilha_b, bloqueada)
VALUES
    ('ilh001', 'ilh002', TRUE),
    ('ilh001', 'ilh004', TRUE),
    ('ilh002', 'ilh003', TRUE),
    ('ilh002', 'ilh006', TRUE),
    ('ilh003', 'ilh004', TRUE),
    ('ilh003', 'ilh005', TRUE),
    ('ilh005', 'ilh006', TRUE);

INSERT INTO area
	(identificador_ilha, nome, tipo_area, chave_imagem_fundo, chave_imagem_frente, visitada)
VALUES
	('ilh001', 'Pastos do Sol Dourado', 'Área de combate', 'cenario_boraboia_pastos', 'cenario_boraboia_pastos_camada_superior', FALSE), -- → are001
	('ilh001', 'Vilarejo de Borabóia', 'Vila', 'cenario_boraboia_vila', null, FALSE), -- → are002
	('ilh001', 'Vale Verdejante', 'Porto', 'cenario_boraboia_vale', null, FALSE), -- → are003
	('ilh001', 'Loja de Borabóia', 'Loja', 'loja_interior', null, FALSE), -- → are004
	('ilh001', 'Casa', 'Vila', 'cenario_boraboia_casa', null, FALSE), -- → are005
	('ilh001', 'Sótão', 'Vila', 'cenario_boraboia_sotao', null, FALSE), -- → are006
	('ilh002', 'Porto de Lurien', 'Porto', 'cenario_lurien_porto', 'cenario_lurien_porto_camada_superior', FALSE), -- → are007
	('ilh002', 'Centro', 'Área neutra', 'cenario_lurien_centro', null, FALSE), -- → are008
	('ilh002', 'Praça de execução', 'Área de combate', 'cenario_lurien_praca', null, FALSE), -- → are009
	('ilh002', 'Beco', 'Área neutra', 'cenario_lurien_beco', null, FALSE), -- → are010
	('ilh002', 'Esconderijo', 'Área neutra', 'cenario_lurien_esconderijo', null, FALSE), -- → are011
	('ilh002', 'Prisão', 'Área neutra', 'cenario_lurien_prisao', null, FALSE), -- → are012
	('ilh003', 'Porto de Frimora', 'Área neutra', 'cenario_frimora_porto', null, FALSE), -- → are013
	('ilh003', 'Vila de Frimora', 'Vila', 'cenario_frimora_vila', null, FALSE), -- → are014
	('ilh003', 'Montanha da Cabra Congelada', 'Área de combate', 'cenario_frimora_montanha', null, FALSE), -- → are015
	('ilh003', 'Cozinha da Vovó Yuba', 'Loja', 'cozinha_interior', null, FALSE), -- → are016
	('ilh004', 'Duna Braba', 'Porto', 'cenario_cactuaraquara_duna', null, FALSE), -- → are017
	('ilh004', 'Cidadela de Cactuaraquara', 'Vila', 'cenario_cactuaraquara_cidadela', null, FALSE), -- → are018
	('ilh004', 'Oásis de Ramtak', 'Área de combate', 'cenario_cactuaraquara_oasis', null, FALSE), -- → are019
	('ilh004', 'Loja de Cactuaraquara', 'Loja', 'loja_interior', null, FALSE), -- → are020
	('ilh005', 'Penumbra dos Ossudos', 'Porto', 'cenario_nublaria_penumbra', null, FALSE), -- → are021
	('ilh005', 'Acampamento de Nublária', 'Vila', 'cenario_nublaria_acampamento', null, FALSE), -- → are022
	('ilh005', 'Floresta', 'Área de combate', 'cenario_nublaria_floresta', null, FALSE), -- → are023
	('ilh005', 'Loja de Nublária', 'Loja', 'loja_interior', null, FALSE), -- → are024
    ('ilh005', 'Yomotsu Hirasaka', 'Yomotsu Hirasaka', null, null) -- → are025
	('ilh006', 'Porto da Égide', 'Porto', 'cenario_quartel_porto', null, FALSE), -- → are026
	('ilh006', 'Interior', 'Área de combate', 'cenario_quartel_interior', null, FALSE), -- → are027
	('ilh006', 'Escritório do Vice-Almirante', 'Área neutra', 'cenario_quartel_escritorio', null, FALSE), -- → are028
	('ilh006', 'Loja da Marinha', 'Loja', 'loja_interior', null, FALSE), -- → are029
	('ilh006', 'Cozinha do Capitão', 'Loja', 'cozinha_interior', null, FALSE); -- → are030

INSERT INTO conexao_entre_areas
    (area_a, area_b, bloqueada)
VALUES
    ('are001', 'are002', TRUE),
    ('are002', 'are003', TRUE),
    ('are002', 'are004', TRUE),
    ('are002', 'are005', TRUE),
    ('are005', 'are006', TRUE),
    ('are007', 'are008', TRUE),
    ('are008', 'are009', TRUE),
    ('are008', 'are010', TRUE),
    ('are009', 'are012', TRUE),
    ('are010', 'are011', TRUE),
    ('are013', 'are014', TRUE),
    ('are014', 'are015', TRUE),
    ('are014', 'are016', TRUE),
    ('are017', 'are018', TRUE),
    ('are018', 'are019', TRUE),
    ('are018', 'are020', TRUE),
    ('are021', 'are022', TRUE),
    ('are022', 'are023', TRUE),
    ('are022', 'are024', TRUE),
    ('are026', 'are027', TRUE),
    ('are027', 'are028', TRUE),
    ('are027', 'are029', TRUE),
    ('are027', 'are030', TRUE);

INSERT INTO caminho
    (identificador_area, tipo_terreno, x, y, largura, altura)
VALUES
    ('are001', 'arena', 3329, 0, 1144, 600),
    ('are001', 'normal', 4473, 197, 36, 180),
    ('are001', 'normal', 826, 216, 2503, 154),
    ('are001', 'normal', 826, 370, 150, 230),
    ('are001', 'normal', 339, 438, 487, 162),
    ('are002', 'normal', 0, 445, 3540, 155),
    ('are002', 'normal', 1728, 412, 174, 33),
    ('are003', 'normal', 0, 236, 1360, 156),
    ('are003', 'arena', 1360, 33, 1226, 567),
    ('are003', 'normal', 2586, 230, 827, 145),
    ('are003', 'normal', 3413, 230, 481, 370),
    ('are003', 'normal', 3894, 313, 361, 158);

INSERT INTO habitante
    (identificador_area, nome, descricao, tipo_habitante, coordenada_x, coordenada_y)
VALUES
    ('are001', 'Aldeão', 'Habitante da Ilha de Borabóia', 'rct', 0, 0),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 290, 300),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 615, 330),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 1650, 340),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 2775, 345),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 2870, 345),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 1000, 450),
    ('are002', 'Aldeão', 'Habitante da Ilha de Borabóia', 'hbt', 915, 323),
    ('are007', 'Cidadão', 'Costuma vender frutas no porto da Cidade de Lurien', 'rct', 0, 0),
    ('are012', 'Revolucionário', 'Oficial do exército revolucionário em missão na Cidade de Lurien', 'rct', 0, 0),
    ('are014', 'Chefe da vila', 'Chefe da vila da Ilha Glacial de Frimora', 'rct', 0, 0),
    ('are019', 'Chefe do vilarejo', 'Chefe do vilarejo de Cactuaraquara', 'rct', 0, 0),
    ('are027', 'Marinheiro', 'Marinheiro de baixo escalão', 'rct', 0, 0);
 
