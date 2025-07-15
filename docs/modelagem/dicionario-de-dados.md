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

- Tamanho (lógico);

- Valores Permitidos;

- Chave (Primária ou Estrangeira);

- Outras Restrições (Not NULL, Unique, Default, etc.).

A adoção dessa metodologia possibilitou a construção de um dicionário de dados sólido e bem estruturado para **Marventura**, ao mesmo tempo em que reforçou o aprendizado dos conceitos de modelagem, normalização e documentação de banco de dados por parte de todos os envolvidos no projeto.



## Convenções
- **Nomes de campos**: Devem ser escritos em `snake_case`.
- **Tipo ID:** O tipo de dados "ID" será uma composição única entre o tipo da tabela, com três letras, e um serial, com três dígitos. Exemplo: "ace005" representa o acessório número 5. Para tabelas que não possuírem o atributo tipo, poderá ser utilizado as três primeiras letras do nome da tabela.
- **Tipo Inteiro:** O tipo de dados "Inteiro" será sempre definido com o tipo `SMALLINT` da linguagem de consulta estruturada (SQL).
- **Tipo Texto:** O tipo de dados "Texto" sempre possuirá um tamanho fixo especificado, por isso será definido com o tipo `CHAR` da linguagem de consulta estruturada. NÃO SERÁ NECESSÁRIO O USO DO TIPO `VARCHAR` SOB HIPÓTESE ALGUMA.
- **Tipo Tempo:** O tipo de dados "Tempo" será sempre definido com o tipo `TIMESTAMP` da linguagem de consulta estruturada.
- **Tamanhos**: Representam o limite máximo de caracteres ou valores.



## Estrutura do Dicionário de Dados

As tabelas 1 a 46 a seguir representam o dicionário de dados do jogo **Marventura**, abrangendo todas as entidades e atributos definidos no modelo relacional.

### Tabela: `tipo_item`

<details>
  <summary>Tabela 1 – Dicionário de Dados da Tabela TipoItem
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 1 – Dicionário de Dados da Tabela TipoItem</strong></p>
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
          <td><code>identificador_item</code></td>
          <td>Identificador único do item.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de item.</td>
          <td>Texto</td>
          <td>3</td>
          <td>"ace", "arm", "fru", "con", "ncn"</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `acessorio`

<details>
  <summary>Tabela 2 – Dicionário de Dados da Tabela Acessório
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 2 – Dicionário de Dados da Tabela Acessório</strong></p>
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
          <td><code>identificador_acessorio</code></td>
          <td>Identificador único do acessório.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do acessório.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição do acessório.</td>
          <td>Texto</td>
          <td>150</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Caracter</td>
          <td>3</td>
          <td>★ (U+2605)</td>
          <td>-</td>
          <td>Default ★ / CHECK</td>
        </tr>
        <tr>
          <td><code>local_encontrado</code></td>
          <td>Local onde é possível encontrar o item.</td>
          <td>Texto</td>
          <td>18</td>
          <td>'Loja de Acessórios'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>preco_de_compra</code></td>
          <td>Valor gasto ao comprar o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>1 a 999</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `arma`

<details>
  <summary>Tabela 3 – Dicionário de Dados da Tabela Arma
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 3 – Dicionário de Dados da Tabela Arma</strong></p>
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
          <td><code>identificador_arma</code></td>
          <td>Identificador único da arma.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome da arma.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição da arma.</td>
          <td>Texto</td>
          <td>150</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Caracter</td>
          <td>3</td>
          <td>★ (U+2605)</td>
          <td>-</td>
          <td>Default ★ / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo_arma</code></td>
          <td>Indica se a arma é uma espada, um estilingue ou um arco.</td>
          <td>Texto</td>
          <td>3</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>local_encontrado</code></td>
          <td>Local onde é possível encontrar o item.</td>
          <td>Texto</td>
          <td>27</td>
          <td>'Loja de Espadas', 'Loja de Estilingues e Arcos'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>preco_de_compra</code></td>
          <td>Valor gasto ao comprar o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>1 a 999</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `fruta`

<details>
  <summary>Tabela 4 – Dicionário de Dados da Tabela Fruta
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 4 – Dicionário de Dados da Tabela Fruta</strong></p>
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
          <td><code>identificador_fruta</code></td>
          <td>Identificador único da fruta.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome da fruta.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição da fruta.</td>
          <td>Texto</td>
          <td>222</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Caracter</td>
          <td>3</td>
          <td>★ (U+2605)</td>
          <td>-</td>
          <td>Default ★ / CHECK</td>
        </tr>
        <tr>
          <td><code>local_encontrado</code></td>
          <td>Local onde é possível encontrar o item.</td>
          <td>Texto</td>
          <td>25</td>
          <td>'Missão', 'Evento'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>preco_de_venda</code></td>
          <td>Valor ganhado ao vender o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>1 a 999</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `consumivel`

