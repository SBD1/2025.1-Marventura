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

```sql
CREATE TABLE tipo_item (
    identificador_item ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('ace', 'arm', 'fru', 'con', 'ncn'))
);
```

```sql
CREATE TABLE arma (
    identificador_arma ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    tipo_arma CHAR(3) NOT NULL CHECK (tipo_arma IN ('esp', 'est', 'arc')),
    local_encontrado CHAR(27) NOT NULL CHECK (local_encontrado IN ('Loja de Espadas', 'Loja de Estilingues e Arcos')),
    preco_de_compra SMALLINT NOT NULL CHECK (preco_de_compra BETWEEN 1 AND 999)
);
```

```sql
CREATE TABLE fruta (
    identificador_fruta ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(222) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Missão', 'Evento')),
    preco_de_venda SMALLINT CHECK (preco_de_venda IS NULL OR preco_de_venda BETWEEN 1 AND 999)
);
```

```sql
CREATE TABLE acessorio (
    identificador_acessorio ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(18) NOT NULL CHECK (local_encontrado IN ('Loja de Acessórios')),
    preco_de_compra SMALLINT NOT NULL CHECK (preco_de_compra BETWEEN 1 AND 999)
);
```

```sql
CREATE TABLE consumivel (
    identificador_consumivel ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(200) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57', 'Cozinha')),
    preco_de_compra SMALLINT CHECK (preco_de_compra IS NULL OR preco_de_compra BETWEEN 1 AND 999),
    preco_de_venda SMALLINT NOT NULL CHECK (preco_de_venda BETWEEN 1 AND 999),
    e_fabricavel BOOLEAN DEFAULT FALSE CHECK (e_fabricavel IN (TRUE, FALSE))
);
```

```sql
CREATE TABLE nao_consumivel (
    identificador_nao_consumivel ID PRIMARY KEY REFERENCES tipo_item(identificador_item),
    nome CHAR(50) NOT NULL,
    descricao CHAR(150) NOT NULL,
    raridade CHAR(3) DEFAULT '★' CHECK (raridade IN ('★', '★★', '★★★')),
    local_encontrado CHAR(25) NOT NULL CHECK (local_encontrado IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57')),
    preco_de_compra SMALLINT CHECK (preco_de_compra IS NULL OR preco_de_compra BETWEEN 1 AND 999),
    preco_de_venda SMALLINT NOT NULL CHECK (preco_de_venda BETWEEN 1 AND 999)
);
```

```sql
CREATE TABLE receita (
    identificador_receita ID PRIMARY KEY,
    consumivel_produzido ID NOT NULL REFERENCES consumivel(identificador_consumivel)
);
```

```sql
CREATE TABLE ingrediente_consumivel (
    identificador_receita ID NOT NULL REFERENCES receita(identificador_receita),
    identificador_consumivel ID NOT NULL REFERENCES consumivel(identificador_consumivel),
    PRIMARY KEY (identificador_receita, identificador_consumivel)
);
```

```sql
CREATE TABLE ingrediente_nao_consumivel (
    identificador_receita ID NOT NULL REFERENCES receita(identificador_receita),
    identificador_nao_consumivel ID NOT NULL REFERENCES nao_consumivel(identificador_nao_consumivel),
    PRIMARY KEY (identificador_receita, identificador_nao_consumivel)
);
```

```sql
CREATE TABLE efeito (
    identificador_efeito ID PRIMARY KEY,
    nome CHAR(15) NOT NULL CHECK (nome IN ('Cura', 'Energia', 'Vida Máxima', 'Energia Máxima', 'Ataque', 'Sorte', 'Eletrificado', 'Congelado', 'Molhado', 'Envenenado', 'Sangramento', 'Queimadura', 'Tontura', 'Cegueira', 'Purificação')),
    valor SMALLINT CHECK (
        (nome = 'Cura' AND valor BETWEEN 1 AND 20) OR
        (nome = 'Energia' AND valor BETWEEN 1 AND 15) OR
        (nome = 'Vida Máxima' AND valor BETWEEN 1 AND 15) OR
        (nome = 'Energia Máxima' AND valor BETWEEN 1 AND 10) OR
        (nome = 'Ataque' AND valor BETWEEN 1 AND 10) OR
        (nome = 'Sorte' AND valor BETWEEN 1 AND 7) OR
        (nome = 'Eletrificado' AND valor BETWEEN 0 AND 1) OR
        (nome = 'Congelado' AND valor BETWEEN 0 AND 1) OR
        (nome = 'Molhado' AND valor BETWEEN 0 AND 1) OR
        (nome = 'Envenenado' AND valor BETWEEN 0 AND 1) OR
        (nome = 'Sangramento' AND valor BETWEEN 0 AND 1) OR
        (nome = 'Queimadura' AND valor BETWEEN 0 AND 1) OR
        (nome = 'Tontura' AND valor BETWEEN 0 AND 1) OR
        (nome = 'Cegueira' AND valor BETWEEN 0 AND 1) OR
        (nome = 'Purificação' AND valor IS NULL)
    )
);
```

