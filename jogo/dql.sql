
## **Tipo de Item**

* **Ver todos os tipos de itens disponíveis.**
    ```sql
    SELECT identificador_item, tipo
    FROM tipo_item;
    ```

* **Ver o tipo de um item específico.**
    ```sql
    SELECT tipo
    FROM tipo_item
    WHERE identificador_item = 1;
    ```

---

## **Efeito**

* **Ver todos os efeitos e suas descrições.**
    ```sql
    SELECT nome, bravura
    FROM efeito;
    ```

* **Ver o nome e a descrição (bravura) de um efeito específico.**
    ```sql
    SELECT nome, bravura
    FROM efeito
    WHERE identificador_efeito = 5;
    ```

---

## **Consumível**

* **Ver todos os consumíveis que podem ser fabricados.**
    ```sql
    SELECT nome, raridade, preco_venda
    FROM consumivel
    WHERE efabricavel = TRUE;
    ```

* **Ver detalhes de um consumível específico.**
    ```sql
    SELECT nome, quantidade, raridade, preco_compra, preco_venda
    FROM consumivel
    WHERE identificador_consumivel = 101;
    ```

* **Ver os atributos de um consumível específico.**
    ```sql
    SELECT nome, tipo, raridade, quantidade, preco_compra, preco_venda, efabricavel
    FROM consumivel
    WHERE identificador_consumivel = 101;
    ```

---

## **Não-Consumível**

* **Ver todos os itens não-consumíveis de raridade 'Raro'.**
    ```sql
    SELECT nome, tipo, preco_venda
    FROM nao_consumivel
    WHERE raridade = 'Raro';
    ```

* **Ver os atributos de um não-consumível específico.**
    ```sql
    SELECT nome, tipo, raridade, quantidade, preco_compra, preco_venda
    FROM nao_consumivel
    WHERE identificador_nao_consumivel = 201;
    ```

---

## **Acessório**

* **Ver todos os acessórios e seus preços de compra.**
    ```sql
    SELECT nome, raridade, preco_compra
    FROM acessorio;
    ```

* **Ver os efeitos associados a um acessório específico.**
    ```sql
    SELECT a.nome AS acessorio_nome, e.nome AS efeito_nome, e.bravura
    FROM acessorio a
    JOIN efeito_acessorio ea ON a.identificador_acessorio = ea.identificador_acessorio
    JOIN efeito e ON ea.identificador_efeito = e.identificador_efeito
    WHERE a.identificador_acessorio = 301;
    ```

* **Ver os atributos de um acessório específico.**
    ```sql
    SELECT nome, tipo, raridade, preco_compra, preco_venda
    FROM acessorio
    WHERE identificador_acessorio = 301;
    ```

---

## **Arma**

* **Ver todas as armas com uma habilidade específica.**
    ```sql
    SELECT a.nome AS arma_nome, h.nome AS habilidade_nome, h.dano AS dano_habilidade
    FROM arma a
    JOIN habilidade h ON a.identificador_habilidade = h.id_habilidade
    WHERE h.nome = 'Aumenta o ataque em 5';
    ```

* **Ver o nome e a raridade de uma arma.**
    ```sql
    SELECT nome, raridade
    FROM arma
    WHERE identificador_arma = 401;
    ```

* **Ver os atributos de uma arma específica.**
    ```sql
    SELECT
        a.nome,
        a.raridade,
        a.preco_compra,
        a.preco_venda,
        h.nome AS habilidade_nome,
        h.dano AS dano_habilidade
    FROM arma a
    LEFT JOIN habilidade h ON a.identificador_habilidade = h.id_habilidade
    WHERE a.identificador_arma = 401;
    ```

---

## **Fruta**

* **Ver todas as frutas e suas habilidades associadas.**
    ```sql
    SELECT f.nome AS fruta_nome, e.nome AS habilidade_nome, e.bravura AS habilidade_descricao
    FROM fruta f
    JOIN efeito e ON f.identificador_habilidade = e.identificador_efeito;
    ```

