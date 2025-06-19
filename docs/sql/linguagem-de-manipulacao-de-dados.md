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

INSERT INTO habilidade (nome, dano, custo) VALUES
('Poder da Fruta do Eco', 5, 1),
('Mordida Feroz', 15, 0),
('Golpe de Espada', 10, 2),
('Tiro de Pistola', 8, 1),
('Avalanche', 12, 3),
('Transformacao', 20, 4);

INSERT INTO tipo_personagem (tipo) VALUES
('Jogador'),
('Chefe'),
('Lacaio'),
('Aliado'),
('Habitante');

INSERT INTO tipo_item (tipo) VALUES
('Fruta'),
('Arma'),
('Consumivel'),
('NaoConsumivel'),
('Acessorio');

INSERT INTO efeito (identificador_efeito, nome, valor) VALUES
(1, 'Restaura PE', 2), (2, 'Restaura PV', 2), (3, 'Restaura PV', 1), (4, 'Restaura PE', 1), (5, 'Restaura PV', 1),
(6, 'Restaura PE', 2), (7, 'Restaura PV', 1), (8, 'Aumenta Ataque', 2), (9, 'Restaura PV', 1), (10, 'Restaura PE', 2),
(11, 'Restaura PV', 3), (12, 'Restaura PE', 3), (13, 'Aumenta Ataque', 3), (14, 'Restaura PV', -1), (15, 'Aumenta Ataque', 2),
(16, 'Restaura PV', 2), (17, 'Restaura PE', 2), (18, 'Restaura PV', 4), (19, 'Restaura PE', 1), (20, 'Aumenta Ataque', 2),
(21, 'Restaura PE', 3), (22, 'Restaura PV', 2), (23, 'Aumenta Ataque', 3), (24, 'Restaura PV', 2), (25, 'Restaura PE', 3),
(26, 'Restaura PV', 1), (27, 'Restaura PV', -2), (28, 'Aumenta Ataque', 3), (29, 'Restaura PV', 2), (30, 'Restaura PE', 3),
(31, 'Restaura PE', 5), (32, 'Restaura PV', 4), (33, 'Restaura PE', 2), (34, 'Restaura PV', 5), (35, 'Restaura PE', 5),
(36, 'Restaura PV', 3), (37, 'Aumenta Ataque', 3), (38, 'Restaura PV', 7), (39, 'Restaura PE', 1), (40, 'Restaura PV', 3),
(41, 'Reduz Ataque', -2), (42, 'Restaura PV', 5), (43, 'Restaura PE', 3), (44, 'Aumenta Ataque', 5), (45, 'Aumenta Sorte', 2),
(46, 'Aumenta Sorte', 1), (47, 'Aumenta Sorte', 4), (48, 'Aumenta Sorte', 1), (49, 'Aumenta Sorte', 3), (50, 'Aumenta Sorte', 2),
(51, 'Restaura PE', 6), (52, 'Restaura PV', 6), (53, 'Restaura PV', 4), (54, 'Aumenta Ataque', 4), (55, 'Restaura PV', 2),
(56, 'Aumenta Ataque', 4), (57, 'Restaura PE', 4), (58, 'Restaura PV', 1), (59, 'Restaura PE', 5), (60, 'Restaura PV', 1),
(61, 'Restaura PE', 5), (62, 'Restaura PV', 3), (63, 'Restaura PE', 1), (64, 'Aumenta Ataque', 3), (65, 'Restaura PE', -1),
(66, 'Aumenta Ataque', 3), (67, 'Restaura PE', 3), (68, 'Aumenta Ataque', 1), (69, 'Aumenta Sorte', 3), (70, 'Aumenta Sorte', 1),
(71, 'Restaura PV', 2), (72, 'Restaura PV', 1);

