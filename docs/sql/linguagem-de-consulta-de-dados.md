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

A seguir estão exemplos de consultas aplicadas ao nosso banco de dados final.

### **Tipo de Item**

* **Ver todos os tipos de itens disponíveis.**
    ```sql
    SELECT identificador_item, tipo
    FROM tipo_item;
    ```

* **Contar quantos tipos de itens existem no total.**
    ```sql
    SELECT COUNT(*) AS total_de_tipos
    FROM tipo_item;
    ```

### **Efeito**

* **Ver todos os efeitos e seus valores.**
    ```sql
    SELECT nome, valor
    FROM efeito;
    ```

* **Encontrar os 5 efeitos curativos mais fortes (que restauram PV).**
    ```sql
    SELECT nome, valor
    FROM efeito
    WHERE nome = 'Restaura PV'
    ORDER BY valor DESC
    LIMIT 5;
    ```

### **Consumível**

* **Ver todos os consumíveis que podem ser fabricados.**
    ```sql
    SELECT nome, raridade, preco_de_venda, descricao
    FROM consumivel
    WHERE e_fabricavel = TRUE;
    ```

* **Listar os 10 consumíveis mais caros para vender.**
    ```sql

    SELECT nome, preco_de_venda, raridade
    FROM consumivel
    ORDER BY preco_de_venda DESC
    LIMIT 10;
    ```

### **Não-Consumível**

* **Ver todos os itens não-consumíveis de raridade '★★'.**
    ```sql
  
    SELECT nome, tipo, preco_de_venda, descricao
    FROM nao_consumivel
    WHERE raridade = '★★';
    ```

* **Calcular a margem de lucro (venda - compra) para itens que podem ser comprados.**
    ```sql
    SELECT nome, (preco_de_venda - preco_de_compra) AS margem_de_lucro
    FROM nao_consumivel
    WHERE preco_de_compra > 0
    ORDER BY margem_de_lucro DESC;
    ```

### **Habilidade**

* **Encontrar todas as habilidades que não custam energia (custo zero).**
    ```sql
    SELECT nome, dano
    FROM habilidade
    WHERE custo = 0;
    ```

* **Listar habilidades pela sua "eficiência" (dano por ponto de custo).**
    ```sql
    SELECT nome, dano, custo, (dano::decimal / custo) AS eficiencia
    FROM habilidade
    WHERE custo > 0
    ORDER BY eficiencia DESC;
    ```

### **Receita**

* **Ver todos os ingredientes para uma receita específica.**
    ```sql
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
    ```

* **Encontrar todas as receitas que usam um ingrediente específico.**
    ```sql
    SELECT
        r.identificador_receita,
        c.nome AS item_produzido
    FROM receita r
    JOIN consumivel c ON r.consumivel_produzido = c.identificador_consumivel
    JOIN ingrediente_nao_consumivel inc ON r.identificador_receita = inc.identificador_receita
    WHERE inc.identificador_nao_consumivel = 8; 
    ```

---


### **Mundo (Salas, Ilhas, Mapas)**

* **Encontrar campos de batalha em um tipo de terreno específico.**
    ```sql
    SELECT sala_id, tipo_terreno, tamanho 
    FROM campo_batalha 
    WHERE tipo_terreno = 'Floresta';
    ```
* **Ver todas as ilhas que pertencem a um mapa específico.**
    ```sql
    SELECT i.id AS id_da_ilha
    FROM ilha i
    JOIN mapa m ON i.id = m.id_ilha
    WHERE m.id_mapa = 1; 
    ```

### **Jogador e Aliados**

* **Encontrar em qual mapa e ilha um determinado jogador está.**
    ```sql
    SELECT j.nome AS nome_jogador, m.id_mapa, m.id_ilha
    FROM jogador j
    JOIN mapa m ON j.id_mapa_pk = m.id_mapa_pk
    WHERE j.id_jogador = 1;
    ```
* **Ver todas as habilidades de um aliado específico.**
    ```sql
    SELECT a.nome AS nome_aliado, h.nome AS nome_habilidade, h.dano, h.custo
    FROM habilidade_aliado ha
    JOIN aliado a ON ha.id_aliado = a.id_aliado
    JOIN habilidade h ON ha.id_habilidade = h.id_habilidade
    WHERE a.nome = 'Shuan';
    ```

