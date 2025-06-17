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

CREATE TABLE efeito (
    identificador_efeito SMALLINT SERIAL PRIMARY KEY,
    nome CHAR(100) NOT NULL,
    valor SMALLINT NOT NULL
);

CREATE TABLE consumivel (
    identificador_consumivel SMALLINT PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('con')),
    nome CHAR(100) NOT NULL,
    descricao CHAR(100) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL CHECK (Raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(100) NOT NULL CHECK (local_encontrado IN ('Campos', 'Cidade', 'Neve', 'Deserto', 'Ilha Assombrada', 'Fortaleza da Marinha')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL,
    e_fabricavel BOOLEAN
);

CREATE TABLE nao_consumivel (
    identificador_nao_consumivel SMALLINT PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (Tipo IN ('ncn')),
    nome CHAR(100) NOT NULL,
    descricao CHAR(100) NOT NULL,
    quantidade SMALLINT NOT NULL,
    raridade CHAR(3) DEFAULT '★' NOT NULL CHECK (Raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(100) NOT NULL CHECK (local_encontrado IN ('Campos', 'Cidade', 'Neve', 'Deserto', 'Ilha Assombrada', 'Fortaleza da Marinha')),
    preco_de_compra SMALLINT NOT NULL,
    preco_de_venda SMALLINT NOT NULL,
);

CREATE TABLE efeito_consumivel (
    identificador_consumivel SMALLINT,
    identificador_efeito SMALLINT,
    PRIMARY KEY (identificador_consumivel, identificador_efeito),
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel),
    FOREIGN KEY (identificador_efeito) REFERENCES efeito(identificador_efeito)
);

CREATE TABLE receita (
    identificador_receita SMALLINT PRIMARY KEY,
    consumivel_produzido SMALLINT,
    FOREIGN KEY (consumivel_roduzido) REFERENCES consumivel(identificador_consumivel)
);

CREATE TABLE ingrediente_consumivel (
    identificador_receita SMALLINT,
    identificador_consumivel SMALLINT,
    PRIMARY KEY (identificador_receita, identificador_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_consumivel) REFERENCES consumivel(identificador_consumivel)
);

CREATE TABLE ingrediente_nao_consumivel (
    identificador_receita SMALLINT,
    identificador_nao_consumivel SMALLINT,
    PRIMARY KEY (identificador_receita, identificador_nao_consumivel),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita),
    FOREIGN KEY (identificador_nao_consumivel) REFERENCES nao_consumivel(identificador_nao_consumivel)
);

CREATE TABLE Campo_de_batalha (
    SalaID SMALLINT PRIMARY KEY,
    TipoSala CHAR(50) NOT NULL,
    Nome CHAR(50),
    TotalSalas SMALLINT,
    Tamanho CHAR(50),
    Tipo CHAR(50),
    QtdInimigos SMALLINT
);

CREATE TABLE Vila (
    SalaID SMALLINT,
    TipoSala CHAR(50) NOT NULL,
    Nome CHAR(50),
    TotalSalas SMALLINT,
    Informacoes CHAR(100),
    PRIMARY KEY (SalaID, TipoSala)
);

CREATE TABLE Porto (
    SalaID SMALLINT,
    TipoSala CHAR(50) NOT NULL,
    Nome CHAR(50),
    TotalSalas SMALLINT,
    QtdBarcos SMALLINT,
    Capacidade SMALLINT,
    SentidoIlha CHAR(50),
    PRIMARY KEY (SalaID, TipoSala)
);

CREATE TABLE Habitante (
    idHabitante SERIAL PRIMARY KEY,
    idMapa SMALLINT,
    IlhaID SMALLINT,
    Tipo CHAR(50),
    Especialidade CHAR(50),
    CoordenadaX SMALLINT,
    CoordenadaY SMALLINT,
    FOREIGN KEY (idMapa, IlhaID) REFERENCES Mapa(MapaID, IlhaID)
);

CREATE TABLE Item (
    ItemID SERIAL PRIMARY KEY,
    Nome CHAR(50) NOT NULL,
    Descricao CHAR(100),
    Tipo CHAR(50)
);

