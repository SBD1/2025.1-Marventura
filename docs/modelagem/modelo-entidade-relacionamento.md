# Modelo Entidade-Relacionamento

---

## Introdução

De acordo com **Silberschatz (2006, p.13)**, um *Modelo Entidade-Relacionamento (MER)* serve para delinear objetos do mundo real. Esses objetos são denominados *Entidades* e as associações existentes entre esses ojetos são denominadas *Relações*. Dessa forma, o conjunto de entidades é denominado *Conjunto de Entidades* e o conjunto das relações é denominado *Conjunto de Relacionamentos*.  

Cada entidade possui um *atributo* ou um conjunto de atributos que são usados para identificar as características dessa entidade.

Um *Diagrama Entidade-Relacionamento (DER)* é um esquema para representar graficamente um MER. Ele é composto por:  

- **Retângulos**: Representam os conjuntos de entidades;  
- **Elipses**: Representam os atributos;  
- **Losângos**: Representam o conjunto de relacionamento entre as entidades;  
- **Linhas**: Une os atributos às entidades e o conjunto de entidades aos relacionamentos;  
- **Triângulos**: Conjunto de relacionamentos do tipo generalização.

O conjunto de relacionamento pode ser também do tipo *generalização*. A generalização é um relacionamento que liga um conjunto de entidades de nível superior à um conjunto de entidades de nível inferior, que compartilham os atributos das entidades superiores. A generalização pode ser classificada de acordo com o tipo de restrição. Ela pode ser de (**Silberschatz (2006, p.194)**):  

- **Participação Total (T)**: Uma entidade de nível superior deve pertencer a pelo menos uma entidade de nível inferior;  
- **Participação Parcial (P)**: Uma entidade de nível superior pode não pertencer a nenhuma entidade de nível inferior.  

E também:  

- **Exclusivo (E)**: Onde a entidade de nível superior não pode pertence a mais de uma entidade de nível inferior;  
- **Sobreposição (S)**: Onde a entidade de nível superior pode pertence a várias entidades de nível inferior.  

Assim sendo, a generalização pode aparecer de quatro formas:  

- Total Exclusivo (T, E);
- Total Sobreposto (T, S);
- Parcial Exclusivo (P, E);
- Parcial Sobreposto (P, S).

E, por fim, "Agregação é uma abstração por meio da qual os relacionamentos são tratados como entidades de nível superior" **Silberschatz (2006, p.196)**. Ela é representada por uma caixa retangular que envolve os conjuntos de entidades e seus relacionamentos.



## Metodologia

Para o desenvolvimento do Modelo Entidade-Relacionamento (MER) do **Marventura**, foi necessário seguir uma abordagem estruturada que garantisse clareza e organização ao longo do processo. Inicialmente, foi realizado um estudo aprofundado sobre modelagem de dados e, mais especificamente, sobre o modelo entidade-relacionamento. Foram analisados conceitos fundamentais como entidades, relacionamentos, atributos, cardinalidade e normalização. Esse estudo permitiu definir uma base sólida para a construção de um modelo coerente e aderente às boas práticas de design de banco de dados.

Com o embasamento teórico estabelecido, foi iniciada a etapa de definição das características do jogo. Neste ponto, foram tomadas decisões importantes relacionadas ao contexto narrativo e mecânico do jogo, como o gênero, os personagens principais, ambientação e elementos-chave de jogabilidade. Esse direcionamento forneceu um norte para identificar quais entidades e relações seriam relevantes para o sistema do jogo.

Para facilitar tanto a visualização quanto a modelagem do MER, optou-se por dividir o modelo em temas. Essa divisão temática permitiu organizar o projeto em partes menores, cada uma representando um domínio específico do jogo, como personagens, itens, missões, localidades e progressão do jogador. Essa segmentação foi essencial para reduzir a complexidade visual do diagrama completo, além de ajudar a manter uma estrutura lógica e modular, facilitando futuras expansões e manutenções.

Essa abordagem incremental e organizada tornou possível construir um modelo claro, consistente e alinhado com os objetivos do jogo, ao mesmo tempo em que respeita os princípios da boa modelagem de dados.



## Diagrama Entidade-Relacionamento

