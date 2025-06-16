CREATE TABLE Efeito (
    IdentificadorEfeito INT PRIMARY KEY,
    Nome VARCHAR(255),
    Valor VARCHAR(255)
);

CREATE TABLE Consumivel (
    IdentificadorConsumivel INT PRIMARY KEY,
    Nome VARCHAR(255),
    Tipo VARCHAR(255),
    Quantidade INT,
    Raridade VARCHAR(50),
    PrecoCompra INT,
    PrecoVenda INT,
    EFabricavel BOOLEAN
);

CREATE TABLE NaoConsumivel (
    IdentificadorNaoConsumivel INT PRIMARY KEY,
    Nome VARCHAR(255),
    Tipo VARCHAR(255),
    Quantidade INT,
    Raridade VARCHAR(50),
    PrecoCompra INT,
    PrecoVenda INT
);

CREATE TABLE EfeitoConsumivel (
    IdentificadorConsumivel INT,
    IdentificadorEfeito INT,
    PRIMARY KEY (IdentificadorConsumivel, IdentificadorEfeito),
    FOREIGN KEY (IdentificadorConsumivel) REFERENCES Consumivel(IdentificadorConsumivel),
    FOREIGN KEY (IdentificadorEfeito) REFERENCES Efeito(IdentificadorEfeito)
);

CREATE TABLE Receita (
    IdentificadorReceita INT PRIMARY KEY,
    IdentificadorConsumivelProduzido INT,
    FOREIGN KEY (IdentificadorConsumivelProduzido) REFERENCES Consumivel(IdentificadorConsumivel)
);

CREATE TABLE IngredienteConsumivel (
    IdentificadorReceita INT,
    IdentificadorConsumivel INT,
    PRIMARY KEY (IdentificadorReceita, IdentificadorConsumivel),
    FOREIGN KEY (IdentificadorReceita) REFERENCES Receita(IdentificadorReceita),
    FOREIGN KEY (IdentificadorConsumivel) REFERENCES Consumivel(IdentificadorConsumivel)
);

CREATE TABLE IngredienteNaoConsumivel (
    IdentificadorReceita INT,
    IdentificadorNaoConsumivel INT,
    PRIMARY KEY (IdentificadorReceita, IdentificadorNaoConsumivel),
    FOREIGN KEY (IdentificadorReceita) REFERENCES Receita(IdentificadorReceita),
    FOREIGN KEY (IdentificadorNaoConsumivel) REFERENCES NaoConsumivel(IdentificadorNaoConsumivel)
);