# Linguagem de Consulta de Dados (DQL)

## Introdução

A **Linguagem de Consulta de Dados (DQL)**, ou *Data Query Language*, é um subconjunto da SQL (*Structured Query Language*) focado exclusivamente na **consulta e recuperação de informações** armazenadas em um banco de dados. Diferentemente de outras partes da SQL, como DML (*Data Manipulation Language*) que modifica dados, ou DDL (*Data Definition Language*) que define a estrutura do banco de dados, a DQL é utilizada para fazer perguntas ao banco de dados e obter conjuntos de resultados.

O comando central e mais emblemático da DQL é o `SELECT`. Através dele, é possível especificar quais colunas de quais tabelas devem ser retornadas, aplicar filtros para selecionar linhas específicas, ordenar os resultados, agregar dados e combinar informações de múltiplas tabelas.

Dominar a DQL é fundamental para qualquer profissional que trabalhe com bancos de dados, incluindo desenvolvedores, analistas de dados, cientistas de dados e administradores de banco de dados (DBAs), pois permite extrair *insights* valiosos e informações precisas dos dados armazenados. 🔍

---

## Metodologia

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
---

## DQL - Linguagem de Consulta de Dados

## Habitante

-   Ver todos os atributos de um habitante específico:
    ```sql
    SELECT identificador_habitante, identificador_mapa, IlhaID, tipo, nome, descricao, especialidade, coordenada_x, coordenada_y
    FROM Habitante
    WHERE identificador_habitante = 2;
    ```

-   Ver quais habitantes possuem uma especialidade específica:
    ```sql
    SELECT identificador_habitante, nome, tipo, especialidade
    FROM Habitante
    WHERE especialidade = 'arm';
    ```

-   Ver habitantes localizados em um Mapa/Ilha específico:
    ```sql
    SELECT identificador_habitante, nome, tipo, especialidade
    FROM Habitante
    WHERE identificador_mapa = 1 AND IlhaID = 1;
    ```

## Jogador

-   Ver todos os atributos de um jogador específico:
    ```sql
    SELECT idJogador, idHabilidade, idMapa, IlhaID, Energia, Vida, Nivel, Sorte, VidaAtual, DanoBase, ExperienciaAtual, CoordenadaX, CoordenadaY
    FROM Jogador
    WHERE idJogador = 1;
    ```

-   Ver atributos de combate (Vida, Nível, Dano Base) de um jogador específico:
    ```sql
    SELECT Vida, Nivel, DanoBase
    FROM Jogador
    WHERE idJogador = 1;
    ```

## Chefe

-   Ver todos os atributos de um chefe específico:
    ```sql
    SELECT idChefe, idHabilidade, idMapa, IlhaID, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo
    FROM Chefe
    WHERE idChefe = 5;
    ```

-   Ver nome, vida e nível de um chefe específico:
    ```sql
    SELECT Nome, Vida, Nivel
    FROM Chefe
    WHERE idChefe = 6;
    ```

-   Ver quais chefes pertencem a um tipo de inimigo específico:
    ```sql
    SELECT idChefe, Nome, Nivel
    FROM Chefe
    WHERE TipoInimigo = 'Humanoide';
    ```

## Missão

-   Ver todos os atributos de uma missão específica:
    ```sql
    SELECT MissaoID, MapaID, IlhaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome
    FROM Missão
    WHERE MissaoID = 12;
    ```

-   Buscar missões por nome (parcial ou completo):
    ```sql
    SELECT MissaoID, Nome, Descricao
    FROM Missão
    WHERE Nome LIKE '%Fera%';
    ```

-   Ver missões atribuídas por um recrutador específico (Habitante):
    ```sql
    SELECT m.MissaoID, m.Nome, h.nome AS NomeRecrutador
    FROM Missão m
    JOIN Habitante h ON m.idRecrutador = h.identificador_habitante
    WHERE h.identificador_habitante = 2;
    ```

-   Ver missões com recrutador que é um Chefe:
    ```sql
    SELECT m.Nome AS NomeMissao, m.Descricao, c.Nome AS NomeRecrutadorChefe
    FROM Missão m
    JOIN Chefe c ON m.idRecrutador = c.idChefe
    WHERE m.idRecrutador IN (7, 9);
    ```

-   Ver missões associadas a um tipo de sala específico (Ex: Campo de Batalha):
    ```sql
    SELECT m.Nome AS NomeMissao, m.Descricao, cb.Nome AS NomeLocal
    FROM Missão m
    JOIN Campo_de_batalha cb ON m.SalaID = cb.SalaID AND m.TipoSala = cb.TipoSala
    WHERE m.TipoSala = 'Campo de Batalha';
    ```

## Campo_de_batalha

-   Ver todos os atributos de um campo de batalha específico:
    ```sql
    SELECT SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos
    FROM Campo_de_batalha
    WHERE SalaID = 201;
    ```

-   Ver campos de batalha de um tipo ambiental específico (Ex: Floresta):
    ```sql
    SELECT SalaID, Nome, Tipo, QtdInimigos
    FROM Campo_de_batalha
    WHERE Tipo = 'Floresta';
    ```

## Vila

-   Ver todos os atributos de uma vila específica:
    ```sql
    SELECT SalaID, TipoSala, Nome, TotalSalas, Informacoes
    FROM Vila
    WHERE SalaID = 101;
    ```

-   Ver informações de todas as vilas cadastradas:
    ```sql
    SELECT Nome, Informacoes
    FROM Vila;
    ```

## Porto

-   Ver todos os atributos de um porto específico:
    ```sql
    SELECT SalaID, TipoSala, Nome, TotalSalas, QtdBarcos, Capacidade, SentidoIlha
    FROM Porto
    WHERE SalaID = 301;
    ```