INSERT INTO nao_consumivel (identificador_nao_consumivel, tipo, nome, descricao, quantidade, raridade, local_encontrado, preco_de_compra, preco_de_venda) VALUES
(8, 'ncn', 'Presa de Lobo', 'Uma presa afiada de um lobo selvagem, usada em artesanato.', 1, '★★', 'Campos', 0, 15),
(12, 'ncn', 'Farinha Misteriosa', 'Um pó fino e branco de origem desconhecida.', 1, '★', 'Cidade', 10, 5),
(13, 'ncn', 'ButterCream de Fuligem', 'Uma pasta escura e fuliginosa, estranhamente cremosa.', 1, '★★', 'Cidade', 20, 8),
(16, 'ncn', 'Medalha de Marinheiro', 'Uma medalha de bronze um pouco gasta, símbolo de bravura.', 1, '★★', 'Fortaleza da Marinha', 0, 20),
(20, 'ncn', 'Pérola Cantante', 'Uma pérola que emite uma melodia suave quando segurada.', 1, '★★', 'Ilha Assombrada', 30, 17),
(23, 'ncn', 'Pedaço de Tecido Rasgado', 'Fragmento de uma bandeira ou vela, marcado pelo tempo.', 1, '★', 'Campos', 0, 8),
(31, 'ncn', 'Faixa de Pirata Estorricado', 'A faixa de um pirata que sobreviveu a uma grande explosão.', 1, '★', 'Deserto', 0, 10),
(35, 'ncn', 'Sombra Engarrafada', 'Um frasco contendo uma sombra que se move lentamente.', 1, '★★', 'Ilha Assombrada', 0, 17),
(36, 'ncn', 'Açúcar Estranho', 'Cristais de açúcar que mudam de cor lentamente.', 1, '★', 'Ilha Assombrada', 5, 2),
(38, 'ncn', 'Essência de Névoa Doce', 'Um líquido que cheira a chuva e doces.', 1, '★★', 'Ilha Assombrada', 10, 4),
(42, 'ncn', 'Peixe Saltitante', 'Um peixe que continua a saltitar mesmo fora dágua.', 1, '★', 'Campos', 0, 11),
(48, 'ncn', 'Chapéu de Marinheiro', 'Um quepe de marinheiro, surpreendentemente limpo.', 1, '★★', 'Fortaleza da Marinha', 0, 15);

