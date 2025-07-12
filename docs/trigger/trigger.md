# Triggers e Stored Procedures

---

## Introdução

**Triggers** e **Stored Procedures** são componentes poderosos e essenciais em sistemas de gerenciamento de banco de dados (SGBDs), que estendem a funcionalidade de um banco de dados além das operações DML básicas. Embora ambos envolvam blocos de código SQL armazenados no banco de dados, eles servem a propósitos distintos e são acionados de maneiras diferentes.

As **Stored Procedures** (ou Procedimentos Armazenados) são sub-rotinas ou programas que podem ser armazenados e executados diretamente no servidor do banco de dados. Elas encapsulam uma série de operações SQL e lógica de negócios, podendo ser chamadas a qualquer momento por aplicações ou usuários. Isso promove a reutilização de código, melhora o desempenho e aumenta a segurança.

Os **Triggers** (ou Gatilhos), por outro lado, são blocos de código SQL que são executados automaticamente em resposta a eventos específicos no banco de dados, como operações DML (INSERT, UPDATE, DELETE) em uma tabela. Eles são usados para impor regras de negócio complexas, manter a integridade referencial ou auditar alterações nos dados.



---

## Metodologia 

O aprendizado e a utilização de Triggers e Stored Procedures geralmente seguem uma abordagem prática e incremental. A metodologia pode ser dividida nas seguintes etapas:

---

### Triggers e Stored Procedures

#### Compreensão dos Conceitos Fundamentais:

* Entender o que é um **Trigger** e como ele se diferencia de outros objetos do banco de dados.
* Diferenciar entre Triggers `BEFORE` (antes do evento) e `AFTER` (depois do evento), e Triggers `FOR EACH ROW` (para cada linha afetada) e `FOR EACH STATEMENT` (para cada instrução).
* Identificar os eventos DML (INSERT, UPDATE, DELETE) que podem acionar um **Trigger**.
* Compreender as variáveis especiais (como `OLD` e `NEW` em alguns SGBDs) que permitem acessar os dados antes e depois da modificação.
* Entender o que é uma **Stored Procedure** e seus benefícios (reutilização, desempenho, segurança).
* Diferenciar entre **Stored Procedures** e **Funções** (Functions), notando que Stored Procedures podem realizar operações DML e não necessariamente retornam um valor.
* Compreender os conceitos de parâmetros de entrada (`IN`), saída (`OUT`) e entrada/saída (`INOUT`).
* Familiarizar-se com estruturas de controle de fluxo dentro de **Stored Procedures** (e.g., `IF/ELSE`, `LOOP`, `WHILE`).

#### Aprendizado dos Comandos Básicos:

* **CREATE TRIGGER**: Aprender a sintaxe para criar um **Trigger**, especificando o nome, o evento (e.g., `AFTER INSERT ON tabela`), o tempo de execução (`BEFORE` ou `AFTER`) e a lógica do Trigger.
* **ALTER TRIGGER**: Entender como modificar ou desabilitar um **Trigger** existente.
* **DROP TRIGGER**: Aprender a remover um **Trigger** do banco de dados.
**CREATE PROCEDURE**: Aprender a sintaxe para criar uma **Stored Procedure**, definindo seu nome, parâmetros e o bloco de código SQL.
* **ALTER PROCEDURE**: Entender como modificar uma **Stored Procedure** existente.
* **DROP PROCEDURE**: Aprender a remover uma **Stored Procedure**.

## Códigos

```sql
-- 1. DOMÍNIO “ID” — formato fixo aaa999
CREATE DOMAIN ID AS CHAR(6)
    CHECK (VALUE ~ '^[a-z]{3}[0-9]{3}$');

COMMENT ON DOMAIN ID IS
    'Identificador gerado por trigger: 3 letras + 3 dígitos (001-999). Inserção manual proibida.';
```

