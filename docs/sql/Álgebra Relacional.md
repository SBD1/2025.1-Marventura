<center>

#  Álgebra Relacional

---

## O que é?

</center>

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

*Compreender a Álgebra Relacional é crucial para cientistas da computação, arquitetos de banco de dados e qualquer pessoa que precise de um entendimento profundo de como os dados são manipulados em sistemas relacionais.*

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

<center>

## Jogador

</center>

**Buscar todas as informações de um jogador específico**  
$$
\sigma_{(\text{identificador\_jogador = 'jog001'})}(jogador)
$$

---

<center>

## Itens, Efeitos e Habilidades

</center>

### Receita

**Ver nome dos consumíveis produzidos por receitas**  
$$
A1 \leftarrow receita \bowtie_{(\text{consumivel\_produzido} = \text{identificador\_consumivel})} (consumivel)
$$
$$
Resultado \leftarrow \rho_{(\text{Receita}, \text{Nome})}(\pi_{(\text{identificador\_receita}, \text{nome})}(A1))
$$

---

<center>

## Mundo e Personagens

</center>

### Ilhas

**Buscar os dados da ilha atual do jogador**  
$$
A1 \leftarrow \sigma_{(\text{identificador\_jogador} = 'jog001')}(jogador)
$$
$$
A2 \leftarrow \pi_{(\text{identificador\_area})}(A1)
$$
$$
A3 \leftarrow \sigma_{(\text{identificador\_area} = A2)}(area)
$$
$$
A4 \leftarrow \pi_{(\text{identificador\_ilha})}(A3)
$$
$$
Resultado \leftarrow \sigma_{(\text{identificador\_ilha} = A4)}(ilha)
$$

**Buscar todas as ilhas conectadas à ilha atual**  
$$
A1 \leftarrow \sigma_{(\text{identificador\_ilha\_a} = 'ilh001')}(\text{conexao\_entre\_ilhas})
$$
$$
A2 \leftarrow \sigma_{(\text{identificador\_ilha\_b} = 'ilh001')}(\text{conexao\_entre\_ilhas})
$$
$$
A3 \leftarrow \pi_{(\text{identificador\_ilha})}(A1) \cup \pi_{(\text{identificador\_ilha})}(A2)
$$
$$
Resultado \leftarrow \sigma_{(\text{identificador\_ilha} \in A3)}(\text{ilha})
$$

---

### Áreas

**Buscar informações da área atual do jogador**  
$$
A1 \leftarrow \sigma_{(\text{identificador\_jogador} = 'jog001')}(jogador)
$$
$$
A2 \leftarrow \pi_{(\text{identificador\_area})}(A1)
$$
$$
A3 \leftarrow \sigma_{(\text{identificador\_area} = (A2))}(area)
$$
$$
Resultado \leftarrow \pi_{(nome, \text{tipo\_area}, \text{chave\_imagem\_fundo}, \text{chave\_imagem\_frente}, visitada)}(A3)
$$

**Buscar caminhos da área atual do jogador**  
$$
A1 \leftarrow \sigma_{(\text{identificador\_jogador} = 'jog001')}(jogador)
$$
$$
A2 \leftarrow \pi_{(\text{identificador\_area})}(A1)
$$
$$
A3 \leftarrow \sigma_{(\text{identificador\_area} = A2)}(caminho)
$$
$$
Resultado \leftarrow \pi_{(\text{tipo\_terreno}, x, y, largura, altura)}(A3)
$$

**Buscar todas as áreas conectadas com a área atual**  
$$
A1 \leftarrow \sigma_{(\text{identificador\_jogador = 'jog001'})}(jogador)
$$
$$
A2 \leftarrow \pi_{(\text{identificador\_area})}(A1)
$$
$$
A3 \leftarrow \sigma_{(\text{identificador\_area\_b} = A2)}(\text{conexao\_entre\_areas}) \bowtie_{(\text{identificador\_area} = \text{identificador\_area\_a})} (area)
$$
$$
A4 \leftarrow \sigma_{(\text{identificador\_area\_a} = A2)}(\text{conexao\_entre\_areas}) \bowtie_{(\text{identificador\_area} = \text{identificador\_area\_b})} (area)
$$
$$
Resultado \leftarrow A3 \cup A4
$$

**Buscar áreas interativas da área atual**  
$$
A1 \leftarrow \sigma_{(\text{identificador\_jogador} = 'jog001')}(jogador)
$$
$$
A2 \leftarrow \pi_{(\text{identificador\_area})}(A1)
$$
$$
A3 \leftarrow \sigma_{(\text{identificador\_area} = A2)}(\text{area\_interativa})
$$
$$
Resultado \leftarrow \pi_{(\text{identificador\_area\_interativa}, \text{chave\_imagem}, x, y, largura, altura)}(A3)
$$

**Buscar o porto de uma ilha específica**  
$$
A1 \leftarrow \sigma_{(\text{identificador\_ilha} = 'ilh001' \wedge \text{tipo\_area} = 'Porto')}(area)
$$
$$
Resultado \leftarrow \pi_{(\text{identificador\_area}, \text{identificador\_ilha}, nome, \text{tipo\_area}, \text{chave\_imagem\_fundo}, \text{chave\_imagem\_frente}, visitada)}(A1)
$$

---

### NPCs

**Buscar inimigos comuns da área atual do jogador (com seus itens e habilidades)**  
$$
L1 \leftarrow \sigma_{(\text{identificador\_jogador} = 'jog001')}(jogador)
$$
$$
L2 \leftarrow \pi_{(\text{identificador\_area})}(L1)
$$
$$
L3 \leftarrow \text{instancia\_lacaio} \bowtie_{(\text{identificador\_lacaio})} (lacaio)
$$
$$
L4 \leftarrow L3 \text{⟕} (\text{habilidade\_personagem} \bowtie habilidade)
$$
$$
L5 \leftarrow inventario \bowtie \text{item\_inventario} \bowtie \text{tipo\_item} \text{⟕} (consumivel \cup \text{nao\_consumivel})
$$
$$
Resultado \leftarrow \sigma_{(\text{instancia\_lacaio.identificador\_area} = \text{L2.identificador\_area})}(L4 \text{⟕} L5)
$$

---

<center>

## 📚 Bibliografia

</center>

- ELMASRI, R.; NAVATHE, S. B. *Sistemas de Banco de Dados*, 7ª ed.
- DATE, C. J. *An Introduction to Database Systems*, 8ª ed.
- SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. *Database System Concepts*, 7ª ed.
- [Oracle SQL Docs](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/index.html)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [SQL Server Docs](https://docs.microsoft.com/en-us/sql/sql-server/sql-server-documentation)

---

<center>

## 📑 Histórico de Versões

</center>


| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 16/06/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 29/06/2025 |
| `1.1` | Atualização da álgebra relacional | [Israel Thalles](https://github.com/IsraelThalles) | 29/06/2025 |  |  |
