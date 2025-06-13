-- DANGER: Este script irá inserir dados nas tabelas.
-- Certifique-se de que as tabelas foram criadas com sucesso usando o script CREATE TABLE completo.

-- ===================================================================================================
-- 3. INSERIR DADOS (INSERT INTO)
--    Insere os dados nas tabelas, seguindo a ordem das dependências para chaves estrangeiras.
-- ===================================================================================================

-- =========== TipoItem ===========
INSERT INTO tipo_item VALUES
(1, 'Consumível'),
(2, 'Não-Consumível'),
(3, 'Acessório'),
(4, 'Arma'),
(5, 'Fruta');

-- =========== Efeito ===========
INSERT INTO efeito VALUES
(1, 'Restaura 2 PE', 'Recupera energia'),
(2, 'Restaura 2 PV', 'Recupera vida'),
(3, 'Restaura 1 PV e 1 PE', 'Recupera vida e energia'),
(4, 'Aumenta o ataque em 2', 'Aumenta dano'),
(5, 'Aumenta o ataque em 3', 'Aumenta dano'),
(6, 'Cura', 'Remove todos efeitos negativos'),
(7, 'Revive', 'Ressuscita personagem'),
(8, 'Aumenta sorte em 2', 'Mais crítico'),
(9, 'Aumenta sorte em 3', 'Mais crítico'),
(10, 'Reduz ataque em 2', 'Enfraquece inimigo'),
(11, 'Restaura 4 PV', 'Cura média'),
(12, 'Restaura 3 PE', 'Energia média'),
(13, 'Restaura 7 PV', 'Cura alta'),
(14, 'Aumenta o ataque em 5', 'Dano alto'),
(15, 'Aumenta vida máxima em 7', 'Mais vida'),
(16, 'Aumenta energia máxima em 5', 'Mais energia'),
(17, 'Restaura 6 PE', 'Muita energia'),
(18, 'Aumenta ataque em 10', 'Ataque extremo'),
(19, 'Restaura -6 PE', 'Drena energia'),
(20, 'Restaura -6 PV', 'Drena vida'),
(21, 'Aumenta ataque em 8', 'Força superior'),
(22, 'Aumenta vida máxima em 10', 'Muita vida'),
(23, 'Aumenta energia máxima em 7', 'Muita energia'),
(24, 'Aumenta sorte em 4', 'Grande crítico'),
(25, 'Aumenta ataque em 4', 'Dano elevado'),
(26, 'Restaura 5 PE', 'Energia máxima');

-- =========== Habilidade ===========
INSERT INTO habilidade VALUES
(1, 'Gomu Gomu no Pistol', 15, 5),
(2, 'Haki do Armamento', 0, 10),
(3, 'Haki da Observação', 0, 8),
(4, 'Haki do Rei', 25, 20),
(5, 'Eco Sonoro', 10, 0),
(6, 'Santoryu: Tatsumaki', 30, 12),
(7, 'Chute do Diabo', 18, 6),
(8, 'Cura Expressa', -15, 10),
(16, 'Fruta do Eco', 0, 0),
(17, 'Fruta da Borracha', 10, 0),
(20, 'Fruta da Areia', 15, 10),
(21, 'Fruta da Fênix', 0, 0),
(24, 'Haki Supremo', 40, 30);

-- =========== Consumivel ===========
INSERT INTO consumivel VALUES
(101, 'Fruta do Mar Azul', 'Consumível', 1, 'Comum', NULL, 5, TRUE),
(102, 'Fruta do Mar Vermelha', 'Consumível', 1, 'Comum', NULL, 5, TRUE),
(103, 'Folha de Hortelã', 'Consumível', 1, 'Comum', NULL, 5, TRUE),
(104, 'Maçã Lustrosa', 'Consumível', 1, 'Comum', NULL, 7, TRUE),
(105, 'Repolho Redondo', 'Consumível', 1, 'Comum', NULL, 5, TRUE),
(106, 'Alga Fresca', 'Consumível', 1, 'Comum', NULL, 6, TRUE),
(107, 'Noz Crocante', 'Consumível', 1, 'Comum', NULL, 2, TRUE),
(108, 'Ervas Aromáticas', 'Consumível', 1, 'Comum', NULL, 3, TRUE),
(109, 'Neve Mágica', 'Consumível', 1, 'Raro', NULL, 12, TRUE),
(110, 'Fruta Cítrica do Oeste', 'Consumível', 1, 'Comum', NULL, 4, TRUE),
(111, 'Côco do Oásis', 'Consumível', 1, 'Comum', NULL, 7, TRUE),
(112, 'Areia Mineral', 'Consumível', 1, 'Comum', NULL, 10, TRUE),
(113, 'Cogumelo Risonho', 'Consumível', 1, 'Comum', NULL, 9, TRUE),
(114, 'Fruta Fluorescente', 'Consumível', 1, 'Raro', NULL, 7, TRUE),
(115, 'Sombra Engarrafada', 'Consumível', 1, 'Épico', NULL, 17, TRUE),
(117, 'Peixe Temperado', 'Consumível', 1, 'Comum', NULL, 5, TRUE),
(128, 'Massa Doce', 'Consumível', 1, 'Comum', NULL, 3, TRUE),
(140, 'Sushi Enrolado', 'Consumível', 1, 'Raro', NULL, 20, TRUE),
(141, 'Chá de Algas', 'Consumível', 1, 'Comum', NULL, 10, TRUE),
(142, 'Pastel de Fruta do Diabo', 'Consumível', 1, 'Épico', NULL, 50, TRUE);