INSERT INTO consumivel (identificador_consumivel, tipo, nome, descricao, quantidade, raridade, local_encontrado, preco_de_compra, preco_de_venda, e_fabricavel) VALUES
(1, 'con', 'Fruta do Mar Azul', 'Uma fruta de cor vibrante com um sabor salgado do mar.', 1, '★', 'Campos', 0, 5, false),
(2, 'con', 'Fruta do Mar Vermelha', 'Uma fruta suculenta e vermelha, comum em planícies.', 1, '★', 'Campos', 0, 5, false),
(3, 'con', 'Folha de Hortelã', 'Uma folha refrescante que revigora o espírito.', 1, '★', 'Campos', 0, 5, false),
(4, 'con', 'Abóbora Redonduda', 'Uma abóbora nutritiva, base de muitas receitas.', 1, '★', 'Campos', 15, 6, false),
(5, 'con', 'Arroz do Planalto', 'Grãos de arroz cultivados nas terras altas e férteis.', 1, '★', 'Campos', 10, 5, false),
(6, 'con', 'Ovo dos Campos', 'Um ovo fresco, pego de ninhos nos campos abertos.', 1, '★', 'Campos', 10, 5, false),
(7, 'con', 'Carne de Ave Brava', 'Carne de uma ave selvagem, um pouco dura mas saborosa.', 1, '★', 'Campos', 0, 7, false),
(9, 'con', 'Maçã Lustrosa', 'Uma maçã tão polida que parece uma joia.', 1, '★', 'Campos', 0, 7, false),
(10, 'con', 'Repolho Redondo', 'Um repolho comum, ingrediente básico para sopas.', 1, '★', 'Campos', 0, 5, false),
(11, 'con', 'Alga Fresca', 'Algas colhidas na costa, com cheiro de mar.', 1, '★', 'Campos', 0, 6, false),
(14, 'con', 'Chá Enlatado', 'Uma bebida popular na cidade, para uma pausa rápida.', 1, '★', 'Cidade', 15, 6, false),
(15, 'con', 'Doce Amassado', 'Um doce simples que sobreviveu a uma longa viagem.', 1, '★', 'Cidade', 0, 2, false),
(17, 'con', 'Noz Crocante', 'Uma noz dura que exige esforço para abrir.', 1, '★', 'Campos', 0, 2, false),
(18, 'con', 'Ervas Aromáticas', 'Um punhado de ervas que perfumam qualquer prato.', 1, '★', 'Campos', 0, 3, false),
(19, 'con', 'Neve Mágica', 'Um punhado de neve que nunca derrete e brilha suavemente.', 1, '★★', 'Neve', 0, 12, false),
(21, 'con', 'Leite de Cabra Alpina', 'Leite cremoso de cabras que vivem nas montanhas de neve.', 1, '★', 'Neve', 10, 6, false),
(22, 'con', 'Chocolate Amargo', 'Um chocolate intenso, preferido pelos habitantes da neve.', 1, '★', 'Neve', 15, 8, false),
(24, 'con', 'Lamento Gelado', 'Um cristal de gelo que emite um som melancólico.', 1, '★★', 'Neve', 0, 12, false),
(25, 'con', 'Fruta Cítrica do Oeste', 'Uma fruta azeda que cresce nos limites do deserto.', 1, '★', 'Deserto', 0, 4, false),
(26, 'con', 'Côco do Oásis', 'Um côco cheio de água fresca, um tesouro no deserto.', 1, '★', 'Deserto', 0, 7, false),
(27, 'con', 'Areia Mineral', 'Grãos de areia com propriedades nutritivas incomuns.', 1, '★★', 'Deserto', 0, 10, false),
(28, 'con', 'Carne do Deserto', 'Carne seca e resistente de uma criatura do deserto.', 1, '★★', 'Deserto', 20, 8, false),
(29, 'con', 'Geleia de Cacto Doce', 'Uma geleia feita da polpa de um cacto raro.', 1, '★★', 'Deserto', 11, 6, false),
(30, 'con', 'Suco Refrescante Solar', 'Um suco que parece conter a luz do sol.', 1, '★', 'Deserto', 7, 4, false),
(32, 'con', 'Fragmento de Miragem', 'Um pedaço de luz solidificada que distorce o ar ao redor.', 1, '★★', 'Deserto', 0, 12, false),
(33, 'con', 'Cogumelo Risonho', 'Um cogumelo que parece sorrir para quem o encontra.', 1, '★', 'Ilha Assombrada', 0, 9, false),
(34, 'con', 'Fruta Fluorescente', 'Uma fruta que brilha no escuro com uma luz azulada.', 1, '★', 'Ilha Assombrada', 0, 7, false),
(37, 'con', 'Doce Fantasmal', 'Um doce translúcido com um sabor etéreo.', 1, '★', 'Ilha Assombrada', 13, 5, false),
(39, 'con', 'Asa de Morcego Noturno', 'A asa de um morcego que habita as cavernas da ilha.', 1, '★', 'Ilha Assombrada', 0, 9, false),
(40, 'con', 'Presa Venenosa', 'Uma presa oca que ainda contém vestígios de veneno.', 1, '★', 'Ilha Assombrada', 0, 7, false),
(41, 'con', 'Amendoim Crocante', 'Um lanche simples, mas satisfatório.', 1, '★', 'Cidade', 0, 3, false),
(43, 'con', 'Pepino de Salmoura', 'Um pepino conservado em salmoura, com sabor forte.', 1, '★', 'Cidade', 0, 5, false),
(44, 'con', 'Ração de Soldado', 'Comida compacta e durável, parte do suprimento da Marinha.', 1, '★★', 'Fortaleza da Marinha', 10, 4, false),
(45, 'con', 'Café Turbinado', 'Um café forte que mantém os marinheiros acordados por dias.', 1, '★', 'Fortaleza da Marinha', 8, 3, false),
(46, 'con', 'Carne de Rei dos Mares', 'Um pedaço raro e delicioso da carne de uma besta marinha.', 1, '★★★', 'Fortaleza da Marinha', 40, 19, false),
(47, 'con', 'Rosquinha Mordida', 'Uma rosquinha com uma única e suspeita marca de mordida.', 1, '★', 'Cidade', 0, 3, false),
(101, 'con', 'Sushi Enrolado', 'Um prato delicado feito com peixe e alga.', 1, '★★', 'Cidade', 0, 15, true),
(102, 'con', 'Chá de Algas', 'Um chá quente com um sabor distinto do mar.', 1, '★', 'Campos', 0, 10, true),
(103, 'con', 'Pastel de Fruta do Diabo', 'Um pastel perigoso com um recheio imprevisível.', 1, '★★', 'Ilha Assombrada', 0, 18, true),
(104, 'con', 'Caldo da Vovó Yuba', 'Um caldo reconfortante que cura corpo e alma.', 1, '★★', 'Deserto', 0, 22, true),
(105, 'con', 'Tônico de Areia', 'Uma bebida revigorante feita com minerais do deserto.', 1, '★★', 'Deserto', 0, 16, true),
(106, 'con', 'Chá Gelado de Neve', 'Um chá feito com neve mágica, extremamente refrescante.', 1, '★★', 'Neve', 0, 15, true),
(107, 'con', 'Receita Secreta do Capitão', 'Uma refeição lendária com poder imenso.', 1, '★★★', 'Fortaleza da Marinha', 0, 27, true),
(108, 'con', 'Carne Grelhada', 'Um pedaço de carne perfeitamente grelhado.', 1, '★★', 'Campos', 0, 18, true),
(109, 'con', 'Pérola Caramelizada', 'Uma pérola comestível coberta por uma casca de açúcar.', 1, '★★', 'Cidade', 0, 13, true),
(110, 'con', 'Pérola da Lua de Inverno', 'Uma iguaria rara feita apenas durante o inverno.', 1, '★★★', 'Neve', 0, 24, true),
(111, 'con', 'Pérola do Sol Escaldante', 'Uma iguaria rara encontrada apenas no auge do verão.', 1, '★★★', 'Deserto', 0, 24, true),
(112, 'con', 'Gelado de Algas', 'Uma sobremesa fria com um toque salgado.', 1, '★', 'Campos', 0, 15, true),
(113, 'con', 'Omurice de Arroz', 'Arroz frito envolto em uma omelete macia.', 1, '★★', 'Cidade', 0, 15, true),
(114, 'con', 'Bolo do Campo', 'Um bolo simples feito com ingredientes frescos dos campos.', 1, '★★', 'Campos', 0, 14, true),
(115, 'con', 'Bombom Nebuloso', 'Um bombom que libera uma pequena névoa ao ser mordido.', 1, '★★', 'Ilha Assombrada', 0, 12, true),
(116, 'con', 'Arroz dos Sete Mares', 'Um prato de arroz com ingredientes de várias partes do mundo.', 1, '★', 'Cidade', 0, 9, true),
(117, 'con', 'Doce da Ilha', 'Um doce tropical feito com frutas exóticas.', 1, '★★', 'Campos', 0, 12, true),
(118, 'con', 'Omelete dos 4 Ventos', 'Uma omelete fofa com ervas de todas as direções.', 1, '★★', 'Campos', 0, 13, true),
(119, 'con', 'Frango Assado Estaladiço', 'Frango assado com uma pele perfeitamente crocante.', 1, '★', 'Cidade', 0, 10, true),
(120, 'con', 'Sopa da Guarda Noturna', 'Uma sopa simples para aquecer as noites frias.', 1, '★', 'Neve', 0, 6, true),
(121, 'con', 'Doce de Duna Dourada', 'Um doce feito com açúcar caramelizado e areia mineral.', 1, '★★', 'Deserto', 0, 16, true),
(122, 'con', 'Bife do Abismo', 'Carne de uma criatura das profundezas, de sabor intenso.', 1, '★★★', 'Fortaleza da Marinha', 0, 35, true),
(123, 'con', 'Sashimi do Fim do Mundo', 'Fatias de um peixe lendário que vive nos confins do oceano.', 1, '★★★', 'Fortaleza da Marinha', 0, 35, true),
(124, 'con', 'Torta do Marujo Feliz', 'Uma torta simples que eleva o moral de qualquer um.', 1, '★', 'Cidade', 0, 10, true),
(125, 'con', 'Doce Assombrado', 'Um doce que parece sussurrar segredos quando você come.', 1, '★★', 'Ilha Assombrada', 0, 12, true),
(126, 'con', 'Curry do Capitão Covarde', 'Um curry picante que te dá coragem (ou desespero).', 1, '★★', 'Fortaleza da Marinha', 0, 13, true),
(127, 'con', 'Elixir Sombrio', 'Uma poção borbulhante de origem duvidosa.', 1, '★★', 'Ilha Assombrada', 0, 18, true),
(128, 'con', 'Poção do Dente Torto', 'Uma poção que fortalece os dentes, ou os entorta.', 1, '★★', 'Ilha Assombrada', 0, 18, true),
(129, 'con', 'Cookie de Chocolate', 'Um cookie clássico, perfeito com um copo de leite.', 1, '★', 'Cidade', 0, 14, true),
(130, 'con', 'Leite Condensado Alpino', 'Leite condensado feito com o melhor leite das montanhas.', 1, '★', 'Neve', 0, 11, true),
(131, 'con', 'Doce do Silêncio Eterno', 'Um doce que, dizem, silencia até os pensamentos mais altos.', 1, '★★', 'Ilha Assombrada', 0, 17, true),
(132, 'con', 'Cacto‑Pop Geladinho', 'Um picolé refrescante feito de cacto.', 1, '★★', 'Deserto', 0, 16, true),
(133, 'con', 'Esfera da Miragem', 'Uma sobremesa gelatinosa que parece uma miragem distante.', 1, '★★', 'Deserto', 0, 17, true),
(134, 'con', 'Amendoins Torrados', 'Amendoins salgados e torrados, um lanche viciante.', 1, '★', 'Cidade', 0, 5, true),
(135, 'con', 'Pickles Pirata', 'Conserva de pepino com um toque de rum.', 1, '★', 'Cidade', 0, 10, true),
(136, 'con', 'Frankenprato', 'Uma mistura bizarra de ingredientes que surpreendentemente é comestível.', 1, '★', 'Ilha Assombrada', 0, 5, true);

