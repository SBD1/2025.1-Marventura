/**********************************************************************************************
* FUNÇÃO TRIGGER PARA GERAR IDS EM TABELAS FILHAS DE tipo_personagem
* ─ Disparada ANTES do INSERT nas tabelas: jogador, aliado, chefe, lacaio e habitante.
* ─ Insere linha correspondente em tipo_elemento_espacial e recupera o ID gerado.
* ─ Atribui o ID gerado à coluna identificador_{nome_da_tabela} da linha a ser inserida.
**********************************************************************************************/
CREATE FUNCTION public.gerar_id_tabelas_personagem()
RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_new_id    ID;
    v_tipo_val  CHAR(3);
BEGIN

    /* 1 ─ Bloqueia inserção manual ------------------------------------------*/
    IF TG_TABLE_NAME = 'jogador' THEN
        IF NEW.identificador_jogador IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_jogador" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'aliado' THEN
        IF NEW.identificador_aliado IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_aliado" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'chefe' THEN
        IF NEW.identificador_chefe IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_chefe" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'lacaio' THEN
        IF NEW.identificador_lacaio IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_lacaio" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'habitante' THEN
        IF NEW.identificador_habitante IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_habitante" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    END IF;


    /* 2 ─ Determina o valor do "tipo" com base na tabela onde o trigger foi disparado */
    IF TG_TABLE_NAME = 'jogador' THEN
        v_tipo_val := 'jog';
    ELSIF TG_TABLE_NAME = 'aliado' THEN
        v_tipo_val := 'ali';
    ELSIF TG_TABLE_NAME = 'chefe' THEN
        v_tipo_val := 'che';
    ELSIF TG_TABLE_NAME = 'lacaio' THEN
        v_tipo_val := 'lac';
    ELSIF TG_TABLE_NAME = 'habitante' THEN
        v_tipo_val := lower( to_jsonb(NEW)->>'tipo_habitante' );
    ELSE
        -- Isso é uma proteção caso o trigger seja acidentalmente anexado a outra tabela
        RAISE EXCEPTION 'Trigger inesperado para a tabela %', TG_TABLE_NAME;
    END IF;


    /* 3 ─ Insere na tabela 'tipo_personagem' e captura o ID gerado pelo trigger de tipo_pessoa */
    INSERT INTO tipo_elemento_espacial (tipo)
    VALUES (v_tipo)
    RETURNING identificador_elemento_espacial INTO v_new_id;


    /* 4 ─ Atribui o ID gerado à nova linha da tabela filha */
    IF TG_TABLE_NAME = 'jogador' THEN
        NEW.identificador_jogador := v_new_id;
    ELSIF TG_TABLE_NAME = 'aliado' THEN
        NEW.identificador_aliado := v_new_id;
    ELSIF TG_TABLE_NAME = 'chefe' THEN
        NEW.identificador_chefe := v_new_id;
    ELSIF TG_TABLE_NAME = 'lacaio' THEN
        NEW.identificador_lacaio := v_new_id;
    ELSIF TG_TABLE_NAME = 'habitante' THEN
        NEW.identificador_habitante := v_new_id;
    END IF;

    RETURN NEW; -- Retorna a linha modificada para que a inserção continue
END;
$$;

COMMENT ON FUNCTION public.gerar_id_tabelas_personagem() IS
'Usada como BEFORE INSERT nas tabelas jogador, aliado, chefe, lacaio e habitante.
Gera ID automaticamente inserindo entrada em tipo_personagem e atribui ao NEW.identificador_{nome_da_tabela}';



/**********************************************************************************************
* FUNÇÃO TRIGGER PARA GERAR IDS EM TABELAS FILHAS DE tipo_elemento_espacial
* ─ Disparada ANTES do INSERT nas tabelas: caminho, obstaculo, area_interativa.
* ─ Insere linha correspondente em tipo_elemento_espacial e recupera o ID gerado.
* ─ Atribui o ID gerado à coluna identificador_{nome_da_tabela} da linha a ser inserida.
**********************************************************************************************/
CREATE FUNCTION public.gerar_id_tabelas_elemento_espacial()
RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_new_id   ID;
    v_tipo     CHAR(3);