### **NPCs (Chefes, Lacaios, Habitantes)**

* **Listar todos os NPCs em uma ilha específica.**
    ```sql
   
    SELECT nome, 'Chefe' as tipo FROM chefe WHERE id_mapa_pk = 1
    UNION ALL
    SELECT nome, 'Lacaio' as tipo FROM lacaio WHERE id_mapa_pk = 1
    UNION ALL
    SELECT nome, 'Aliado' as tipo FROM aliado WHERE id_mapa_pk = 1
    UNION ALL
    SELECT nome, 'Habitante' as tipo FROM habitante WHERE id_mapa_pk = 1;
    ```

* **Encontrar o chefe com a maior quantidade de vida.**
    ```sql
    SELECT nome, vida, nivel
    FROM chefe
    ORDER BY vida DESC
    LIMIT 1;
    ```

---

### **Interações e Eventos**

### **Batalha**

* **Ver um registro de batalhas, mostrando jogador e chefe.**
    ```sql
    SELECT 
        b.identificador_batalha, 
        j.nome AS nome_jogador, 
        c.nome AS nome_chefe
    FROM batalha b
    JOIN jogador j ON b.identificador_jogador = j.id_jogador
    JOIN chefe c ON b.identificador_chefe = c.id_chefe;
    ```

* **Listar todos os lacaios que participaram de uma batalha específica.**
    ```sql
    SELECT l.nome AS nome_lacaio
    FROM batalha_instancia_lacaio bil
    JOIN instancia_lacaio il ON bil.identificador_instancia_lacaio = il.id_instancia_lacaio
    JOIN lacaio l ON il.identificador_lacaio = l.id_lacaio
    WHERE bil.identificador_batalha = 1;
    ```

### **Missão**

* **Encontrar todas as missões dadas por um recrutador específico.**
    ```sql
    SELECT m.nome, m.descricao
    FROM missao m
    WHERE m.id_recrutador = 1; 
    ```
* **Encontrar todas as missões que requerem um item de um tipo específico.**
    ```sql
    SELECT m.nome AS nome_missao, ti.tipo AS tipo_item_necessario
    FROM missao m
    JOIN ItemMissao im ON m.missao_id = im.missao_id
    JOIN tipo_item ti ON im.identificador_item = ti.identificador_item
    WHERE ti.tipo = 'Fruta';
    ```
### **Negociação**

* **Ver o histórico de negociações de um jogador.**
    ```sql
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
    ```

### **Inventário**
* **Ver o conteúdo do inventário de um jogador.**
    ```sql
    SELECT
        inv.id_inventario,
        j.nome AS dono_do_inventario,
        ti.tipo AS tipo_de_item_no_inventario
    FROM ItemInventario ii
    JOIN Inventario inv ON ii.id_inventario = inv.id_inventario
    JOIN jogador j ON inv.id_jogador = j.id_jogador
    JOIN tipo_item ti ON ii.identificador_item = ti.identificador_item
    WHERE j.id_jogador = 1;
    ```

---
### **Navegação**

* **Ver para quais ilhas é possível navegar a partir de uma ilha específica.**
    ```sql
    SELECT 
        ilha_a.id AS id_origem, 
        ilha_b.id AS id_destino
    FROM corredor_maritimo cm
    JOIN ilha ilha_a ON cm.ilha_a = ilha_a.id
    JOIN ilha ilha_b ON cm.ilha_b = ilha_b.id
    WHERE cm.ilha_a = 1; 
    ```

* **Ver os monstros e obstáculos de um mar que conecta duas ilhas.**
    ```sql
    SELECT 
        cm.ilha_a, 
        cm.ilha_b, 
        m.monstro, 
        m.obstaculo
    FROM controlador_mar ctm
    JOIN mar m ON ctm.mar_id = m.mar_id
    JOIN corredor_maritimo cm ON ctm.maritimo_id = cm.maritimo_id;
    ```

* **Listar todos os barcos ancorados em um porto específico.**
    ```sql
    SELECT b.nome, b.tipo, b.melhoria
    FROM barco_porto bp
    JOIN barco b ON bp.barco_id = b.id
    WHERE bp.sala_id = 16; 
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