-- =========== NaoConsumivel ===========
INSERT INTO nao_consumivel VALUES
(201, 'Carne de Ave Brava', 'Não-Consumível', 1, 'Comum', NULL, 7),
(202, 'Presa de Lobo', 'Não-Consumível', 1, 'Comum', NULL, 15),
(203, 'Doce Amassado', 'Não-Consumível', 1, 'Comum', NULL, 2),
(204, 'Medalha de Marinheiro', 'Não-Consumível', 1, 'Raro', NULL, 20),
(205, 'Pedaço de Tecido Rasgado', 'Não-Consumível', 1, 'Comum', NULL, 8),
(206, 'Lamento Gelado', 'Não-Consumível', 1, 'Raro', NULL, 12),
(207, 'Faixa de Pirata Estorricado', 'Não-Consumível', 1, 'Comum', NULL, 10),
(208, 'Fragmento de Miragem', 'Não-Consumível', 1, 'Raro', NULL, 12),
(209, 'Asa de Morcego Noturno', 'Não-Consumível', 1, 'Comum', NULL, 9),
(210, 'Presa Venenosa', 'Não-Consumível', 1, 'Raro', NULL, 7),
(301, 'Base Botas Areia', 'Não-Consumível', 1, 'Raro', NULL, NULL),
(302, 'Base Coração Coral', 'Não-Consumível', 1, 'Épico', NULL, NULL),
(303, 'Base Ampola Brisa', 'Não-Consumível', 1, 'Raro', NULL, NULL),
(304, 'Base Bracelete Estrela', 'Não-Consumível', 1, 'Épico', NULL, NULL),
(401, 'Base Espadinha', 'Não-Consumível', 1, 'Comum', NULL, NULL),
(402, 'Base Corte Areia', 'Não-Consumível', 1, 'Comum', NULL, NULL),
(403, 'Base Gume Coral', 'Não-Consumível', 1, 'Raro', NULL, NULL),
(404, 'Base Espada Fantasma', 'Não-Consumível', 1, 'Raro', NULL, NULL),
(501, 'Base Fruta Eco', 'Não-Consumível', 1, 'Épico', NULL, NULL),
(502, 'Base Fruta Borracha', 'Não-Consumível', 1, 'Lendária', NULL, NULL),
(503, 'Base Fruta Areia', 'Não-Consumível', 1, 'Rara', NULL, NULL);

-- =========== Acessorio ===========
INSERT INTO acessorio VALUES
(301, 'Botas de Areia Firme', 'Acessório', 1, '★★', 35, NULL),
(302, 'Coração de Coral', 'Acessório', 1, '★★★', 60, NULL),
(303, 'Ampola da Brisa do Mar', 'Acessório', 1, '★★', 40, NULL),
(304, 'Bracelete Estrela-do-Mar', 'Acessório', 1, '★★★', 65, NULL);

-- =========== Arma ===========
INSERT INTO arma VALUES
(401, 'Espadinha do Marinheiro', 'Arma', 1, '★', 50, NULL, 5),
(402, 'Corte de Areia', 'Arma', 1, '★', 55, NULL, 2),
(403, 'Gume de Coral', 'Arma', 1, '★★', 80, NULL, 4),
(404, 'Espada Fantasma', 'Arma', 1, '★★', 90, NULL, 24);

-- =========== Fruta ===========
INSERT INTO fruta VALUES
(501, 'Fruta do Eco', 'Fruta', 1, 'Épico', NULL, NULL, 16),
(502, 'Fruta da Borracha', 'Fruta', 1, 'Lendária', NULL, NULL, 17),
(503, 'Fruta da Areia', 'Fruta', 1, 'Rara', NULL, NULL, 20);

-- =========== EfeitoConsumivel ===========
INSERT INTO efeito_consumivel VALUES
(1, 101), (2, 102), (3, 103), (4, 110), (5, 114), (6, 109);

-- =========== EfeitoAcessorio ===========
INSERT INTO efeito_acessorio VALUES
(15, 301), (22, 302), (16, 303), (23, 304);

-- =========== TipoPersonagem ===========
INSERT INTO tipo_personagem VALUES
(1, 'Pirata'),
(2, 'Marinheiro'),
(3, 'Revolucionário'),
(4, 'Caçador de Recompensas'),
(5, 'Cidadão'),
(6, 'Médico'),
(7, 'Inventor'),
(8, 'Espadachim'),
(9, 'Atirador'),
(10, 'Cozinheiro'),
(11, 'Navegador'),
(12, 'Músico');