```sql
CREATE FUNCTION public.gerar_id()
RETURNS trigger
LANGUAGE plpgsql AS
$$
DECLARE
    prefixo text;
    nome_da_sequencia text;
    numero_serial bigint;
BEGIN
    -- 2.1 Bloqueia inserção manual
    IF TG_TABLE_NAME = 'habilidade' AND NEW.identificador_habilidade IS NOT NULL THEN
        RAISE EXCEPTION 'A coluna "identificador_habilidade" é gerada automaticamente; não forneça valor manualmente.';
    ELSIF TG_TABLE_NAME = 'receita' AND NEW.identificador_receita IS NOT NULL THEN
        RAISE EXCEPTION 'A coluna "identificador_receita" é gerada automaticamente; não forneça valor manualmente.';
    -- Adicione os outros casos conforme necessário

    -- 2.2 Obtém o prefixo
    prefixo := lower(to_jsonb(NEW)->>'tipo');
    IF prefixo IS NULL THEN
        prefixo := lower(substr(TG_TABLE_NAME, 1, 3));
    END IF;

    -- 2.3 Valida o prefixo
    IF prefixo !~ '^[a-z]{3}$' THEN
        RAISE EXCEPTION 'prefixo inválido: precisa ser 3 letras (a-z). Obtido = "%".', prefixo;
    END IF;

    -- 2.4 Gera nome da sequência
    nome_da_sequencia := format('%I_%s_seq', TG_TABLE_NAME, prefixo);
    PERFORM 1 FROM pg_class WHERE relkind = 'S' AND relname = nome_da_sequencia;
    IF NOT FOUND THEN
        EXECUTE format('CREATE SEQUENCE %I START 1', nome_da_sequencia);
    END IF;

    -- 2.5 Pega o número
    EXECUTE format('SELECT nextval(%L)', nome_da_sequencia) INTO numero_serial;

    -- 2.6 Monta o ID
    IF TG_TABLE_NAME = 'habilidade' THEN
        NEW.identificador_habilidade := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'receita' THEN
        NEW.identificador_receita := prefixo || lpad(numero_serial::text, 3, '0');
    -- Continue para os demais casos
    END IF;

    RETURN NEW;
END;
$$;
```

```sql
CREATE FUNCTION public.gerar_id_tabelas_personagem()
RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    novo_id    ID;
    prefixo  CHAR(3);
BEGIN
    IF TG_TABLE_NAME = 'jogador' THEN
        IF NEW.identificador_jogador IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_jogador" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'jog';
    ELSIF TG_TABLE_NAME = 'aliado' THEN
        IF NEW.identificador_aliado IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_aliado" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'ali';
    ELSIF TG_TABLE_NAME = 'chefe' THEN
        IF NEW.identificador_chefe IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_chefe" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'che';
    ELSIF TG_TABLE_NAME = 'lacaio' THEN
        IF NEW.identificador_lacaio IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_lacaio" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'lac';
    ELSIF TG_TABLE_NAME = 'habitante' THEN
        IF NEW.identificador_habitante IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_habitante" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := lower(to_jsonb(NEW)->>'tipo_habitante');
    ELSE
        RAISE EXCEPTION 'Trigger inesperado para a tabela %', TG_TABLE_NAME;
    END IF;

    INSERT INTO tipo_personagem (tipo)
    VALUES (prefixo)
    RETURNING identificador_personagem INTO novo_id;

    IF TG_TABLE_NAME = 'jogador' THEN
        NEW.identificador_jogador := novo_id;
    ELSIF TG_TABLE_NAME = 'aliado' THEN
        NEW.identificador_aliado := novo_id;
    ELSIF TG_TABLE_NAME = 'chefe' THEN
        NEW.identificador_chefe := novo_id;
    ELSIF TG_TABLE_NAME = 'lacaio' THEN
        NEW.identificador_lacaio := novo_id;
    ELSIF TG_TABLE_NAME = 'habitante' THEN
        NEW.identificador_habitante := novo_id;
    END IF;

    RETURN NEW;
END;
$$;
```
```sql
CREATE FUNCTION public.gerar_id_tabelas_elemento_espacial()
RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    novo_id   ID;
    prefixo   CHAR(3);
BEGIN
    IF TG_TABLE_NAME = 'caminho' THEN
        IF NEW.identificador_caminho IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_caminho" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'cam';
    ELSIF TG_TABLE_NAME = 'obstaculo' THEN
        IF NEW.identificador_obstaculo IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_obstaculo" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'obs';
    ELSIF TG_TABLE_NAME = 'area_interativa' THEN
        IF NEW.identificador_area_interativa IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_area_interativa" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'ari';
    ELSE
        RAISE EXCEPTION 'Trigger usada em tabela incorreta: %', TG_TABLE_NAME;
    END IF;

    INSERT INTO tipo_elemento_espacial (tipo)
    VALUES (prefixo)
    RETURNING identificador_elemento_espacial INTO novo_id;

    IF TG_TABLE_NAME = 'caminho' THEN
        NEW.identificador_caminho := novo_id;
    ELSIF TG_TABLE_NAME = 'obstaculo' THEN
        NEW.identificador_obstaculo := novo_id;
    ELSIF TG_TABLE_NAME = 'area_interativa' THEN
        NEW.identificador_area_interativa := novo_id;
    END IF;

    RETURN NEW;
END;
$$;
```