INSERT INTO efeito_consumivel (identificador_consumivel, identificador_efeito) VALUES
(1, 1), (2, 2), (3, 3), (9, 4), (10, 5), (11, 6), (14, 7), (15, 8), (17, 2), (18, 9), (19, 10), (21, 11), (22, 12), (25, 13),
(26, 14), (27, 11), (28, 15), (29, 16), (30, 17), (33, 18), (34, 19), (37, 20), (41, 21), (43, 22), (44, 23), (45, 24),
(46, 25), (47, 56), (101, 26), (102, 27), (103, 28), (104, 29), (105, 30), (106, 31), (107, 32), (108, 33), (109, 34),
(110, 35), (111, 36), (112, 37), (113, 38), (114, 39), (115, 40), (116, 41), (117, 42), (118, 43), (119, 33), (120, 44),
(121, 45), (122, 46), (123, 47), (124, 39), (125, 12), (126, 31), (127, 48), (128, 49), (129, 50), (130, 51), (131, 52),
(132, 53), (133, 54), (134, 55), (135, 40), (136, 8);

INSERT INTO receita (identificador_receita, consumivel_produzido) VALUES
(1, 101), (2, 102), (3, 103), (4, 104), (5, 104), (6, 105), (7, 106), (8, 107), (9, 108), (10, 109), (11, 110),
(12, 111), (13, 112), (14, 113), (15, 114), (16, 115), (17, 115), (18, 116), (19, 116), (20, 116), (21, 116),
(22, 117), (23, 118), (24, 118), (25, 119), (26, 120), (27, 120), (28, 121), (29, 122), (30, 123), (31, 124),
(32, 125), (33, 126), (34, 127), (35, 128), (36, 129), (37, 130), (38, 131), (39, 132), (40, 133), (41, 134),
(42, 135), (43, 136);

