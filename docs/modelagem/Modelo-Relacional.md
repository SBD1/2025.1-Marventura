# Modelo Relacional

---

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

---

A **Figura 1** é uma junção de todos os diagramas relacionais apresentados nas figuras anteriores, integrando as entidades e relacionamentos dos itens do inventário, personagens, missões e mapas em uma única estrutura abrangente. Este diagrama relacional consolidado oferece uma visão completa do sistema de jogo, permitindo entender como todas as partes interagem entre si.
<details>
  <summary>Figura 1 – Diagrama Relacional final - Clique na imagem para melhor visualização
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
      <path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" />
    </svg>
  </summary>
  <div align="center">
    <p><strong>Figura 1 – Diagrama Relacional final</strong></p>
      <img src="https://raw.githubusercontent.com/SBD1/2025.1-Marventura/refs/heads/main/docs/assets/MLR.jpeg" alt="Modelo Logico Relacional">
      <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p>
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
| `2.2` | Adição do diagrama dos Personagens | [Israel Thalles](https://github.com/IsraelThalles) | 02/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 |
| `2.3` | Atualização do diagrama dos Itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 02/05/2025 |
| `2.4` | Adição do diagrama relacional final | [Pablo Serra](https://github.com/Pabloserrapxx) | 02/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 |
| `2.5` | Normalização do diagrama dos Personagens | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 16/06/2025 |
| `2.6` | Correção das restrições de chaves do diagrama dos Itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 16/06/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 17/06/2025 |
| `2.7` | Atualização do diagrama do Mapa | [Israel Thalles](https://github.com/IsraelThalles) | 17/06/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 19/06/2025 |
| `2.8` | Atualização do diagrama dos Itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 19/06/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 19/06/2025 |
| `2.9` | Atualização do diagrama dos personagens | [Israel Thalles](https://github.com/IsraelThalles) | 19/06/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 27/06/2025 |
| `2.10` | Atualização do diagrama dos Itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 27/06/2025 | - | - |
| `2.11` | Normalização do diagrama dos Itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 05/07/2025 |  |  |
| `3.0` | Novo Modelo Logico Relacional | [Diassis](https://github.com/Diaxiz) | 10/07/2025 |  |  |