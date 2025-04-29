# Dicionário de Dados

---

## Introdução

O dicionário de dados é uma ferramenta essencial no desenvolvimento de qualquer sistema que utilize persistência de informações, como é o caso de jogos digitais com componentes estruturados. Segundo *Silberschatz, Korth e Sudarshan (2006)*, o dicionário de dados é uma coleção de metadados — dados que descrevem outros dados — utilizada para registrar informações detalhadas sobre os elementos presentes no banco de dados, como nomes de atributos, tipos, restrições, relações entre tabelas e significados.

No contexto do jogo com tema One Piece, o dicionário de dados atua como uma base de referência para o design e a lógica do jogo. Ele descreve entidades fundamentais como `jogador`, `inimigo`, `item`, `mapa`, `missao`, entre outras, definindo seus atributos (ex.: Nome, vidaAtual, raridade), os tipos de dados (texto, inteiro, booleano), regras de negócio (valores permitidos, obrigatoriedade, unicidade) e interações possíveis entre elas.

Essa documentação garante que:

- O time de desenvolvimento implemente corretamente a estrutura do banco de dados;

- O design do jogo mantenha coerência nos elementos e atributos apresentados ao jogador;

- A equipe narrativa saiba quais dados estão disponíveis para enriquecer a história;

- E que futuras expansões ou manutenções no jogo sejam feitas com segurança e clareza.

Além disso, o dicionário ajuda a evitar inconsistências, facilita a integração entre diferentes partes do projeto e serve como referência técnica durante todo o ciclo de vida do jogo.

Assim, seguindo os princípios propostos por Silberschatz et al., o dicionário de dados no desenvolvimento deste jogo não é apenas um recurso de documentação, mas sim um instrumento estratégico para garantir a qualidade e escalabilidade do projeto.



## Metodologia

Para a elaboração do dicionário de dados do jogo **Marventura**, foi adotada uma abordagem colaborativa, com foco tanto na eficiência do desenvolvimento quanto no aprendizado individual e coletivo da equipe. A construção desse material seguiu uma sequência de etapas organizadas de forma participativa:

**1 - Modelagem Relacional:**  
O processo teve início já na criação do modelo relacional do banco de dados, no qual foram identificadas as entidades fundamentais para representar os elementos do jogo. Esse modelo serviu de base para compreender as relações e atributos essenciais do sistema.

**2 - Divisão das Entidades entre os Integrantes:**  
Em seguida, as entidades foram distribuídas entre os integrantes do grupo. Cada membro ficou responsável por uma ou mais tabelas derivadas do modelo relacional. Essa divisão teve como objetivo não apenas agilizar a produção, mas também promover o aprendizado prático de modelagem e documentação de dados, permitindo que cada integrante se aprofundasse em aspectos específicos da estrutura do banco.

**3 - Criação das Tabelas do Dicionário de Dados:**  
A partir das entidades designadas, cada integrante elaborou as tabelas correspondentes em formato *Markdown*, contendo os seguintes elementos para cada atributo:

- Nome do Atributo;

- Descrição;

- Tipo de Dados;

- Tamanho;

- Valores Permitidos;

- Chave (Primária ou Estrangeira);

- Outras Restrições (Not NULL, Unique, Default, etc.).

A adoção dessa metodologia possibilitou a construção de um dicionário de dados sólido e bem estruturado para **Marventura**, ao mesmo tempo em que reforçou o aprendizado dos conceitos de modelagem, normalização e documentação de banco de dados por parte de todos os envolvidos no projeto.



## Estrutura do Dicionário de Dados

As tabelas 1 a N a seguir representam o dicionário de dados do jogo **Marventura**, abrangendo todas as entidades e atributos definidos no modelo relacional.

### Tabela: `acessorio`