CREATE TABLE Habilidade (
    identificador_habilidade SERIAL PRIMARY KEY,
    dano SMALLINT NOT NULL CHECK (dano >= 0 AND dano <= 15),
    custo SMALLINT NOT NULL CHECK (custo >= 0 AND custo <= 4),
    nome CHAR(50) NOT NULL,
    tipo CHAR(8) NOT NULL CHECK (tipo IN ('fruta', 'espada', 'soco', 'projétil'))
);

CREATE TABLE TipoItem (
    IdentificadorItem SERIAL PRIMARY KEY,
    Tipo CHAR(50) NOT NULL
);

CREATE TABLE Ilha (
    ID SERIAL PRIMARY KEY,
    SalaID SMALLINT,
    TipoSala CHAR(50),
    Tamanho CHAR(50),
    Nome CHAR(50),
    Quantidade_sala SMALLINT,
    Tipo CHAR(50),
    FOREIGN KEY (SalaID, TipoSala) REFERENCES Campo_de_batalha(SalaID, TipoSala),
    FOREIGN KEY (SalaID, TipoSala) REFERENCES Vila(SalaID, TipoSala),
    FOREIGN KEY (SalaID, TipoSala) REFERENCES Porto(SalaID, TipoSala)
);

CREATE TABLE Mapa (
    MapaID SMALLINT,
    IlhaID SMALLINT,
    TotalIlhas SMALLINT,
    TotalItensChave SMALLINT,
    PRIMARY KEY (MapaID, IlhaID),
    FOREIGN KEY (IlhaID) REFERENCES Ilha(ID)
);

CREATE TABLE Jogador (
    idJogador SERIAL PRIMARY KEY,
    idHabilidade SMALLINT NOT NULL,
    idMapa SMALLINT NOT NULL,
    IlhaID SMALLINT NOT NULL,
    Energia SMALLINT DEFAULT 100 CHECK (Energia >= 0 AND Energia <= 999),
    Vida SMALLINT DEFAULT 100 CHECK (Vida >= 0 AND Vida <= 999),
    Nivel SMALLINT DEFAULT 1 CHECK (Nivel >= 1 AND Nivel <= 99),
    Sorte SMALLINT DEFAULT 0 CHECK (Sorte >= 0 AND Sorte <= 99),
    VidaAtual SMALLINT DEFAULT 100 CHECK (VidaAtual <= Vida),
    DanoBase SMALLINT NOT NULL CHECK (DanoBase >= 0 AND DanoBase <= 999),
    ExperienciaAtual SMALLINT DEFAULT 0 CHECK (ExperienciaAtual >= 0 AND ExperienciaAtual <= 99999),
    CoordenadaX SMALLINT NOT NULL CHECK (CoordenadaX >= -9999 AND CoordenadaX <= 9999),
    CoordenadaY SMALLINT NOT NULL CHECK (CoordenadaY >= -9999 AND CoordenadaY <= 9999),
    FOREIGN KEY (idHabilidade) REFERENCES Habilidade(identificador_habilidade),
    FOREIGN KEY (idMapa, IlhaID) REFERENCES Mapa(MapaID, IlhaID)
);

CREATE TABLE Chefe (
    idChefe SERIAL PRIMARY KEY,
    idHabilidade SMALLINT NOT NULL,
    idMapa SMALLINT NOT NULL,
    IlhaID SMALLINT NOT NULL,
    Nome CHAR(50),
    Descrição CHAR(100),
    CoordenadaX SMALLINT NOT NULL CHECK (CoordenadaX >= -9999 AND CoordenadaX <= 9999),
    CoordenadaY SMALLINT NOT NULL CHECK (CoordenadaY >= -9999 AND CoordenadaY <= 9999),
    Vida SMALLINT DEFAULT 100 CHECK (Vida >= 0 AND Vida <= 999),
    Nivel SMALLINT DEFAULT 1 CHECK (Nivel >= 1 AND Nivel <= 99),
    DanoBase SMALLINT NOT NULL CHECK (DanoBase >= 0 AND DanoBase <= 999),
    Experiencia SMALLINT NOT NULL CHECK (Experiencia >= 0 AND Experiencia <= 999),
    TipoInimigo CHAR(50),
    FOREIGN KEY (idHabilidade) REFERENCES Habilidade(identificador_habilidade),
    FOREIGN KEY (idMapa, IlhaID) REFERENCES Mapa(MapaID, IlhaID)
);