-- =========== Mapa ===========
INSERT INTO mapa VALUES
(1, 5, 1),
(2, 3, 1),
(3, 2, 1),
(4, 2, 1),
(5, 1, 1),
(6, 1, 2);

-- =========== Jogador ===========
INSERT INTO jogador VALUES
(1, 1, 16, 1, 'Protagonista', 10, 20, 1, 5, 20, 2, 0, 0, 0);

-- =========== Receita ===========
INSERT INTO receita VALUES
(1, 140, 1),
(2, 141, 1),
(3, 142, 1);

-- =========== IngredienteConsumivel ===========
INSERT INTO ingrediente_consumivel VALUES
(1, 117), (1, 106),
(2, 106),
(3, 102), (3, 128);

-- =========== Chefe ===========
INSERT INTO chefe VALUES
(1, 4, 1, 'Fera dos Campos', 12, 50, 5, 100, 10, 10),
(2, 24, 6, 'Vice-Almirante Caelum Drayke', 25, 100, 15, 1000, 50, 50);

-- =========== Lacaio ===========
INSERT INTO lacaio VALUES
(1, 7, 1, 'Animal Selvagem', 3, 10, 1, 5, 1, 2),
(2, 8, 2, 'Brutamontes', 7, 30, 4, 40, 0, 0);

-- =========== Instancia_Lacaio ===========
INSERT INTO instancia_lacaio VALUES
(1, 1, 10),
(2, 2, 30);

-- =========== Aliado ===========
INSERT INTO aliado VALUES
(1, 3, 'Aliado do Deserto', 15, 1, 15, 3, 0, 0);

-- =========== Habitante ===========
INSERT INTO habitante VALUES
(1, 1, 'Aldeão Gentil', 'Aldeão', NULL, 0, 0),
(2, 4, 'Médica do Gelo', 'Médica', 'Curandeira', 5, 5),
(3, 2, 'Sanji', 'Cozinheiro', 'Cozinha', 2, 2);

-- =========== HabilidadeAliado ===========
INSERT INTO habilidade_aliado VALUES
(1, 2), (1, 20);

-- =========== Campo_de_batalha ===========
INSERT INTO campo_batalha VALUES
(1, 'Gramado', 3, 'Grande'),
(2, 'Floresta Densa', 8, 'Média');

-- =========== Vila ===========
INSERT INTO vila VALUES
(2, 4, 'Pequena vila rural');

-- =========== Porto ===========
INSERT INTO porto VALUES
(3, 2, 10, FALSE);

-- =========== Missao ===========
INSERT INTO missao VALUES
(1, 'Herói dos Campos', 'Ajudar moradores da vila e derrotar a fera dos campos.', 1, 1, 1, 'campo_batalha', 1),
(2, 'Rebelião Urbana', 'Ajudar rebeldes e buscar pistas da irmã.', 2, 1, 1, 'vila', 2);

-- =========== Batalha ===========
INSERT INTO batalha VALUES (1, 1, NULL, 1, NULL, 100);
INSERT INTO batalha VALUES (2, 1, NULL, NULL, 1, 5);

-- =========== Batalha_Instancia_Lacaio ===========
INSERT INTO batalha_instancia_lacaio VALUES (1, 1);

-- =========== Negociacao ===========
INSERT INTO negociacao VALUES
(1, 1, 1, 1, 5, 25.00, 'Compra'),
(2, 2, 1, 2, 2, 14.00, 'Venda');

-- =========== Ilha ===========
INSERT INTO ilha VALUES
(1, 1, 'Campo', 'Média', 'Ilha do Início', 4),
(2, 2, 'Floresta', 'Pequena', 'Ilha do Leste', 2);

-- =========== Mar ===========
INSERT INTO mar VALUES
(1, 'Rei dos Mares', 'Tempestade');

-- =========== MapaMar ===========
INSERT INTO mapa_mar VALUES
(1, 1);

-- =========== Corredor_maritimo ===========
INSERT INTO corredor_maritimo VALUES
(1, 1, 2);

-- =========== Controlador_mar ===========
INSERT INTO controlador_mar VALUES
(1, 1);

-- =========== Barco (NOVO FORMATO) ===========
INSERT INTO barco VALUES
(1, 'Pequeno', 'Canoa Simples', NULL, 3),
(2, 'Médio', 'Navio Rebeldes', 'Melhoria: Vela', NULL);

-- =========== BarcoPorto ===========
INSERT INTO barco_porto VALUES
(1, 3);

-- =========== Controlador_barco ===========
INSERT INTO controlador_barco VALUES
(1, 1);

-- =========== Marco ===========
INSERT INTO marco VALUES
(1, 'Rei dos Mares', 'Tempestade');

-- =========== Inventario ===========
INSERT INTO Inventario VALUES
(1, 1, 'Jogador Principal');

-- =========== ItemInventario ===========
INSERT INTO ItemInventario VALUES
(1, 1),
(1, 3),
(1, 4);

-- =========== ItemMissao ===========
INSERT INTO ItemMissao VALUES
(1, 1),
(2, 2);