<details>
  <summary>Tabela 5 – Dicionário de Dados da Tabela Consumivel
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 5 – Dicionário de Dados da Tabela Consumivel</strong></p>
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
          <td><code>identificador_consumivel</code></td>
          <td>Identificador único do consumivel.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do consumivel.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição do consumível.</td>
          <td>Texto</td>
          <td>200</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Caracter</td>
          <td>3</td>
          <td>★ (U+2605)</td>
          <td>-</td>
          <td>Default ★ / CHECK</td>
        </tr>
        <tr>
          <td><code>local_encontrado</code></td>
          <td>Local onde é possível encontrar o item.</td>
          <td>Texto</td>
          <td>25</td>
          <td>'Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57', 'Cozinha'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>preco_de_compra</code></td>
          <td>Valor gasto ao comprar o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>1 a 999</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>preco_de_venda</code></td>
          <td>Valor ganhado ao vender o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>1 a 999</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>e_fabricavel</code></td>
          <td>Indica se o item pode ser obtido através de receita.</td>
          <td>Boleano</td>
          <td>1</td>
          <td>TRUE, FALSE</td>
          <td>-</td>
          <td>Default FALSE</td>
        </tr>
        <tr>
          <td><code>e_coletado</code></td>
          <td>Indica se o item pode ser obtido através de exploração no mapa.</td>
          <td>Boleano</td>
          <td>1</td>
          <td>TRUE, FALSE</td>
          <td>-</td>
          <td>Default FALSE</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `nao_consumivel`

<details>
  <summary>Tabela 6 – Dicionário de Dados da Tabela Não-Consumivel
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 6 – Dicionário de Dados da Tabela Não-Consumivel</strong></p>
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
          <td><code>identificador_nao_consumivel</code></td>
          <td>Identificador único do não-consumível.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do Não-Consumivel.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição do não-consumível.</td>
          <td>Texto</td>
          <td>150</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Caracter</td>
          <td>3</td>
          <td>★ (U+2605)</td>
          <td>-</td>
          <td>Default ★ / CHECK</td>
        </tr>
        <tr>
          <td><code>local_encontrado</code></td>
          <td>Local onde é possível encontrar o item.</td>
          <td>Texto</td>
          <td>25</td>
          <td>'Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>preco_de_compra</code></td>
          <td>Valor gasto ao comprar o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>1 a 999</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>preco_de_venda</code></td>
          <td>Valor ganhado ao vender o item.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>1 a 999</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>e_coletado</code></td>
          <td>Indica se o item pode ser obtido através de exploração no mapa.</td>
          <td>Boleano</td>
          <td>1</td>
          <td>TRUE, FALSE</td>
          <td>-</td>
          <td>Default FALSE</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `receita`

<details>
  <summary>Tabela 7 – Dicionário de Dados da Tabela Receita
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 7 – Dicionário de Dados da Tabela Receita</strong></p>
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
          <td><code>identificador_receita</code></td>
          <td>Identificador único da receita.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>consumivel_produzido</code></td>
          <td>Chave estrangeira que identifica o consumível gerado pela receita.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `efeito`

<details>
  <summary>Tabela 8 – Dicionário de Dados da Tabela Efeito
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 8 – Dicionário de Dados da Tabela Efeito</strong></p>
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
          <td><code>identificador_efeito</code></td>
          <td>Identificador único do efeito.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do efeito.</td>
          <td>Texto</td>
          <td>15</td>
          <td>'Cura', 'Energia', 'Vida Máxima', 'Energia Máxima', 'Ataque', 'Sorte', 'Eletrificado', 'Congelado', 'Molhado', 'Envenenado', 'Sangramento', 'Queimadura', 'Tontura', 'Cegueira', 'Purificação'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>valor</code></td>
          <td>Valor do efeito.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>1 a 20, NULL</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `habilidade`

<details>
  <summary>Tabela 9 – Dicionário de Dados da Tabela Habilidade
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 9 – Dicionário de Dados da Tabela Habilidade</strong></p>
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
          <td><code>identificador_habilidade</code></td>
          <td>Identificador único da habilidade.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_efeito</code></td>
          <td>Identificador único do efeito.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>-</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome da habilidade.</td>
          <td>Texto</td>
          <td>25</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição da habilidade.</td>
          <td>Texto</td>
          <td>200</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>dano</code></td>
          <td>Dano causado pela habilidade.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>1 a 15</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>custo</code></td>
          <td>Custo para usar a habilidade.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>0 a 4</td>
          <td>-</td>
          <td>Default 0</td>
        </tr>
        <tr>
          <td><code>tipo_de_ataque</code></td>
          <td>Indica se é uma habilidade de soco, espada, estilingue, arco ou fruta.</td>
          <td>Texto</td>
          <td>10</td>
          <td>"fruta", "espada", "soco", "estilingue", "arco"</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo_de_alvo</code></td>
          <td>Indica a forma de atacar e a quantidade de alvos que a habilidade atinge.</td>
          <td>Texto</td>
          <td>15</td>
          <td>"fila", "alvo_terrestre", "terrestre", "alvo_livre", "area"</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `ingrediente_consumivel`

