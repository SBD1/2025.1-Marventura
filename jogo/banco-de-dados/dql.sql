SELECT identificador_habitante, identificador_mapa, IlhaID, tipo, nome, descricao, especialidade, coordenada_x, coordenada_y
FROM Habitante
WHERE identificador_habitante = 2;

SELECT identificador_habitante, nome, tipo, especialidade
FROM Habitante
WHERE especialidade = 'arm';

SELECT identificador_habitante, nome, tipo, especialidade
FROM Habitante
WHERE identificador_mapa = 1 AND IlhaID = 1;

SELECT idJogador, idHabilidade, idMapa, IlhaID, Energia, Vida, Nivel, Sorte, VidaAtual, DanoBase, ExperienciaAtual, CoordenadaX, CoordenadaY
FROM Jogador
WHERE idJogador = 1;

SELECT Vida, Nivel, DanoBase
FROM Jogador
WHERE idJogador = 1;

SELECT idChefe, idHabilidade, idMapa, IlhaID, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo
FROM Chefe
WHERE idChefe = 5;

SELECT Nome, Vida, Nivel
FROM Chefe
WHERE idChefe = 6;

SELECT idChefe, Nome, Nivel
FROM Chefe
WHERE TipoInimigo = 'Humanoide';

SELECT MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome
FROM Missão
WHERE MissaoID = 12;

SELECT MissaoID, Nome, Descricao
FROM Missão
WHERE Nome LIKE '%Fera%';

SELECT m.MissaoID, m.Nome, h.nome AS NomeRecrutador
FROM Missão m
JOIN Habitante h ON m.idRecrutador = h.identificador_habitante
WHERE h.identificador_habitante = 2;

SELECT m.Nome AS NomeMissao, m.Descricao, c.Nome AS NomeRecrutadorChefe
FROM Missão m
JOIN Chefe c ON m.idRecrutador = c.idChefe
WHERE m.idRecrutador IN (7, 9);

SELECT m.Nome AS NomeMissao, m.Descricao, cb.Nome AS NomeLocal
FROM Missão m
JOIN Campo_de_batalha cb ON m.SalaID = cb.SalaID AND m.TipoSala = cb.TipoSala
WHERE m.TipoSala = 'Campo de Batalha';

SELECT SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos
FROM Campo_de_batalha
WHERE SalaID = 201;

SELECT SalaID, Nome, Tipo, QtdInimigos
FROM Campo_de_batalha
WHERE Tipo = 'Floresta';

SELECT SalaID, TipoSala, Nome, TotalSalas, Informacoes
FROM Vila
WHERE SalaID = 101;

SELECT Nome, Informacoes
FROM Vila;

SELECT SalaID, TipoSala, Nome, TotalSalas, QtdBarcos, Capacidade, SentidoIlha
FROM Porto
WHERE SalaID = 301;

SELECT Nome, QtdBarcos, Capacidade
FROM Porto
WHERE QtdBarcos > 3;

SELECT ItemID, Nome, Descricao, Tipo
FROM Item
WHERE ItemID = 11;

SELECT Nome, Descricao
FROM Item
WHERE Tipo = 'Fruta';

SELECT im.MissaoID, ti.Tipo AS TipoItem, i.Nome AS NomeItem, i.Descricao AS DescricaoItem
FROM ItemMissão im
JOIN Item i ON im.IdentificadorItem = i.ItemID
JOIN TipoItem ti ON i.Tipo = ti.Tipo
WHERE im.MissaoID = 12;

SELECT im.MissaoID, m.Nome AS NomeMissao, m.Descricao AS DescricaoMissao
FROM ItemMissão im
JOIN Missão m ON im.MissaoID = m.MissaoID
WHERE im.IdentificadorItem = 11;


SELECT MarID, Mostro, Obstaculo
FROM Mar
WHERE MarID = 1;

SELECT MarID, Mostro
FROM Mar
WHERE Mostro LIKE '%Serpente%';


SELECT marítimoID, IlhaA, IlhaB
FROM Corredor_maritimo
WHERE marítimoID = 1;

SELECT c.marítimoID, ia.Nome AS NomeIlhaA, ib.Nome AS NomeIlhaB
FROM Corredor_maritimo c
JOIN Ilha ia ON c.IlhaA = ia.ID
JOIN Ilha ib ON c.IlhaB = ib.ID
WHERE c.marítimoID = 1;


SELECT MapaID, IlhaID, MarID
FROM MapaMar
WHERE MapaID = 1 AND IlhaID = 1;

SELECT mm.MapaID, mm.IlhaID, m.Nome AS NomeMapa, i.Nome AS NomeIlha, mar.Mostro
FROM MapaMar mm
JOIN Mapa m ON mm.MapaID = m.MapaID AND mm.IlhaID = m.IlhaID
JOIN Ilha i ON m.IlhaID = i.ID
JOIN Mar mar ON mm.MarID = mar.MarID
WHERE mm.MarID = 1;

SELECT marítimoID, MarID
FROM Controller_mar
WHERE marítimoID = 1;

SELECT cm.marítimoID, cm.MarID, cor.IlhaA, mar.Mostro
FROM Controller_mar cm
JOIN Corredor_maritimo cor ON cm.marítimoID = cor.marítimoID
JOIN Mar mar ON cm.MarID = mar.MarID
WHERE cm.marítimoID = 1;

SELECT Tipo, Melhoria, Nome, Nivel
FROM Barco
WHERE Tipo = 'Canoa';

SELECT Tipo, Nome, Nivel
FROM Barco
WHERE Nivel > 5;

SELECT TipoSala, TipoBarco, SalaID
FROM BarcoPorto
WHERE SalaID = 301;

SELECT bp.TipoSala, bp.SalaID, p.Nome AS NomePorto, b.Nome AS NomeBarco, b.Nivel AS NivelBarco
FROM BarcoPorto bp
JOIN Porto p ON bp.TipoSala = p.TipoSala AND bp.SalaID = p.SalaID
JOIN Barco b ON bp.TipoBarco = b.Tipo
WHERE bp.TipoBarco = 'Canoa';


SELECT IDBarco, marítimoID
FROM Controller_barco
WHERE IDBarco = 'Canoa';

SELECT cb.IDBarco, cb.marítimoID, b.Nome AS NomeBarco, cm.IlhaA AS CorredorIlhaA
FROM Controller_barco cb
JOIN Barco b ON cb.IDBarco = b.Tipo
JOIN Corredor_maritimo cm ON cb.marítimoID = cm.marítimoID
WHERE cb.IDBarco = 'Canoa';