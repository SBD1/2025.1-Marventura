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
          <td><code>identificador_acessorio</code></td>
          <td>Identificador único do acessório.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de item.</td>
          <td>Texto</td>
          <td>3</td>
          <td>"ace"</td>
          <td>-</td>
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
          <td>Default = 0 / Not NULL</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Caracter</td>
          <td>3</td>
          <td>★ (U+2605)</td>
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
          <td><code>identificador_arma</code></td>
          <td>Identificador único da arma.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de item.</td>
          <td>Texto</td>
          <td>3</td>
          <td>"arm"</td>
          <td>-</td>
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
          <td>Default = 0 / Not NULL</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Caracter</td>
          <td>3</td>
          <td>★ (U+2605)</td>
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
          <td><code>identificador_consumivel</code></td>
          <td>Identificador único do consumivel.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de item.</td>
          <td>Texto</td>
          <td>3</td>
          <td>"con"</td>
          <td>-</td>
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
          <td>Default = 0 / Not NULL</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Caracter</td>
          <td>3</td>
          <td>★ (U+2605)</td>
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
          <td><code>identificador_nao_consumivel</code></td>
          <td>Identificador único do não-consumível.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK, FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Identificador de tipo de item.</td>
          <td>Texto</td>
          <td>3</td>
          <td>"ncn"</td>
          <td>-</td>
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
          <td>Default = 0 / Not Null</td>
        </tr>
        <tr>
          <td><code>raridade</code></td>
          <td>Nível de raridade do item.</td>
          <td>Caracter</td>
          <td>3</td>
          <td>★ (U+2605)</td>
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
          <td>Identificador único do consumível gerado por essa receita.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Unique / Not NULL / CHECK</td>
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
          <td>100</td>
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

### Tabela: `habilidade`

<details>
  <summary>Tabela 7 – Dicionário de Dados da Entidade Habilidade
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 7 – Dicionário de Dados da Entidade Habilidade</strong></p>
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
          <td><code>dano</code></td>
          <td>Dano causado pela habilidade.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>&gt;= 0, &lt;= 15</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>custo</code></td>
          <td>Custo para usar a habilidade.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>&gt;= 0, &lt;= 4</td>
          <td>-</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `ingrediente_consumivel`

<details>
  <summary>Tabela 8 – Dicionário de Dados da Tabela Ingrediente Consumível
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 8 – Dicionário de Dados da Tabela Ingrediente Consumível</strong></p>
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
          <td>FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_consumivel</code></td>
          <td>Identificador único do consumível.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
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
  <summary>Tabela 9 – Dicionário de Dados da Tabela Ingrediente Não-Consumível
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 9 – Dicionário de Dados da Tabela Ingrediente Não-Consumível</strong></p>
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
          <td>FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_nao_consumivel</code></td>
          <td>Identificador único do não-consumível.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
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
  <summary>Tabela 10 – Dicionário de Dados da Tabela Efeito Acessório
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 10 – Dicionário de Dados da Tabela Efeito Acessório</strong></p>
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
          <td>FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_acessorio</code></td>
          <td>Identificador único do acessório.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
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
  <summary>Tabela 11 – Dicionário de Dados da Tabela Efeito Consumível
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 11 – Dicionário de Dados da Tabela Efeito Consumível</strong></p>
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
          <td>FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
        <tr>
          <td><code>identificador_consumivel</code></td>
          <td>Identificador único do consumível.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Unique / Not NULL / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/MatheusHenrickSantos">Matheus Henrick</a>.</p>
  </div>
</details>

---

### Tabela: `mapa`

<details>
  <summary>Tabela 12 – Dicionário de Dados da Entidade Mapa
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 12 – Dicionário de Dados da Entidade Mapa</strong></p>
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
          <td><code>id</code></td>
          <td>Identificador único do mapa.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do mapa.</td>
          <td>Texto</td>
          <td>100</td>
          <td>a-z, A-Z</td>
          <td>–</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/F1reFinger">Helder Lourenço</a></p>
  </div>
</details>


---

### Tabela `ilha`

<details>
  <summary>Tabela 13 – Dicionário de Dados da Entidade Ilha
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 13 – Dicionário de Dados da Entidade Ilha</strong></p>
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
          <td><code>id</code></td>
          <td>Identificador único da ilha.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome da ilha.</td>
          <td>Texto</td>
          <td>100</td>
          <td>a-z, A-Z</td>
          <td>–</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Tipo da ilha.</td>
          <td>Texto</td>
          <td>15</td>
          <td>"vulcânica", "deserta", etc.</td>
          <td>–</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>tamanho</code></td>
          <td>Tamanho da ilha.</td>
          <td>Inteiro</td>
          <td>2</td>
          <td>&ge; 1</td>
          <td>–</td>
          <td>Default = 1 / Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/F1reFinger">Helder Lourenço</a></p>
  </div>
</details>

---

### Tabela `barco`

<details>
  <summary>Tabela 14 – Dicionário de Dados da Entidade Barco
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <strong>Tabela 14 – Dicionário de Dados da Entidade Barco</strong>
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
          <td><code>id</code></td>
          <td>Identificador único do barco.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>nome</code></td>
          <td>Nome do barco.</td>
          <td>Texto</td>
          <td>50</td>
          <td>Letras</td>
          <td>–</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>velocidade</code></td>
          <td>Velocidade máxima.</td>
          <td>Decimal</td>
          <td>5</td>
          <td>&gt; 0</td>
          <td>–</td>
          <td>Default = 1.0 / Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/F1reFinger">Helder Lourenço</a></p>
  </div>
</details>

---

### Tabela `sala`

<details>
  <summary>Tabela 15 – Dicionário de Dados da Entidade Sala
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 15 – Dicionário de Dados da Entidade Sala</strong></p>
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
          <td><code>id</code></td>
          <td>Identificador único da sala.</td>
          <td>ID</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Unique / Not NULL</td>
        </tr>
        <tr>
          <td><code>ilha_id</code></td>
          <td>Ilha onde a sala está.</td>
          <td>FK</td>
          <td>6</td>
          <td>Padrão do tipo ID</td>
          <td>FK</td>
          <td>Not NULL</td>
        </tr>
        <tr>
          <td><code>tipo</code></td>
          <td>Tipo da sala.</td>
          <td>Texto</td>
          <td>50</td>
          <td>"normal", "tesouro", etc.</td>
          <td>–</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/F1reFinger">Helder Lourenço</a></p>
  </div>
</details>

---




## Convenções
- **Nomes de campos**: Devem ser escritos em `snake_case`.
- **Tipos de dados**: Devem seguir os padrões do banco de dados utilizado.
  - **Importante:** O tipo de dados "ID" será alfanumérico, composto por três números de 0 a 9 e três caracteres de 'a' a 'z'.
- **Tamanhos**: Representam o limite máximo de caracteres ou valores.



## 📚 Bibliografia

> SILBERSCHATZ, Abraham; KORTH, Henry F.; SUDARSHAN, S. Fundamentos de bases de datos. 5. ed. Madrid: McGraw-Hill España, 2006.



## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 29/04/2025 | - | - |
| `1.1` | Adição das tabelas referentes aos itens | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 02/05/2025 |
| `1.2` | Adição das tabelas referentes ao mapa | [Helder Lourenço](https://github.com/F1reFinger) | 02/05/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 02/05/2025 |