```sql
CREATE FUNCTION public.gerar_id_tabelas_item()
RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    novo_id   ID;
    tipo      CHAR(3);
BEGIN
    IF TG_TABLE_NAME = 'acessorio' THEN
        IF NEW.identificador_acessorio IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_acessorio" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'ace';
    ELSIF TG_TABLE_NAME = 'arma' THEN
        IF NEW.identificador_arma IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_arma" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'arm';
    ELSIF TG_TABLE_NAME = 'fruta' THEN
        IF NEW.identificador_fruta IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_fruta" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'fru';
    ELSIF TG_TABLE_NAME = 'consumivel' THEN
        IF NEW.identificador_consumivel IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_consumivel" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'con';
    ELSIF TG_TABLE_NAME = 'nao_consumivel' THEN
        IF NEW.identificador_nao_consumivel IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_nao_consumivel" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'ncn';
    ELSE
        RAISE EXCEPTION 'Trigger usada em tabela não esperada: %', TG_TABLE_NAME;
    END IF;

    INSERT INTO tipo_item (tipo)
    VALUES (tipo)
    RETURNING identificador_item INTO novo_id;

    IF TG_TABLE_NAME = 'acessorio' THEN
        NEW.identificador_acessorio := novo_id;
    ELSIF TG_TABLE_NAME = 'arma' THEN
        NEW.identificador_arma := novo_id;
    ELSIF TG_TABLE_NAME = 'fruta' THEN
        NEW.identificador_fruta := novo_id;
    ELSIF TG_TABLE_NAME = 'consumivel' THEN
        NEW.identificador_consumivel := novo_id;
    ELSIF TG_TABLE_NAME = 'nao_consumivel' THEN
        NEW.identificador_nao_consumivel := novo_id;
    END IF;

    RETURN NEW;
END;
$$;
```

```sql
CREATE OR REPLACE FUNCTION public.func_limpar_item_inventario_quantidade_zero()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantidade <= 0 THEN
        DELETE FROM item_inventario
        WHERE identificador_inventario = NEW.identificador_inventario
          AND identificador_item = NEW.identificador_item;
        RETURN NULL; -- Não insere/atualiza a linha se a quantidade for 0 ou menos
    END IF;
    RETURN NEW; -- Continua a operação de INSERT/UPDATE
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_limpar_item_inventario_quantidade_zero
BEFORE INSERT OR UPDATE ON item_inventario
FOR EACH ROW
EXECUTE FUNCTION public.func_limpar_item_inventario_quantidade_zero();

COMMENT ON FUNCTION public.func_limpar_item_inventario_quantidade_zero() IS
'Função para o trigger que limpa registros de item_inventario quando a quantidade chega a zero ou menos.';
COMMENT ON TRIGGER trg_limpar_item_inventario_quantidade_zero IS
'Trigger que executa a função func_limpar_item_inventario_quantidade_zero ANTES de INSERT ou UPDATE em item_inventario, removendo itens com quantidade <= 0.';
```

