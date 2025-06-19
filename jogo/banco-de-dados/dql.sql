SELECT identificador_item, tipo
FROM tipo_item;

SELECT COUNT(*) AS total_de_tipos
FROM tipo_item;

SELECT nome, valor
FROM efeito;

SELECT nome, valor
FROM efeito
WHERE nome = 'Restaura PV'
ORDER BY valor DESC
LIMIT 5;

SELECT nome, raridade, preco_de_venda, descricao
FROM consumivel
WHERE e_fabricavel = TRUE;

SELECT nome, preco_de_venda, raridade
FROM consumivel
ORDER BY preco_de_venda DESC
LIMIT 10;

SELECT nome, tipo, preco_de_venda, descricao
FROM nao_consumivel
WHERE raridade = '★★';

SELECT nome, (preco_de_venda - preco_de_compra) AS margem_de_lucro
FROM nao_consumivel
WHERE preco_de_compra > 0
ORDER BY margem_de_lucro DESC;

SELECT nome, dano
FROM habilidade
WHERE custo = 0;

SELECT nome, dano, custo, (dano::decimal / custo) AS eficiencia
FROM habilidade
WHERE custo > 0
ORDER BY eficiencia DESC;

SELECT 'Consumível' AS tipo_ingrediente, ing_c.nome AS nome_ingrediente
FROM receita r
JOIN ingrediente_consumivel ic ON r.identificador_receita = ic.identificador_receita
JOIN consumivel ing_c ON ic.identificador_consumivel = ing_c.identificador_consumivel
WHERE r.identificador_receita = 3

UNION ALL

SELECT 'Não-Consumível' AS tipo_ingrediente, ing_nc.nome AS nome_ingrediente
FROM receita r
JOIN ingrediente_nao_consumivel inc ON r.identificador_receita = inc.identificador_receita
JOIN nao_consumivel ing_nc ON inc.identificador_nao_consumivel = ing_nc.identificador_nao_consumivel
WHERE r.identificador_receita = 3;

SELECT
    r.identificador_receita,
    c.nome AS item_produzido
FROM receita r
JOIN consumivel c ON r.consumivel_produzido = c.identificador_consumivel
JOIN ingrediente_nao_consumivel inc ON r.identificador_receita = inc.identificador_receita
WHERE inc.identificador_nao_consumivel = 8;

SELECT sala_id, tipo_terreno, tamanho 
FROM campo_batalha 
WHERE tipo_terreno = 'Floresta';

SELECT i.id AS id_da_ilha
FROM ilha i
JOIN mapa m ON i.id = m.id_ilha
WHERE m.id_mapa = 1;

SELECT j.nome AS nome_jogador, m.id_mapa, m.id_ilha
FROM jogador j
JOIN mapa m ON j.id_mapa_pk = m.id_mapa_pk
WHERE j.id_jogador = 1;

SELECT a.nome AS nome_aliado, h.nome AS nome_habilidade, h.dano, h.custo
FROM habilidade_aliado ha
JOIN aliado a ON ha.id_aliado = a.id_aliado
JOIN habilidade h ON ha.id_habilidade = h.id_habilidade
WHERE a.nome = 'Shuan';

SELECT nome, 'Chefe' as tipo FROM chefe WHERE id_mapa_pk = 1
UNION ALL
SELECT nome, 'Lacaio' as tipo FROM lacaio WHERE id_mapa_pk = 1
UNION ALL
SELECT nome, 'Aliado' as tipo FROM aliado WHERE id_mapa_pk = 1
UNION ALL
SELECT nome, 'Habitante' as tipo FROM habitante WHERE id_mapa_pk = 1;

SELECT nome, vida, nivel
FROM chefe
ORDER BY vida DESC
LIMIT 1;

SELECT 
    b.identificador_batalha, 
    j.nome AS nome_jogador, 
    c.nome AS nome_chefe
FROM batalha b
JOIN jogador j ON b.identificador_jogador = j.id_jogador
JOIN chefe c ON b.identificador_chefe = c.id_chefe;

SELECT l.nome AS nome_lacaio
FROM batalha_instancia_lacaio bil
JOIN instancia_lacaio il ON bil.identificador_instancia_lacaio = il.id_instancia_lacaio
JOIN lacaio l ON il.identificador_lacaio = l.id_lacaio
WHERE bil.identificador_batalha = 1;

SELECT m.nome, m.descricao
FROM missao m
WHERE m.id_recrutador = 1;

SELECT m.nome AS nome_missao, ti.tipo AS tipo_item_necessario
FROM missao m
JOIN ItemMissao im ON m.missao_id = im.missao_id
JOIN tipo_item ti ON im.identificador_item = ti.identificador_item
WHERE ti.tipo = 'Fruta';

SELECT 
    n.identificador_negociacao,
    n.tipo,
    ti.tipo AS tipo_de_item,
    n.quantidade,
    n.preco_final,
    v.nome AS nome_vendedor
FROM negociacao n
JOIN habitante v ON n.identificador_vendedor = v.identificador_habitante
JOIN tipo_item ti ON n.identificador_item = ti.identificador_item
WHERE n.identificador_jogador = 1;

SELECT
    inv.id_inventario,
    j.nome AS dono_do_inventario,
    ti.tipo AS tipo_de_item_no_inventario
FROM ItemInventario ii
JOIN Inventario inv ON ii.id_inventario = inv.id_inventario
JOIN jogador j ON inv.id_jogador = j.id_jogador
JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
WHERE j.id_jogador = 1;

SELECT 
    ilha_a.id AS id_origem, 
    ilha_b.id AS id_destino
FROM corredor_maritimo cm
JOIN ilha ilha_a ON cm.ilha_a = ilha_a.id
JOIN ilha ilha_b ON cm.ilha_b = ilha_b.id
WHERE cm.ilha_a = 1;

SELECT 
    cm.ilha_a, 
    cm.ilha_b, 
    m.monstro, 
    m.obstaculo
FROM controlador_mar ctm
JOIN mar m ON ctm.mar_id = m.mar_id
JOIN corredor_maritimo cm ON ctm.maritimo_id = cm.maritimo_id;

SELECT b.nome, b.tipo, b.melhoria
FROM barco_porto bp
JOIN barco b ON bp.barco_id = b.id
WHERE bp.sala_id = 16;