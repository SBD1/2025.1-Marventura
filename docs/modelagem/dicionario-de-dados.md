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

As tabelas 1 a 41 a seguir representam o dicionário de dados do jogo **Marventura**, abrangendo todas as entidades e atributos definidos no modelo relacional.

### Tabela: `aliado`

<details>
  <summary>Tabela – Dicionário de Dados da Tabela Aliado
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela – Dicionário de Dados da Tabela Aliado</strong></p>
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
          <td><code>id_aliado</code></td>
          <td>Identificador único do aliado.</td>
          <td>ID</td>
          <td></td>
          <td>Inteiros positivos</td>
          <td>PK</td>
          <td>Not NULL / Unique</td>
        </tr>
        <tr>
          <td><code>id_tipo_personagem</code></td>
          <td>Referência ao personagem do tipo aliado.</td>
          <td>ID</td>
          <td></td>
          <td>IDs da tabela Tipo_Personagem</td>
          <td>FK</td>
          <td>Not NULL</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---
### Tabela: `area`

<details>
  <summary>Tabela 02 – Dicionário de Dados da Tabela Area
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 02 – Dicionário de Dados da Tabela Area</strong></p>
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
          <td><code>id_area</code></td>
          <td>Identificador único da tabela area.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `area_interacao`

<details>
  <summary>Tabela 03 – Dicionário de Dados da Tabela Area_interacao
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 03 – Dicionário de Dados da Tabela Area_interacao</strong></p>
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
          <td><code>id_area_interacao</code></td>
          <td>Identificador único da tabela area_interacao.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `caminho`

<details>
  <summary>Tabela 04 – Dicionário de Dados da Tabela Caminho
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 04 – Dicionário de Dados da Tabela Caminho</strong></p>
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
          <td><code>id_caminho</code></td>
          <td>Identificador único da tabela caminho.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `chefe`

<details>
  <summary>Tabela 05 – Dicionário de Dados da Tabela Chefe
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 05 – Dicionário de Dados da Tabela Chefe</strong></p>
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
          <td><code>id_chefe</code></td>
          <td>Identificador único da tabela chefe.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `conexao_entre_areas`

<details>
  <summary>Tabela 06 – Dicionário de Dados da Tabela Conexao_entre_areas
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 06 – Dicionário de Dados da Tabela Conexao_entre_areas</strong></p>
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
          <td><code>id_conexao_entre_areas</code></td>
          <td>Identificador único da tabela conexao_entre_areas.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `conexao_entre_ilhas`

<details>
  <summary>Tabela 07 – Dicionário de Dados da Tabela Conexao_entre_ilhas
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 07 – Dicionário de Dados da Tabela Conexao_entre_ilhas</strong></p>
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
          <td><code>id_conexao_entre_ilhas</code></td>
          <td>Identificador único da tabela conexao_entre_ilhas.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `dialogo`

<details>
  <summary>Tabela 08 – Dicionário de Dados da Tabela Dialogo
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 08 – Dicionário de Dados da Tabela Dialogo</strong></p>
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
          <td><code>id_dialogo</code></td>
          <td>Identificador único da tabela dialogo.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `efeito`

<details>
  <summary>Tabela 09 – Dicionário de Dados da Tabela Efeito
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 09 – Dicionário de Dados da Tabela Efeito</strong></p>
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
          <td><code>id_efeito</code></td>
          <td>Identificador único da tabela efeito.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `estado_chefe`

<details>
  <summary>Tabela 10 – Dicionário de Dados da Tabela Estado_chefe
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 10 – Dicionário de Dados da Tabela Estado_chefe</strong></p>
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
          <td><code>id_estado_chefe</code></td>
          <td>Identificador único da tabela estado_chefe.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `estado_instancia_lacaio`

<details>
  <summary>Tabela 11 – Dicionário de Dados da Tabela Estado_instancia_lacaio
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 11 – Dicionário de Dados da Tabela Estado_instancia_lacaio</strong></p>
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
          <td><code>id_estado_instancia_lacaio</code></td>
          <td>Identificador único da tabela estado_instancia_lacaio.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `habilidade`

<details>
  <summary>Tabela 12 – Dicionário de Dados da Tabela Habilidade
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 12 – Dicionário de Dados da Tabela Habilidade</strong></p>
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
          <td><code>id_habilidade</code></td>
          <td>Identificador único da tabela habilidade.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `habilidade_personagem`

<details>
  <summary>Tabela 13 – Dicionário de Dados da Tabela Habilidade_personagem
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 13 – Dicionário de Dados da Tabela Habilidade_personagem</strong></p>
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
          <td><code>id_habilidade_personagem</code></td>
          <td>Identificador único da tabela habilidade_personagem.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `habitante`

<details>
  <summary>Tabela 14 – Dicionário de Dados da Tabela Habitante
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 14 – Dicionário de Dados da Tabela Habitante</strong></p>
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
          <td><code>id_habitante</code></td>
          <td>Identificador único da tabela habitante.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `ilha`