<details>
  <summary>Tabela 10 – Dicionário de Dados da Tabela Ingrediente Consumível
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 10 – Dicionário de Dados da Tabela Ingrediente Consumível</strong></p>
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
          <td><code>identificador_receita</code></td>
          <td>Identificador único da receita.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_consumivel</code></td>
          <td>Identificador único do consumível.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `ingrediente_nao_consumivel`

<details>
  <summary>Tabela 11 – Dicionário de Dados da Tabela Ingrediente Não-Consumível
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 11 – Dicionário de Dados da Tabela Ingrediente Não-Consumível</strong></p>
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
          <td><code>identificador_receita</code></td>
          <td>Identificador único da receita.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_nao_consumivel</code></td>
          <td>Identificador único do não-consumível.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `efeito_acessorio`

<details>
  <summary>Tabela 12 – Dicionário de Dados da Tabela Efeito Acessório
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 12 – Dicionário de Dados da Tabela Efeito Acessório</strong></p>
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
          <td><code>identificador_efeito</code></td>
          <td>Identificador único do efeito.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_acessorio</code></td>
          <td>Identificador único do acessório.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `efeito_consumivel`

<details>
  <summary>Tabela 13 – Dicionário de Dados da Tabela Efeito Consumível
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 13 – Dicionário de Dados da Tabela Efeito Consumível</strong></p>
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
          <td><code>identificador_efeito</code></td>
          <td>Identificador único do efeito.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_consumivel</code></td>
          <td>Identificador único do consumível.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `habilidade_arma`

<details>
  <summary>Tabela 14 – Dicionário de Dados da Tabela Habilidade Arma
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 14 – Dicionário de Dados da Tabela Habilidade Arma</strong></p>
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
          <td><code>identificador_habilidade</code></td>
          <td>Identificador único da habilidade.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_arma</code></td>
          <td>Identificador único da arma.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `habilidade_fruta`

<details>
  <summary>Tabela 15 – Dicionário de Dados da Tabela Habilidade Fruta
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 16 – Dicionário de Dados da Tabela Habilidade Fruta</strong></p>
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
          <td><code>identificador_habilidade</code></td>
          <td>Identificador único da habilidade.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_fruta</code></td>
          <td>Identificador único da fruta.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela `ilha`

<details>
  <summary>Tabela 16 – Dicionário de Dados da Tabela Ilha
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 16 – Dicionário de Dados da Tabela Ilha</strong></p>
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
          <td><code>identificador_ilha</code></td>
          <td>Identificador único da ilha.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome da ilha.</td>
          <td>Texto</td>
          <td>30</td>
          <td>'Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57'</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `conexao_entre_ilhas`

<details>
  <summary>Tabela 17 – Dicionário de Dados da Tabela Conexão Entre Ilhas
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <strong>Tabela 17 – Dicionário de Dados da Tabela Conexão Entre Ilhas</strong>
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
          <td><code>identificador_ilha_a</code></td>
          <td>Identificador único da ilha de origem.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_ilha_b</code></td>
          <td>Identificador único da ilha de destino.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_progresso</code></td>
          <td>Identificador único de progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>bloqueada</code></td>
          <td>Indica se a rota entre a ilha de origem e de destino está bloqueada.</td>
          <td>Boleano</td>
          <td>1</td>
          <td>True. False</td>
          <td>-</td>
          <td>DEFAULT True</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `area`

<details>
  <summary>Tabela 18 – Dicionário de Dados da Tabela Área
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 18 – Dicionário de Dados da Tabela Área</strong></p>
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
          <td><code>identificador_area</code></td>
          <td>Identificador único da área.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_ilha</code></td>
          <td>Identificador único da ilha a qual a área pertence.</td>
          <td>FK</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>tipo_area</code></td>
          <td>Identificador de tipo da área.</td>
          <td>Texto</td>
          <td>16</td>
          <td>"Área de combate", "Área neutra", "Vila", "Porto", "Loja", "Yomotsu Hirasaka"</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome da área.</td>
          <td>Texto</td>
          <td>30</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>chave_imagem_fundo</code></td>
          <td>Identificador da imagem de fundo da área.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, "_"</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>chave_imagem_frente</code></td>
          <td>Identificador da imagem de frente da área.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, "_"</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `conexao_entre_areas`

<details>
  <summary>Tabela 19 – Dicionário de Dados da Tabela Conexão Entre Áreas
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <strong>Tabela 19 – Dicionário de Dados da Tabela Conexão Entre Áreas</strong>
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
          <td><code>identificador_area_origem</code></td>
          <td>Identificador único da área de origem.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area_destino</code></td>
          <td>Identificador único da área de destino.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>ponto_geracao_x</code></td>
          <td>Ponto no eixo x para a local onde o jogador deverá aparecer ao mudar de área.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>1 a 5000</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>ponto_geracao_y</code></td>
          <td>Ponto no eixo y para a local onde o jogador deverá aparecer ao mudar de área.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>1 a 5000</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>orientacao</code></td>
          <td>Lado que o jogador está virado.</td>
          <td>Texto</td>
          <td>8</td>
          <td>'esquerda', 'direita'</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `tipo_elemento_espacial`

