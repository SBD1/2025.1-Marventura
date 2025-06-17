# Álgebra Relacional

## Introdução

A Álgebra Relacional é uma **linguagem de consulta processual** que fornece um conjunto de operações primitivas para manipular e recuperar dados em um banco de dados relacional. É a base teórica e o fundamento matemático do SQL (Structured Query Language). Ao contrário do SQL, que é uma linguagem declarativa (você descreve o que quer, e não como obtê-lo), a Álgebra Relacional descreve os **passos sequenciais** (o "como") para derivar um resultado a partir de relações existentes.

Ela opera sobre relações (que são visualmente representadas como tabelas) e produz novas relações como resultado. Isso significa que a saída de uma operação pode ser a entrada para outra, permitindo a construção de consultas complexas de forma modular.

A Álgebra Relacional é um componente essencial na otimização de consultas de SGBDs, pois os otimizadores convertem consultas SQL em planos de execução baseados em operações de Álgebra Relacional.

As operações fundamentais da Álgebra Relacional incluem:

* **Seleção ($\sigma$)**: Filtra tuplas (linhas) de uma relação que satisfazem uma condição.
* **Projeção ($\pi$)**: Seleciona colunas específicas (atributos) de uma relação, removendo duplicatas nas tuplas resultantes.
* **União ($\cup$)**: Combina tuplas de duas relações compatíveis (mesmo número e tipo de atributos), removendo duplicatas.
* **Interseção ($\cap$)**: Retorna tuplas que existem em ambas as relações compatíveis.
* **Diferença ($-$ )**: Retorna tuplas que existem na primeira relação, mas não na segunda relação compatível.
* **Produto Cartesiano ($\times$)**: Combina cada tupla de uma relação com cada tupla de outra, formando uma nova relação com todos os atributos de ambas.
* **Junção Natural ($\Join$)**: Combina tuplas de duas relações com base em atributos comuns de mesmo nome e domínio, eliminando colunas duplicadas.
* **Renomeação ($\rho$)**: Permite renomear uma relação ou seus atributos.

Compreender a Álgebra Relacional é crucial para cientistas da computação, arquitetos de banco de dados e qualquer pessoa que precise de um entendimento profundo de como os dados são manipulados em sistemas relacionais.

---

## Metodologia

O aprendizado e a utilização da Álgebra Relacional geralmente seguem uma abordagem teórica e prática, focando na lógica de manipulação de conjuntos de dados. A metodologia pode ser dividida nas seguintes etapas:

1.  **Compreensão dos Conceitos Fundamentais**:
    * Entender o que são relações, tuplas e atributos no contexto de um modelo relacional.
    * Diferenciar a natureza procedural da Álgebra Relacional da natureza declarativa de linguagens como SQL.
    * Familiarizar-se com os símbolos e notações padrão da Álgebra Relacional.

2.  **Aprendizado das Operações Básicas**:
    * Dominar cada uma das operações fundamentais (Seleção, Projeção, União, Interseção, Diferença, Produto Cartesiano, Junção Natural, Renomeação).
    * Entender as condições de compatibilidade de esquema para operações como União, Interseção e Diferença.
    * Praticar a aplicação de cada operação individualmente sobre relações de exemplo.

---

# Álgebra Relacional 


 

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
| `1.0` | Criação do documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 16/06/2025 |  |  |