```sql
CREATE TABLE efeito_acessorio (
    identificador_efeito ID NOT NULL REFERENCES efeito(identificador_efeito),
    identificador_acessorio ID NOT NULL REFERENCES acessorio(identificador_acessorio),
    PRIMARY KEY (identificador_efeito, identificador_acessorio)
);
```

```sql
CREATE TABLE efeito_consumivel (
    identificador_efeito ID NOT NULL REFERENCES efeito(identificador_efeito),
    identificador_consumivel ID NOT NULL REFERENCES consumivel(identificador_consumivel),
    PRIMARY KEY (identificador_efeito, identificador_consumivel)
);
```

```sql
CREATE TABLE habilidade (
    identificador_habilidade ID PRIMARY KEY,
    identificador_efeito ID REFERENCES efeito(identificador_efeito),
    nome CHAR(50) NOT NULL,
    descricao CHAR(200) NOT NULL,
    tipo_de_ataque CHAR(10) NOT NULL CHECK (tipo_de_ataque IN ('soco', 'espada', 'estilingue', 'arco', 'fruta')),
    tipo_de_alvo CHAR(15) NOT NULL CHECK (tipo_de_alvo IN ('fila', 'alvo_terrestre', 'terrestre', 'alvo_livre', 'area')),
    dano SMALLINT NOT NULL,
    custo SMALLINT DEFAULT 0
);
```

```sql
CREATE TABLE habilidade_arma (
    identificador_habilidade ID NOT NULL REFERENCES habilidade(identificador_habilidade),
    identificador_arma ID NOT NULL REFERENCES arma (identificador_arma),
    PRIMARY KEY (identificador_habilidade, identificador_arma)
);
```

```sql
CREATE TABLE habilidade_fruta (
    identificador_habilidade ID NOT NULL REFERENCES habilidade(identificador_habilidade),
    identificador_fruta ID NOT NULL REFERENCES fruta (identificador_fruta),
    PRIMARY KEY (identificador_habilidade, identificador_fruta)
);
```

```sql
CREATE TABLE progresso (
    identificador_progresso ID PRIMARY KEY,
    numero_do_slot SMALLINT NOT NULL UNIQUE CHECK (numero_do_slot BETWEEN 1 AND 3),
    data_ultimo_salvamento TIMESTAMP DEFAULT now(),
    ocupado BOOLEAN NOT NULL DEFAULT FALSE
);
```

```sql
CREATE TABLE ilha (
    identificador_ilha ID PRIMARY KEY,
    nome CHAR(30) CHECK (nome IN ('Ilha de Borabóia', 'Cidade de Lurien', 'Ilha Glacial de Frimora', 'Cactuaraquara', 'Nublária', 'Quartel Naval D-57'))
);
```

```sql
CREATE TABLE area (
    identificador_area ID PRIMARY KEY,
    identificador_ilha ID REFERENCES ilha(identificador_ilha),
    nome CHAR(30) CHECK (nome ~ '^[a-zA-Z áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\\-]+$'),
    tipo_area CHAR(25) NOT NULL CHECK (tipo_area IN ('Área de combate', 'Área neutra', 'Vila', 'Porto', 'Loja', 'Yomotsu Hirasaka')),
    chave_imagem_fundo CHAR(50) CHECK (chave_imagem_fundo ~ '^[a-z _]+$'),
    chave_imagem_frente CHAR(50) CHECK (chave_imagem_frente ~ '^[a-z _]+$'),
    CHECK (
        tipo_area = 'Yomotsu Hirasaka' OR identificador_ilha IS NOT NULL
    )
);
```

```sql
CREATE TABLE conexao_entre_areas (
    identificador_area_origem ID NOT NULL REFERENCES area(identificador_area),
    identificador_area_destino ID NOT NULL REFERENCES area(identificador_area),
    ponto_geracao_x SMALLINT CHECK (ponto_geracao_x BETWEEN 0 AND 5000),
    ponto_geracao_y SMALLINT CHECK (ponto_geracao_y BETWEEN 0 AND 5000),
    orientacao CHAR(8) CHECK (orientacao IN ('esquerda', 'direita')),
    PRIMARY KEY (identificador_area_origem, identificador_area_destino)
);
```

