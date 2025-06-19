/**********************************************************************************************
* 1. DOMÍNIO “ID” ─ formato fixo aaa999  (3 letras minúsculas + 3 dígitos)
**********************************************************************************************/
CREATE DOMAIN ID AS CHAR(6)
CHECK (VALUE ~ '^[a-z]{3}[0-9]{3}$');

COMMENT ON DOMAIN ID IS
'Identificador gerado por trigger: 3 letras + 3 dígitos (001-999). Inserção manual proibida.';

/**********************************************************************************************
2. FUNÇÃO GENÉRICA                                                          (plpgsql ≥ 9.6)
    ─  Pega NEW.tipo (3 letras) se existir; senão 3 1ªs letras do nome da tabela
    ─  Mantém um contador separado (sequence) por prefixo
    ─  Reinicia em 001 para cada novo prefixo
    ─  Impede qualquer tentativa de inserir “id” manualmente
**********************************************************************************************/
CREATE FUNCTION public.gerar_id()
RETURNS trigger
LANGUAGE plpgsql AS
$$
DECLARE
    prefixo             text;      -- 3 letras
    nome_da_sequencia   text;      -- nome da sequência gerada on-the-fly
    numero_serial       bigint;    -- próximo número da sequência
BEGIN
    /* 2.1 ─ Bloqueia inserção manual ********************************************/
    IF NEW.id IS NOT NULL THEN
        RAISE EXCEPTION 
            'A coluna "id" é gerada automaticamente; não forneça valor manualmente.';
    END IF;

    /* 2.2 ─ obtém o prefixo ---------------------------------------------------*/
    prefixo := lower(NEW.tipo);       -- tenta coluna “tipo”
    IF prefixo IS NULL THEN
        prefixo := lower( substr(TG_TABLE_NAME, 1, 3) );  -- 3 letras da tabela
    END IF;

    /* 2.3 ─ valida que são exatamente 3 letras --------------------------------*/
    IF prefixo !~ '^[a-z]{3}$' THEN
        RAISE EXCEPTION 
            'prefixo inválido: precisa ser 3 letras (a-z). Obtido = "%".', prefixo;
    END IF;

    /* 2.4 ─ sequência dedicada ao par (tabela + prefixo) ----------------------*/
    nome_da_sequencia := format('%I_%s_seq', TG_TABLE_NAME, prefixo);  -- ex.: acessorio_ace_seq

    -- cria se não existir (concorrência leve OK)
    PERFORM 1 FROM pg_class WHERE relkind = 'S' AND relname = nome_da_sequencia;
    IF NOT FOUND THEN
        EXECUTE format('CREATE SEQUENCE %I START 1', nome_da_sequencia);
    END IF;

    /* 2.5 ─ Pega o próximo número ---------------------------------------------*/
    EXECUTE format('SELECT nextval(%L)', nome_da_sequencia) INTO numero_serial;

    /* 2.6 ─ Monta o ID --------------------------------------------------------*/
    NEW.id := prefixo || lpad(numero_serial::text, 3, '0');   -- ex.: ace001

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION public.gerar_id() IS
'Gera automaticamente IDs no formato aaa999. 
prefixo: coluna "tipo" (se existir) ou 3 primeiras letras do nome da tabela. 
Valor numérico reinicia em 001 para cada prefixo. Usuário não pode inserir o id.' ;

/**********************************************************************************************
* 3. COMO USAR
*    Crie a coluna `id ID` + TRIGGER BEFORE INSERT  (mesma função serve para todas)
**********************************************************************************************/