INSERT INTO ingrediente_consumivel (identificador_receita, identificador_consumivel) VALUES
(1, 11), (2, 11), (3, 2), (3, 28), (4, 28), (4, 18), (5, 28), (5, 3), (6, 27), (7, 19), (7, 3), (8, 101), (8, 104), (9, 28),
(11, 109), (11, 19), (12, 109), (12, 19), (13, 11), (13, 19), (14, 5), (14, 6), (15, 6), (17, 22), (18, 5), (18, 1), (19, 5),
(19, 2), (20, 5), (20, 25), (21, 5), (21, 34), (22, 26), (22, 25), (23, 6), (23, 3), (24, 6), (24, 18), (25, 7), (25, 18),
(26, 10), (26, 11), (27, 10), (27, 7), (28, 27), (28, 26), (29, 46), (29, 24), (30, 46), (31, 4), (32, 4), (33, 4),
(33, 28), (34, 39), (35, 40), (35, 30), (36, 17), (36, 22), (37, 21), (38, 24), (38, 19), (39, 29), (39, 25), (40, 32),
(40, 27), (41, 41), (42, 43), (42, 28);

INSERT INTO ingrediente_nao_consumivel (identificador_receita, identificador_nao_consumivel) VALUES
(1, 42), (6, 38), (10, 20), (10, 36), (15, 12), (16, 35), (16, 38), (17, 35), (30, 35), (31, 12), (32, 38), (34, 35), (37, 36);