```sql
CREATE TABLE tipo_personagem (
    identificador_personagem ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('hbt', 'rct', 'coz', 'ven', 'ali', 'jog', 'lac', 'che'))
);
```

```sql
CREATE TABLE jogador (
    identificador_jogador ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    identificador_progresso ID UNIQUE REFERENCES progresso(identificador_progresso),
    nome char(6) NOT NULL CHECK (nome IN ('Silvie', 'Shuan')),
    descricao CHAR(300),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    energia SMALLINT CHECK (energia BETWEEN 5 AND 35),
    vida SMALLINT CHECK (vida BETWEEN 10 AND 70),
    nivel SMALLINT CHECK (nivel BETWEEN 0 AND 60),
    sorte SMALLINT CHECK (sorte BETWEEN 1 AND 10),
    vida_atual SMALLINT CHECK (vida_atual BETWEEN 0 AND vida),
    experiencia_atual SMALLINT CHECK (experiencia_atual BETWEEN 0 AND 600),
    moedas_totais SMALLINT NOT NULL CHECK (moedas_totais BETWEEN 0 AND 999)
);
```

```sql
CREATE TABLE aliado (
    identificador_aliado ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    identificador_progresso ID UNIQUE REFERENCES progresso(identificador_progresso),
    nome char(6) NOT NULL CHECK (nome IN ('Silvie', 'Shuan')),
    descricao CHAR(300),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida SMALLINT  CHECK (vida BETWEEN 10 AND 70),
    nivel SMALLINT CHECK (nivel BETWEEN 0 AND 60),
    vida_atual SMALLINT CHECK (vida_atual BETWEEN 0 AND vida)
);
```

```sql
CREATE TABLE chefe (
    identificador_chefe ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    nome CHAR(28),
    descricao CHAR(100),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 10 AND 60),
    experiencia SMALLINT,
    moedas_totais SMALLINT NOT NULL CHECK (moedas_totais BETWEEN 0 AND 999)
);
```

```sql
CREATE TABLE lacaio (
    identificador_lacaio ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    nome CHAR(20),
    descricao CHAR(100),
    vida SMALLINT,
    nivel SMALLINT CHECK (nivel BETWEEN 0 AND 60),
    experiencia SMALLINT,
    tempo_reacao SMALLINT
);
```

```sql
CREATE TABLE habitante (
    identificador_habitante ID PRIMARY KEY REFERENCES tipo_personagem(identificador_personagem),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    nome CHAR(27),
    descricao CHAR(500),
    chave_imagem CHAR(50) CHECK (chave_imagem ~ '^[a-z _]+$'),
    tipo_habitante CHAR(3) NOT NULL CHECK (tipo_habitante IN ('hbt', 'ven', 'coz', 'rct')),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    especialidade char(3) CHECK (especialidade IN ('arm', 'ace', 'com')),
    moedas_totais SMALLINT NOT NULL CHECK (moedas_totais BETWEEN 0 AND 999)
);
```

```sql
CREATE TABLE instancia_lacaio (
    identificador_instancia_lacaio ID PRIMARY KEY,
    identificador_lacaio ID NOT NULL REFERENCES lacaio(identificador_lacaio),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    coordenada_x SMALLINT CHECK (coordenada_x BETWEEN 0 AND 5000),
    coordenada_y SMALLINT CHECK (coordenada_y BETWEEN 0 AND 5000),
    moedas_totais SMALLINT NOT NULL CHECK (moedas_totais BETWEEN 0 AND 999)
);
```

```sql
CREATE TABLE barco (
    identificador_barco ID PRIMARY KEY,
    identificador_progresso ID NOT NULL REFERENCES progresso(identificador_progresso),
    tipo_barco CHAR(3) NOT NULL CHECK (tipo_barco IN ('can', 'vel', 'nav')),
    nome CHAR(30) NOT NULL,
    descricao CHAR (150) NOT NULL,
    estado CHAR (9) NOT NULL CHECK (estado IN ('bloquedo', 'adquirido', 'destruido'))
);
```

```sql
CREATE TABLE habilidade_personagem (
    identificador_personagem ID,
    identificador_habilidade ID,
    PRIMARY KEY (identificador_personagem, identificador_habilidade),
    FOREIGN KEY (identificador_personagem) REFERENCES tipo_personagem(identificador_personagem),
    FOREIGN KEY (identificador_habilidade) REFERENCES habilidade(identificador_habilidade)
);
```