<details>
  <summary>Tabela 20 – Dicionário de Dados da Tabela Tipo Elemento Espacial
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 20 – Dicionário de Dados da Tabela Tipo Elemento Espacial</strong></p>
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
          <td><code>identificador_elemento_espacial</code></td>
          <td>Identificador único do elemento espacial.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo do elemento espacial.</td>
          <td>Texto</td>
          <td>3</td>
          <td>"ari", "obs", "cam"</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `obstaculo`

<details>
  <summary>Tabela 21 – Dicionário de Dados da Tabela Obstaculo
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 21 – Dicionário de Dados da Tabela Obstaculo</strong></p>
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
          <td><code>identificador_obstaculo</code></td>
          <td>Identificador único do obstáculo.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area</code></td>
          <td>Identificador da área onde o obstáculo está localizado.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>chave_imagem</code></td>
          <td>Identificador da imagem do obstáculo.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, "_"</td>
          <td>-</td>
          <td>-</td>
        </tr>
        <tr>
          <td><code>x</code></td>
          <td>Coordenada X do obstáculo.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>y</code></td>
          <td>Coordenada Y do obstáculo.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>largura</code></td>
          <td>Largura do obstáculo.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>altura</code></td>
          <td>Altura do obstáculo.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `area_interativa`

<details>
  <summary>Tabela 22 – Dicionário de Dados da Tabela Area Interativa
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 22 – Dicionário de Dados da Tabela Area Interativa</strong></p>
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
          <td><code>identificador_area_interativa</code></td>
          <td>Identificador único da área interativa.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area_origem</code></td>
          <td>Identificador da área onde a área interativa está localizado.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area_destino</code></td>
          <td>Identificador da área onde a área interativa irá levar</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_missao</code></td>
          <td>Identificador da missão acionada pela área interativa.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>chave_imagem</code></td>
          <td>Identificador da imagem da área interativa.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, "_"</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>x</code></td>
          <td>Coordenada X do obstáculo.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>y</code></td>
          <td>Coordenada Y do obstáculo.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>largura</code></td>
          <td>Largura do obstáculo.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>altura</code></td>
          <td>Altura do obstáculo.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>chance_sucesso</code></td>
          <td>Chance de obter recompensa ao interagir com o objeto.</td>
          <td>Decimal</td>
          <td>1</td>
          <td>0.0 a 1.0</td>
          <td>-</td>
          <td>DEFAULT 1.0 / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo_evento</code></td>
          <td>Tipo de evento ativado pela área.</td>
          <td>Texto</td>
          <td>10</td>
          <td>'embarcar', 'investigar', 'mudar_area', 'missao'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>metodo_ativacao</code></td>
          <td>Forma em que o evento associado à área é ativado.</td>
          <td>Texto</td>
          <td>7</td>
          <td>'ativo', 'passivo'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>ativa</code></td>
          <td>Indica se a área está ativa.</td>
          <td>Boleano</td>
          <td>1</td>
          <td>True, False</td>
          <td>-</td>
          <td>Not NULL / DEFAULT True</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `recompensa_de_exploração`

<details>
  <summary>Tabela 23 – Dicionário de Dados da Tabela Recompensa De Exploração
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 23 – Dicionário de Dados da Tabela Recompensa De Exploração</strong></p>
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
          <td><code>identificador_area_interativa</code></td>
          <td>Identificador da área interativa.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_jogador</code></td>
          <td>Identificador do jogador que interagiu com o objeto.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>data_da_tentativa</code></td>
          <td>A data da última tentativa de conseguir um item em uma área interativa específica.</td>
          <td>Tempo</td>
          <td>Tamanho de um <em>timestamp</em></td>
          <td>Padrão do tipo</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `progresso`

<details>
  <summary>Tabela 24 – Dicionário de Dados da Tabela Progresso
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 24 – Dicionário de Dados da Tabela Progresso</strong></p>
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
          <td><code>identificador_progresso</code></td>
          <td>Identificador do progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>numero_do_slot</code></td>
          <td>Número do espaço de salvamento.</td>
          <td>Inteiro</td>
          <td>1</td>
          <td>1 a 3</td>
          <td>-</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>data_ultimo_salvamento</code></td>
          <td>A data do último salvamento do progresso.</td>
          <td>Tempo</td>
          <td>Tamanho de um <em>timestamp</em></td>
          <td>Padrão do tipo</td>
          <td>-</td>
          <td>Not NULL / DEFAULT now( )</td>
        </tr>
        <tr>
          <td><code>ocupado</code></td>
          <td>Indica se o espaço já foi usado para salvar os dados.</td>
          <td>Boleano</td>
          <td>1</td>
          <td>True, False</td>
          <td>-</td>
          <td>Not NULL / DEFAULT FALSE</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela `barco`

