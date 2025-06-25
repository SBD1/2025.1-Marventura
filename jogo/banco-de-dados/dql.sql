-- Buscar informações básicas do jogador
SELECT * FROM jogador;

-- Buscar inventário do jogador


-- Buscar informações da área atual
SELECT nome, tipo_area, chave_imagem_fundo, chave_imagem_frente, visitada
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
SELECT  il.identificador_instancia_lacaio,
        il.coordenada_x,
        il.coordenada_y,
        il.vida_atual,

        l.identificador_lacaio,
        l.nome AS nome_lacaio,
        l.descricao AS descricao_lacaio,
        l.vida AS vida_total,
        l.nivel,
        l.experiencia,

        h.nome AS nome_habilidade,
        h.dano,
        h.tipo_de_habilidade,
        h.tipo_de_ataque,

        ti.identificador_item,
        ti.tipo AS tipo_item,

        consumivel.nome AS nome_consumivel,
        nao_consumivel.nome AS nome_nao_consumivel

    FROM instancia_lacaio il
    JOIN lacaio l ON il.identificador_lacaio = l.identificador_lacaio
    LEFT JOIN habilidade h ON l.identificador_habilidade = h.identificador_habilidade

    LEFT JOIN inventario inv ON inv.identificador_personagem = l.identificador_lacaio
    LEFT JOIN item_inventario ii ON ii.identificador_inventario = inv.identificador_inventario
    LEFT JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item

    -- subtipos possíveis do item
    LEFT JOIN consumivel ON consumivel.identificador_consumivel = ti.identificador_item
    LEFT JOIN nao_consumivel ON nao_consumivel.identificador_nao_consumivel = ti.identificador_item

    WHERE il.identificador_area = = (
        SELECT identificador_area
        FROM jogador
        WHERE identificador_jogador = 'jog001'
    );
