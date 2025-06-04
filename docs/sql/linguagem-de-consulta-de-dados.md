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