CREATE TABLE Missão (
    MissaoID SERIAL PRIMARY KEY,
    MapaID SMALLINT NOT NULL,
    IlhaID SMALLINT NOT NULL,
    idLogador SMALLINT NOT NULL,
    SalaID SMALLINT NOT NULL,
    TipoSala CHAR(50) NOT NULL,
    idRecrutador SMALLINT NOT NULL,
    Descricao CHAR(100) NOT NULL,
    Nome CHAR(50) NOT NULL,
    FOREIGN KEY (SalaID, TipoSala) REFERENCES Campo_de_batalha(SalaID, TipoSala),
    FOREIGN KEY (SalaID, TipoSala) REFERENCES Vila(SalaID, TipoSala),
    FOREIGN KEY (SalaID, TipoSala) REFERENCES Porto(SalaID, TipoSala),
    FOREIGN KEY (idLogador) REFERENCES Jogador(idJogador),
    FOREIGN KEY (idRecrutador) REFERENCES Habitante(idHabitante),
    FOREIGN KEY (MapaID, IlhaID) REFERENCES Mapa(MapaID, IlhaID)
);

CREATE TABLE ItemMissão (
    MissaoID SMALLINT,
    IdentificadorItem SMALLINT,
    PRIMARY KEY (MissaoID, IdentificadorItem),
    FOREIGN KEY (MissaoID) REFERENCES Missão(MissaoID),
    FOREIGN KEY (IdentificadorItem) REFERENCES TipoItem(IdentificadorItem)
);

CREATE TABLE Mar (
    MarID SERIAL PRIMARY KEY,
    Mostro CHAR(50),
    Obstaculo CHAR(50)
);

CREATE TABLE Corredor_maritimo (
    marítimoID SERIAL PRIMARY KEY,
    IlhaA SMALLINT NOT NULL,
    IlhaB SMALLINT NOT NULL,
    FOREIGN KEY (IlhaA) REFERENCES Ilha(ID),
    FOREIGN KEY (IlhaB) REFERENCES Ilha(ID)
);

CREATE TABLE MapaMar (
    MapaID SMALLINT,
    IlhaID SMALLINT,
    MarID SMALLINT,
    PRIMARY KEY (MapaID, IlhaID, MarID),
    FOREIGN KEY (MapaID, IlhaID) REFERENCES Mapa(MapaID, IlhaID),
    FOREIGN KEY (MarID) REFERENCES Mar(MarID)
);

CREATE TABLE Controller_mar (
    marítimoID SMALLINT,
    MarID SMALLINT,
    PRIMARY KEY (marítimoID, MarID),
    FOREIGN KEY (marítimoID) REFERENCES Corredor_maritimo(marítimoID),
    FOREIGN KEY (MarID) REFERENCES Mar(MarID)
);

CREATE TABLE Barco (
    Tipo CHAR(50) PRIMARY KEY,
    Melhoria CHAR(50),
    Nome CHAR(50),
    Nivel SMALLINT
);

CREATE TABLE BarcoPorto (
    TipoSala CHAR(50),
    TipoBarco CHAR(50),
    SalaID SMALLINT,
    PRIMARY KEY (TipoSala, TipoBarco, SalaID),
    FOREIGN KEY (TipoSala, SalaID) REFERENCES Porto(TipoSala, SalaID),
    FOREIGN KEY (TipoBarco) REFERENCES Barco(Tipo)
);

CREATE TABLE Controller_barco (
    IDBarco CHAR(50),
    marítimoID SMALLINT,
    PRIMARY KEY (IDBarco, marítimoID),
    FOREIGN KEY (IDBarco) REFERENCES Barco(Tipo),
    FOREIGN KEY (marítimoID) REFERENCES Corredor_maritimo(marítimoID)
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
