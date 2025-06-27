SELECT receita.identificador_receita AS Receita, consumivel.nome AS Nome
FROM receita JOIN consumivel ON receita.consumivel_produzido = consumivel.identificador_consumivel


-- Buscar informações básicas do jogador
SELECT * FROM jogador;


-- Buscar inventário do jogador


-- Buscar os dados da ilha atual do jogador
SELECT * FROM ilha
	WHERE identificador_ilha = (
		SELECT identificador_ilha FROM area
			WHERE identificador_area = (
		        SELECT identificador_area
		        FROM jogador
		        WHERE identificador_jogador = 'jog001'
		    )
	);


-- Buscar informações da área atual
SELECT
    TRIM(nome) AS nome,
    TRIM(tipo_area) AS tipo_area,
    TRIM(chave_imagem_fundo) AS chave_imagem_fundo,
    TRIM(chave_imagem_frente) AS chave_imagem_frente,
    visitada
FROM area
    WHERE identificador_area = (
        SELECT identificador_area
        FROM jogador
        WHERE identificador_jogador = 'jog001'
    );


-- Buscar caminhos da área atual
SELECT tipo_terreno, x, y, largura, altura
    FROM caminho
    WHERE identificador_area = (
        SELECT identificador_area
        FROM jogador
        WHERE identificador_jogador = 'jog001'
    );


-- Buscar inimigos comuns da área atual
SELECT 
    il.identificador_instancia_lacaio,
    il.coordenada_x,
    il.coordenada_y,
    il.vida_atual,
	il.moedas_totais,

    l.identificador_lacaio,
    l.nome AS nome_lacaio,
    l.descricao AS descricao_lacaio,
    l.vida AS vida_total,
    l.nivel,
    l.experiencia,

    h.identificador_habilidade,
    h.nome AS nome_habilidade,
    h.dano,
    h.tipo_de_ataque,
    h.tipo_de_alvo,

    ti.identificador_item,
    ti.tipo AS tipo_item,

    consumivel.nome AS consumivel_saqueavel,
    nao_consumivel.nome AS nao_consumivel_saqueavel

FROM instancia_lacaio il
JOIN lacaio l ON il.identificador_lacaio = l.identificador_lacaio

-- Habilidades do lacaio (1 ou mais)
LEFT JOIN habilidade_personagem hp ON hp.identificador_personagem = l.identificador_lacaio
LEFT JOIN habilidade h ON h.identificador_habilidade = hp.identificador_habilidade

-- Inventário geral do lacaio
LEFT JOIN inventario inv ON inv.identificador_personagem = l.identificador_lacaio AND inv.tipo_inventario = 'ger'
LEFT JOIN item_inventario ii ON ii.identificador_inventario = inv.identificador_inventario
LEFT JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item

-- Subtipos possíveis do item
LEFT JOIN consumivel ON consumivel.identificador_consumivel = ti.identificador_item
LEFT JOIN nao_consumivel ON nao_consumivel.identificador_nao_consumivel = ti.identificador_item

-- Restrição pela área atual do jogador
WHERE il.identificador_area = (
    SELECT identificador_area
    FROM jogador
    WHERE identificador_jogador = 'jog001'
);


-- Buscar todas as áreas que se conectam com a área atual
SELECT a.*
FROM conexao_entre_areas ca
JOIN area a
  ON a.identificador_area = ca.identificador_area_a
     AND ca.identificador_area_b = (
        SELECT identificador_area
        FROM jogador
        WHERE identificador_jogador = 'jog001'
    )

UNION

SELECT a.*
FROM conexao_entre_areas ca
JOIN area a
  ON a.identificador_area = ca.identificador_area_b
     AND ca.identificador_area_a = (
        SELECT identificador_area
        FROM jogador
        WHERE identificador_jogador = 'jog001'
    );


-- Buscar todas as áreas interativas da área atual
SELECT
    ai.identificador_area_interativa,
    TRIM(ai.chave_imagem) AS chave_imagem,
    ai.x,
    ai.y,
    ai.largura,
    ai.altura
FROM area_interativa ai
WHERE ai.identificador_area = (
    SELECT identificador_area
    FROM jogador
    WHERE identificador_jogador = 'jog001'
);


-- Buscar todas as ilhas que se conectam com a ilha atual
SELECT i.*
FROM conexao_entre_ilhas c
JOIN ilha i ON i.identificador_ilha = 
    CASE
        WHEN c.identificador_ilha_a = 'ilh001' THEN c.identificador_ilha_b
        ELSE c.identificador_ilha_a
    END
WHERE 'ilh001' IN (c.identificador_ilha_a, c.identificador_ilha_b);