-   Ver portos que possuem mais de um determinado número de barcos:
    ```sql
    SELECT Nome, QtdBarcos, Capacidade
    FROM Porto
    WHERE QtdBarcos > 3;
    ```

## Item

-   Ver todos os atributos de um item específico:
    ```sql
    SELECT ItemID, Nome, Descricao, Tipo
    FROM Item
    WHERE ItemID = 11;
    ```

-   Ver todos os itens de um tipo específico (Ex: Fruta):
    ```sql
    SELECT Nome, Descricao
    FROM Item
    WHERE Tipo = 'Fruta';
    ```

## ItemMissão

-   Ver todos os itens associados a uma missão específica:
    ```sql
    SELECT im.IdentificadorItem, ti.Tipo AS TipoItem, i.Nome AS NomeItem, i.Descricao AS DescricaoItem
    FROM ItemMissão im
    JOIN Item i ON im.IdentificadorItem = i.ItemID
    JOIN TipoItem ti ON i.Tipo = ti.Tipo
    WHERE im.MissaoID = 12;
    ```

-   Ver todas as missões que contêm um item específico:
    ```sql
    SELECT im.MissaoID, m.Nome AS NomeMissao, m.Descricao AS DescricaoMissao
    FROM ItemMissão im
    JOIN Missão m ON im.MissaoID = m.MissaoID
    WHERE im.IdentificadorItem = 11;
    ```

## Mar

-   Ver todos os atributos de um mar específico:
    ```sql
    SELECT MarID, Mostro, Obstaculo
    FROM Mar
    WHERE MarID = 1;
    ```

-   Ver mares com um tipo de monstro específico:
    ```sql
    SELECT MarID, Mostro
    FROM Mar
    WHERE Mostro LIKE '%Serpente%';
    ```

## Corredor_maritimo

-   Ver todos os atributos de um corredor marítimo específico:
    ```sql
    SELECT marítimoID, IlhaA, IlhaB
    FROM Corredor_maritimo
    WHERE marítimoID = 1;
    ```

-   Ver nomes das ilhas de um corredor marítimo específico:
    ```sql
    SELECT c.marítimoID, ia.Nome AS NomeIlhaA, ib.Nome AS NomeIlhaB
    FROM Corredor_maritimo c
    JOIN Ilha ia ON c.IlhaA = ia.ID
    JOIN Ilha ib ON c.IlhaB = ib.ID
    WHERE c.marítimoID = 1;
    ```

## MapaMar

-   Ver todos os atributos de uma entrada em MapaMar:
    ```sql
    SELECT MapaID, IlhaID, MarID
    FROM MapaMar
    WHERE MapaID = 1 AND IlhaID = 1;
    ```

-   Ver detalhes de Mapa, Ilha e Mar associados em MapaMar:
    ```sql
    SELECT mm.MapaID, mm.IlhaID, m.Nome AS NomeMapa, i.Nome AS NomeIlha, mar.Mostro
    FROM MapaMar mm
    JOIN Mapa m ON mm.MapaID = m.MapaID AND mm.IlhaID = m.IlhaID
    JOIN Ilha i ON m.IlhaID = i.ID
    JOIN Mar mar ON mm.MarID = mar.MarID
    WHERE mm.MarID = 1;
    ```

## Controller_mar

-   Ver todos os atributos de uma entrada em Controller_mar:
    ```sql
    SELECT marítimoID, MarID
    FROM Controller_mar
    WHERE marítimoID = 1;
    ```

-   Ver detalhes de corredor marítimo e mar associados em Controller_mar:
    ```sql
    SELECT cm.marítimoID, cm.MarID, cor.IlhaA, mar.Mostro
    FROM Controller_mar cm
    JOIN Corredor_maritimo cor ON cm.marítimoID = cor.marítimoID
    JOIN Mar mar ON cm.MarID = mar.MarID
    WHERE cm.marítimoID = 1;
    ```

## Barco

-   Ver todos os atributos de um barco específico (por Tipo):
    ```sql
    SELECT Tipo, Melhoria, Nome, Nivel
    FROM Barco
    WHERE Tipo = 'Canoa';
    ```

-   Ver barcos com nível acima de N:
    ```sql
    SELECT Tipo, Nome, Nivel
    FROM Barco
    WHERE Nivel > 5;
    ```

## BarcoPorto

-   Ver todos os atributos de uma entrada em BarcoPorto:
    ```sql
    SELECT TipoSala, TipoBarco, SalaID
    FROM BarcoPorto
    WHERE SalaID = 301;
    ```

-   Ver detalhes de porto e barco associados em BarcoPorto:
    ```sql
    SELECT bp.TipoSala, bp.SalaID, p.Nome AS NomePorto, b.Nome AS NomeBarco, b.Nivel AS NivelBarco
    FROM BarcoPorto bp
    JOIN Porto p ON bp.TipoSala = p.TipoSala AND bp.SalaID = p.SalaID
    JOIN Barco b ON bp.TipoBarco = b.Tipo
    WHERE bp.TipoBarco = 'Canoa';
    ```

## Controller_barco

-   Ver todos os atributos de uma entrada em Controller_barco:
    ```sql
    SELECT IDBarco, marítimoID
    FROM Controller_barco
    WHERE IDBarco = 'Canoa';
    ```

-   Ver detalhes de barco e corredor marítimo associados em Controller_barco:
    ```sql
    SELECT cb.IDBarco, cb.marítimoID, b.Nome AS NomeBarco, cm.IlhaA AS CorredorIlhaA
    FROM Controller_barco cb
    JOIN Barco b ON cb.IDBarco = b.Tipo
    JOIN Corredor_maritimo cm ON cb.marítimoID = cm.marítimoID
    WHERE cb.IDBarco = 'Canoa';
    ```


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
