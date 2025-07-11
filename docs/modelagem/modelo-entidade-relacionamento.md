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

A **Figura 1** reúne todas as entidades e relacionamentos apresentados nos diagramas anteriores, compondo uma visão unificada do modelo de dados do jogo. Nela, é possível visualizar de forma integrada como os sistemas de inventário, personagens, mapa e missões se conectam, evidenciando a estrutura lógica que sustenta o funcionamento geral do jogo.


<details>
  <summary>Figura 1 – Diagrama Entidade-Relacionamento final - Clique na imagem para melhor visualização
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Figura 1 – Diagrama Entidade-Relacionamento final</strong></p>
    <a href="assets/diagrama-entidade-relacionamento-completo-v7.2.png" target="_blank">
      <img src="https://raw.githubusercontent.com/SBD1/2025.1-Marventura/refs/heads/main/docs/assets/mer.jpg" alt="Diagrama Entidade Relacionamento">
      <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p>
    </a>
  </div>
</details>

## 🌍 Ambiente e Mapa

O mundo de *Marventura* é composto por diversas ilhas interconectadas por mares exploráveis. Cada ilha possui áreas distintas, repletas de obstáculos, caminhos e zonas interativas que ampliam a imersão e os desafios do jogador. As conexões entre áreas e entre ilhas criam uma sensação contínua de exploração, permitindo ao jogador desvendar regiões secretas e retornar a locais anteriores com novas habilidades.

---

## 🧍 Personagens

O jogo conta com uma variedade de personagens, divididos entre jogáveis e não-jogáveis. O jogador é representado como um personagem com progressão própria, podendo adquirir itens, habilidades e participar de combates. Já os NPCs se subdividem em aliados, habitantes, chefes e lacaios, cada um com papéis únicos no enredo, como fornecer informações, atribuir missões ou servir como inimigos a serem enfrentados.

---

## 🎯 Missões

As missões são elementos centrais da narrativa e da progressão do jogador. Elas podem ser principais ou secundárias, e envolvem interações com NPCs, coleta de itens, exploração de áreas ou derrotar inimigos específicos. Cada missão pode recompensar o jogador com experiência, itens ou desbloqueio de novas áreas do mapa.

---

## 📖 História

A trama de *Marventura* gira em torno de um protagonista em busca de respostas sobre seu passado, navegando entre ilhas misteriosas e enfrentando forças que ameaçam o equilíbrio do arquipélago. Conforme o jogador avança, descobre fragmentos da história escondidos em áreas interativas, diálogos e eventos, construindo aos poucos a mitologia e o destino do mundo que habita.

---


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
| `3.2` | Adicionado Diagrama Entidade-Relacionamento de Missões | [Diassis](https://github.com/Diaxiz) | 30/04/2025 | [Pablo Serra](https://github.com/IsraelThalles), [Israel Thalles](https://github.com/IsraelThalles) | 01/05/2025 |
| `4.0` | Adição do diagrama do mapa | [Israel Thalles](https://github.com/IsraelThalles) | 01/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 01/05/2025 |
| `4.1` | Adição do diagrama Entidade-Relacionamento final | [Pablo Serra](https://github.com/Pabloserrapxx) | 02/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 23/05/2025 |
| `4.2` | Atualização do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 23/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 |
| `4.3` | Normalização do diagrama dos Personagens | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 16/06/2025 |
| `4.4` | Alteração do diagrama dos itens para um link incorporado | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 16/06/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 17/06/2025 |
| `4.5` | Atualização do diagrama do mapa | [Israel Thalles](https://github.com/IsraelThalles) | 17/06/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 19/06/2025 |
| `4.6` | Atualização do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 19/06/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 19/06/2025 |
| `4.7` | Atualização do diagrama dos personagens | [Israel Thalles](https://github.com/IsraelThalles) | 19/06/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 27/06/2025 |
| `4.8` | Atualização do diagrama dos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 27/06/2025 |  |  |
| `5.0` | Novo MER | [Diassis](https://github.com/Diaxiz) | 10/07/2025 |  |  |