```sql
CREATE TABLE receitas_conhecidas (
    identificador_progresso ID,
    identificador_receita ID,
    PRIMARY KEY (identificador_progresso, identificador_receita),
    FOREIGN KEY (identificador_progresso) REFERENCES progresso(identificador_progresso),
    FOREIGN KEY (identificador_receita) REFERENCES receita(identificador_receita)
);
```

```sql
CREATE TABLE inventario (
    identificador_inventario ID PRIMARY KEY,
    identificador_personagem ID NOT NULL REFERENCES tipo_personagem(identificador_personagem),
    identificador_progresso ID NOT NULL REFERENCES progresso(identificador_progresso),
    tipo_inventario CHAR(3) DEFAULT 'moc' NOT NULL CHECK (tipo_inventario IN ('moc', 'kit'))
);
```

```sql
CREATE TABLE item_inventario (
    identificador_inventario ID,
    identificador_item ID,
    quantidade SMALLINT DEFAULT 0 CHECK (quantidade BETWEEN 0 AND 99),
    PRIMARY KEY (identificador_inventario, identificador_item),
    FOREIGN KEY (identificador_inventario) REFERENCES inventario(identificador_inventario),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item)
);
```

```sql
CREATE TABLE ilha_visitada (
    identificador_progresso ID REFERENCES progresso(identificador_progresso),
    identificador_ilha ID REFERENCES ilha(identificador_ilha),
    PRIMARY KEY (identificador_progresso, identificador_ilha),
    visitada BOOLEAN NOT NULL DEFAULT FALSE
);
```

```sql
CREATE TABLE conexao_entre_ilhas (
    identificador_ilha_a ID NOT NULL REFERENCES ilha(identificador_ilha),
    identificador_ilha_b ID NOT NULL REFERENCES ilha(identificador_ilha),
    identificador_progresso ID NOT NULL REFERENCES progresso(identificador_progresso),
    bloqueada BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (identificador_ilha_a, identificador_ilha_b, identificador_progresso)
);
```

```sql
CREATE TABLE area_visitada (
    identificador_progresso ID REFERENCES progresso(identificador_progresso),
    identificador_area ID REFERENCES area(identificador_area),
    PRIMARY KEY (identificador_progresso, identificador_area),
    visitada BOOLEAN NOT NULL DEFAULT FALSE
);
```

```sql
CREATE TABLE estado_instancia_lacaio (
    identificador_progresso ID REFERENCES progresso(identificador_progresso),
    identificador_instancia_lacaio ID REFERENCES instancia_lacaio(identificador_instancia_lacaio),
    identificador_area_atual ID REFERENCES area(identificador_area),
    vida_atual SMALLINT,
    data_da_morte TIMESTAMP DEFAULT NULL,
    PRIMARY KEY (identificador_progresso, identificador_instancia_lacaio)
);
```

```sql
CREATE TABLE estado_chefe (
    identificador_progresso ID REFERENCES progresso(identificador_progresso),
    identificador_chefe ID REFERENCES chefe(identificador_chefe),
    identificador_area_atual ID REFERENCES area(identificador_area),
    vida_atual SMALLINT,
    data_da_morte TIMESTAMP DEFAULT NULL,
    PRIMARY KEY (identificador_progresso, identificador_chefe)
);
```

```sql
CREATE TABLE negociacao (
    identificador_negociacao ID PRIMARY KEY,
    identificador_item ID NOT NULL REFERENCES tipo_item(identificador_item),
    identificador_jogador ID NOT NULL REFERENCES jogador(identificador_jogador),
    identificador_vendedor ID NOT NULL REFERENCES habitante(identificador_habitante),
    quantidade SMALLINT CHECK (quantidade BETWEEN 0 AND 99),
    preco_final SMALLINT,
    tipo_negociacao CHAR(6) NOT NULL CHECK (tipo_negociacao IN ('compra', 'venda'))
);
```

```sql
CREATE TABLE missao (
    identificador_missao ID PRIMARY KEY,
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    identificador_recrutador ID REFERENCES habitante(identificador_habitante),
    identificador_missao_dependente ID REFERENCES missao(identificador_missao),
    descricao CHAR(100),
    nome CHAR(50) NOT NULL,
    nivel_de_desbloqueio SMALLINT NOT NULL CHECK (nivel_de_desbloqueio BETWEEN 0 AND 60)
);
```