BEGIN

    -- 1. Bloqueia inserções manuais nos identificadores
    IF TG_TABLE_NAME = 'caminho' THEN
        IF NEW.identificador_caminho IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_caminho" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'obstaculo' THEN
        IF NEW.identificador_obstaculo IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_obstaculo" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'area_interativa' THEN
        IF NEW.identificador_area_interativa IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_area_interativa" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    END IF;


    -- 2. Determina o tipo com base na tabela
    IF TG_TABLE_NAME = 'caminho' THEN
        v_tipo := 'cam';
    ELSIF TG_TABLE_NAME = 'obstaculo' THEN
        v_tipo := 'obs';
    ELSIF TG_TABLE_NAME = 'area_interativa' THEN
        v_tipo := 'ari';
    ELSE
        RAISE EXCEPTION 'Trigger usada em tabela incorreta: %', TG_TABLE_NAME;
    END IF;


    -- 3. Insere na tabela tipo_elemento_espacial e obtém o ID
    INSERT INTO tipo_elemento_espacial (tipo)
    VALUES (v_tipo)
    RETURNING identificador_elemento_espacial INTO v_new_id;


    -- 4. Atribui o ID gerado à nova linha da tabela filha
    IF TG_TABLE_NAME = 'caminho' THEN
        NEW.identificador_caminho := v_new_id;
    ELSIF TG_TABLE_NAME = 'obstaculo' THEN
        NEW.identificador_obstaculo := v_new_id;
    ELSIF TG_TABLE_NAME = 'area_interativa' THEN
        NEW.identificador_area_interativa := v_new_id;
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION public.gerar_id_tabelas_elemento_espacial() IS
'Usada como BEFORE INSERT nas tabelas caminho, obstaculo e area_interativa.
Gera ID automaticamente inserindo entrada em tipo_elemento_espacial e atribui ao NEW.identificador_{nome_da_tabela}';



/**********************************************************************************************
* FUNÇÃO TRIGGER PARA GERAR IDS EM TABELAS FILHAS DE tipo_mapa
* ─ Disparada ANTES do INSERT nas tabelas: ilha e mar.
* ─ Insere linha correspondente em tipo_mapa e recupera o ID gerado.
* ─ Atribui o ID gerado à coluna identificador_{nome_da_tabela} da nova tupla.
**********************************************************************************************/
CREATE FUNCTION public.gerar_id_tabelas_mapa()
RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_new_id   ID;
    v_tipo     CHAR(3);
BEGIN
    -- 1. Bloqueia inserções manuais nos identificadores
    IF TG_TABLE_NAME = 'ilha' THEN
        IF NEW.identificador_ilha IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_ilha" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    ELSIF TG_TABLE_NAME = 'mar' THEN
        IF NEW.identificador_mar IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_mar" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
    END IF;


    -- 2. Define o tipo com base na tabela alvo
    IF TG_TABLE_NAME = 'ilha' THEN
        v_tipo := 'ilh';
    ELSIF TG_TABLE_NAME = 'mar' THEN
        v_tipo := 'mar';
    ELSE
        RAISE EXCEPTION 'Trigger usada em tabela não esperada: %', TG_TABLE_NAME;
    END IF;


    -- 3. Insere entrada em tipo_mapa e obtém ID
    INSERT INTO tipo_mapa (tipo)
    VALUES (v_tipo)
    RETURNING identificador_mapa INTO v_new_id;


    -- 4. Atribui o ID gerado à nova linha
    IF TG_TABLE_NAME = 'ilha' THEN
        NEW.identificador_ilha := v_new_id;
    ELSIF TG_TABLE_NAME = 'mar' THEN
        NEW.identificador_mar := v_new_id;
    END IF;

    RETURN NEW;
END;
$$;

COMMENT ON FUNCTION public.gerar_id_tabelas_mapa() IS
'Usada como BEFORE INSERT nas tabelas ilha e mar.
Gera ID automaticamente inserindo entrada em tipo_elemento_espacial e atribui ao NEW.identificador_{nome_da_tabela}';