<details>
  <summary>Tabela 25 – Dicionário de Dados da Tabela Barco
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 25 – Dicionário de Dados da Tabela Barco</strong></p>
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
          <td><code>identificador_barco</code></td>
          <td>Identificador único do barco.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_progresso</code></td>
          <td>Identificador do progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo_barco</code></td>
          <td>Identificador de tipo do barco.</td>
          <td>Texto</td>
          <td>3</td>
          <td>'can', 'vel', 'nav'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do barco.</td>
          <td>Texto</td>
          <td>30</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição do barco.</td>
          <td>Texto</td>
          <td>150</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>estado</code></td>
          <td>Estado do barco.</td>
          <td>Texto</td>
          <td>9</td>
          <td>'bloquedo', 'adquirido', 'destruido'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `jogador`

<details>
  <summary>Tabela 26 – Dicionário de Dados da Tabela Jogador
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 26 – Dicionário de Dados da Tabela Jogador</strong></p>
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
          <td><code>identificador_jogador</code></td>
          <td>Identificador único do jogador.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_progresso</code></td>
          <td>Identificador do progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area</code></td>
          <td>Identificador da área atual do jogador.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do jogador.</td>
          <td>Texto</td>
          <td>6</td>
          <td>"Silvie", "Shuan"</td>
          <td>-</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição do jogador.</td>
          <td>Texto</td>
          <td>300</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>energia</code></td>
          <td>Energia máxima do jogador.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>5 a 35</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>energia_atual</code></td>
          <td>Energia atual do jogador.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>5 a energia</td>
          <td>-</td>
          <td>DEFAULT 5 / CHECK (energia_atual <= energia)</td>
        </tr>
        <tr>
          <td><code>vida</code></td>
          <td>Vida máxima do jogador.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>10 a 70</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>nivel</code></td>
          <td>Nível atual do jogador.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>1 a 60</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>sorte</code></td>
          <td>Valor de sorte do jogador.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>1 a 10</td>
          <td>-</td>
          <td>DEFAULT 1 / CHECK</td>
        </tr>
        <tr>
          <td><code>vida_atual</code></td>
          <td>Vida atual do jogador.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0 a vida</td>
          <td>-</td>
          <td>CHECK (vida_atual <= vida)</td>
        </tr>
        <tr>
          <td><code>experiencia_atual</code></td>
          <td>Experiência atual acumulada pelo jogador.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 6000</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>moedas_totais</code></td>
          <td>Quantidade de moedas que o jogador possui.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0 a 999</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>coordenada_x</code></td>
          <td>Coordenada X atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>coordenada_y</code></td>
          <td>Coordenada Y atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `aliado`

<details>
  <summary>Tabela 27 – Dicionário de Dados da Tabela Aliado
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 27 – Dicionário de Dados da Tabela Aliado</strong></p>
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
          <td><code>identificador_aliado</code></td>
          <td>Identificador único do aliado.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area</code></td>
          <td>Identificador da área atual do aliado.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_progresso</code></td>
          <td>Identificador do progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do Aliado.</td>
          <td>Texto</td>
          <td>6</td>
          <td>"Silvie", "Shuan"</td>
          <td>-</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição do Aliado.</td>
          <td>Texto</td>
          <td>300</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>vida</code></td>
          <td>Vida máxima do aliado.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>10 a 70</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>nivel</code></td>
          <td>Nível atual do aliado.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>1 a 60</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>vida_atual</code></td>
          <td>Vida atual do aliado.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>0 a vida</td>
          <td>-</td>
          <td>CHECK (vida_atual <= vida)</td>
        </tr>
        <tr>
          <td><code>coordenada_x</code></td>
          <td>Coordenada X atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>coordenada_y</code></td>
          <td>Coordenada Y atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `habitante`

<details>
  <summary>Tabela 28 – Dicionário de Dados da Tabela Habitante
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 28 – Dicionário de Dados da Tabela Habitante</strong></p>
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
          <td><code>identificador_habitante</code></td>
          <td>Identificador único do habitante.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area</code></td>
          <td>Identificador da área atual do habitante.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do habitante.</td>
          <td>Texto</td>
          <td>27</td>
          <td>-a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição do habitante.</td>
          <td>Texto</td>
          <td>500</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>tipo_habitante</code></td>
          <td>Tipo de habitante.</td>
          <td>Texto</td>
          <td>3</td>
          <td>'hbt', 'ven', 'coz', 'rct'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>especialidade</code></td>
          <td>Tipo de item vendido pelo vendedor.</td>
          <td>Texto</td>
          <td>3</td>
          <td>"arm", "ace", "com"</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>moedas_totais</code></td>
          <td>Quantidade de moedas que o habitante possui.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0 a 999</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>chave_imagem</code></td>
          <td>Nome da chave da imagem do habitante.</td>
          <td>Texto</td>
          <td>50</td>
          <td>a-z, '_'</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>coordenada_x</code></td>
          <td>Coordenada X atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>coordenada_y</code></td>
          <td>Coordenada Y atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `lacaio`

