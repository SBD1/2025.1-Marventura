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

## Pessoa

></center>

**Ver o tipo de uma pessoa**  
$$\pi_{tipo} (\sigma_{id=3}(Pessoa))$$

---

<center>

## Inventário

</center>

**Acessar o inventário de uma pessoa X e ver os atributos (pessoa, tamanho e inventario_ocupado)**  
$$\pi_{pessoa,tamanho,inventario\_ocupado} (\sigma_{pessoa=2}(Inventário))$$

**Ver os itens do inventário de uma pessoa X**  
$$\pi_{item,nome} (\sigma_{i.inventario = 2}(instancia\_item \bowtie (arma \cup ferramenta \cup comida \cup medicamento \cup utilizável)))$$

---

<center>

## Jogador

</center>

**Ver (habilidade_briga, vida e força) de um jogador X**  
>$$\pi_{habilidade\_briga,vida,força} (\sigma_{id=1}(Jogador))$$

---

<center>

##  Itens, Efeitos e Habilidades

</center>

###  Tipo de Item
**Ver todos os tipos de itens disponíveis**  
$$\pi_{identificador\_item, tipo}(tipo\_item)$$

**Contar quantos tipos de itens existem no total**  
$$\mathcal{G}_{\text{COUNT}(*)\rightarrow total\_de\_tipos}(tipo\_item)$$

---

###  Efeito

**Ver todos os efeitos e seus valores**  
$$\pi_{nome, valor}(efeito)$$

**Encontrar os 5 efeitos curativos mais fortes (que restauram PV)**  
$$\tau_{valor \text{ DESC}}(\sigma_{nome = 'Restaura PV'}(efeito))$$  


---

###  Consumível

**Ver todos os consumíveis que podem ser fabricados**  
$$\pi_{nome, raridade, preco\_venda, descricao}(\sigma_{e\_fabricavel = TRUE}(consumivel))$$

**Listar os 10 consumíveis mais caros para vender**  
$$\tau_{preco\_venda \text{ DESC}}(\pi_{nome, preco\_venda, raridade}(consumivel))$$

---

###  Não-Consumível

**Ver todos os itens não-consumíveis de raridade '★★'**  
$$\pi_{nome, tipo, preco\_venda, descricao}(\sigma_{raridade = '★★'}(nao\_consumivel))$$

**Calcular a margem de lucro (venda - compra) para itens que podem ser comprados**  
$$\pi_{nome, (preco\_de\_venda - preco\_de\_compra) \rightarrow margem\_de\_lucro}(\sigma_{preco\_de\_compra > 0}(nao\_consumivel))$$

---

### Habilidade

**Encontrar todas as habilidades que não custam energia (custo zero)**  
$$\pi_{nome, dano}(\sigma_{custo = 0}(habilidade))$$

**Listar habilidades pela sua "eficiência" (dano por ponto de custo)**  
$$\pi_{nome, dano, custo, (dano/custo) \rightarrow eficiencia}(\sigma_{custo > 0}(habilidade))$$

---

### Receita

**Ver todos os ingredientes para uma receita específica**  
$$
\begin{gather*}
\rho_{tipo\_ingrediente \rightarrow 'Consumível', nome\_ingrediente \rightarrow nome}(\pi_{nome}(\sigma_{id\_receita=3}(receita) \bowtie ingrediente\_consumivel \bowtie consumivel)) \\
\cup \\
\rho_{tipo\_ingrediente \rightarrow 'Não-Consumível', nome\_ingrediente \rightarrow nome}(\pi_{nome}(\sigma_{id\_receita=3}(receita) \bowtie ingrediente\_nao\_consumivel \bowtie nao\_consumivel))
\end{gather*}
$$

**Encontrar todas as receitas que usam um ingrediente específico**  
$$
\pi_{item\_produzido \leftarrow c.nome}((\sigma_{identificador\_nao\_consumivel=8}(ingrediente\_nao\_consumivel)) \bowtie_{identificador\_receita} receita \bowtie_{consumivel\_produzido=identificador\_consumivel} consumivel)
$$

---

<center>

## Mundo e Personagens

</center>

###  Mundo (Salas, Ilhas, Mapas)

**Encontrar campos de batalha em um tipo de terreno específico**  
$$\pi_{sala\_id, tipo\_terreno, tamanho}(\sigma_{tipo\_terreno = 'Floresta'}(campo\_batalha))$$

**Ver todas as ilhas que pertencem a um mapa específico**  
$$
\rho_{id\_da\_ilha \rightarrow id, id\_da\_sala\_base \rightarrow sala\_id}(\pi_{id, sala\_id}(\sigma_{id\_mapa=1}(mapa) \bowtie_{mapa.id\_ilha = ilha.id} ilha))
$$

---

### Jogador e Aliados

**Encontrar em qual mapa e ilha um determinado jogador está**  
$$\pi_{nome\_jogador \leftarrow nome, id\_mapa, id\_ilha}(\sigma_{id\_jogador=1}(jogador) \bowtie_{id\_mapa\_pk} mapa)$$