<details>
  <summary>Tabela 1 – Dicionário de Dados da Entidade Acessório
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 1 – Dicionário de Dados da Entidade Acessório</strong></p>
    <table>
      <thead>
        <tr>
          <th>Nome do Atributo</th>
          <th>Descrição</th>
          <th>Tipo de Dados</th>
          <th>Tamanho</th>
          <th>Valores Permitidos</th>
          <th>É chave?</th>
          <th>Outras Restrições</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>identificador</code></td>
          <td>Identificador único do acessório.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de item.</td>
          <td>Texto</td>
          <td>10</td>
          <td>"ace"</td>
          <td>PK</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do acessório.</td>
          <td>Texto</td>
          <td>100</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>quantidade</code></td>
          <td>Quantidade de cada item.</td>
          <td>Inteiro</td>
          <td>1</td>
          <td>&gt;= 0, &lt;= 1</td>
          <td>-</td>
          <td>Default = 0</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Numérico</td>
          <td>1</td>
          <td>1, 2, 3</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>preco_de_compra</code></td>
          <td>Valor gasto ao comprar o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>&gt;= 1, &lt;= 999</td>
          <td>-</td>
          <td>Default = 1 / Not NULL</td>
        </tr>
        <tr>
          <td><code>preco_de_venda</code></td>
          <td>Valor ganhado ao vender o item.</td>
          <td>-</td>
          <td>-</td>
          <td>NULL</td>
          <td>-</td>
          <td>-</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `arma`

<details>
  <summary>Tabela 2 – Dicionário de Dados da Entidade Arma
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 2 – Dicionário de Dados da Entidade Arma</strong></p>
    <table>
      <thead>
        <tr>
          <th>Nome do Atributo</th>
          <th>Descrição</th>
          <th>Tipo de Dados</th>
          <th>Tamanho</th>
          <th>Valores Permitidos</th>
          <th>É chave?</th>
          <th>Outras Restrições</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>identificador</code></td>
          <td>Identificador único da arma.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de item.</td>
          <td>Texto</td>
          <td>10</td>
          <td>"arm"</td>
          <td>PK</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome da arma.</td>
          <td>Texto</td>
          <td>100</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>quantidade</code></td>
          <td>Quantidade de cada item.</td>
          <td>Inteiro</td>
          <td>1</td>
          <td>&gt;= 0, &lt;= 1</td>
          <td>-</td>
          <td>Default = 0</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Numérico</td>
          <td>1</td>
          <td>1, 2, 3</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>preco_de_compra</code></td>
          <td>Valor gasto ao comprar o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>&gt;= 1, &lt;= 999</td>
          <td>-</td>
          <td>Default = 1 / Not NULL</td>
        </tr>
        <tr>
          <td><code>preco_de_venda</code></td>
          <td>Valor ganhado ao vender o item.</td>
          <td>-</td>
          <td>-</td>
          <td>NULL</td>
          <td>-</td>
          <td>-</td>
        </tr>
        <tr>
          <td><code>dano_da_arma</code></td>
          <td>Dano causado pela arma em pontos de vida.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>&gt;= 1, &lt;= 25</td>
          <td>-</td>
          <td>Default = 1 / Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `consumivel`

<details>
  <summary>Tabela 3 – Dicionário de Dados da Entidade Consumivel
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 3 – Dicionário de Dados da Entidade Consumivel</strong></p>
    <table>
      <thead>
        <tr>
          <th>Nome do Atributo</th>
          <th>Descrição</th>
          <th>Tipo de Dados</th>
          <th>Tamanho</th>
          <th>Valores Permitidos</th>
          <th>É chave?</th>
          <th>Outras Restrições</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>identificador</code></td>
          <td>Identificador único do consumivel.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de item.</td>
          <td>Texto</td>
          <td>10</td>
          <td>"con"</td>
          <td>PK</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do consumivel.</td>
          <td>Texto</td>
          <td>100</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>quantidade</code></td>
          <td>Quantidade de cada item.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>&gt;= 0, &lt;= 99</td>
          <td>-</td>
          <td>Default = 0</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Numérico</td>
          <td>1</td>
          <td>1, 2, 3</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>preco_de_compra</code></td>
          <td>Valor gasto ao comprar o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>&gt;= 1, &lt;= 999</td>
          <td>-</td>
          <td>Default = 1 / Not NULL</td>
        </tr>
        <tr>
          <td><code>preco_de_venda</code></td>
          <td>Valor ganhado ao vender o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>&gt;= 1, &lt;= 999</td>
          <td>-</td>
          <td>Default = 1 / Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `nao_consumivel`