<details>
  <summary>Tabela 29 – Dicionário de Dados da Tabela Lacaio
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 29 – Dicionário de Dados da Tabela Lacaio</strong></p>
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
          <td><code>identificador_lacaio</code></td>
          <td>Identificador único do lacaio.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do lacaio.</td>
          <td>Texto</td>
          <td>20</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição do lacaio.</td>
          <td>Texto</td>
          <td>100</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>vida</code></td>
          <td>Vida máxima do lacaio.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>8 a 70</td>
          <td>-</td>
          <td>-</td>
        </tr>
        <tr>
          <td><code>nivel</code></td>
          <td>Nível do lacaio.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>1 a 60</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>experiencia</code></td>
          <td>Experiência que o lacaio dá ao jogador ao ser derrotado.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>0 a 30</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>coordenada_x</code></td>
          <td>Coordenada X atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `chefe`

<details>
  <summary>Tabela 30 – Dicionário de Dados da Tabela Chefe
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 30 – Dicionário de Dados da Tabela Chefe</strong></p>
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
          <td><code>identificador_chefe</code></td>
          <td>Identificador único do chefe.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area</code></td>
          <td>Identificador da área atual do chefe.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do chefe.</td>
          <td>Texto</td>
          <td>28</td>
          <td>a-z, A-Z, '-'</td>
          <td>-</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>descricao</code></td>
          <td>Descrição do chefe.</td>
          <td>Texto</td>
          <td>100</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>vida</code></td>
          <td>Vida máxima do chefe.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>10 a 150</td>
          <td>-</td>
          <td>-</td>
        </tr>
        <tr>
          <td><code>nivel</code></td>
          <td>Nível do chefe.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>10 a 60</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>experiencia</code></td>
          <td>Experiência que o chefe dá ao jogador ao ser derrotado.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>0 a 30</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>coordenada_x</code></td>
          <td>Coordenada X atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>coordenada_y</code></td>
          <td>Coordenada Y atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `instancia_lacaio`

<details>
  <summary>Tabela 31 – Dicionário de Dados da Tabela Instancia Lacaio
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 31 – Dicionário de Dados da Tabela Instancia Lacaio</strong></p>
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
          <td><code>identificador_instancia_lacaio</code></td>
          <td>Identificador parcial único da instância de lacaio.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_lacaio</code></td>
          <td>Identificador do lacaio gerador da instância.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area</code></td>
          <td>Identificador da área atual da instância do lacaio.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>moedas_totais</code></td>
          <td>Quantidade de moedas que o habitante possui.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>0 a 999</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>coordenada_x</code></td>
          <td>Coordenada X atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>coordenada_y</code></td>
          <td>Coordenada Y atual no mapa.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `tipo_personagem`

<details>
  <summary>Tabela 32 – Dicionário de Dados da Tabela Tipo Personagem
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 32 – Dicionário de Dados da Tabela Tipo Personagem</strong></p>
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
          <td><code>identificador_personagem</code></td>
          <td>Identificador único do personagem.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de personagem.</td>
          <td>Texto</td>
          <td>3</td>
          <td>"hbt", "rct", "coz", "ven", "ali", "jog", "lac", "che"</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `inventario`

<details>
  <summary>Tabela 33 – Dicionário de Dados da Tabela Inventário
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 33 – Dicionário de Dados da Tabela Inventário</strong></p>
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
          <td><code>identificador_inventario</code></td>
          <td>Identificador parcial único do inventário.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_personagem</code></td>
          <td>Identificador do personagem que possui o inventário.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_progresso</code></td>
          <td>Identificador do progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo_inventario</code></td>
          <td>Identificador de tipo de inventário.</td>
          <td>Texto</td>
          <td>3</td>
          <td>"moc", "kit"</td>
          <td>-</td>
          <td>Not NULL / DEFAULT moc / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `item_inventario`

<details>
  <summary>Tabela 34 – Dicionário de Dados da Tabela Item Inventário
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 34 – Dicionário de Dados da Tabela Item Inventário</strong></p>
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
          <td><code>identificador_inventario</code></td>
          <td>Identificador único do inventário.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_item</code></td>
          <td>Identificador único do item.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>quantidade</code></td>
          <td>Quantidade do item no inventário.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>0 a 99</td>
          <td>-</td>
          <td>DEFAULT 0 / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `habilidade_personagem`

<details>
  <summary>Tabela 35 – Dicionário de Dados da Tabela Habilidade Personagem
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 35 – Dicionário de Dados da Tabela Habilidade Personagem</strong></p>
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
          <td><code>identificador_habilidade</code></td>
          <td>Identificador único da habilidade.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_personagem</code></td>
          <td>Identificador único do personagem.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `ilha_visitada`

<details>
  <summary>Tabela 36 – Dicionário de Dados da Tabela Ilha Visitada
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <strong>Tabela 36 – Dicionário de Dados da Tabela Ilha Visitada</strong>
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
          <td><code>identificador_ilha</code></td>
          <td>Identificador único da ilha.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_progresso</code></td>
          <td>Identificador único de progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>visitada</code></td>
          <td>Indica se a ilha já foi visitada.</td>
          <td>Boleano</td>
          <td>1</td>
          <td>True. False</td>
          <td>-</td>
          <td>Not NULL / DEFAULT False</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `receitas_conhecidas`

