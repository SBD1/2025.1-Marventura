# **Linguagem de Consulta de Dados (DQL)**

## **Introdução**

A **Linguagem de Consulta de Dados (DQL)**, ou *Data Query Language*, é um subconjunto da SQL (*Structured Query Language*) focado exclusivamente na **consulta e recuperação de informações** armazenadas em um banco de dados. Diferentemente de outras partes da SQL, como DML (*Data Manipulation Language*) que modifica dados, ou DDL (*Data Definition Language*) que define a estrutura do banco de dados, a DQL é utilizada para fazer perguntas ao banco de dados e obter conjuntos de resultados.

O comando central e mais emblemático da DQL é o `SELECT`. Através dele, é possível especificar quais colunas de quais tabelas devem ser retornadas, aplicar filtros para selecionar linhas específicas, ordenar os resultados, agregar dados e combinar informações de múltiplas tabelas.

Dominar a DQL é fundamental para qualquer profissional que trabalhe com bancos de dados, incluindo desenvolvedores, analistas de dados, cientistas de dados e administradores de banco de dados (DBAs), pois permite extrair *insights* valiosos e informações precisas dos dados armazenados. 🔍

-----

## **Metodologia**

A elaboração deste conteúdo seguiu as seguintes etapas:

1.  **Compreensão dos Fundamentos do Banco de Dados Relacional**:
    * Entender a estrutura de tabelas, colunas, linhas, chaves primárias e estrangeiras.
    * Visualizar como os dados são organizados e relacionados.

2.  **O Comando `SELECT` Básico**:
    * Selecionar todas as colunas de uma tabela: `SELECT * FROM nome_da_tabela;`
    * Selecionar colunas específicas: `SELECT coluna1, coluna2 FROM nome_da_tabela;`
    * Uso de `AS` para criar *aliases* para colunas, melhorando a legibilidade dos resultados.

3.  **Filtragem de Dados com `WHERE`**:
    * Aplicar condições para selecionar apenas as linhas que atendem a critérios específicos.
    * Uso de operadores de comparação (`=`, `>`, `<`, `<>`, `!=`, `>=`, `<=`).
    * Uso de operadores lógicos (`AND`, `OR`, `NOT`).
    * Uso de operadores como `BETWEEN`, `LIKE`, `IN`, `IS NULL`.

-----

## **DQL - Exemplos de Consultas**

### Consultas de Jogador

```sql
-- Buscar dados de um jogador pelo ID
SELECT
    identificador_jogador,
    identificador_area,
    TRIM(nome) AS nome,
    TRIM(descricao) AS descricao,
    coordenada_x,
    coordenada_y,
    TRIM(orientacao) AS orientacao,
    energia,
    vida,
    nivel,
    sorte,
    vida_atual,
    experiencia_atual,
    moedas_totais
FROM jogador
WHERE identificador_jogador = %s;
```

```sql
-- Verificar se um registro de jogador existe
SELECT 1 FROM jogador WHERE identificador_jogador = %s;
```

### Consultas de Inventário e Itens