<details>
  <summary>Tabela 4 – Dicionário de Dados da Entidade Não-Consumivel
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 4 – Dicionário de Dados da Entidade Não-Consumivel</strong></p>
    <table>
      <thead>
        <tr>
          <th>Nome do Atributo</th>
          <th>Descrição</th>
          <th>Tipo de Dados</th>
          <th>Tamanho</th>
          <th>Valores Permitidos</th>
          <th>É chave?</th>
          <th>Outras Restrições</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>identificador</code></td>
          <td>Identificador único do Não-Consumivel.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de item.</td>
          <td>Texto</td>
          <td>10</td>
          <td>"ncn"</td>
          <td>PK</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do Não-Consumivel.</td>
          <td>Texto</td>
          <td>100</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>quantidade</code></td>
          <td>Quantidade de cada item.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>&gt;= 0, &lt;= 99</td>
          <td>-</td>
          <td>Default = 0</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Numérico</td>
          <td>1</td>
          <td>1, 2, 3</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>preco_de_compra</code></td>
          <td>Valor gasto ao comprar o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>&gt;= 1, &lt;= 999</td>
          <td>-</td>
          <td>Default = 1 / Not NULL</td>
        </tr>
        <tr>
          <td><code>preco_de_venda</code></td>
          <td>Valor ganhado ao vender o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>&gt;= 1, &lt;= 999</td>
          <td>-</td>
          <td>Default = 1 / Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `receita`

<details>
  <summary>Tabela 5 – Dicionário de Dados da Entidade Receita
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 5 – Dicionário de Dados da Entidade Receita</strong></p>
    <table>
      <thead>
        <tr>
          <th>Nome do Atributo</th>
          <th>Descrição</th>
          <th>Tipo de Dados</th>
          <th>Tamanho</th>
          <th>Valores Permitidos</th>
          <th>É chave?</th>
          <th>Outras Restrições</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>identificador</code></td>
          <td>Identificador único da receita.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>id_consumivel</code></td>
          <td>Identificador único do consumível.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>FK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>id_não_consumivel</code></td>
          <td>Identificador único do não-consumível.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>FK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>quantidade</code></td>
          <td>Quantidade de cada item.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>&gt;= 0, &lt;= 99</td>
          <td>-</td>
          <td>Default = 0</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `efeito`

<details>
  <summary>Tabela 6 – Dicionário de Dados da Entidade Efeito
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 6 – Dicionário de Dados da Entidade Efeito</strong></p>
    <table>
      <thead>
        <tr>
          <th>Nome do Atributo</th>
          <th>Descrição</th>
          <th>Tipo de Dados</th>
          <th>Tamanho</th>
          <th>Valores Permitidos</th>
          <th>É chave?</th>
          <th>Outras Restrições</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>identificador</code></td>
          <td>Identificador único do efeito.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>id_acessório</code></td>
          <td>Identificador único do acessório.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>FK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>id_arma</code></td>
          <td>Identificador único da arma.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0-9</td>
          <td>FK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Tipo do efeito.</td>
          <td>Texto</td>
          <td>20</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>valor</code></td>
          <td>Valor do efeito.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>&gt;= 0, &lt;= 15</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---



## Convenções
- **Nomes de campos**: Devem ser escritos em `snake_case`.
- **Tipos de dados**: Devem seguir os padrões do banco de dados utilizado.
- **Tamanhos**: Representam o limite máximo de caracteres ou valores.



## 📚 Bibliografia

> SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. Fundamentos de bases de datos. 5. ed. Madrid: McGraw-Hill España, 2006.



## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 29/04/2025 |  |  |