<details>
  <summary>Tabela 37 – Dicionário de Dados da Tabela Receitas Conhecidas
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 37 – Dicionário de Dados da Tabela Receitas Conhecidas</strong></p>
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
          <td><code>identificador_progresso</code></td>
          <td>Identificador do progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_receita</code></td>
          <td>Identificador único da receita.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `negociacao`

<details>
  <summary>Tabela 38 – Dicionário de Dados da Tabela Negociação
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 38 – Dicionário de Dados da Tabela Negociação</strong></p>
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
          <td><code>identificador_negociacao</code></td>
          <td>Identificador único do negociação.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_item</code></td>
          <td>Identificador único de item.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_jogador</code></td>
          <td>Identificador único de jogador.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_vendedor</code></td>
          <td>Identificador único de vendedor.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>quantidade</code></td>
          <td>Quantidade de cada item.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>0 a 99</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>preco_final</code></td>
          <td>Valor total gasto ao comprar uma quantia de itens.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>1 a 98901</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>tipo_negociacao</code></td>
          <td>Identificador de tipo de negociação.</td>
          <td>Texto</td>
          <td>6</td>
          <td>"compra", "venda</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela `area_visitada`

<details>
  <summary>Tabela 39 – Dicionário de Dados da Tabela Área Visitada
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <strong>Tabela 39 – Dicionário de Dados da Tabela Área Visitada</strong>
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
          <td><code>identificador_area</code></td>
          <td>Identificador único da área.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_progresso</code></td>
          <td>Identificador único de progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>visitada</code></td>
          <td>Indica se a área já foi visitada.</td>
          <td>Boleano</td>
          <td>1</td>
          <td>True. False</td>
          <td>-</td>
          <td>Not NULL / DEFAULT False</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `missao`

<details>
  <summary>Tabela 40 – Dicionário de Dados da Tabela Missão
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 40 – Dicionário de Dados da Tabela Missão</strong></p>
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
          <td><code>identificador_missao</code></td>
          <td>Identificador único da missão.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area</code></td>
          <td>Identificador único da área onde a missão ocorre.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
         <tr>
          <td><code>identificador_recrutador</code></td>
          <td>Identificador único do personagem que ofereceu a missão.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>CHECK</td>
        </tr>
         <tr>
          <td><code>identificador_missao_dependente</code></td>
          <td>Identificador único da próxima missão que depende dessa.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>CHECK</td>
        </tr>
         <tr>
          <td><code>descricao</code></td>
          <td>Texto descritivo detalhado dos objetivos e contexto da missão.</td>
          <td>Texto</td>
          <td>500</td>
          <td>a-z, A-Z</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
         <tr>
          <td><code>nome</code></td>
          <td>Nome ou título curto da missão.</td>
          <td>Texto</td>
          <td>100</td>
          <td>a-z, A-Z, 0-9</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
         <tr>
          <td><code>nivel_de_desbloqueio</code></td>
          <td>Nível necessário do jogador para desbloquear a missão.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>1 a 60</td>
          <td>-</td>
          <td>Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Pabloserrapxx">Pablo Serra</a>.</p> 
  </div>
</details>

---

### Tabela `caminho`

<details>
  <summary>Tabela 41 – Dicionário de Dados da Tabela Caminho
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 41 – Dicionário de Dados da Tabela Caminho</strong></p>
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
          <td><code>identificador_caminho</code></td>
          <td>Identificador único do caminho.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area</code></td>
          <td>Identificador da área onde o caminho está localizado.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo_terreno</code></td>
          <td>Identificador de tipo de terreno do caminho.</td>
          <td>Texto</td>
          <td>6</td>
          <td>"normal", "neve", "arena"</td>
          <td>-</td>
          <td>CHECK / DEFAULT "normal"</td>
        </tr>
        <tr>
          <td><code>x</code></td>
          <td>Coordenada X do caminho.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>y</code></td>
          <td>Coordenada Y do caminho.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>largura</code></td>
          <td>Largura do caminho.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>altura</code></td>
          <td>Altura do caminho.</td>
          <td>Inteiro</td>
          <td>4</td>
          <td>0 a 5000</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/IsraelThalles">Israel Thalles</a>.</p>
  </div>
</details>

---

### Tabela: `estado_instancia_lacaio`

<details>
  <summary>Tabela 42 – Dicionário de Dados da Tabela Estado Instancia Lacaio
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 42 – Dicionário de Dados da Tabela Estado Instancia Lacaio</strong></p>
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
          <td><code>identificador_progresso</code></td>
          <td>Identificador do progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_instancia_lacaio</code></td>
          <td>Identificador parcial único da instância de lacaio.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area_atual</code></td>
          <td>Identificador da área atual da instância do lacaio.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>vida_atual</code></td>
          <td>Vida atual do lacaio.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>8 a 70</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>data_da_morte</code></td>
          <td>A data e hora que o lacaio foi movido para o Yomotsu.</td>
          <td>Tempo</td>
          <td>Tamanho de um <em>timestamp</em></td>
          <td>Padrão do tipo</td>
          <td>-</td>
          <td>DEFAULT NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `estado_chefe`

