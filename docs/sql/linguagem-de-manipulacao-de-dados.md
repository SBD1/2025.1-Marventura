# Linguagem de Manipulação de Dados (DML)

## Introdução

A Linguagem de Manipulação de Dados (DML) é um subconjunto de linguagens de banco de dados usado para **recuperar, inserir, excluir e modificar informações** em um banco de dados. É um componente essencial dos Sistemas de Gerenciamento de Banco de Dados (SGBDs). Ela permite que os usuários realizem as operações mais comuns e fundamentais em um banco de dados: a consulta e a modificação dos dados. Diferentemente da Linguagem de Definição de Dados (DDL), que se preocupa com a estrutura e o esquema do banco de dados, a DML foca no conteúdo.

As operações DML são geralmente executadas usando comandos específicos que são parte de uma linguagem de consulta mais ampla, como SQL (*Structured Query Language*). Esses comandos são o coração da interação diária com qualquer banco de dados relacional.

Os principais comandos DML incluem:

* `SELECT`: Usado para consultar e recuperar dados das tabelas do banco de dados.
* `INSERT`: Usado para adicionar novas linhas (registros) a uma tabela.
* `UPDATE`: Usado para modificar os dados existentes em uma ou mais linhas de uma tabela.
* `DELETE`: Usado para remover linhas de uma tabela.

Compreender a DML é crucial para desenvolvedores, analistas de dados, administradores de banco de dados e qualquer pessoa que precise interagir com dados armazenados de forma estruturada. 

---

## Metodologia

O aprendizado e a utilização da Linguagem de Manipulação de Dados (DML) geralmente seguem uma abordagem prática e incremental. A metodologia pode ser dividida nas seguintes etapas:

1.  **Compreensão dos Conceitos Fundamentais**:
    * Entender o que é um banco de dados relacional e seus componentes (tabelas, colunas, linhas, chaves primárias e estrangeiras).
    * Diferenciar DML de outras linguagens de banco de dados como DDL (*Data Definition Language*) e DCL (*Data Control Language*).

2.  **Aprendizado dos Comandos Básicos**:
    * **`SELECT`**: Iniciar com consultas simples para recuperar todas as colunas ou colunas específicas de uma tabela. Aprender a usar a cláusula `WHERE` para filtrar registros com base em condições.
    * **`INSERT`**: Praticar a inserção de novos registros em tabelas, especificando valores para todas as colunas ou um subconjunto delas.
    * **`UPDATE`**: Aprender a modificar registros existentes, utilizando a cláusula `WHERE` para especificar quais registros devem ser atualizados e a cláusula `SET` para definir os novos valores.
    * **`DELETE`**: Entender como remover registros de uma tabela, usando a cláusula `WHERE` para evitar a exclusão acidental de todos os dados. 

3.  **Prática com Exercícios e Projetos**:
    * Resolver problemas práticos que envolvam a criação de cenários e a manipulação de dados para atender a requisitos específicos.
    * Utilizar SGBDs reais (como MySQL, PostgreSQL, SQL Server, Oracle) para executar os comandos e observar os resultados. Ferramentas com interface gráfica (como DBeaver, pgAdmin, SQL Developer) podem auxiliar na visualização.
---

# DML - Linguagem de Manipulação de Dados

</CENTER>
---