-- =========== Inserções no Restante das Tabelas ===========
INSERT INTO campo_batalha (tipo_terreno, qtd_de_pessoas, tamanho) VALUES
('Floresta', 1, 'Pequeno'), ('Floresta', 1, 'Medio'), ('Urbano', 5, 'Pequeno'), ('Urbano', 1, 'Medio'),
('Neve', 3, 'Pequeno'), ('Costa', 10, 'Medio'), ('Deserto', 1, 'Grande'), ('Deserto', 0, 'Pequeno'),
('Deserto', 1, 'Medio'), ('Misterioso', 0, 'Medio'), ('Militar', 10, 'Grande'), ('Aquatico', 1, 'Enorme');

INSERT INTO vila (total_salas, informacoes) VALUES
(1, 'Primeira vila encontrada, amigavel.'),
(1, 'Vila fria, moradores desconfiados.'),
(1, 'Vila com medica famosa.');

INSERT INTO porto (qtd_barcos, capacidade, sendo_ilha) VALUES
(5, 100, FALSE);

INSERT INTO ilha (sala_id) VALUES
(13), (16), (14), (7), (10), (11);

INSERT INTO mapa (id_mapa, id_ilha) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6);

INSERT INTO jogador (id_personagem, id_habilidade, id_mapa_pk, nome, dano_base, coordenada_x, coordenada_y) VALUES
(1, 1, 1, 'Protagonista', 10, 0, 0);

INSERT INTO habitante (id_mapa_pk, nome, tipo, descricao, especialidade, coordenada_x, coordenada_y) VALUES
(1, 'Aldeao', 'rec', 'Aldeao que acorda o protagonista.', NULL, 10, 5),
(6, 'Medico', 'coz', 'Medica famosa da vila da neve.', NULL, 15, 10),
(5, 'Morador Secreto', 'hbt', 'Morador escondido na ilha fantasma.', NULL, 50, 50);

INSERT INTO chefe (id_habilidade, id_mapa_pk, nome, dano, vida, nivel, experiencia, coordenada_x, coordenada_y) VALUES
(2, 1, 'A Fera', 20, 150, 5, 50, 10, 10),
(3, 2, 'Comandante da Marinha', 30, 200, 10, 100, 25, 25),
(4, 2, 'Lider Rebelde', 15, 120, 8, 80, 20, 15),
(3, 4, 'Lider Pirata do Deserto', 40, 250, 15, 150, 5, 5),
(6, 6, 'Marinheiro Nobre - Final', 50, 300, 20, 200, 40, 40);