* **Ver os atributos de uma fruta específica.**
    ```sql
    SELECT f.nome, f.tipo, f.raridade, f.preco_compra, f.preco_venda, e.nome AS habilidade_nome, e.bravura
    FROM fruta f
    LEFT JOIN efeito e ON f.identificador_habilidade = e.identificador_efeito
    WHERE f.identificador_fruta = 501;
    ```

---

## **Habilidade**

* **Ver habilidades com dano maior que 20.**
    ```sql
    SELECT nome, dano, custo
    FROM habilidade
    WHERE dano > 20;
    ```

---

## **Receita**

* **Ver o consumível produzido por uma receita específica e o jogador associado.**
    ```sql
    SELECT
        r.identificador_receita,
        c.nome AS consumivel_produzido,
        j.nome AS jogador_dono_receita
    FROM receita r
    JOIN consumivel c ON r.consumivel_produzido = c.identificador_consumivel
    LEFT JOIN jogador j ON r.id_jogador = j.id_jogador
    WHERE r.identificador_receita = 1;
    ```

* **Ver todos os ingredientes (consumíveis e não-consumíveis) para uma receita específica.**
    ```sql
    SELECT
        r.identificador_receita,
        cp.nome AS consumivel_produzido,
        'Consumível' AS tipo_ingrediente,
        ic.identificador_consumivel AS id_ingrediente,
        ing_c.nome AS nome_ingrediente
    FROM receita r
    JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
    LEFT JOIN ingrediente_consumivel ic ON r.identificador_receita = ic.identificador_receita
    LEFT JOIN consumivel ing_c ON ic.identificador_consumivel = ing_c.identificador_consumivel
    WHERE r.identificador_receita = 1
    UNION ALL
    SELECT
        r.identificador_receita,
        cp.nome AS consumivel_produzido,
        'Não-Consumível' AS tipo_ingrediente,
        inc.identificador_nao_consumivel AS id_ingrediente,
        ing_nc.nome AS nome_ingrediente
    FROM receita r
    JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
    LEFT JOIN ingrediente_nao_consumivel inc ON r.identificador_receita = inc.identificador_receita
    LEFT JOIN nao_consumivel ing_nc ON inc.identificador_nao_consumivel = ing_nc.identificador_nao_consumivel
    WHERE r.identificador_receita = 1;
    ```

* **Ver fabricações possíveis com um item específico (ingrediente).**
    ```sql
    SELECT
        r.identificador_receita,
        cp.nome AS consumivel_produzido_nome,
        cp.identificador_consumivel AS consumivel_produzido_id
    FROM receita r
    JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
    JOIN ingrediente_consumivel ic ON r.identificador_receita = ic.identificador_receita
    WHERE ic.identificador_consumivel = 106; -- Exemplo para consumível ID 106 ('Alga Fresca')
    ```

* **Ver todas as fabricações de um jogador.**
    ```sql
    SELECT
        r.identificador_receita,
        cp.nome AS consumivel_produzido_nome
    FROM receita r
    JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
    WHERE r.id_jogador = 1;
    ```

---

## **Tipo de Personagem**

* **Ver o tipo de uma pessoa (personagem) específica.**
    ```sql
    SELECT tipo
    FROM tipo_personagem
    WHERE id_personagem = 1;
    ```

---

## **Mapa**

* **Ver informações de um mapa específico.**
    ```sql
    SELECT id_mapa, total_ilhas, total_item_chave
    FROM mapa
    WHERE id_mapa = 1;
    ```

---

## **Jogador**

* **Ver (nome, vida atual e nível) de um jogador.**
    ```sql
    SELECT nome, vida_atual, nivel
    FROM jogador
    WHERE id_jogador = 1;
    ```

* **Ver o tipo de personagem e a habilidade principal de um jogador.**
    ```sql
    SELECT
        j.nome AS jogador_nome,
        tp.tipo AS tipo_personagem,
        h.nome AS habilidade_principal
    FROM jogador j
    LEFT JOIN tipo_personagem tp ON j.id_personagem = tp.id_personagem
    LEFT JOIN habilidade h ON j.id_habilidade = h.id_habilidade
    WHERE j.id_jogador = 1;
    ```