```sql
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

INSERT INTO Habilidade (identificador_habilidade, dano, custo, nome, tipo) VALUES
(DEFAULT, 5, 1, 'Poder da Fruta do Eco', 'fruta');
INSERT INTO Habilidade (identificador_habilidade, dano, custo, nome, tipo) VALUES
(DEFAULT, 15, 0, 'Mordida Feroz', 'soco');
INSERT INTO Habilidade (identificador_habilidade, dano, custo, nome, tipo) VALUES
(DEFAULT, 10, 2, 'Golpe de Espada', 'espada');
INSERT INTO Habilidade (identificador_habilidade, dano, custo, nome, tipo) VALUES
(DEFAULT, 8, 1, 'Tiro de Pistola', 'projétil');
INSERT INTO Habilidade (identificador_habilidade, dano, custo, nome, tipo) VALUES
(DEFAULT, 12, 3, 'Avalanche', 'soco');
INSERT INTO Habilidade (identificador_habilidade, dano, custo, nome, tipo) VALUES
(DEFAULT, 20, 4, 'Transformacao', 'fruta');

INSERT INTO Ilha (ID, SalaID, TipoSala, Tamanho, Nome, Quantidade_sala, Tipo) VALUES
(DEFAULT, NULL, NULL, 'Grande', 'Ilha Principal', 3, 'Continente');
INSERT INTO Ilha (ID, SalaID, TipoSala, Nome, Quantidade_sala, Tipo) VALUES
(DEFAULT, 301, 'Porto', 'Ilha da Cidade', 5, 'Urbana');
INSERT INTO Ilha (ID, SalaID, TipoSala, Nome, Quantidade_sala, Tipo) VALUES
(DEFAULT, 401, 'Vila', 'Ilha do Norte', 2, 'Gélida');
INSERT INTO Ilha (ID, SalaID, TipoSala, Nome, Quantidade_sala, Tipo) VALUES
(DEFAULT, 501, 'Campo de Batalha', 'Ilha do Deserto', 3, 'Desértica');
INSERT INTO Ilha (ID, SalaID, TipoSala, Nome, Quantidade_sala, Tipo) VALUES
(DEFAULT, 701, 'Campo de Batalha', 'Ilha Fantasma', 1, 'Misteriosa');
INSERT INTO Ilha (ID, SalaID, TipoSala, Nome, Quantidade_sala, Tipo) VALUES
(DEFAULT, 801, 'Campo de Batalha', 'Ilha da Fortaleza', 1, 'Militar');

INSERT INTO Mapa (MapaID, IlhaID, TotalIlhas, TotalItensChave) VALUES
(1, 1, 1, 0);
INSERT INTO Mapa (MapaID, IlhaID, TotalIlhas, TotalItensChave) VALUES
(2, 2, 1, 1);
INSERT INTO Mapa (MapaID, IlhaID, TotalIlhas, TotalItensChave) VALUES
(3, 3, 1, 0);
INSERT INTO Mapa (MapaID, IlhaID, TotalIlhas, TotalItensChave) VALUES
(4, 4, 1, 0);
INSERT INTO Mapa (MapaID, IlhaID, TotalIlhas, TotalItensChave) VALUES
(5, 5, 1, 2);
INSERT INTO Mapa (MapaID, IlhaID, TotalIlhas, TotalItensChave) VALUES
(6, 6, 1, 3);

INSERT INTO Jogador (idJogador, idHabilidade, idMapa, IlhaID, Energia, Vida, Nivel, Sorte, VidaAtual, DanoBase, ExperienciaAtual, CoordenadaX, CoordenadaY) VALUES
(DEFAULT, 1, 1, 1, 100, 100, 1, 0, 100, 10, 0, 0, 0);

INSERT INTO Habitante (identificador_habitante, identificador_mapa, IlhaID, tipo, nome, descricao, especialidade, coordenada_x, coordenada_y) VALUES
(DEFAULT, 1, 1, 'rec', 'Aldeao', 'Aldeao que acorda o protagonista.', NULL, 10, 5);
INSERT INTO Habitante (identificador_habitante, identificador_mapa, IlhaID, tipo, nome, descricao, especialidade, coordenada_x, coordenada_y) VALUES
(DEFAULT, 6, 6, 'coz', 'Medico', 'Medica famosa da vila da neve.', 'curador', 15, 10);
INSERT INTO Habitante (identificador_habitante, identificador_mapa, IlhaID, tipo, nome, descricao, especialidade, coordenada_x, coordenada_y) VALUES
(DEFAULT, 5, 5, 'hbt', 'Morador Secreto', 'Morador escondido na ilha fantasma.', NULL, 50, 50);

INSERT INTO Chefe (idChefe, idHabilidade, idMapa, IlhaID, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(DEFAULT, 2, 1, 1, 'A Fera', 'Animal selvagem que ataca plantacoes.', 10, 10, 150, 5, 20, 50, 'Animal');
INSERT INTO Chefe (idChefe, idHabilidade, idMapa, IlhaID, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(DEFAULT, 3, 2, 2, 'Comandante da Marinha', 'Lider corrupto da Marinha na cidade.', 25, 25, 200, 10, 30, 100, 'Humanoide');
INSERT INTO Chefe (idChefe, idHabilidade, idMapa, IlhaID, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(DEFAULT, 4, 2, 2, 'Lider Rebelde', 'Lider de um grupo de rebeldes que conhece a irma do protagonista.', 20, 15, 120, 8, 15, 80, 'Humanoide');
INSERT INTO Chefe (idChefe, idHabilidade, idMapa, IlhaID, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(DEFAULT, 3, 4, 4, 'Lider Pirata do Deserto', 'Chefao dos piratas no deserto.', 5, 5, 250, 15, 40, 150, 'Humanoide');
INSERT INTO Chefe (idChefe, idHabilidade, idMapa, IlhaID, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo) VALUES
(DEFAULT, 6, 6, 6, 'Marinheiro Nobre - Forma Final', 'Vilao final com dupla personalidade.', 40, 40, 300, 20, 50, 200, 'Humanoide');

INSERT INTO TipoItem (IdentificadorItem, Tipo) VALUES
(DEFAULT, 'Fruta');

INSERT INTO Item (ItemID, Nome, Descricao, Tipo) VALUES
(DEFAULT, 'Fruta Estranha', 'Fruta de gosto horrivel que concede poderes de eco.', 'Fruta');

INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(201, 'Campo de Batalha', 'Clareira Selvagem', 1, 'Pequeno', 'Floresta', 1);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(202, 'Campo de Batalha', 'Bosque Assombrado', 1, 'Medio', 'Floresta', 1);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(302, 'Campo de Batalha', 'Setor de Registros', 1, 'Pequeno', 'Urbano', 5);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(303, 'Campo de Batalha', 'Praca Central', 1, 'Medio', 'Urbano', 1);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(402, 'Campo de Batalha', 'Trilha Congelada', 1, 'Pequeno', 'Neve', 3);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(403, 'Campo de Batalha', 'Litoral Norte', 1, 'Medio', 'Costa', 10);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(501, 'Campo de Batalha', 'Dunas Arenosas', 1, 'Grande', 'Deserto', 1);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(502, 'Campo de Batalha', 'Ruinas Antigas', 1, 'Pequeno', 'Deserto', 0);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(503, 'Campo de Batalha', 'Oasis da Batalha', 1, 'Medio', 'Deserto', 1);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(701, 'Campo de Batalha', 'Ilha Fantasma', 1, 'Medio', 'Misterioso', 0);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(801, 'Campo de Batalha', 'Fortaleza da Marinha', 1, 'Grande', 'Militar', 10);
INSERT INTO Campo_de_batalha (SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos) VALUES
(802, 'Campo de Batalha', 'Aguas Tempestuosas', 1, 'Enorme', 'Aquatico', 1);

INSERT INTO Vila (SalaID, TipoSala, Nome, TotalSalas, Informacoes) VALUES
(101, 'Vila', 'Vila Inicial', 1, 'Primeira vila encontrada, amigavel.');
INSERT INTO Vila (SalaID, TipoSala, Nome, TotalSalas, Informacoes) VALUES
(401, 'Vila', 'Vilarejo do Norte', 1, 'Vila fria, moradores desconfiados.');
INSERT INTO Vila (SalaID, TipoSala, Nome, TotalSalas, Informacoes) VALUES
(601, 'Vila', 'Vila da Neve', 1, 'Vila com medica famosa.');

INSERT INTO Porto (SalaID, TipoSala, Nome, TotalSalas, QtdBarcos, Capacidade, SentidoIlha) VALUES
(301, 'Porto', 'Porto da Cidade', 1, 5, 100, 'Leste');

INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 1, 1, 1, 201, 'Campo de Batalha', 2, 'Derrotar o animal selvagem que atacou o protagonista no caminho para a vila.', 'Animal Selvagem');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 1, 1, 1, 202, 'Campo de Batalha', 2, 'Enfrentar a fera que esta atacando camponeses e destruindo plantacoes perto da vila.', 'A Fera da Vila');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 2, 2, 1, 301, 'Porto', 2, 'Salvar o velho vendedor de frutas sendo agredido no porto da cidade.', 'Vendedor Agressao');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 2, 2, 1, 302, 'Campo de Batalha', 7, 'Invadir os registros da prisao para libertar inocentes e buscar pistas sobre a irma do protagonista.', 'Infiltracao Prisao');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 2, 2, 1, 303, 'Campo de Batalha', 7, 'Lutar e derrotar o comandante da Marinha na cidade.', 'Comandante da Marinha');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 3, 3, 1, 402, 'Campo de Batalha', 1, 'Lutar contra lobos no caminho para o vilarejo do norte.', 'Ataque de Lobos');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 3, 3, 1, 403, 'Campo de Batalha', 1, 'Defender o vilarejo do norte de um ataque de piratas.', 'Defesa do Vilarejo');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 4, 4, 1, 501, 'Campo de Batalha', 1, 'Lutar contra o verme de areia que destruiu o barco no deserto.', 'Verme da Areia');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 4, 4, 1, 502, 'Campo de Batalha', 1, 'Destruir suprimentos e usar ilusoes para diminuir o numero de piratas no deserto.', 'Estrategia do Deserto');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 4, 4, 1, 503, 'Campo de Batalha', 1, 'Lutar e derrotar o lider dos piratas no deserto.', 'Lider Pirata do Deserto');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 5, 5, 1, 701, 'Campo de Batalha', 4, 'Passar por treinamento e coletar materiais para aprender tecnica secreta.', 'Treinamento Secreto');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 6, 6, 1, 801, 'Campo de Batalha', 1, 'Realizar favores para os marinheiros enquanto espera o marinheiro nobre.', 'Favores na Fortaleza');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 6, 6, 1, 802, 'Campo de Batalha', 1, 'Derrotar uma besta marinha no caminho para a fortaleza.', 'Besta Marinha');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 6, 6, 1, 801, 'Campo de Batalha', 9, 'Lutar contra o marinheiro nobre em sua forma hibrida.', 'Marinheiro Nobre - Hibrido');
INSERT INTO Missão (MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome) VALUES
(DEFAULT, 6, 6, 1, 801, 'Campo de Batalha', 9, 'Luta final contra o marinheiro nobre em sua forma completa.', 'Marinheiro Nobre - Final');

INSERT INTO ItemMissão (MissaoID, IdentificadorItem) VALUES
(12, 11);

INSERT INTO Mar (MarID, Mostro, Obstaculo) VALUES
(DEFAULT, 'Kraken', 'Corais');
INSERT INTO Mar (MarID, Mostro, Obstaculo) VALUES
(DEFAULT, 'Serpente Marinha', 'Redemoinhos');

INSERT INTO Corredor_maritimo (marítimoID, IlhaA, IlhaB) VALUES
(DEFAULT, 1, 2);
INSERT INTO Corredor_maritimo (marítimoID, IlhaA, IlhaB) VALUES
(DEFAULT, 2, 3);
INSERT INTO Corredor_maritimo (marítimoID, IlhaA, IlhaB) VALUES
(DEFAULT, 3, 4);

INSERT INTO MapaMar (MapaID, IlhaID, MarID) VALUES
(1, 1, 1);
INSERT INTO MapaMar (MapaID, IlhaID, MarID) VALUES
(2, 2, 2);

INSERT INTO Controller_mar (marítimoID, MarID) VALUES
(1, 1);
INSERT INTO Controller_mar (marítimoID, MarID) VALUES
(2, 2);

INSERT INTO Barco (Tipo, Melhoria, Nome, Nivel) VALUES
('Canoa', 'Nenhuma', 'Pequena Canoa', 1);
INSERT INTO Barco (Tipo, Melhoria, Nome, Nivel) VALUES
('Barco a Vela', 'Vela Reforçada', 'Vento Veloz', 5);
INSERT INTO Barco (Tipo, Melhoria, Nome, Nivel) VALUES
('Navio Pirata', 'Canhoes', 'Terror dos Mares', 10);

INSERT INTO BarcoPorto (TipoSala, TipoBarco, SalaID) VALUES
('Porto', 'Canoa', 301);
INSERT INTO BarcoPorto (TipoSala, TipoBarco, SalaID) VALUES
('Porto', 'Barco a Vela', 301);

INSERT INTO Controller_barco (IDBarco, marítimoID) VALUES
('Canoa', 1);
INSERT INTO Controller_barco (IDBarco, marítimoID) VALUES
('Barco a Vela', 2);
```


## 📚 Bibliografia

* ELMASRI, R.; NAVATHE, S. B. *Sistemas de Banco de Dados*. 7. ed. Pearson Education do Brasil, 2018.
* DATE, C. J. *An Introduction to Database Systems*. 8. ed. Addison-Wesley, 2003.
* SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. *Database System Concepts*. 7. ed. McGraw-Hill Education, 2019.
* Oracle Database SQL Language Reference. Disponível em: [https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/index.html](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/index.html) (Acesso em 28 de maio de 2025).
* PostgreSQL Documentation. Disponível em: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/) (Acesso em 28 de maio de 2025).
* Microsoft SQL Server Documentation. Disponível em: [https://docs.microsoft.com/en-us/sql/sql-server/sql-server-documentation](https://docs.microsoft.com/en-us/sql/sql-server/sql-server-documentation) (Acesso em 28 de maio de 2025).
---

## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 29/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 |