```sql
-- Buscar o inventário completo de um jogador
SELECT
    ii.identificador_item,
    ii.quantidade,
    ti.tipo as tipo_item,
    CASE
        WHEN ti.tipo = 'con' THEN TRIM(c.nome)
        WHEN ti.tipo = 'ncn' THEN TRIM(nc.nome)
        WHEN ti.tipo = 'arm' THEN TRIM(a.nome)
        WHEN ti.tipo = 'ace' THEN TRIM(ac.nome)
        WHEN ti.tipo = 'fru' THEN TRIM(f.nome)
    END as nome_item,
    CASE
        WHEN ti.tipo = 'con' THEN TRIM(c.descricao)
        WHEN ti.tipo = 'ncn' THEN TRIM(nc.descricao)
        WHEN ti.tipo = 'arm' THEN TRIM(a.descricao)
        WHEN ti.tipo = 'ace' THEN TRIM(ac.descricao)
        WHEN ti.tipo = 'fru' THEN TRIM(f.descricao)
    END as descricao,
    CASE
        WHEN ti.tipo = 'con' THEN c.preco_de_compra
        WHEN ti.tipo = 'ncn' THEN nc.preco_de_compra
        WHEN ti.tipo = 'arm' THEN a.preco_de_compra
        WHEN ti.tipo = 'ace' THEN ac.preco_de_compra
        WHEN ti.tipo = 'fru' THEN NULL
    END as preco_compra,
    CASE
        WHEN ti.tipo = 'con' THEN c.preco_de_venda
        WHEN ti.tipo = 'ncn' THEN nc.preco_de_venda
        WHEN ti.tipo = 'arm' THEN NULL
        WHEN ti.tipo = 'ace' THEN NULL
        WHEN ti.tipo = 'fru' THEN f.preco_de_venda
    END as preco_venda
FROM inventario inv
JOIN item_inventario ii ON inv.identificador_inventario = ii.identificador_inventario
JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item
LEFT JOIN consumivel c ON ii.identificador_item = c.identificador_consumivel AND ti.tipo = 'con'
LEFT JOIN nao_consumivel nc ON ii.identificador_item = nc.identificador_nao_consumivel AND ti.tipo = 'ncn'
LEFT JOIN arma a ON ii.identificador_item = a.identificador_arma AND ti.tipo = 'arm'
LEFT JOIN acessorio ac ON ii.identificador_item = ac.identificador_acessorio AND ti.tipo = 'ace'
LEFT JOIN fruta f ON ii.identificador_item = f.identificador_fruta AND ti.tipo = 'fru'
WHERE inv.identificador_personagem = %s
AND inv.tipo_inventario = 'ger'
AND ii.quantidade > 0
```

```sql
-- Buscar o ID do inventário geral de um personagem
SELECT identificador_inventario FROM inventario WHERE identificador_personagem = %s AND tipo_inventario = 'ger'
```

```sql
-- Buscar os tipos de itens em um inventário
SELECT
    ii.identificador_item,
    ti.tipo AS tipo_geral
FROM iteminventario ii
JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
WHERE ii.id_inventario = %s
ORDER BY ti.tipo;
```


```sql
-- Buscar o tipo de um item específico
SELECT tipo
FROM tipo_item
WHERE identificador_item = %s;
```

### Consultas de Personagens (NPCs)

```sql
-- Buscar o tipo de um personagem
SELECT tipo
FROM tipo_personagem
WHERE id_personagem = %s;
```

```sql
-- Buscar atributos de um lacaio
SELECT nome, dano, vida, nivel, experiencia
FROM lacaio
WHERE id_lacaio = %s;
```

```sql
-- Buscar todos os lacaios em uma área
SELECT
    il.identificador_instancia_lacaio,
    il.coordenada_x AS x,
    il.coordenada_y AS y,
    il.vida_atual,
    il.moedas_totais,
    l.identificador_lacaio,
    TRIM(l.nome) AS nome_lacaio,
    TRIM(l.descricao) AS descricao_lacaio,
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
LEFT JOIN habilidade_personagem hp ON hp.identificador_personagem = l.identificador_lacaio
LEFT JOIN habilidade h ON h.identificador_habilidade = hp.identificador_habilidade
LEFT JOIN inventario inv ON inv.identificador_personagem = l.identificador_lacaio AND inv.tipo_inventario = 'ger'
LEFT JOIN item_inventario ii ON ii.identificador_inventario = inv.identificador_inventario
LEFT JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item
LEFT JOIN consumivel ON consumivel.identificador_consumivel = ti.identificador_item
LEFT JOIN nao_consumivel ON nao_consumivel.identificador_nao_consumivel = ti.identificador_item
WHERE il.identificador_area = %s;
```

```sql
-- Buscar atributos de um chefe
SELECT nome, dano, vida, nivel, experiencia
FROM chefe
WHERE id_chefe = %s;
```

```sql
-- Buscar atributos de um aliado
SELECT nome, vida, nivel, vida_atual, dano_base
FROM aliado
WHERE id_aliado = %s;
```

```sql
-- Buscar dados de um habitante
SELECT nome, tipo, especialidade, coordenada_x, coordenada_y
FROM habitante
WHERE id_habitante = %s;
```

### Consultas de Locais (Ilhas, Áreas)

```sql
-- Buscar informações de uma ilha
SELECT
    identificador_ilha,
    TRIM(nome) AS nome,
    visitada
FROM ilha WHERE identificador_ilha = %s;
```

```sql
-- Buscar caminhos de uma área
SELECT TRIM(tipo_terreno) AS tipo_terreno, x, y, largura, altura
FROM caminho
WHERE identificador_area = %s;
```