```sql
CREATE TABLE dialogo (
    identificador_dialogo ID PRIMARY KEY,
    identificador_personagem ID REFERENCES tipo_personagem(identificador_personagem),
    identificador_missao ID REFERENCES missao(identificador_missao),
    sequencia_local SMALLINT CHECK (sequencia_local > 0),
    genero CHAR(1) CHECK (genero IN ('M', 'F')),
    dialogo CHAR(500)
);
```

```sql
CREATE TABLE estado_missao (
    identificador_missao ID REFERENCES missao(identificador_missao),
    identificador_progresso ID REFERENCES progresso(identificador_progresso),
    estado CHAR(9) NOT NULL DEFAULT 'pendente' CHECK (estado IN ('concluida', 'aceita', 'pendente')),
    PRIMARY KEY (identificador_missao, identificador_progresso)
);
```

```sql
CREATE TABLE tipo_elemento_espacial (
    identificador_elemento_espacial ID PRIMARY KEY,
    tipo CHAR(3) NOT NULL CHECK (tipo IN ('ari', 'obs', 'cam'))
);
```

```sql
CREATE TABLE obstaculo (
    identificador_obstaculo ID PRIMARY KEY REFERENCES tipo_elemento_espacial(identificador_elemento_espacial),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    chave_imagem CHAR(50) CHECK (chave_imagem ~ '^[a-z _]+$'),
    x SMALLINT CHECK (x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (y BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (largura BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (altura BETWEEN 0 AND 5000)
);
```

```sql
CREATE TABLE caminho (
    identificador_caminho ID PRIMARY KEY REFERENCES tipo_elemento_espacial(identificador_elemento_espacial),
    identificador_area ID NOT NULL REFERENCES area(identificador_area),
    tipo_terreno CHAR(6) DEFAULT 'normal' CHECK (tipo_terreno IN ('normal', 'neve', 'arena')),
    x SMALLINT CHECK (x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (y BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (largura BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (altura BETWEEN 0 AND 5000)
);
```

```sql
CREATE TABLE area_interativa (
    identificador_area_interativa ID PRIMARY KEY REFERENCES tipo_elemento_espacial(identificador_elemento_espacial),
    identificador_area_origem ID NOT NULL REFERENCES area(identificador_area),
    identificador_area_destino ID REFERENCES area(identificador_area),
    identificador_missao ID REFERENCES missao(identificador_missao),
    chave_imagem CHAR(50) CHECK (chave_imagem ~ '^[a-z _]+$'),
    x SMALLINT CHECK (x BETWEEN 0 AND 5000),
    y SMALLINT CHECK (y BETWEEN 0 AND 5000),
    largura SMALLINT CHECK (largura BETWEEN 0 AND 5000),
    altura SMALLINT CHECK (altura BETWEEN 0 AND 5000),
    chance_sucesso DECIMAL DEFAULT 1.0 CHECK (chance_sucesso BETWEEN 0.0 AND 1.0),
    tipo_evento CHAR(10) NOT NULL CHECK (
        tipo_evento IN ('embarcar', 'investigar', 'mudar_area', 'missao')
    ),
    metodo_ativacao CHAR(7) NOT NULL CHECK (metodo_ativacao IN ('ativo', 'passivo')),
    ativa BOOLEAN NOT NULL DEFAULT TRUE,
    CHECK (
        (tipo_evento <> 'mudar_area' OR identificador_area_destino IS NOT NULL)
        AND
        (tipo_evento <> 'missao' OR identificador_missao IS NOT NULL)
    )
);
```

```sql
CREATE TABLE recompensa_de_exploracao (
    identificador_recompensa ID PRIMARY KEY,
    identificador_area_interativa ID NOT NULL REFERENCES area_interativa(identificador_area_interativa),
    data_da_tentativa TIMESTAMP NOT NULL DEFAULT now()
);
```

```sql
CREATE TABLE item_missao (
    identificador_missao ID,
    identificador_item ID,
    PRIMARY KEY (identificador_missao, identificador_item),
    FOREIGN KEY (identificador_missao) REFERENCES missao(identificador_missao),
    FOREIGN KEY (identificador_item) REFERENCES tipo_item(identificador_item)
);
```

```sql
CREATE TABLE jogador_equipamento (
    identificador_jogador ID PRIMARY KEY REFERENCES jogador(identificador_jogador),
    identificador_arma ID REFERENCES arma(identificador_arma),
    identificador_acessorio ID REFERENCES acessorio(identificador_acessorio),
    identificador_fruta ID REFERENCES fruta(identificador_fruta)
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