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
    /* 2.1 ─ Bloqueia inserção manual ------------------------------------------*/
    IF TG_TABLE_NAME = 'habilidade' THEN
        IF NEW.identificador_habilidade IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_habilidade" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'receita' THEN
        IF NEW.identificador_receita IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_receita" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'efeito' THEN
        IF NEW.identificador_efeito IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_efeito" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'tipo_mapa' THEN
        IF NEW.identificador_mapa IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_mapa" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'area' THEN
        IF NEW.identificador_area IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_area" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'evento' THEN
        IF NEW.identificador_evento IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_evento" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'tipo_elemento_espacial' THEN
        IF NEW.identificador_elemento_espacial IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_elemento_espacial" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'recompensa_de_exploracao' THEN
        IF NEW.identificador_recompensa IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_recompensa" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'tipo_personagem' THEN
        IF NEW.identificador_personagem IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_personagem" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'instancia_lacaio' THEN
        IF NEW.identificador_instancia_lacaio IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_instancia_lacaio" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'batalha' THEN
        IF NEW.identificador_batalha IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_batalha" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'inventario' THEN
        IF NEW.identificador_inventario IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_inventario" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'negociacao' THEN
        IF NEW.identificador_negociacao IS NOT NULL THEN
            RAISE EXCEPTION 'A coluna "identificador_negociacao" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    END IF;

    /* 2.2 ─ obtém o prefixo ---------------------------------------------------*/
    prefixo := lower( to_jsonb(NEW)->>'tipo' );       -- tenta coluna “tipo”
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
    IF TG_TABLE_NAME = 'habilidade' THEN
        NEW.identificador_habilidade := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'receita' THEN
        NEW.identificador_receita := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'efeito' THEN
        NEW.identificador_efeito := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'tipo_mapa' THEN
        NEW.identificador_mapa := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'area' THEN
        NEW.identificador_area := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'evento' THEN
        NEW.identificador_evento := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'tipo_elemento_espacial' THEN
        NEW.identificador_elemento_espacial := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'recompensa_de_exploracao' THEN
        NEW.identificador_recompensa := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'tipo_personagem' THEN
        NEW.identificador_personagem := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'instancia_lacaio' THEN
        NEW.identificador_instancia_lacaio := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'batalha' THEN
        NEW.identificador_batalha := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'inventario' THEN
        NEW.identificador_inventario := prefixo || lpad(numero_serial::text, 3, '0');
    ELSIF TG_TABLE_NAME = 'negociacao' THEN
        NEW.identificador_negociacao := prefixo || lpad(numero_serial::text, 3, '0');
    END IF;


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