```sql
-- Buscar obstáculos de uma área
SELECT *
FROM obstaculo
WHERE identificador_area = %s;
```

```sql
-- Buscar informações de uma área
SELECT
    identificador_area,
    identificador_ilha,
    TRIM(nome) AS nome,
    TRIM(tipo_area) AS tipo_area,
    TRIM(chave_imagem_fundo) AS chave_imagem_fundo,
    TRIM(chave_imagem_frente) AS chave_imagem_frente,
    visitada
FROM area
WHERE identificador_area = %s;
```

```sql
-- Buscar o porto de uma ilha
SELECT
    identificador_area,
    identificador_ilha,
    TRIM(nome) AS nome,
    TRIM(tipo_area) AS tipo_area,
    TRIM(chave_imagem_fundo) AS chave_imagem_fundo,
    TRIM(chave_imagem_frente) AS chave_imagem_frente,
    visitada
FROM area
WHERE identificador_ilha = %s AND tipo_area = 'Porto';
```

```sql
-- Buscar áreas interativas em uma área
SELECT
    identificador_area_interativa,
    identificador_area,
    TRIM(chave_imagem) AS chave_imagem,
    x,
    y,
    largura,
    altura,
    TRIM(tipo_evento) AS tipo_evento
FROM area_interativa
WHERE identificador_area = %s;
```

```sql
-- Buscar eventos de embarcar
SELECT
    e.identificador_evento,
    TRIM(e.tipo_evento) AS tipo_evento,
    e.identificador_porto_destino,
    e.ponto_geracao_x,
    e.ponto_geracao_y,
    TRIM(e.orientacao) AS orientacao
FROM area_interativa_evento aie
JOIN evento e ON e.identificador_evento = aie.identificador_evento
WHERE aie.identificador_area_interativa = %s;
```

```sql
-- Buscar evento de mudança de área
SELECT
    e.identificador_evento,
    TRIM(e.tipo_evento) AS tipo_evento,
    e.ponto_geracao_x,
    e.ponto_geracao_y,
    TRIM(e.orientacao) AS orientacao,
    a_dest.identificador_area AS area_destino
FROM area_interativa_evento aie
JOIN evento e ON e.identificador_evento = aie.identificador_evento
JOIN area_interativa ai ON ai.identificador_area_interativa = aie.identificador_area_interativa
JOIN area a_dest ON a_dest.identificador_area =
    CASE
        WHEN e.identificador_area_a = ai.identificador_area THEN e.identificador_area_b
        ELSE e.identificador_area_a
    END
WHERE aie.identificador_area_interativa = %s;
```

```sql
-- Buscar conexões de uma ilha
SELECT i.identificador_ilha, TRIM(i.nome) AS nome, i.visitada
FROM conexao_entre_ilhas c
JOIN ilha i ON i.identificador_ilha =
    CASE
        WHEN c.identificador_ilha_a = %s THEN c.identificador_ilha_b
        ELSE c.identificador_ilha_a
    END
WHERE %s IN (c.identificador_ilha_a, c.identificador_ilha_b);
```

```sql
-- Buscar todas as "pessoas" (entidades) em um local
SELECT id_jogador AS id, nome, 'Jogador' AS tipo_entidade, coordenada_x, coordenada_y FROM jogador WHERE id_mapa = %s
UNION ALL
SELECT id_lacaio AS id, nome, 'Lacaio' AS tipo_entidade, coordenada_x, coordenada_y FROM lacaio WHERE id_mapa = %s
UNION ALL
SELECT id_chefe AS id, nome, 'Chefe' AS tipo_entidade, coordenada_x, coordenada_y FROM chefe WHERE id_mapa = %s
UNION ALL
SELECT id_aliado AS id, nome, 'Aliado' AS tipo_entidade, coordenada_x, coordenada_y FROM aliado WHERE id_mapa = %s
UNION ALL
SELECT id_habitante AS id, nome, 'Habitante' AS tipo_entidade, coordenada_x, coordenada_y FROM habitante WHERE id_mapa = %s
ORDER BY tipo_entidade, nome;
```

```sql
-- Buscar itens em um local (adaptado para contar itens chave)
SELECT m.id_mapa, m.total_item_chave
FROM mapa m
WHERE m.id_mapa = %s;
```

### Consultas de Fabricação (Receitas)