A **Figura 1** abaixo apresenta o diagrama Entidade-Relacionamento pensado para representar os itens do inventário do jogador, que vão desde os itens equipáveis e não-equipáveis, como moedas (não-equipável) e espadas (equipável), ambos não consumíveis, e itens consumíveis, como os itens de recuperação de vida e energia.

<details>
  <summary>Figura 1 – Diagrama Entidade-Relacionamento dos Itens do Inventário
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 1 – Diagrama Entidade-Relacionamento dos Itens do Inventário</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/diagrama-entidade-relacionamento-item-v2.2.png?raw=true">
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

Os efeitos *Cura* e *Recuperação de energia* são aqueles obtidos através de itens consumíveis e são usados para recuperar os pontos que foram perdidos desses atributos, sem ultrapassar o máximo, enquanto os efeitos *Aumento de vida* e *Aumento de energia* são aplicáveis aos acessórios e servem para aumentar o limite máximo desses atributos. Ademais, *Ataque* e *Sorte* aplicam-se a ambos. Todos esses efeitos possuem três tipos: pequeno, médio e grande, que estão relacionados com as raridades ★, ★★ e ★★★, respectivamente, com excessão de *Sorte* que possui apenas um nível.

---

A **Figura 2** abaixo apresenta o diagrama Entidade-Relacionamento com foco nos personagens que abarca tanto o personagem jogável, que é o próprio jogador, quanto os personagens não-jogáveis, que são os inimigos e os habitantes.

<details>
  <summary>Figura 2 – Diagrama Entidade-Relacionamento dos Personagens
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 2 – Diagrama Entidade-Relacionamento dos Personagens</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/diagrama-entidade-relacionamento-personagem-v3.0.png?raw=true">
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

Nesse diagrama, é possível perceber que todos os tipos de personagens podem ou não ter um inventário de itens. Porém, esse inventário é útil apenas para o Jogador, os Inimigos (que funcionaria como os itens de queda) e os Vendedores (que funcionaria como o estoque). Os demais personagens não possuem um inventário de itens.

---

<details>
  <summary>Figura 3 – Diagrama Entidade-Relacionamento do Mapa
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 3 – Diagrama Entidade-Relacionamento do Mapa</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/diagrama-entidade-relacionamento-mapa-v1.0.png?raw=true">
    <p>Autor: <a href="https://github.com/F1reFinger">Helder Lourenço</a>.</p>
  </div>
</details>

---

A **Figura 4** apresenta o diagrama Entidade-Relacionamento com foco nas missões e elementos do cenário interativo. O jogador é a entidade central, sendo capaz de realizar diversas missões, as quais estão disponíveis em diferentes mapas. Durante o jogo, o jogador obtém itens por meio do relacionamento "Dropa", que associa os itens adquiridos a ele.

<details>
  <summary>Figura 4 – Diagrama Entidade-Relacionamento de missões
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 4 – Diagrama Entidade-Relacionamento de missões</strong></p>
    <img src="https://github.com/SBD1/2025.1-Marventura/blob/main/docs/assets/diagrama_missoesv1.0.png?raw=true">
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p>
  </div>
</details>

---

## 📚 Bibliografia

> SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. Fundamentos de bases de datos. 5. ed. Madrid: McGraw-Hill España, 2006.



## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 17/04/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 17/04/2025 |
| `1.1` | Atualização do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 24/04/2025 | - | - |
| `2.0` | Adição do diagrama de personagens | [Israel Thalles](https://github.com/IsraelThalles) | 23/04/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 23/04/2025 |
| `2.1` | Adição da versão 2.0 do diagrama de personagens | [Israel Thalles](https://github.com/IsraelThalles) | 26/04/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 26/04/2025 |
| `3.0` | Refatoração do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 26/04/2025 | [Pablo Serra](https://github.com/Pabloserrapxx) | 30/04/2025  |
| `3.1` | Correção dos atributos do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 30/04/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 30/04/2025 |
| `3.2` | Adicionado Diagrama Entidade-Relacionamento de Missoes | [Diassis](https://github.com/Diaxiz) | 30/04/2025 | [Pablo Serra](https://github.com/IsraelThalles), [Israel Thalles](https://github.com/IsraelThalles) | 01/05/2025 |
| `4.0` | Adição do diagrama do mapa | [Israel Thalles](https://github.com/IsraelThalles) | 01/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 01/05/2025 |
