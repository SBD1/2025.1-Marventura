# Linguagem de Definição de Dados (DDL)

## Introdução

A **Linguagem de Definição de Dados (DDL - *Data Definition Language*)** é um componente fundamental dos Sistemas Gerenciadores de Banco de Dados (SGBDs). Ela compreende um conjunto de comandos SQL (*Structured Query Language*) utilizados para **definir, modificar e excluir a estrutura de um banco de dados e seus objetos**. Ao contrário da Linguagem de Manipulação de Dados (DML), que lida com os dados em si, a DDL foca na **esquematização** do banco de dados, estabelecendo as tabelas, índices, visões, procedimentos armazenados, funções, gatilhos, entre outros, e definindo suas características e relacionamentos.

Os comandos DDL são responsáveis por criar o esqueleto onde os dados serão armazenados. Eles permitem que os desenvolvedores e administradores de banco de dados especifiquem os **tipos de dados** para cada coluna, as **restrições de integridade** (como chaves primárias e estrangeiras, valores únicos, não nulos) e os **relacionamentos entre as tabelas**. A correta utilização da DDL é crucial para garantir a integridade, consistência e eficiência de um banco de dados, pois a estrutura definida influencia diretamente o desempenho das operações de manipulação de dados e a segurança das informações.

---

## Metodologia

Para a elaboração deste material sobre DDL, foram seguidas as seguintes etapas metodológicas:

Pesquisa Bibliográfica: Levantamento e estudo de livros, artigos e documentação oficial sobre SQL e DDL.

Estudo de Casos: Elaboração de exemplos práticos, simulando a criação e modificação de tabelas e outros objetos.

Revisão Técnica: Verificação e validação do conteúdo por especialistas em bancos de dados para garantir a precisão e atualidade das informações.

---

## DDL - Linguagem de Definição de Dados

</CENTER>
---