<details>
  <summary>Tabela 43 – Dicionário de Dados da Tabela Estado Chefe
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 43 – Dicionário de Dados da Tabela Estado Chefe</strong></p>
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
          <td><code>identificador_progresso</code></td>
          <td>Identificador do progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_chefe</code></td>
          <td>Identificador parcial único do chefe.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_area_atual</code></td>
          <td>Identificador da área atual do chefe.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>vida_atual</code></td>
          <td>Vida atual do chefe.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>8 a 70</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>data_da_morte</code></td>
          <td>A data e hora que o chefe foi movido para o Yomotsu.</td>
          <td>Tempo</td>
          <td>Tamanho de um <em>timestamp</em></td>
          <td>Padrão do tipo</td>
          <td>-</td>
          <td>DEFAULT NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `dialogo`

<details>
  <summary>Tabela 44 – Dicionário de Dados da Tabela Diálogo
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 44 – Dicionário de Dados da Tabela Diálogo</strong></p>
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
          <td><code>identificador_dialogo</code></td>
          <td>Identificador do diálogo.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_personagem</code></td>
          <td>Identificador do personagem.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_missao</code></td>
          <td>Identificador da missão.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>sequencia_local</code></td>
          <td>Sequência usada para controlar a ordem dos diálogos em uma missão.</td>
          <td>Inteiro</td>
          <td>3</td>
          <td>Maior que 0</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>genero</code></td>
          <td>Caractere usado para definir o gênero das falas envolvendo o jogador.</td>
          <td>Caractere</td>
          <td>1</td>
          <td>'M', 'F'</td>
          <td>-</td>
          <td>CHECK</td>
        </tr>
        <tr>
          <td><code>dialogo</code></td>
          <td>Texto dos diálogos.</td>
          <td>Texto</td>
          <td>500</td>
          <td>Qualquer caracter</td>
          <td>-</td>
          <td>-</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `estado_missao`

<details>
  <summary>Tabela 45 – Dicionário de Dados da Tabela Estado Missão
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 45 – Dicionário de Dados da Tabela Estado Missão</strong></p>
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
          <td><code>identificador_progresso</code></td>
          <td>Identificador do progresso.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_missao</code></td>
          <td>Identificador da missão.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>estado</code></td>
          <td>Estado da missão.</td>
          <td>Texto</td>
          <td>9</td>
          <td>'concluida', 'aceita', 'pendente'</td>
          <td>-</td>
          <td>Not NULL / DEFAULT 'pendente' / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `item_missao`

<details>
  <summary>Tabela 46 – Dicionário de Dados da Tabela Item Missão
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 46 – Dicionário de Dados da Tabela Item Missão</strong></p>
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
          <td><code>identificador_item</code></td>
          <td>Identificador único do item.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_missao</code></td>
          <td>Identificador da missão.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>quantidade</code></td>
          <td>Quantidade do item recebido.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>1 a 99</td>
          <td>-</td>
          <td>DEFAULT 1 / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---



## 📚 Bibliografia

> SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. Fundamentos de bases de datos. 5. ed. Madrid: McGraw-Hill España, 2006.



## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 29/04/2025 | - | - |
| `1.1` | Adição das tabelas referentes aos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 02/05/2025 |
| `1.2` | Adição das tabelas referentes ao mapa | [Helder Lourenço](https://github.com/F1reFinger) | 02/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 |
| `1.3` | Adição das tabelas referentes aos personagens | [Israel Thalles](https://github.com/IsraelThalles) | 02/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 |
| `1.4` | Atualizando as restrições | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 | - | - |
| `1.5` | Adição das tabelas referentes a missão | [Pablo Serra](https://github.com/Pabloserrapxx) | 02/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 |
| `1.6` | Atualização das tabelas referentes aos itens e adição da tabela "fruta" | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 23/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 15/06/2025 |
| `1.7` | Atualização da seção de convenções e das tabelas referentes aos personagens | [Israel Thalles](https://github.com/IsraelThalles) | 15/06/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 16/06/2025 |
| `1.8` | Atualização das restrições e valores permitidos das tabelas referentes aos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 16/06/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 18/06/2025 |
| `1.9` | Atualização das tabelas referentes ao mapa | [Israel Thalles](https://github.com/IsraelThalles) | 18/06/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 19/06/2025 |
| `1.10` | Atualização dos valores dos atributos das tabelas referentes aos itens e criação da tabela TipoItem | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 19/06/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 19/06/2025 |
| `1.11` | Atualização do dicionário dos personagens | [Israel Thalles](https://github.com/IsraelThalles) | 19/06/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 15/07/2025 |
| `2.0` | Revisão e atualização do dicionário de dados para refletir o DDL | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 15/07/2025 |  |  |