* **Buscar missões de um jogador.**
    ```sql
    SELECT
        j.nome AS nome_jogador,
        m.nome AS nome_missao,
        m.descricao AS descricao_missao
    FROM jogador j
    JOIN missao m ON j.id_jogador = m.id_jogador
    WHERE j.id_jogador = 1;
    ```

* **Buscar o mapa e as coordenadas atuais de um jogador.**
    ```sql
    SELECT
        j.nome AS jogador_nome,
        ma.total_ilhas AS total_ilhas_mapa,
        j.coordenada_x,
        j.coordenada_y
    FROM jogador j
    JOIN mapa ma ON j.id_mapa = ma.id_mapa
    WHERE j.id_jogador = 1;
    ```

---

## **Chefe**

* **Ver o nome, dano e vida de um chefe.**
    ```sql
    SELECT nome, dano, vida
    FROM chefe
    WHERE id_chefe = 1;
    ```

* **Ver chefes em um mapa específico e suas habilidades.**
    ```sql
    SELECT
        c.nome AS chefe_nome,
        m.id_mapa,
        h.nome AS habilidade_chefe
    FROM chefe c
    JOIN mapa m ON c.id_mapa = m.id_mapa
    LEFT JOIN habilidade h ON c.id_habilidade = h.id_habilidade
    WHERE c.id_mapa = 1;
    ```

---

## **Lacaio**

* **Ver todos os lacaios com nível menor que 5.**
    ```sql
    SELECT nome, nivel, experiencia
    FROM lacaio
    WHERE nivel < 5;
    ```

* **Ver a vida atual de uma instância de lacaio.**
    ```sql
    SELECT
        l.nome AS lacaio_nome,
        il.vida_atual
    FROM instancia_lacaio il
    JOIN lacaio l ON il.id_lacaio = l.id_lacaio
    WHERE il.id_instancia_lacaio = 1;
    ```

* **Ver atributos de um lacaio específico.**
    ```sql
    SELECT nome, dano, vida, nivel, experiencia
    FROM lacaio
    WHERE id_lacaio = 1;
    ```

---

## **Aliado**

* **Ver o nome, vida atual e nível de um aliado.**
    ```sql
    SELECT nome, vida_atual, nivel
    FROM aliado
    WHERE id_aliado = 1;
    ```

* **Ver as habilidades de um aliado específico.**
    ```sql
    SELECT
        a.nome AS aliado_nome,
        h.nome AS habilidade_nome,
        h.bravura AS habilidade_descricao
    FROM aliado a
    JOIN habilidade_aliado ha ON a.id_aliado = ha.id_aliado
    JOIN habilidade h ON ha.id_habilidade = h.id_habilidade
    WHERE a.id_aliado = 1;
    ```

* **Ver atributos de um aliado específico.**
    ```sql
    SELECT nome, vida, nivel, vida_atual, dano_base
    FROM aliado
    WHERE id_aliado = 1;
    ```

---

## **Habitante**

* **Ver todos os habitantes de um mapa específico.**
    ```sql
    SELECT nome, tipo, especialidade
    FROM habitante
    WHERE id_mapa = 1;
    ```

* **Ver habitantes que têm uma especialidade.**
    ```sql
    SELECT nome, tipo, especialidade
    FROM habitante
    WHERE especialidade IS NOT NULL;
    ```

* **Ver dados de um habitante pelo ID.**
    ```sql
    SELECT nome, tipo, especialidade, coordenada_x, coordenada_y
    FROM habitante
    WHERE id_habitante = 1;
    ```

---

## **Inventário**

* **Acessar o inventário de um jogador e ver seus atributos.**
    ```sql
    SELECT id_inventario, nome, id_jogador
    FROM inventario
    WHERE id_jogador = 1;
    ```

* **Ver os tipos de itens no inventário de um jogador.**
    ```sql
    SELECT
        ii.identificador_item,
        ti.tipo AS tipo_geral
    FROM iteminventario ii
    JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
    WHERE ii.id_inventario = 1
    ORDER BY ti.tipo;
    ```

---

## **Batalha**

