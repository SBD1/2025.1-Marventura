-- Inserindo ilhas com base na imagem
INSERT INTO ilhas (nome, tipo, tamanho, quantidade_sala) VALUES
('Ilha do Vale Verde', 'Natural', 10, 3),           -- 1
('Ilha da Cidade Perdida', 'Urbana', 12, 4),        -- 2
('Ilha das Neves Eternas', 'Gélida', 8, 2),         -- 3
('Ilha do Deserto Árido', 'Desértica', 9, 3),       -- 4
('Ilha dos Espíritos', 'Assombrada', 11, 4),        -- 5
('Ilha do Castelo Imperial', 'Histórica', 10, 3);   -- 6

-- Exemplo de mar associando monstros/obstáculos a ilhas
INSERT INTO mar (tipo, ilha_id) VALUES
('Monstro', 5),
('Obstaculo', 4),
('Monstro', 3);

-- Inserindo portos
INSERT INTO porto (nome, ilha_id) VALUES
('Porto Verdejante', 1),
('Porto Fantasma', 5),
('Porto Imperial', 6);

-- Conexões entre ilhas com base nas linhas vermelhas da imagem
INSERT INTO corredor_maritmo (ilha_a, ilha_b, sentido) VALUES
(1, 2, 'duplo'),
(1, 4, 'duplo'),
(1, 6, 'duplo'),
(2, 3, 'duplo'),
(2, 5, 'duplo'),
(2, 6, 'duplo'),
(3, 4, 'duplo'),
(3, 5, 'duplo'),
(4, 5, 'duplo'),
(5, 6, 'duplo');
