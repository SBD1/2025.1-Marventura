

* **Ver todos os atributos de um habitante específico:**

    ```sql
    SELECT idHabitante, idMapa, Tipo, Especialidade, CoordenadaX, CoordenadaY
    FROM Habitante
    WHERE idHabitante = 2; 
    ```

* **Ver quais habitantes possuem uma especialidade específica:**

    ```sql
    SELECT idHabitante, Tipo, Especialidade
    FROM Habitante
    WHERE Especialidade = 'Nenhum'; 
    ```

* **Ver habitantes localizados em um Mapa específico:**

    ```sql
    SELECT idHabitante, Tipo, Especialidade
    FROM Habitante
    WHERE idMapa = 101; -- Exemplo: ID do mapa da 'Vila Inicial'
    ```

### Jogador

A tabela `Jogador` contém os dados específicos dos personagens controlados pelos jogadores.

* **Ver todos os atributos de um jogador específico:**

    ```sql
    SELECT idJogador, idHabilidade, idMapa, Energia, Vida, Nivel, Sorte, VidaAtual, DanoBase, ExperienciaAtual, CoordenadaX, CoordenadaY
    FROM Jogador
    WHERE idJogador = 1; -- Exemplo: ID do Protagonista
    ```

* **Ver atributos de combate (Vida, Nível, Dano Base) de um jogador específico:**

    ```sql
    SELECT Vida, Nivel, DanoBase
    FROM Jogador
    WHERE idJogador = 1; -- Exemplo: ID do Protagonista
    ```

### Chefe

* **Ver todos os atributos de um chefe específico:**

    ```sql
    SELECT idChefe, idHabilidade, idMapa, Nome, Descrição, CoordenadaX, CoordenadaY, Vida, Nivel, DanoBase, Experiencia, TipoInimigo
    FROM Chefe
    WHERE idChefe = 5; 
    ```

* **Ver nome, vida e nível de um chefe específico:**

    ```sql
    SELECT Nome, Vida, Nivel
    FROM Chefe
    WHERE idChefe = 6; 
    ```

* **Ver quais chefes pertencem a um tipo de inimigo específico:**

    ```sql
    SELECT idChefe, Nome, Nivel
    FROM Chefe
    WHERE TipoInimigo = 'Humanoide';
    ```

### Missão

A tabela `Missão` detalha as diferentes tarefas e objetivos do jogo.

* **Ver todos os atributos de uma missão específica:**

    ```sql
    SELECT MissaoID, MapaID, idLogador, SalaID, TipoSala, idRecrutador, Descricao, Nome
    FROM Missão
    WHERE MissaoID = 11;
    ```

* **Buscar missões por nome (parcial ou completo):**

    ```sql
    SELECT MissaoID, Nome, Descricao
    FROM Missão
    WHERE Nome LIKE '%Fera%'; 
    ```

* **Ver missões atribuídas por um recrutador específico (Habitante):**

    ```sql
    SELECT MissaoID, Nome, Descricao
    FROM Missão
    WHERE idRecrutador = 2; 
    ```

* **Ver missões com recrutador que é um Chefe:**

    ```sql
    SELECT m.Nome AS NomeMissao, m.Descricao, c.Nome AS NomeRecrutadorChefe
    FROM Missão m
    JOIN Chefe c ON m.idRecrutador = c.idChefe
    WHERE m.idRecrutador IN (7, 9); 
    ```

* **Ver missões associadas a um tipo de sala específico (Ex: Campo de Batalha):**

    ```sql
    SELECT m.Nome AS NomeMissao, m.Descricao, cb.Nome AS NomeLocal
    FROM Missão m
    JOIN Campo_de_batalha cb ON m.SalaID = cb.SalaID AND m.TipoSala = cb.TipoSala
    WHERE m.TipoSala = 'Campo de Batalha';
    ```

### Campo_de_batalha

A tabela `Campo_de_batalha` armazena informações sobre as áreas de combate.

* **Ver todos os atributos de um campo de batalha específico:**

    ```sql
    SELECT SalaID, TipoSala, Nome, TotalSalas, Tamanho, Tipo, QtdInimigos
    FROM Campo_de_batalha
    WHERE SalaID = 201;
    ```

* **Ver campos de batalha de um tipo ambiental específico (Ex: Floresta):**

    ```sql
    SELECT SalaID, Nome, Tipo, QtdInimigos
    FROM Campo_de_batalha
    WHERE Tipo = 'Floresta';
    ```

### Vila

A tabela `Vila` contém dados sobre os vilarejos no mundo.

* **Ver todos os atributos de uma vila específica:**

    ```sql
    SELECT SalaID, TipoSala, Nome, TotalSalas, Informacoes
    FROM Vila
    WHERE SalaID = 101; 
    ```

* **Ver informações de todas as vilas cadastradas:**

    ```sql
    SELECT Nome, Informacoes
    FROM Vila;
    ```

### Porto

A tabela `Porto` armazena dados sobre as localidades portuárias.

* **Ver todos os atributos de um porto específico:**

    ```sql
    SELECT SalaID, TipoSala, Nome, TotalSalas, QtdBarcos, Capacidade, SentidoIlha
    FROM Porto
    WHERE SalaID = 301; -- Exemplo: ID do 'Porto da Cidade'
    ```

* **Ver portos que possuem mais de um determinado número de barcos:**

    ```sql
    SELECT Nome, QtdBarcos, Capacidade
    FROM Porto
    WHERE QtdBarcos > 3;
    ```

### Item

A tabela `Item` lista todos os itens disponíveis no jogo.

* **Ver todos os atributos de um item específico:**

    ```sql
    SELECT ItemID, Nome, Descricao, Tipo
    FROM Item
    WHERE ItemID = 10; -- Exemplo: ID da 'Fruta Estranha'
    ```

* **Ver todos os itens de um tipo específico (Ex: Fruta):**

    ```sql
    SELECT Nome, Descricao
    FROM Item
    WHERE Tipo = 'Fruta';
    ```

### ItemMissão

A tabela `ItemMissão` associa itens a missões, indicando quais itens estão relacionados a quais missões.

* **Ver todos os itens associados a uma missão específica:**

    ```sql
    SELECT im.IdentificadorItem, i.Nome AS NomeItem, i.Descricao AS DescricaoItem
    FROM ItemMissão im
    JOIN Item i ON im.IdentificadorItem = i.ItemID
    WHERE im.MissaoID = 11; 
    ```

* **Ver todas as missões que contêm um item específico:**

    ```sql
    SELECT im.MissaoID, m.Nome AS NomeMissao, m.Descricao AS DescricaoMissao
    FROM ItemMissão im
    JOIN Missão m ON im.MissaoID = m.MissaoID
    WHERE im.IdentificadorItem = 10; 
    ```