```sql
CREATE OR REPLACE PROCEDURE public.sp_gerenciar_equipamento_jogador(
    p_identificador_jogador ID,
    p_identificador_arma ID DEFAULT NULL,
    p_identificador_acessorio ID DEFAULT NULL,
    p_identificador_fruta ID DEFAULT NULL
)
LANGUAGE plpgsql AS $$
BEGIN
    -- Tenta inserir ou atualizar o equipamento do jogador
    INSERT INTO jogador_equipamento (identificador_jogador, identificador_arma, identificador_acessorio, identificador_fruta)
    VALUES (p_identificador_jogador, p_identificador_arma, p_identificador_acessorio, p_identificador_fruta)
    ON CONFLICT (identificador_jogador) DO UPDATE
    SET
        identificador_arma = COALESCE(p_identificador_arma, jogador_equipamento.identificador_arma),
        identificador_acessorio = COALESCE(p_identificador_acessorio, jogador_equipamento.identificador_acessorio),
        identificador_fruta = COALESCE(p_identificador_fruta, jogador_equipamento.identificador_fruta);
    
END;
$$;

COMMENT ON PROCEDURE public.sp_gerenciar_equipamento_jogador(ID, ID, ID, ID) IS
'Gerencia o equipamento de um jogador. Insere ou atualiza os IDs de arma, acessório e fruta.
Passe NULL para desequipar um slot específico.
Ex: CALL sp_gerenciar_equipamento_jogador(''jog001'', p_identificador_arma := ''arm001''); -- Equipa arma
Ex: CALL sp_gerenciar_equipamento_jogador(''jog001'', p_identificador_arma := NULL);    -- Desequipa arma
Ex: CALL sp_gerenciar_equipamento_jogador(''jog001'', p_identificador_acessorio := ''ace001''); -- Equipa acessório (mantém arma)
';
```
```sql
CREATE OR REPLACE FUNCTION public.func_jogador_subir_nivel()
RETURNS TRIGGER AS $$
DECLARE
    xp_necessario_proximo_nivel INT;
    excedente_xp INT;
BEGIN
    -- Calcula o XP necessário para o próximo nível (ex: Nivel 1 precisa de 100, Nivel 2 precisa de 200, Nivel N precisa de N*100)
    -- Assegura que o XP mínimo seja 100 para o nível 1 (nível 0)
    xp_necessario_proximo_nivel := (NEW.nivel + 1) * 100; 

    -- Loop para permitir múltiplas subidas de nível se o XP for suficiente
    WHILE NEW.experiencia_atual >= xp_necessario_proximo_nivel LOOP
        NEW.nivel := NEW.nivel + 1;
        NEW.vida := NEW.vida + 5;        -- Aumenta vida máxima
        NEW.energia := NEW.energia + 2;  -- Aumenta energia máxima
        NEW.vida_atual := NEW.vida;      -- Cura o jogador para a nova vida máxima

        -- Reduz a experiência_atual pelo custo do nível, mantendo o excedente
        NEW.experiencia_atual := NEW.experiencia_atual - xp_necessario_proximo_nivel;
        
        RAISE NOTICE 'Jogador % subiu para o Nível %! Nova Vida: %, Nova Energia: %', NEW.nome, NEW.nivel, NEW.vida, NEW.energia;

        -- Recalcula XP necessário para o *próximo* próximo nível
        xp_necessario_proximo_nivel := (NEW.nivel + 1) * 100;
    END LOOP;

    RETURN NEW; -- Retorna a linha modificada para que a atualização continue
END;
$$ LANGUAGE plpgsql;

-- Trigger: trg_jogador_subir_nivel
CREATE TRIGGER trg_jogador_subir_nivel
BEFORE UPDATE OF experiencia_atual ON jogador
FOR EACH ROW
WHEN (NEW.experiencia_atual > OLD.experiencia_atual) -- Só dispara se a XP aumentou
EXECUTE FUNCTION public.func_jogador_subir_nivel();

COMMENT ON FUNCTION public.func_jogador_subir_nivel() IS
'Função para o trigger que gerencia a subida de nível do jogador, ajustando atributos e experiência.';
COMMENT ON TRIGGER trg_jogador_subir_nivel IS
'Trigger que executa a função func_jogador_subir_nivel ANTES de UPDATES na experiencia_atual do jogador, para subir de nível automaticamente.';

```
```sql

-- Stored Procedure: sp_derrotar_lacaio
CREATE OR REPLACE PROCEDURE public.sp_derrotar_lacaio(
    p_identificador_instancia_lacaio ID,
    p_identificador_jogador ID
)
LANGUAGE plpgsql AS $$
DECLARE
    v_identificador_lacaio ID;
    v_nome_lacaio CHAR(20);
    v_experiencia_lacaio SMALLINT;
    v_moedas_instancia SMALLINT;
    v_id_inventario_lacaio ID;
    v_id_inventario_jogador ID;
    item_do_lacaio RECORD;
BEGIN
    
    SELECT
        il.identificador_lacaio,
        l.nome,
        l.experiencia,
        il.moedas_totais
    INTO
        v_identificador_lacaio,
        v_nome_lacaio,
        v_experiencia_lacaio,
        v_moedas_instancia
    FROM instancia_lacaio il
    JOIN lacaio l ON il.identificador_lacaio = l.identificador_lacaio
    WHERE il.identificador_instancia_lacaio = p_identificador_instancia_lacaio;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Instância do lacaio % não encontrada.', p_identificador_instancia_lacaio;
    END IF;

    -- 3. Atualizar vida da instância do lacaio para 0 (marcar como "morto")
    UPDATE instancia_lacaio
    SET vida_atual = 0
    WHERE identificador_instancia_lacaio = p_identificador_instancia_lacaio;

    -- 4. Adicionar XP e moedas ao jogador
    UPDATE jogador
    SET
        experiencia_atual = experiencia_atual + v_experiencia_lacaio,
        moedas_totais = moedas_totais + v_moedas_instancia
    WHERE identificador_jogador = p_identificador_jogador;

    -- 5. Obter IDs dos inventários
    SELECT identificador_inventario INTO v_id_inventario_lacaio
    FROM inventario
    WHERE identificador_personagem = v_identificador_lacaio AND tipo_inventario = 'ger';

    SELECT identificador_inventario INTO v_id_inventario_jogador
    FROM inventario
    WHERE identificador_personagem = p_identificador_jogador AND tipo_inventario = 'ger';

    IF v_id_inventario_lacaio IS NULL THEN
        RAISE NOTICE 'Lacaio % não possui inventário geral para saquear.', v_nome_lacaio;
    END IF;
    IF v_id_inventario_jogador IS NULL THEN
        RAISE EXCEPTION 'Jogador % não possui inventário geral para receber itens.', p_identificador_jogador;
    END IF;

    -- 6. Transferir itens do inventário do lacaio para o inventário do jogador
    IF v_id_inventario_lacaio IS NOT NULL THEN
        FOR item_do_lacaio IN (SELECT identificador_item, quantidade FROM item_inventario WHERE identificador_inventario = v_id_inventario_lacaio) LOOP
            -- Adicionar item ao inventário do jogador (UPSERT)
            INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
            VALUES (v_id_inventario_jogador, item_do_lacaio.identificador_item, item_do_lacaio.quantidade)
            ON CONFLICT (identificador_inventario, identificador_item) DO UPDATE
            SET quantidade = item_inventario.quantidade + EXCLUDED.quantidade;

            -- Remover item do inventário do lacaio
            DELETE FROM item_inventario
            WHERE identificador_inventario = v_id_inventario_lacaio
              AND identificador_item = item_do_lacaio.identificador_item;
        END LOOP;
    END IF;

    -- 7. Deletar a instância do lacaio do mundo (se necessário, ou manter para re-spawn)
    DELETE FROM instancia_lacaio WHERE identificador_instancia_lacaio = p_identificador_instancia_lacaio;

    RAISE NOTICE 'Lacaio % (instância: %) derrotado. XP e moedas concedidos ao jogador %.', v_nome_lacaio, p_identificador_instancia_lacaio, p_identificador_jogador;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Erro ao derrotar lacaio %: %', p_identificador_instancia_lacaio, SQLERRM;
END;
$$;

COMMENT ON PROCEDURE public.sp_derrotar_lacaio(ID, ID) IS
'Gerencia a derrota de um lacaio: atualiza vida, transfere XP, moedas e itens para o jogador, e remove a instância do lacaio.';

```
```sql

CREATE FUNCTION validar_efeito()
RETURNS TRIGGER AS $$
BEGIN
    -- Efeitos que exigem valor numérico
    IF NEW.nome = 'Cura' AND (NEW.valor IS NULL OR NEW.valor NOT BETWEEN 1 AND 20) THEN
        RAISE EXCEPTION 'Valor inválido para Cura (1-20).';
    ELSIF NEW.nome = 'Energia' AND (NEW.valor IS NULL OR NEW.valor NOT BETWEEN 1 AND 15) THEN
        RAISE EXCEPTION 'Valor inválido para Energia (1-15).';
    ELSIF NEW.nome = 'Vida Máxima' AND (NEW.valor IS NULL OR NEW.valor NOT BETWEEN 1 AND 15) THEN
        RAISE EXCEPTION 'Valor inválido para Vida Máxima (1-15).';
    ELSIF NEW.nome = 'Energia Máxima' AND (NEW.valor IS NULL OR NEW.valor NOT BETWEEN 1 AND 10) THEN
        RAISE EXCEPTION 'Valor inválido para Energia Máxima (1-10).';
    ELSIF NEW.nome = 'Ataque' AND (NEW.valor IS NULL OR NEW.valor NOT BETWEEN 1 AND 10) THEN
        RAISE EXCEPTION 'Valor inválido para Ataque (1-10).';
    ELSIF NEW.nome = 'Sorte' AND (NEW.valor IS NULL OR NEW.valor NOT BETWEEN 1 AND 7) THEN
        RAISE EXCEPTION 'Valor inválido para Sorte (1-7).';

    -- Efeitos que NÃO devem ter valor (de status)
    ELSIF NEW.nome IN ('Eletrificado', 'Congelado', 'Molhado', 'Envenenado', 'Sangramento', 'Queimadura', 'Tontura', 'Cegueira', 'Purificação')
          AND NEW.valor IS NOT NULL THEN
        RAISE EXCEPTION 'O efeito "%" não deve ter valor definido.', NEW.nome;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validar_efeito
BEFORE INSERT OR UPDATE ON efeito
FOR EACH ROW
EXECUTE FUNCTION validar_efeito();
```
```sql

BEGIN;

SELECT 'mis001' AS id_missao, 'jog001' AS id_jogador INTO @id_missao, @id_jogador;
SELECT 'ncn001' AS id_item_recompensa, 5 AS quantidade_item INTO @id_item_recompensa, @quantidade_item;
SELECT 50 AS xp_ganho, 20 AS moedas_ganhas INTO @xp_ganho, @moedas_ganhas;


UPDATE jogador
SET
    experiencia_atual = experiencia_atual + @xp_ganho,
    moedas_totais = moedas_totais + @moedas_ganhas
WHERE identificador_jogador = @id_jogador;

IF NOT FOUND THEN
    ROLLBACK;
    RAISE EXCEPTION 'Jogador % não encontrado.', @id_jogador;
END IF;


INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
SELECT
    inv.identificador_inventario,
    @id_item_recompensa,
    @quantidade_item
FROM inventario inv
WHERE inv.identificador_personagem = @id_jogador AND inv.tipo_inventario = 'ger'
ON CONFLICT (identificador_inventario, identificador_item) DO UPDATE
SET quantidade = item_inventario.quantidade + EXCLUDED.quantidade;


COMMIT;
```