```sql
CREATE SEQUENCE global_numeric_id_sequence
    START WITH 1
    INCREMENT BY 1
    NO CYCLE;

CREATE TABLE tipo_item (
    identificador_item SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE efeito (
    identificador_efeito SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    bravura TEXT
);

CREATE TABLE habilidade (
    id_habilidade SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    dano INT CHECK (dano >= 0 AND dano <= 15) NOT NULL,
    custo INT CHECK (custo >= 0 AND custo <= 4) NOT NULL
);

CREATE TABLE tipo_personagem (
    id_personagem SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE campo_batalha (
    sala_id SERIAL PRIMARY KEY,
    tipo_terreno VARCHAR(50),
    qtd_de_pessoas INT,
    tamanho VARCHAR(50)
);

CREATE TABLE porto (
    sala_id SERIAL PRIMARY KEY,
    qtd_barcos INT,
    capacidade INT,
    sendo_ilha BOOLEAN
);

CREATE TABLE vila (
    sala_id SERIAL PRIMARY KEY,
    total_salas INT,
    informacoes TEXT
);

CREATE TABLE ilha (
    id SERIAL PRIMARY KEY,
    sala_id INT UNIQUE NOT NULL,
    tipo VARCHAR(50),
    tamanho VARCHAR(50),
    nome VARCHAR(100),
    quantidade_sala INT,
    FOREIGN KEY (sala_id) REFERENCES campo_batalha(sala_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE mapa (
    id_mapa INT NOT NULL,
    id_ilha INT NOT NULL,
    total_ilhas INT,
    total_item_chave INT,
    PRIMARY KEY (id_mapa, id_ilha),
    FOREIGN KEY (id_ilha) REFERENCES ilha(id)
);

CREATE TABLE consumivel (
    identificador_consumivel SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50) CHECK (raridade IN ('★', '★★', '★★★')),
    preco_compra DECIMAL(10, 2) NOT NULL,
    preco_venda DECIMAL(10, 2) NOT NULL,
    e_fabricavel BOOLEAN,
    FOREIGN KEY (tipo) REFERENCES tipo_item(tipo)
);

CREATE TABLE nao_consumivel (
    identificador_nao_consumivel SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50) CHECK (raridade IN ('★', '★★', '★★★')),
    preco_compra DECIMAL(10, 2) NOT NULL,
    preco_venda DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (tipo) REFERENCES tipo_item(tipo)
);

CREATE TABLE acessorio (
    identificador_acessorio INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50),
    preco_compra DECIMAL(10,2),
    preco_venda DECIMAL(10,2),
    FOREIGN KEY (identificador_acessorio) REFERENCES nao_consumivel(identificador_nao_consumivel)
);

CREATE TABLE arma (
    identificador_arma INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50),
    preco_compra DECIMAL(10,2),
    preco_venda DECIMAL(10,2),
    identificador_habilidade INT,
    FOREIGN KEY (identificador_arma) REFERENCES nao_consumivel(identificador_nao_consumivel),
    FOREIGN KEY (identificador_habilidade) REFERENCES habilidade(id_habilidade)
);

CREATE TABLE fruta (
    identificador_fruta INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    quantidade INT DEFAULT 1,
    raridade VARCHAR(50),
    preco_compra DECIMAL(10,2),
    preco_venda DECIMAL(10,2),
    identificador_habilidade INT,
    FOREIGN KEY (identificador_fruta) REFERENCES nao_consumivel(identificador_nao_consumivel),
    FOREIGN KEY (identificador_habilidade) REFERENCES efeito(identificador_efeito)
);

CREATE TABLE efeito_consumivel (
    identificador_efeito INT,
    identificador_consumivel INT,
    PRIMARY KEY (identificador_efeito, identificador_consumivel),
    FOREIGN KEY (identificador_efeito) REFERENCES efeito(identificador_efeito),
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel)
);

CREATE TABLE efeito_acessorio (
    identificador_efeito INT,
    identificador_acessorio INT,
    PRIMARY KEY (identificador_efeito, identificador_acessorio),
    FOREIGN KEY (identificador_efeito) REFERENCES efeito(identificador_efeito),
    FOREIGN KEY (identificador_acessorio) REFERENCES acessorio(identificador_acessorio)
);

CREATE TABLE jogador (
    id_jogador SERIAL PRIMARY KEY,
    id_personagem INT,
    id_habilidade INT,
    id_mapa INT NOT NULL,
    id_ilha INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    energia INT CHECK (energia >= 0 AND energia <= 999) DEFAULT 100,
    vida INT CHECK (vida >= 0 AND vida <= 999) DEFAULT 100,
    nivel INT CHECK (nivel >= 1 AND nivel <= 99) DEFAULT 1,
    sorte INT CHECK (sorte >= 0 AND sorte <= 99) DEFAULT 0,
    vida_atual INT DEFAULT 100 CHECK (vida_atual <= vida),
    dano_base INT NOT NULL CHECK (dano_base >= 0 AND dano_base <= 999),
    experiencia_atual INT DEFAULT 0 CHECK (experiencia_atual >= 0 AND experiencia_atual <= 99999),
    coordenada_x DECIMAL(10,2) NOT NULL CHECK (coordenada_x >= 0 AND coordenada_x <= 5000),
    coordenada_y DECIMAL(10,2) NOT NULL CHECK (coordenada_y >= 0 AND coordenada_y <= 5000),
    FOREIGN KEY (id_personagem) REFERENCES tipo_personagem(id_personagem),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade),
    FOREIGN KEY (id_mapa, id_ilha) REFERENCES mapa(id_mapa, id_ilha)
);

CREATE TABLE receita (
    identificador_receita SERIAL PRIMARY KEY,
    consumivel_produzido INT,
    id_jogador INT,
    FOREIGN KEY (consumivel_produzido) REFERENCES consumivel(identificador_consumivel),
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador)
);

CREATE TABLE ingrediente_consumivel (
    identificador_receita INT,
    identificador_consumivel INT,
    PRIMARY KEY (identificador_receita, identificador_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel)
);

CREATE TABLE ingrediente_nao_consumivel (
    identificador_receita INT,
    identificador_nao_consumivel INT,
    PRIMARY KEY (identificador_receita, identificador_nao_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_nao_consumivel) REFERENCES nao_consumivel(identificador_nao_consumivel)
);

CREATE TABLE chefe (
    id_chefe SERIAL PRIMARY KEY,
    id_habilidade INT,
    id_mapa INT NOT NULL,
    id_ilha INT NOT NULL,
    nome VARCHAR(28) NOT NULL UNIQUE,
    dano INT CHECK (dano >= 0 AND dano <= 999),
    vida INT CHECK (vida >= 0 AND vida <= 999) DEFAULT 100,
    nivel INT CHECK (nivel >= 1 AND nivel <= 99) DEFAULT 1,
    experiencia INT NOT NULL CHECK (experiencia >= 0 AND experiencia <= 30),
    coordenada_x DECIMAL(10,2) NOT NULL CHECK (coordenada_x >= 0 AND coordenada_x <= 5000),
    coordenada_y DECIMAL(10,2) NOT NULL CHECK (coordenada_y >= 0 AND coordenada_y <= 5000),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade),
    FOREIGN KEY (id_mapa, id_ilha) REFERENCES mapa(id_mapa, id_ilha)
);

CREATE TABLE lacaio (
    id_lacaio SERIAL PRIMARY KEY,
    id_habilidade INT,
    id_mapa INT NOT NULL,
    id_ilha INT NOT NULL,
    nome VARCHAR(15) NOT NULL,
    dano INT CHECK (dano >= 0 AND dano <= 999),
    vida INT CHECK (vida >= 0 AND vida <= 999) DEFAULT 100,
    nivel INT CHECK (nivel >= 1 AND nivel <= 99) DEFAULT 1,
    experiencia INT NOT NULL CHECK (experiencia >= 0 AND experiencia <= 30),
    coordenada_x DECIMAL(10,2) NOT NULL CHECK (coordenada_x >= 0 AND coordenada_x <= 5000),
    coordenada_y DECIMAL(10,2) NOT NULL CHECK (coordenada_y >= 0 AND coordenada_y <= 5000),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade),
    FOREIGN KEY (id_mapa, id_ilha) REFERENCES mapa(id_mapa, id_ilha)
);

CREATE TABLE instancia_lacaio (
    id_instancia_lacaio SERIAL PRIMARY KEY,
    identificador_lacaio INT NOT NULL,
    vida_atual INT DEFAULT 100 CHECK (vida_atual >= 0 AND vida_atual <= 999),
    FOREIGN KEY (identificador_lacaio) REFERENCES lacaio(id_lacaio)
);

CREATE TABLE aliado (
    id_aliado SERIAL PRIMARY KEY,
    id_mapa INT NOT NULL,
    id_ilha INT NOT NULL,
    nome VARCHAR(6) NOT NULL UNIQUE,
    descricao VARCHAR(100) NOT NULL,
    vida INT CHECK (vida >= 0 AND vida <= 999) DEFAULT 100,
    nivel INT CHECK (nivel >= 1 AND nivel <= 99) DEFAULT 1,
    vida_atual INT DEFAULT 100 CHECK (vida_atual <= vida),
    dano_base INT CHECK (dano_base >= 0 AND dano_base <= 999),
    coordenada_x DECIMAL(10,2) NOT NULL CHECK (coordenada_x >= 0 AND coordenada_x <= 5000),
    coordenada_y DECIMAL(10,2) NOT NULL CHECK (coordenada_y >= 0 AND coordenada_y <= 5000),
    FOREIGN KEY (id_mapa, id_ilha) REFERENCES mapa(id_mapa, id_ilha)
);

CREATE TABLE habitante (
    identificador_habitante SERIAL PRIMARY KEY,
    identificador_mapa INT NOT NULL,
    id_ilha INT NOT NULL,
    nome VARCHAR(15) NOT NULL,
    tipo VARCHAR(3) NOT NULL CHECK (tipo IN ('hbt', 'rec', 'coz', 'ven')),
    descricao VARCHAR(100) NOT NULL,
    especialidade VARCHAR(3) CHECK (especialidade IN ('arm', 'ace', 'com')),
    coordenada_x DECIMAL(10,2) NOT NULL CHECK (coordenada_x >= 0 AND coordenada_x <= 5000),
    coordenada_y DECIMAL(10,2) NOT NULL CHECK (coordenada_y >= 0 AND coordenada_y <= 5000),
    FOREIGN KEY (identificador_mapa, id_ilha) REFERENCES mapa(id_mapa, id_ilha)
);

CREATE TABLE habilidade_aliado (
    id_aliado INT,
    id_habilidade INT,
    PRIMARY KEY (id_aliado, id_habilidade),
    FOREIGN KEY (id_aliado) REFERENCES aliado(id_aliado),
    FOREIGN KEY (id_habilidade) REFERENCES habilidade(id_habilidade)
);

CREATE TABLE batalha (
    identificador_batalha SERIAL PRIMARY KEY,
    identificador_jogador INT,
    identificador_aliado INT,
    identificador_chefe INT,
    identificador_instancia_lacaio INT,
    experiencia_ganha INT,
    FOREIGN KEY (identificador_jogador) REFERENCES jogador(id_jogador),
    FOREIGN KEY (identificador_aliado) REFERENCES aliado(id_aliado),
    FOREIGN KEY (identificador_chefe) REFERENCES chefe(id_chefe),
    FOREIGN KEY (identificador_instancia_lacaio) REFERENCES instancia_lacaio(id_instancia_lacaio)
);

CREATE TABLE batalha_instancia_lacaio (
    identificador_batalha INT,
    identificador_instancia_lacaio INT,
    PRIMARY KEY (identificador_batalha, identificador_instancia_lacaio),
    FOREIGN KEY (identificador_batalha) REFERENCES batalha(identificador_batalha),
    FOREIGN KEY (identificador_instancia_lacaio) REFERENCES instancia_lacaio(id_instancia_lacaio)
);

CREATE TABLE negociacao (
    identificador_negociacao SERIAL PRIMARY KEY,
    identificador_item INT NOT NULL,
    identificador_jogador INT NOT NULL,
    identificador_vendedor INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 0 CHECK (quantidade >= 0 AND quantidade <= 99),
    preco_final DECIMAL(10,2) NOT NULL DEFAULT 1 CHECK (preco_final >= 1 AND preco_final <= 98901),
    tipo VARCHAR(6) NOT NULL CHECK (tipo IN ('compra', 'venda')),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item),
    FOREIGN KEY (identificador_jogador) REFERENCES jogador(id_jogador),
    FOREIGN KEY (identificador_vendedor) REFERENCES habitante(identificador_habitante)
);

CREATE TABLE missao (
    missao_id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    mapa_id INT NOT NULL,
    ilha_id INT NOT NULL,
    id_jogador INT,
    id_recrutador INT,
    tipo_sala VARCHAR(50) NOT NULL CHECK (tipo_sala IN ('campo_batalha', 'porto', 'vila')),
    sala_id INT NOT NULL,
    FOREIGN KEY (mapa_id, ilha_id) REFERENCES mapa(id_mapa, id_ilha),
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador),
    FOREIGN KEY (id_recrutador) REFERENCES habitante(identificador_habitante)
);

CREATE TABLE mar (
    mar_id SERIAL PRIMARY KEY,
    monstro VARCHAR(100),
    obstaculo VARCHAR(100)
);

CREATE TABLE mapa_mar (
    mapa_id INT NOT NULL,
    mar_id INT NOT NULL,
    ilha_id INT NOT NULL,
    PRIMARY KEY (mapa_id, ilha_id, mar_id),
    FOREIGN KEY (mapa_id, ilha_id) REFERENCES mapa(id_mapa, id_ilha),
    FOREIGN KEY (mar_id) REFERENCES mar(mar_id)
);

CREATE TABLE corredor_maritimo (
    maritimo_id SERIAL PRIMARY KEY,
    ilha_a INT NOT NULL,
    ilha_b INT NOT NULL,
    FOREIGN KEY (ilha_a) REFERENCES ilha(id),
    FOREIGN KEY (ilha_b) REFERENCES ilha(id)
);

CREATE TABLE controlador_mar (
    maritimo_id INT NOT NULL,
    mar_id INT NOT NULL,
    PRIMARY KEY (maritimo_id, mar_id),
    FOREIGN KEY (maritimo_id) REFERENCES corredor_maritimo(maritimo_id),
    FOREIGN KEY (mar_id) REFERENCES mar(mar_id)
);

CREATE TABLE barco (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    nome VARCHAR(100),
    melhoria TEXT,
    porto_id INT,
    FOREIGN KEY (porto_id) REFERENCES porto(sala_id)
);

CREATE TABLE barco_porto (
    barco_id INT NOT NULL,
    sala_id INT NOT NULL,
    PRIMARY KEY (barco_id, sala_id),
    FOREIGN KEY (barco_id) REFERENCES barco(id),
    FOREIGN KEY (sala_id) REFERENCES porto(sala_id)
);

CREATE TABLE controlador_barco (
    barco_id INT NOT NULL,
    maritimo_id INT NOT NULL,
    PRIMARY KEY (barco_id, maritimo_id),
    FOREIGN KEY (barco_id) REFERENCES barco(id),
    FOREIGN KEY (maritimo_id) REFERENCES corredor_maritimo(maritimo_id)
);

CREATE TABLE marco (
    mar_id INT PRIMARY KEY,
    monstro VARCHAR(100),
    obstaculo VARCHAR(100),
    FOREIGN KEY (mar_id) REFERENCES mar(mar_id)
);

CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_jogador INT NOT NULL,
    nome VARCHAR(100),
    FOREIGN KEY (id_jogador) REFERENCES jogador(id_jogador)
);

CREATE TABLE ItemInventario (
    id_inventario INT NOT NULL,
    identificador_item INT NOT NULL,
    PRIMARY KEY (id_inventario, identificador_item),
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item)
);

CREATE TABLE ItemMissao (
    missao_id INT NOT NULL,
    identificador_item INT NOT NULL,
    PRIMARY KEY (missao_id, identificador_item),
    FOREIGN KEY (missao_id) REFERENCES missao(missao_id),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item)
);

```
---




## 📚 Bibliografia

* ELMASRI, R.; NAVATHE, S. B. *Sistemas de Banco de Dados*. 7. ed. Pearson Education do Brasil, 2018.
* DATE, C. J. *An Introduction to Database Systems*. 8. ed. Addison-Wesley, 2003.
* SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. *Database System Concepts*. 7. ed. McGraw-Hill Education, 2019.
* Oracle Database SQL Language Reference. Disponível em: [https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/index.html](https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/index.html) (Acesso em 28 de maio de 2025).
* PostgreSQL Documentation. Disponível em: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/) (Acesso em 28 de maio de 2025).
* Microsoft SQL Server Documentation. Disponível em: [https://docs.microsoft.com/en-us/sql/sql-server/sql-server-documentation](https://docs.microsoft.com/en-us/sql/sql-server/sql-server-documentation) (Acesso em 28 de maio de 2025).

---

## 📑 Histórico de Versões

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 29/05/2025 | [Israel Thalles](https://github.com/IsraelThalles) | 31/05/2025 |
 `1.1` | adicionado as consultas | [Pablo Serra](https://github.com/Pabloserrapxx) | 16/06/2025 |  |  |