* **Ver todas as batalhas de um jogador específico e a experiência ganha.**
    ```sql
    SELECT
        b.id_batalha,
        j.nome AS jogador_nome,
        b.experiencia_ganha,
        COALESCE(c.nome, l.nome) AS inimigo_enfrentado
    FROM batalha b
    JOIN jogador j ON b.id_jogador = j.id_jogador
    LEFT JOIN chefe c ON b.id_chefe = c.id_chefe
    LEFT JOIN instancia_lacaio il ON b.id_instancia_lacaio = il.id_instancia_lacaio
    LEFT JOIN lacaio l ON il.id_lacaio = l.id_lacaio
    WHERE j.id_jogador = 1;
    ```

---

## **Negociação**

* **Ver todas as negociações de um jogador e o tipo de item negociado.**
    ```sql
    SELECT
        n.id_negociacao,
        j.nome AS jogador_nome,
        h.nome AS vendedor_nome,
        ti.tipo AS tipo_item_negociado,
        n.quantidade,
        n.preco_final,
        n.tipo AS tipo_negociacao
    FROM negociacao n
    JOIN jogador j ON n.id_jogador = j.id_jogador
    JOIN habitante h ON n.id_vendedor = h.id_habitante
    JOIN tipo_item ti ON n.identificador_item = ti.identificador_item
    WHERE j.id_jogador = 1;
    ```

---

## **Missão**

* **Buscar todas as missões e seus detalhes.**
    ```sql
    SELECT
        m.nome AS nome_missao,
        m.descricao,
        map.total_ilhas AS mapa_missao,
        j.nome AS jogador_associado,
        h.nome AS recrutador,
        m.tipo_sala,
        m.sala_id
    FROM missao m
    LEFT JOIN mapa map ON m.mapa_id = map.id_mapa
    LEFT JOIN jogador j ON m.id_jogador = j.id_jogador
    LEFT JOIN habitante h ON m.id_recrutador = h.id_habitante;
    ```

* **Ver missões em um tipo de sala específico (ex: 'vila').**
    ```sql
    SELECT nome, descricao
    FROM missao
    WHERE tipo_sala = 'vila';
    ```

* **Ver o item que uma missão vai dar.**
    ```sql
    SELECT
        im.identificador_item,
        ti.tipo AS tipo_geral
    FROM itemmissao im
    JOIN tipo_item ti ON im.identificador_item = ti.identificador_item
    WHERE im.missao_id = 1;
    ```

* **Ver o lugar que uma missão está.**
    ```sql
    SELECT
        m.nome AS nome_missao,
        m.tipo_sala,
        m.sala_id,
        CASE
            WHEN m.tipo_sala = 'campo_batalha' THEN cb.tamanho || ' - ' || cb.tipo_terreno
            WHEN m.tipo_sala = 'porto' THEN 'Porto - ' || p.capacidade || ' barcos'
            WHEN m.tipo_sala = 'vila' THEN 'Vila - ' || v.informacoes
            ELSE 'Local desconhecido'
        END AS detalhes_local
    FROM missao m
    LEFT JOIN campo_batalha cb ON m.tipo_sala = 'campo_batalha' AND m.sala_id = cb.sala_id
    LEFT JOIN porto p ON m.tipo_sala = 'porto' AND m.sala_id = p.sala_id
    LEFT JOIN vila v ON m.tipo_sala = 'vila' AND m.sala_id = v.sala_id
    WHERE m.missao_id = 1;
    ```

* **Ver o (nome, descrição) de uma missão específica.**
    ```sql
    SELECT nome, descricao
    FROM missao
    WHERE missao_id = 2;
    ```

---

## **Salas (Campo de Batalha, Porto, Vila)**

* **Ver todos os campos de batalha e seus tamanhos.**
    ```sql
    SELECT sala_id, tipo_terreno, tamanho
    FROM campo_batalha;
    ```

* **Ver todos os portos com capacidade maior que 5.**
    ```sql
    SELECT sala_id, qtd_barcos, capacidade
    FROM porto
    WHERE capacidade > 5;
    ```

* **Ver informações de uma vila específica.**
    ```sql
    SELECT sala_id, total_salas, informacoes
    FROM vila
    WHERE sala_id = 2;
    ```