```sql
-- Buscar uma receita específica e seus ingredientes
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
WHERE r.identificador_receita = %s
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
WHERE r.identificador_receita = %s;
```

```sql
-- Buscar receitas por ingrediente consumível
SELECT
    r.identificador_receita,
    cp.nome AS consumivel_produzido_nome,
    cp.identificador_consumivel AS consumivel_produzido_id
FROM receita r
JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
JOIN ingrediente_consumivel ic ON r.identificador_receita = ic.identificador_receita
WHERE ic.identificador_consumivel = %s;
```

```sql
-- Buscar receitas por ingrediente não consumível
SELECT
    r.identificador_receita,
    cp.nome AS consumivel_produzido_nome,
    cp.identificador_consumivel AS consumivel_produzido_id
FROM receita r
JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
JOIN ingrediente_nao_consumivel inc ON r.identificador_receita = inc.identificador_receita
WHERE inc.identificador_nao_consumivel = %s;
```

```sql
-- Buscar receitas aprendidas por um jogador
SELECT
    r.identificador_receita,
    cp.nome AS consumivel_produzido_nome
FROM receita r
JOIN consumivel cp ON r.consumivel_produzido = cp.identificador_consumivel
WHERE r.id_jogador = %s;
```

### Consultas de Missões

```sql
-- Buscar missões de um jogador
SELECT m.nome, m.descricao
FROM missao m
WHERE m.id_jogador = %s;
```

```sql
-- Buscar item de recompensa de uma missão
SELECT
    im.identificador_item,
    ti.tipo AS tipo_geral
FROM itemmissao im
JOIN tipo_item ti ON im.identificador_item = ti.identificador_item
WHERE im.missao_id = %s;
```

```sql
-- Buscar o local de uma missão
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
WHERE m.missao_id = %s;
```

```sql
-- Buscar detalhes de uma missão
SELECT nome, descricao
FROM missao
WHERE missao_id = %s;
```

### Consultas de Tipos de Itens Específicos

```sql
-- Buscar atributos de uma arma
SELECT
    a.nome,
    a.raridade,
    a.preco_compra,
    a.preco_venda,
    h.nome AS habilidade_nome,
    h.dano AS dano_habilidade
FROM arma a
LEFT JOIN habilidade h ON a.identificador_habilidade = h.id_habilidade
WHERE a.identificador_arma = %s;
```

```sql
-- Buscar atributos de um consumível
SELECT nome, tipo, raridade, quantidade, preco_compra, preco_venda, efabricavel
FROM consumivel
WHERE identificador_consumivel = %s;
```

```sql
-- Buscar atributos de um acessório
SELECT nome, tipo, raridade, preco_compra, preco_venda
FROM acessorio
WHERE identificador_acessorio = %s;
```

```sql
-- Buscar atributos de um não consumível
SELECT nome, tipo, raridade, quantidade, preco_compra, preco_venda
FROM nao_consumivel
WHERE identificador_nao_consumivel = %s;
```

```sql
-- Buscar atributos de uma fruta
SELECT f.nome, f.tipo, f.raridade, f.preco_compra, f.preco_venda, e.nome AS habilidade_nome, e.bravura
FROM fruta f
LEFT JOIN efeito e ON f.identificador_habilidade = e.identificador_efeito
WHERE f.identificador_fruta = %s;
```

### Consultas de Vendedor e Negociação

```sql
-- Buscar vendedores em uma área
SELECT
    h.identificador_habitante,
    TRIM(h.nome) as nome,
    TRIM(h.descricao) as descricao,
    h.coordenada_x,
    h.coordenada_y,
    h.moedas_totais
FROM habitante h
WHERE h.identificador_area = %s
AND h.tipo_habitante = 'ven'
```