INSERT INTO lacaio (id_habilidade, id_mapa_pk, nome, dano, vida, nivel, experiencia, coordenada_x, coordenada_y) VALUES
(2, 1, 'Lobo Selvagem', 8, 50, 2, 10, 12, 12),
(4, 2, 'Soldado Marinha', 10, 60, 3, 15, 30, 30);

INSERT INTO instancia_lacaio (identificador_lacaio, vida_atual) VALUES
(1, 50),
(2, 60);

INSERT INTO aliado (id_mapa_pk, nome, descricao, vida, nivel, dano_base) VALUES
(3, 'Shuan', 'Aliado caçador do vilarejo do norte.', 120, 7, 15),
(5, 'Silvie', 'Lider dos moradores da ilha fantasma.', 150, 9, 20);

INSERT INTO habilidade_aliado (id_aliado, id_habilidade) VALUES
(1, 5);

INSERT INTO missao (nome, descricao, id_mapa_pk, id_jogador, id_recrutador, tipo_sala, sala_id) VALUES
('Animal Selvagem', 'Derrotar o animal selvagem que atacou o protagonista.', 1, 1, 1, 'campo_batalha', 1),
('A Fera da Vila', 'Enfrentar a fera das plantacoes.', 1, 1, 1, 'campo_batalha', 2),
('Vendedor Agressao', 'Salvar o vendedor de frutas.', 2, 1, 1, 'porto', 16),
('Infiltracao Prisao', 'Invadir registros da prisao.', 2, 1, 3, 'campo_batalha', 3),
('Comandante da Marinha', 'Lutar contra o comandante da Marinha.', 2, 1, 3, 'campo_batalha', 4),
('Ataque de Lobos', 'Lutar contra lobos no caminho.', 3, 1, 1, 'campo_batalha', 5),
('Defesa do Vilarejo', 'Defender vilarejo de piratas.', 3, 1, 1, 'campo_batalha', 6),
('Verme da Areia', 'Lutar contra o verme no deserto.', 4, 1, 1, 'campo_batalha', 7),
('Estrategia do Deserto', 'Diminuir piratas no deserto.', 4, 1, 1, 'campo_batalha', 8),
('Lider Pirata do Deserto', 'Derrotar lider pirata.', 4, 1, 1, 'campo_batalha', 9),
('Treinamento Secreto', 'Passar por treinamento e coletar materiais.', 5, 1, 3, 'campo_batalha', 10),
('Favores na Fortaleza', 'Realizar favores para os marinheiros.', 6, 1, 1, 'campo_batalha', 11),
('Besta Marinha', 'Derrotar besta marinha.', 6, 1, 1, 'campo_batalha', 12),
('Marinheiro Nobre - Hibrido', 'Lutar contra Marinheiro Nobre hibrido.', 6, 1, 5, 'campo_batalha', 11),
('Marinheiro Nobre - Final', 'Luta final contra Marinheiro Nobre completo.', 6, 1, 5, 'campo_batalha', 11);

INSERT INTO negociacao (identificador_item, identificador_jogador, identificador_vendedor, quantidade, preco_final, tipo) VALUES
(3, 1, 1, 5, 250.00, 'compra');

INSERT INTO Inventario (id_jogador, nome) VALUES
(1, 'Bolsa de Itens');

INSERT INTO ItemInventario (id_inventario, identificador_item) VALUES
(1, 1);

INSERT INTO ItemMissao (missao_id, identificador_item) VALUES
(1, 1);

INSERT INTO batalha (identificador_jogador, identificador_chefe) VALUES
(1, 1);

INSERT INTO batalha_instancia_lacaio (identificador_batalha, identificador_instancia_lacaio) VALUES
(1, 1);

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
 `1.1` | adicionado as consultas | [Pablo Serra](https://github.com/Pabloserrapxx) | 16/06/2025 |  |  |