<details>
  <summary>Tabela 15 – Dicionário de Dados da Tabela Ilha
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 15 – Dicionário de Dados da Tabela Ilha</strong></p>
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
          <td><code>id_ilha</code></td>
          <td>Identificador único da tabela ilha.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `inimigo`

<details>
  <summary>Tabela 16 – Dicionário de Dados da Tabela Inimigo
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 16 – Dicionário de Dados da Tabela Inimigo</strong></p>
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
          <td><code>id_inimigo</code></td>
          <td>Identificador único da tabela inimigo.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `instancia_lacaio`

<details>
  <summary>Tabela 17 – Dicionário de Dados da Tabela Instancia_lacaio
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 17 – Dicionário de Dados da Tabela Instancia_lacaio</strong></p>
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
          <td><code>id_instancia_lacaio</code></td>
          <td>Identificador único da tabela instancia_lacaio.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `inventario`

<details>
  <summary>Tabela 18 – Dicionário de Dados da Tabela Inventario
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 18 – Dicionário de Dados da Tabela Inventario</strong></p>
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
          <td><code>id_inventario</code></td>
          <td>Identificador único da tabela inventario.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `jogador`

<details>
  <summary>Tabela 19 – Dicionário de Dados da Tabela Jogador
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 19 – Dicionário de Dados da Tabela Jogador</strong></p>
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
          <td><code>id_jogador</code></td>
          <td>Identificador único da tabela jogador.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `lacaio`

<details>
  <summary>Tabela 20 – Dicionário de Dados da Tabela Lacaio
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 20 – Dicionário de Dados da Tabela Lacaio</strong></p>
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
          <td><code>id_lacaio</code></td>
          <td>Identificador único da tabela lacaio.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `missao`

<details>
  <summary>Tabela 21 – Dicionário de Dados da Tabela Missao
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 21 – Dicionário de Dados da Tabela Missao</strong></p>
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
          <td><code>id_missao</code></td>
          <td>Identificador único da tabela missao.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `missao_item`

<details>
  <summary>Tabela 22 – Dicionário de Dados da Tabela Missao_item
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 22 – Dicionário de Dados da Tabela Missao_item</strong></p>
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
          <td><code>id_missao_item</code></td>
          <td>Identificador único da tabela missao_item.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `npc`

<details>
  <summary>Tabela 23 – Dicionário de Dados da Tabela Npc
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 23 – Dicionário de Dados da Tabela Npc</strong></p>
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
          <td><code>id_npc</code></td>
          <td>Identificador único da tabela npc.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `obstaculo`

<details>
  <summary>Tabela 24 – Dicionário de Dados da Tabela Obstaculo
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 24 – Dicionário de Dados da Tabela Obstaculo</strong></p>
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
          <td><code>id_obstaculo</code></td>
          <td>Identificador único da tabela obstaculo.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `personagem`

<details>
  <summary>Tabela 25 – Dicionário de Dados da Tabela Personagem
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 25 – Dicionário de Dados da Tabela Personagem</strong></p>
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
          <td><code>id_personagem</code></td>
          <td>Identificador único da tabela personagem.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `progresso`

<details>
  <summary>Tabela 26 – Dicionário de Dados da Tabela Progresso
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 26 – Dicionário de Dados da Tabela Progresso</strong></p>
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
          <td><code>id_progresso</code></td>
          <td>Identificador único da tabela progresso.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `recompensa_exploracao`

<details>
  <summary>Tabela 27 – Dicionário de Dados da Tabela Recompensa_exploracao
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 27 – Dicionário de Dados da Tabela Recompensa_exploracao</strong></p>
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
          <td><code>id_recompensa_exploracao</code></td>
          <td>Identificador único da tabela recompensa_exploracao.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `tipo_item`

<details>
  <summary>Tabela 28 – Dicionário de Dados da Tabela Tipo_item
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 28 – Dicionário de Dados da Tabela Tipo_item</strong></p>
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
          <td><code>id_tipo_item</code></td>
          <td>Identificador único da tabela tipo_item.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
  </div>
</details>

---

### Tabela: `tipo_personagem`

<details>
  <summary>Tabela 29 – Dicionário de Dados da Tabela Tipo_personagem
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" /></svg>
  </summary>
  <div align="center">
    <p><strong>Tabela 29 – Dicionário de Dados da Tabela Tipo_personagem</strong></p>
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
          <td><code>id_tipo_personagem</code></td>
          <td>Identificador único da tabela tipo_personagem.</td>
          <td>ID</td>
          <td></td>
          <td>Padrão do tipo ID</td>
          <td>PK</td>
          <td>Not NULL / Unique / CHECK</td>
        </tr>
      </tbody>
    </table>
    <p>Autor: <a href="https://github.com/Diaxiz">Diassis</a>.</p> 
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
| `1.11` | Atualização do dicionário dos personagens | [Israel Thalles](https://github.com/IsraelThalles) | 19/06/2025 |  |  |
| `1.12` | Novo dicionário de dados | [Diassis](https://github.com/Diaxiz) | 10/07/2025 |  |  |