```sql


BEGIN;


SELECT 'jog001' AS id_jogador1, 'jog002' AS id_jogador2 INTO @id_jogador1, @id_jogador2;
SELECT 'con001' AS id_item1_para_troca, 1 AS qtd_item1 INTO @id_item1_para_troca, @qtd_item1; 
SELECT 'arm001' AS id_item2_para_troca, 1 AS qtd_item2 INTO @id_item2_para_troca, @qtd_item2; 
SELECT 10 AS moedas_de_jogador1_para_jogador2 INTO @moedas_de_jogador1_para_jogador2;


SELECT identificador_inventario INTO @inv1 FROM inventario WHERE identificador_personagem = @id_jogador1 AND tipo_inventario = 'ger';
SELECT identificador_inventario INTO @inv2 FROM inventario WHERE identificador_personagem = @id_jogador2 AND tipo_inventario = 'ger';

UPDATE item_inventario
SET quantidade = quantidade - @qtd_item1
WHERE identificador_inventario = @inv1 AND identificador_item = @id_item1_para_troca AND quantidade >= @qtd_item1;
IF NOT FOUND THEN ROLLBACK; RAISE EXCEPTION 'Jogador 1 não tem item ou quantidade suficiente.'; END IF;

INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
VALUES (@inv2, @id_item1_para_troca, @qtd_item1)
ON CONFLICT (identificador_inventario, identificador_item) DO UPDATE
SET quantidade = item_inventario.quantidade + EXCLUDED.quantidade;


UPDATE item_inventario
SET quantidade = quantidade - @qtd_item2
WHERE identificador_inventario = @inv2 AND identificador_item = @id_item2_para_troca AND quantidade >= @qtd_item2;
IF NOT FOUND THEN ROLLBACK; RAISE EXCEPTION 'Jogador 2 não tem item ou quantidade suficiente.'; END IF;

INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
VALUES (@inv1, @id_item2_para_troca, @qtd_item2)
ON CONFLICT (identificador_inventario, identificador_item) DO UPDATE
SET quantidade = item_inventario.quantidade + EXCLUDED.quantidade;


UPDATE jogador
SET moedas_totais = moedas_totais - @moedas_de_jogador1_para_jogador2
WHERE identificador_jogador = @id_jogador1 AND moedas_totais >= @moedas_de_jogador1_para_jogador2;
IF NOT FOUND THEN ROLLBACK; RAISE EXCEPTION 'Jogador 1 não tem moedas suficientes.'; END IF;

UPDATE jogador
SET moedas_totais = moedas_totais + @moedas_de_jogador1_para_jogador2
WHERE identificador_jogador = @id_jogador2;


DELETE FROM item_inventario WHERE quantidade <= 0;

COMMIT;

```
```sql


BEGIN;


SELECT 'hbt002' AS id_npc, 'are002' AS id_area INTO @id_npc, @id_area;
SELECT 'ven' AS novo_tipo_habitante, 'Mercador da Vila' AS novo_nome_npc INTO @novo_tipo_habitante, @novo_nome_npc;
SELECT 'con010' AS id_item_secreto, 10 AS qtd_item_secreto INTO @id_item_secreto, @qtd_item_secreto;


UPDATE habitante
SET
    tipo_habitante = @novo_tipo_habitante,
    nome = @novo_nome_npc,
    descricao = 'Antigo aldeão, agora um mercador de itens raros.',
    especialidade = 'rar' 
WHERE identificador_habitante = @id_npc;


INSERT INTO inventario (identificador_personagem, tipo_inventario)
VALUES (@id_npc, 'ger')
ON CONFLICT (identificador_personagem) DO NOTHING;


SELECT identificador_inventario INTO @inv_npc FROM inventario WHERE identificador_personagem = @id_npc AND tipo_inventario = 'ger';


INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
VALUES (@inv_npc, @id_item_secreto, @qtd_item_secreto)
ON CONFLICT (identificador_inventario, identificador_item) DO UPDATE
SET quantidade = item_inventario.quantidade + EXCLUDED.quantidade;



COMMIT;
```
```sql

BEGIN;


SELECT 'jog00X' AS id_novo_jogador, 'Silvie' AS nome_personagem INTO @id_novo_jogador, @nome_personagem;
SELECT 'are001' AS area_inicial, 1950 AS x_inicial, 140 AS y_inicial INTO @area_inicial, @x_inicial, @y_inicial;


INSERT INTO jogador (
    identificador_jogador, 
    identificador_area, nome, descricao, coordenada_x, coordenada_y,
    energia, vida, nivel, sorte, vida_atual, experiencia_atual, moedas_totais
)
VALUES (
    @id_novo_jogador, 
    @area_inicial, @nome_personagem, 'Um novo aventureiro pronto para explorar!', @x_inicial, @y_inicial,
    35, 70, 1, 5, 70, 0, 100
);


INSERT INTO inventario (identificador_personagem, tipo_inventario)
VALUES (@id_novo_jogador, 'ger');
SELECT identificador_inventario INTO @id_inventario_ger FROM inventario WHERE identificador_personagem = @id_novo_jogador AND tipo_inventario = 'ger';


INSERT INTO inventario (identificador_personagem, tipo_inventario)
VALUES (@id_novo_jogador, 'kit');
SELECT identificador_inventario INTO @id_inventario_kit FROM inventario WHERE identificador_personagem = @id_novo_jogador AND tipo_inventario = 'kit';


INSERT INTO item_inventario (identificador_inventario, identificador_item, quantidade)
VALUES
    (@id_inventario_ger, 'con001', 3), 
    (@id_inventario_ger, 'ncn001', 1); 

INSERT INTO jogador_equipamento (identificador_jogador) VALUES (@id_novo_jogador);

COMMIT;
```

