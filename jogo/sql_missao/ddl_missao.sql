
-- Criação da sequência global para IDs numéricos autoincrementados
CREATE SEQUENCE global_numeric_id_sequence
    START WITH 1
    INCREMENT BY 1
    NO CYCLE;

-- Tabela para Campo_de_batalha (Mantida como antes)
CREATE TABLE Campo_de_batalha (
    SalaID INT PRIMARY KEY,
    TipoSala CHAR(50) NOT NULL,
    Nome CHAR(50),
    TotalSalas SMALLINT,
    Tamanho CHAR(50),
    Tipo CHAR(50),
    QtdInimigos SMALLINT
);

-- Tabela para Vila (Mantida como antes)
CREATE TABLE Vila (
    SalaID INT,
    TipoSala CHAR(50) NOT NULL,
    Nome CHAR(50),
    TotalSalas SMALLINT,
    Informacoes CHAR(100),
    PRIMARY KEY (SalaID, TipoSala)
);

-- Tabela para Porto (Mantida como antes)
CREATE TABLE Porto (
    SalaID INT,
    TipoSala CHAR(50) NOT NULL,
    Nome CHAR(50),
    TotalSalas SMALLINT,
    QtdBarcos SMALLINT,
    Capacidade SMALLINT,
    SentidoIlha CHAR(50),
    PRIMARY KEY (SalaID, TipoSala)
);

-- Tabela para Habitante (Para NPCs, como antes)
CREATE TABLE Habitante (
    idHabitante INT PRIMARY KEY DEFAULT NEXTVAL('global_numeric_id_sequence'),
    idMapa INT, -- FK para tabela Mapa (não definida aqui)
    Tipo CHAR(50),
    Especialidade CHAR(50),
    CoordenadaX SMALLINT,
    CoordenadaY SMALLINT
);


CREATE TABLE Item (
    ItemID INT PRIMARY KEY DEFAULT NEXTVAL('global_numeric_id_sequence'),
    Nome CHAR(50) NOT NULL,
    Descricao CHAR(100),
    Tipo CHAR(50)
);

CREATE TABLE Jogador (
    idJogador INT PRIMARY KEY DEFAULT NEXTVAL('global_numeric_id_sequence'), 
    idHabilidade INT NOT NULL, 
    idMapa INT NOT NULL, 
    Energia SMALLINT DEFAULT 100,
    Vida SMALLINT DEFAULT 100, 
    Nivel SMALLINT DEFAULT 1, 
    Sorte SMALLINT DEFAULT 0, 
    VidaAtual SMALLINT DEFAULT 100, 
    DanoBase SMALLINT NOT NULL,
    ExperienciaAtual SMALLINT DEFAULT 0,
    CoordenadaX INT NOT NULL, 
    CoordenadaY INT NOT NULL, 
    CONSTRAINT chk_vida_atual CHECK (VidaAtual <= Vida),
    CONSTRAINT chk_energia CHECK (Energia >= 0 AND Energia <= 999), 
    CONSTRAINT chk_vida CHECK (Vida >= 0 AND Vida <= 999), 
    CONSTRAINT chk_nivel CHECK (Nivel >= 1 AND Nivel <= 99), 
    CONSTRAINT chk_sorte CHECK (Sorte >= 0 AND Sorte <= 99), 
    CONSTRAINT chk_dano_base CHECK (DanoBase >= 0 AND DanoBase <= 999), 
    CONSTRAINT chk_experiencia_atual CHECK (ExperienciaAtual >= 0 AND ExperienciaAtual <= 99999),
                                                                                                    
    CONSTRAINT chk_coordenada_x CHECK (CoordenadaX >= -9999 AND CoordenadaX <= 9999),
    CONSTRAINT chk_coordenada_y CHECK (CoordenadaY >= -9999 AND CoordenadaY <= 9999),
    FOREIGN KEY para Habilidade e Mapa (assumindo suas tabelas existem/serão criadas),
    FOREIGN KEY (idHabilidade) REFERENCES Habilidade(idHabilidade),
    FOREIGN KEY (idMapa) REFERENCES Mapa(idMapa)
);

CREATE TABLE Chefe (
    idChefe INT PRIMARY KEY DEFAULT NEXTVAL('global_numeric_id_sequence'),
    idHabilidade INT NOT NULL, 
    idMapa INT NOT NULL, 
    Nome CHAR(50), 
    Descrição CHAR(100),
    CoordenadaX INT NOT NULL, 
    CoordenadaY INT NOT NULL,
    Vida SMALLINT DEFAULT 100, 
    Nivel SMALLINT DEFAULT 1, 
    DanoBase SMALLINT NOT NULL,
    Experiencia SMALLINT NOT NULL, 
    TipoInimigo CHAR(50), 
    CONSTRAINT chk_chefe_vida CHECK (Vida >= 0 AND Vida <= 999),
    CONSTRAINT chk_chefe_nivel CHECK (Nivel >= 1 AND Nivel <= 99),
    CONSTRAINT chk_chefe_dano_base CHECK (DanoBase >= 0 AND DanoBase <= 999),
    CONSTRAINT chk_chefe_experiencia CHECK (Experiencia >= 0 AND Experiencia <= 999),
    CONSTRAINT chk_chefe_coordenada_x CHECK (CoordenadaX >= -9999 AND CoordenadaX <= 9999),
    CONSTRAINT chk_chefe_coordenada_y CHECK (CoordenadaY >= -9999 AND CoordenadaY <= 9999)
   
);


CREATE TABLE Missão (
    MissaoID INT PRIMARY KEY DEFAULT NEXTVAL('global_numeric_id_sequence'),
    MapaID INT NOT NULL, 
    idLogador INT NOT NULL, 
    SalaID INT NOT NULL,
    TipoSala CHAR(50) NOT NULL,
    idRecrutador INT NOT NULL, 
    Descricao CHAR(100) NOT NULL,
    Nome CHAR(50) NOT NULL,
    FOREIGN KEY (SalaID, TipoSala) REFERENCES Campo_de_batalha(SalaID, TipoSala),
    FOREIGN KEY (SalaID, TipoSala) REFERENCES Vila(SalaID, TipoSala),
    FOREIGN KEY (SalaID, TipoSala) REFERENCES Porto(SalaID, TipoSala),
    FOREIGN KEY (idLogador) REFERENCES Jogador(idJogador), 
    FOREIGN KEY (idRecrutador) REFERENCES Habitante(idHabitante)
);

-- Tabela para ItemMissão 
CREATE TABLE ItemMissão (
    MissaoID INT,
    IdentificadorItem INT PRIMARY KEY DEFAULT NEXTVAL('global_numeric_id_sequence'),
    PRIMARY KEY (MissaoID, IdentificadorItem), 
    FOREIGN KEY (MissaoID) REFERENCES Missão(MissaoID),
    FOREIGN KEY (IdentificadorItem) REFERENCES Item(ItemID) 
);