**Ver todas as habilidades de um aliado específico**  
$$
\pi_{nome\_aliado \leftarrow a.nome, nome\_habilidade \leftarrow h.nome, dano, custo}(\sigma_{a.nome='Shuan'}(aliado) \bowtie_{id\_aliado} habilidade\_aliado \bowtie_{id\_habilidade} habilidade)
$$

---

### NPCs (Chefes, Lacaios, Habitantes)

**Listar todos os NPCs em uma ilha específica**  
$$
\begin{gather*}
\rho_{tipo \rightarrow 'Chefe'}(\pi_{nome}(\sigma_{id\_mapa\_pk=1}(chefe))) \cup \rho_{tipo \rightarrow 'Lacaio'}(\pi_{nome}(\sigma_{id\_mapa\_pk=1}(lacaio))) \\
\cup \rho_{tipo \rightarrow 'Aliado'}(\pi_{nome}(\sigma_{id\_mapa\_pk=1}(aliado))) \cup \rho_{tipo \rightarrow 'Habitante'}(\pi_{nome}(\sigma_{id\_mapa\_pk=1}(habitante)))
\end{gather*}
$$

**Encontrar o chefe com a maior quantidade de vida**  
$$\tau_{vida \text{ DESC}}(\pi_{nome, vida, nivel}(chefe))$$ *(limitado ao primeiro)*

---

<center>

## Interações e Eventos

</center>

###  Batalha

**Ver um registro de batalhas, mostrando jogador e chefe**  
$$\pi_{id\_batalha, nome\_jogador \leftarrow j.nome, nome\_chefe \leftarrow c.nome}(batalha \bowtie_{id\_jogador} jogador \bowtie_{id\_chefe} chefe)$$

**Listar todos os lacaios que participaram de uma batalha específica**  
$$
\pi_{nome\_lacaio \leftarrow nome}((\sigma_{identificador\_batalha=1}(batalha\_instancia\_lacaio)) \bowtie_{identificador\_instancia\_lacaio=id\_instancia\_lacaio} instancia\_lacaio \bowtie_{identificador\_lacaio=id\_lacaio} lacaio)
$$

---

###  Missão

**Encontrar todas as missões dadas por um recrutador específico**  
$$\pi_{nome, descricao}(\sigma_{id\_recrutador=1}(missao))$$

**Encontrar todas as missões que requerem um item de um tipo específico**  
$$
\pi_{nome\_missao \leftarrow m.nome, tipo\_item\_necessario \leftarrow ti.tipo}((\sigma_{tipo='Fruta'}(tipo\_item)) \bowtie_{identificador\_item} ItemMissao \bowtie_{missao\_id} missao)
$$

---

### Negociação

**Ver o histórico de negociações de um jogador**  
$$
\pi_{id\_negociacao, tipo, tipo\_item, qtd, preco, vendedor \leftarrow v.nome}((\sigma_{id\_jogador=1}(jogador)) \bowtie_{id\_jogador} negociacao \bowtie_{id\_vendedor} habitante \bowtie_{id\_item} tipo\_item)
$$

---

### Inventário

**Ver o conteúdo do inventário de um jogador**  
$$
\pi_{id\_inventario, dono \leftarrow j.nome, tipo\_item \leftarrow ti.tipo}((\sigma_{id\_jogador=1}(jogador)) \bowtie_{id\_jogador} Inventario \bowtie_{id\_inventario} ItemInventario \bowtie_{id\_item} tipo\_item)
$$

---

<center>

##  Navegação

</center>

###  Mar e Rotas

**Ver para quais ilhas é possível navegar a partir de uma ilha específica**  
$$
\pi_{id\_origem \leftarrow ilha\_a.id, id\_destino \leftarrow ilha\_b.id}(\sigma_{ilha\_a=1}(corredor\_maritimo) \bowtie_{ilha\_a=id}(\rho_{ilha\_a}(ilha)) \bowtie_{ilha\_b=id}(\rho_{ilha\_b}(ilha)))
$$

**Ver os monstros e obstáculos de um mar que conecta duas ilhas**  
$$\pi_{ilha\_a, ilha\_b, monstro, obstaculo}(controlador\_mar \bowtie_{maritimo\_id} corredor\_maritimo \bowtie_{mar\_id} mar)$$

---

### Barcos

**Listar todos os barcos ancorados em um porto específico**  
$$\pi_{nome, tipo, melhoria}(\sigma_{sala\_id=16}(barco\_porto) \bowtie_{barco\_id} barco)$$

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

| Versão | Descrição           | Autor(es)                                              | Data de Produção | Revisor(es) | Data de Revisão |
|--------|---------------------|--------------------------------------------------------|------------------|-------------|-----------------|
| 1.0    | Criação do documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 16/06/2025       |             |                 |
