# Linguagem de Manipulação de Dados (DML)

## Introdução

A Linguagem de Manipulação de Dados (DML) é um subconjunto de linguagens de banco de dados usado para **recuperar, inserir, excluir e modificar informações** em um banco de dados. É um componente essencial dos Sistemas de Gerenciamento de Banco de Dados (SGBDs). Ela permite que os usuários realizem as operações mais comuns e fundamentais em um banco de dados: a consulta e a modificação dos dados. Diferentemente da Linguagem de Definição de Dados (DDL), que se preocupa com a estrutura e o esquema do banco de dados, a DML foca no conteúdo.

As operações DML são geralmente executadas usando comandos específicos que são parte de uma linguagem de consulta mais ampla, como SQL (*Structured Query Language*). Esses comandos são o coração da interação diária com qualquer banco de dados relacional.

Os principais comandos DML incluem:

* `SELECT`: Usado para consultar e recuperar dados das tabelas do banco de dados.
* `INSERT`: Usado para adicionar novas linhas (registros) a uma tabela.
* `UPDATE`: Usado para modificar os dados existentes em uma ou mais linhas de uma tabela.
* `DELETE`: Usado para remover linhas de uma tabela.

Compreender a DML é crucial para desenvolvedores, analistas de dados, administradores de banco de dados e qualquer pessoa que precise interagir com dados armazenados de forma estruturada. 

---

## Metodologia

O aprendizado e a utilização da Linguagem de Manipulação de Dados (DML) geralmente seguem uma abordagem prática e incremental. A metodologia pode ser dividida nas seguintes etapas:

1.  **Compreensão dos Conceitos Fundamentais**:
    * Entender o que é um banco de dados relacional e seus componentes (tabelas, colunas, linhas, chaves primárias e estrangeiras).
    * Diferenciar DML de outras linguagens de banco de dados como DDL (*Data Definition Language*) e DCL (*Data Control Language*).

2.  **Aprendizado dos Comandos Básicos**:
    * **`SELECT`**: Iniciar com consultas simples para recuperar todas as colunas ou colunas específicas de uma tabela. Aprender a usar a cláusula `WHERE` para filtrar registros com base em condições.
    * **`INSERT`**: Praticar a inserção de novos registros em tabelas, especificando valores para todas as colunas ou um subconjunto delas.
    * **`UPDATE`**: Aprender a modificar registros existentes, utilizando a cláusula `WHERE` para especificar quais registros devem ser atualizados e a cláusula `SET` para definir os novos valores.
    * **`DELETE`**: Entender como remover registros de uma tabela, usando a cláusula `WHERE` para evitar a exclusão acidental de todos os dados. 

3.  **Prática com Exercícios e Projetos**:
    * Resolver problemas práticos que envolvam a criação de cenários e a manipulação de dados para atender a requisitos específicos.
    * Utilizar SGBDs reais (como MySQL, PostgreSQL, SQL Server, Oracle) para executar os comandos e observar os resultados. Ferramentas com interface gráfica (como DBeaver, pgAdmin, SQL Developer) podem auxiliar na visualização.
---

# DML - Linguagem de Manipulação de Dados



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
