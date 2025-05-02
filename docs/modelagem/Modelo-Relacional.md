# Modelo Relacional

## Introdução

Dando continuidade ao processo de modelagem de dados iniciado com o Modelo Entidade-Relacionamento (MER) — conforme apresentado anteriormente, baseado nos conceitos de *Silberschatz (2006)* — avançamos agora para a construção do Modelo Relacional, que é uma representação mais detalhada e formal, adequada para implementação em sistemas de gerenciamento de banco de dados relacionais.

  De acordo com *C. J. Date (2004, p. 47)*, o Modelo Relacional é fundamentado na teoria dos conjuntos e na lógica de predicados, e organiza os dados em estruturas chamadas relações (ou tabelas). Cada relação contém um conjunto de tuplas (linhas) e atributos (colunas), onde:

 *   Cada atributo representa uma propriedade da entidade ou do relacionamento;
 *   Cada tupla representa uma instância individual dessa entidade;
 *   As chaves primárias garantem a unicidade dos registros;
 *   As chaves estrangeiras asseguram a integridade referencial entre tabelas.

O Modelo Relacional é amplamente utilizado por sua simplicidade, clareza e robustez, permitindo uma representação lógica do banco de dados que é independente da implementação física.

## Metodologia

Partindo do Modelo Entidade-Relacionamento (MER) previamente desenvolvido para o projeto Marventura — o qual foi elaborado com base em uma divisão temática e estruturada das entidades e relacionamentos mais relevantes do sistema — foi possível avançar para a construção do Modelo Relacional, mantendo a coerência estrutural e lógica da modelagem de dados.

Para realizar essa transição, foi adotada a abordagem teórica proposta por C. J. Date, que orienta a conversão sistemática de entidades e relacionamentos do MER em tabelas relacionais. Essa conversão seguiu os seguintes passos:

1.  Transformação de entidades em tabelas com seus respectivos atributos e definição da chave primária;
2.  Conversão de relacionamentos em chaves estrangeiras ou tabelas associativas, de acordo com a cardinalidade;
3.  Aplicação dos conceitos de normalização, a fim de evitar redundâncias e assegurar a integridade dos dados;

## Diagrama Modelo Relacional

A **Figura 1** abaixo apresenta o Diagrama relacional construído para representar a organização dos dados de um sistema de jogo, tendo a entidade missão como elemento central de conexão entre os demais componentes. Cada missão está associada a um Item, que pode ser necessário para completá-la, e a um Mapa, que define o local onde a missão ocorre. Além disso, a missão está diretamente ligada ao jogador, indicando quem a executa, e também ao `controller_missão`, responsável por agrupar ou organizar missões em conjuntos coerentes.

<details>
  <summary>Figura 1 – Diagrama Relacional das Missões
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 1 – Diagrama Relacional das Missões</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/modelo-relacional-missão-v1.0.png?raw=true">
    <p>Autor: <a href="https://github.com/Pabloserrapxx">Pablo Serra</a>.</p>
  </div>
</details>

---

<details>
  <summary>Figura 2 – Diagrama Relacional do Mapa
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 2 – Diagrama Relacional do Mapa</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/modelo-relacional-mapa-v1.0.png?raw=true">
    <p>Autor: <a href="https://github.com/F1reFinger">Helder Lourenço</a>.</p>
  </div>
</details>

---

A **Figura 3** abaixo apresenta o Diagrama Relacional com foque nos itens do inventário. Nela é possível observar que somente as entidades específicas apareceram, pois no *Diagrama Entidade-Relacionamento dos Itens do Inventário* a especialização para essas entidades é total e exclusiva. Note que os relacionamentos também foram modelados para as tabelas auxiliares `HabilidadeArma`, `HabilidadeFruta`, `IngredienteConsumível`, `IngredienteNãoConsumível`, `EfeitoAcessório` e `EfeitoConsumível`.

<details>
  <summary>Figura 3 – Diagrama Relacional dos Itens do Inventário
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 3 – Diagrama Relacional dos Itens do Inventário</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/modelo-relacional-item-v1.0.png?raw=true">
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---



## 📚 Bibliografia

>*   DATE, C. J. **Introdução a Sistemas de Bancos de Dados**. 8. ed. Rio de Janeiro: Campus, 2004.
>*   SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. **Fundamentos de bases de datos**. 5. ed. Madrid: McGraw-Hill España, 2006.


## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 17/04/2025 | [Diassis Bezerra](https://github.com/Diaxiz) | 20/04/2025 |
| `1.1` | Adição do diagrama das Missões | [Pablo Serra](https://github.com/Pabloserrapxx) | 30/04/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 30/04/2025 |
| `2.0` | Adição do diagrama do Mapa | [Israel Thalles](https://github.com/IsraelThalles) | 01/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 01/05/2025 |
| `2.1` | Adição do diagrama dos Itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 01/05/2025 | [Helder Lourenço](https://github.com/F1reFinger) | 01/05/2025 |