* **Buscar informações de uma sala (genérico).**
    ```sql
    SELECT *
    FROM campo_batalha -- Ou 'porto', ou 'vila'
    WHERE sala_id = 1; -- Adapte o ID e a tabela conforme necessário
    ```

---

## **Ilha**

* **Ver todas as ilhas e a qual sala (campo de batalha) elas estão associadas.**
    ```sql
    SELECT
        i.nome AS nome_ilha,
        i.tipo AS tipo_ilha,
        cb.tipo_terreno AS tipo_terreno_associado,
        cb.tamanho AS tamanho_campo_batalha
    FROM ilha i
    JOIN campo_batalha cb ON i.sala_id = cb.sala_id;
    ```

---

## **Mar**

* **Ver todos os mares e seus monstros/obstáculos.**
    ```sql
    SELECT mar_id, monstro, obstaculo
    FROM mar;
    ```

* **Ver informações de um Marco.**
    ```sql
    SELECT mar_id, monstro, obstaculo
    FROM marco
    WHERE mar_id = 1;
    ```

---

## **Corredor Marítimo**

* **Ver todas as rotas marítimas entre ilhas.**
    ```sql
    SELECT
        cm.maritimo_id,
        ia.nome AS ilha_origem,
        ib.nome AS ilha_destino
    FROM corredor_maritimo cm
    JOIN ilha ia ON cm.ilha_a = ia.id
    JOIN ilha ib ON cm.ilha_b = ib.id;
    ```

---

## **Barco**

* **Ver todos os barcos com melhorias.**
    ```sql
    SELECT nome, nivel, melhoria
    FROM barco
    WHERE melhoria IS NOT NULL;
    ```

* **Ver os barcos que estão em um porto específico.**
    ```sql
    SELECT
        b.nome AS nome_barco,
        bp.sala_id AS id_porto
    FROM barco_porto bp
    JOIN barco b ON bp.tipo_barco = b.tipo_barco
    WHERE bp.sala_id = 3;
    ```

---

## **Locais**

* **Ver quais pessoas estão em um local (mapa) específico.**
    ```sql
    SELECT
        id, nome, tipo_entidade, coordenada_x, coordenada_y
    FROM (
        SELECT id_jogador AS id, nome, 'Jogador' AS tipo_entidade, coordenada_x, coordenada_y FROM jogador WHERE id_mapa = 1
        UNION ALL
        SELECT id_lacaio AS id, nome, 'Lacaio' AS tipo_entidade, coordenada_x, coordenada_y FROM lacaio WHERE id_mapa = 1
        UNION ALL
        SELECT id_chefe AS id, nome, 'Chefe' AS tipo_entidade, coordenada_x, coordenada_y FROM chefe WHERE id_mapa = 1
        UNION ALL
        SELECT id_aliado AS id, nome, 'Aliado' AS tipo_entidade, coordenada_x, coordenada_y FROM aliado WHERE id_mapa = 1
        UNION ALL
        SELECT id_habitante AS id, nome, 'Habitante' AS tipo_entidade, coordenada_x, coordenada_y FROM habitante WHERE id_mapa = 1
    ) AS PessoasNoLocal
    ORDER BY tipo_entidade, nome;
    ```

* **Ver quais itens estão em um local (mapa) específico.**
    * *Nota: Seu esquema não liga itens a 'lugares' diretamente, apenas itens chave aos mapas. Adaptação conceitual.*
    ```sql
    SELECT m.id_mapa, m.total_item_chave AS quantidade_itens_chave
    FROM mapa m
    WHERE m.id_mapa = 1;
    ```

---

## **Inconsistências (Exemplo de Verificação)**

* **Comando para verificar inconsistências no inventário.**
    * *Nota: Seu esquema não tem 'tamanho' para itens nem 'inventario_ocupado'. Esta é uma adaptação conceitual para verificar itens no inventário que não têm um 'tipo' válido.*
    ```sql
    SELECT ii.id_inventario, ii.identificador_item
    FROM iteminventario ii
    LEFT JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
    WHERE ti.identificador_item IS NULL;
    ```

---