```sql
-- Buscar o inventário de um vendedor
SELECT
    ii.identificador_item,
    ii.quantidade,
    ti.tipo as tipo_item,
    CASE
        WHEN ti.tipo = 'con' THEN TRIM(c.nome)
        WHEN ti.tipo = 'ncn' THEN TRIM(nc.nome)
        WHEN ti.tipo = 'arm' THEN TRIM(a.nome)
        WHEN ti.tipo = 'ace' THEN TRIM(ac.nome)
        WHEN ti.tipo = 'fru' THEN TRIM(f.nome)
    END as nome_item,
    CASE
        WHEN ti.tipo = 'con' THEN TRIM(c.descricao)
        WHEN ti.tipo = 'ncn' THEN TRIM(nc.descricao)
        WHEN ti.tipo = 'arm' THEN TRIM(a.descricao)
        WHEN ti.tipo = 'ace' THEN TRIM(ac.descricao)
        WHEN ti.tipo = 'fru' THEN TRIM(f.descricao)
    END as descricao,
    CASE
        WHEN ti.tipo = 'con' AND c.preco_de_compra IS NOT NULL THEN c.preco_de_compra
        WHEN ti.tipo = 'ncn' AND nc.preco_de_compra IS NOT NULL THEN nc.preco_de_compra
        WHEN ti.tipo = 'arm' THEN a.preco_de_compra
        WHEN ti.tipo = 'ace' THEN ac.preco_de_compra
        WHEN ti.tipo = 'con' AND c.preco_de_venda IS NOT NULL THEN c.preco_de_venda * 2
        WHEN ti.tipo = 'ncn' AND nc.preco_de_venda IS NOT NULL THEN nc.preco_de_venda * 2
        WHEN ti.tipo = 'fru' AND f.preco_de_venda IS NOT NULL THEN f.preco_de_venda * 2
        ELSE NULL
    END as preco_compra,
    CASE
        WHEN ti.tipo = 'con' THEN c.preco_de_venda
        WHEN ti.tipo = 'ncn' THEN nc.preco_de_venda
        WHEN ti.tipo = 'arm' THEN NULL
        WHEN ti.tipo = 'ace' THEN NULL
        WHEN ti.tipo = 'fru' THEN f.preco_de_venda
    END as preco_venda
FROM inventario inv
JOIN item_inventario ii ON inv.identificador_inventario = ii.identificador_inventario
JOIN tipo_item ti ON ti.identificador_item = ii.identificador_item
LEFT JOIN consumivel c ON ii.identificador_item = c.identificador_consumivel AND ti.tipo = 'con'
LEFT JOIN nao_consumivel nc ON ii.identificador_item = nc.identificador_nao_consumivel AND ti.tipo = 'ncn'
LEFT JOIN arma a ON ii.identificador_item = a.identificador_arma AND ti.tipo = 'arm'
LEFT JOIN acessorio ac ON ii.identificador_item = ac.identificador_acessorio AND ti.tipo = 'ace'
LEFT JOIN fruta f ON ii.identificador_item = f.identificador_fruta AND ti.tipo = 'fru'
WHERE inv.identificador_personagem = %s
AND inv.tipo_inventario = 'ger'
AND ii.quantidade > 0
```

```sql
-- Buscar a arma equipada de um jogador
SELECT
    je.identificador_arma AS identificador_item,
    'arm' AS tipo_item,
    TRIM(a.nome) AS nome_item,
    TRIM(a.descricao) AS descricao,
    a.raridade,
    a.preco_de_compra
FROM jogador_equipamento je
JOIN arma a ON je.identificador_arma = a.identificador_arma
WHERE je.identificador_jogador = %s;
```

```sql
-- [Reset] Buscar inventários dos vendedores
SELECT identificador_personagem, identificador_inventario FROM inventario WHERE identificador_personagem LIKE 'ven%%'
```

```sql
-- Verificar inconsistências no inventário
SELECT ii.id_inventario, ii.identificador_item
FROM iteminventario ii
LEFT JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
WHERE ti.identificador_item IS NULL;
```

---
## **📚 Bibliografia**

  * ELMASRI, R.; NAVATHE, S. B. *Sistemas de Banco de Dados*. 7. ed. Pearson Education do Brasil, 2018.
  * DATE, C. J. *An Introduction to Database Systems*. 8. ed. Addison-Wesley, 2003.
  * SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. *Database System Concepts*. 7. ed. McGraw-Hill Education, 2019.
  * PostgreSQL Documentation. Disponível em: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/) (Acesso em 18 de junho de 2025).
  * Microsoft SQL Server Documentation. Disponível em: [https://docs.microsoft.com/en-us/sql/sql-server/](https://docs.microsoft.com/en-us/sql/sql-server/) (Acesso em 18 de junho de 2025).

---

## **📑 Histórico de Versões**

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 29/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 |
| `1.1` | adicionado as consultas | [Pablo Serra](https://github.com/Pabloserrapxx) | 16/06/2025 |  |  |
| `1.2` | atualizado o documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 08/07/2025 |  |  |