```sql

BEGIN;

SELECT 'jog001' AS id_jogador, 'con007' AS id_pocao_curativa INTO @id_jogador, @id_pocao_curativa; -- Chá Enlatado


SELECT identificador_inventario INTO @id_inventario_jogador FROM inventario WHERE identificador_personagem = @id_jogador AND tipo_inventario = 'ger';


UPDATE item_inventario
SET quantidade = quantidade - 1
WHERE identificador_inventario = @id_inventario_jogador AND identificador_item = @id_pocao_curativa AND quantidade >= 1;
IF NOT FOUND THEN ROLLBACK; RAISE EXCEPTION 'Poção não encontrada no inventário ou quantidade insuficiente.'; END IF;


-- Buscar efeitos do consumível (como feito em DBManager.usar_consumivel)
SELECT e.nome, e.valor INTO @efeito_nome, @efeito_valor
FROM efeito_consumivel ec
JOIN efeito e ON ec.identificador_efeito = e.identificador_efeito
WHERE ec.identificador_consumivel = @id_pocao_curativa AND e.nome = 'Cura';

IF FOUND THEN
    UPDATE jogador
    SET vida_atual = LEAST(vida, vida_atual + @efeito_valor)
    WHERE identificador_jogador = @id_jogador;
END IF;


INSERT INTO status_jogador (identificador_jogador, identificador_efeito, duracao_turnos)
VALUES (@id_jogador, 'efe091', 3); -- Aplica Tontura por 3 turnos



COMMIT;
```
---
## **📚 Bibliografia**

  * ELMASRI, R.; NAVATHE, S. B. *Sistemas de Banco de Dados*. 7. ed. Pearson Education do Brasil, 2018.
  * DATE, C. J. *An Introduction to Database Systems*. 8. ed. Addison-Wesley, 2003.
  * SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. *Database System Concepts*. 7. ed. McGraw-Hill Education, 2019.
  * PostgreSQL Documentation. Disponível em: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/) (Acesso em 18 de junho de 2025).
  * Microsoft SQL Server Documentation. Disponível em: [https://docs.microsoft.com/en-us/sql/sql-server/](https://docs.microsoft.com/en-us/sql/sql-server/) (Acesso em 18 de junho de 2025).

---

## **📑 Histórico de Versões**

| Versão | Descrição | Autor(es) | Data de Produção | Revisor(es) | Data de Revisão | 
| :----: | --------- | --------- | :--------------: | ----------- | :-------------: |
| `1.0` | Criação do documento | [Pablo Serra](https://github.com/Pabloserrapxx) | 08/07/2025 | [Matheus Henrick](https://github.com/MatheusHenrickSantos) | 11/07/2025 |