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
    novo_id    ID;
    prefixo  CHAR(3);
BEGIN

    /* 1 ─ Bloqueia inserção manual e determina o valor do "prefixo" ------------*/
    IF TG_TABLE_NAME = 'jogador' THEN
        IF NEW.identificador_jogador IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_jogador" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'jog';
    ELSIF TG_TABLE_NAME = 'aliado' THEN
        IF NEW.identificador_aliado IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_aliado" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'ali';
    ELSIF TG_TABLE_NAME = 'chefe' THEN
        IF NEW.identificador_chefe IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_chefe" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'che';
    ELSIF TG_TABLE_NAME = 'lacaio' THEN
        IF NEW.identificador_lacaio IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_lacaio" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'lac';
    ELSIF TG_TABLE_NAME = 'habitante' THEN
        IF NEW.identificador_habitante IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_habitante" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := lower( to_jsonb(NEW)->>'tipo_habitante' );
    ELSE
        -- Isso é uma proteção caso o trigger seja acidentalmente anexado a outra tabela
        RAISE EXCEPTION 'Trigger inesperado para a tabela %', TG_TABLE_NAME;
    END IF;


    /* 2 ─ Insere na tabela 'tipo_personagem' e captura o ID gerado pelo trigger de tipo_pessoa */
    INSERT INTO tipo_personagem (tipo)
    VALUES (prefixo)
    RETURNING identificador_personagem INTO novo_id;


    /* 3 ─ Atribui o ID gerado à nova linha da tabela filha */
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
    novo_id   ID;
    prefixo     CHAR(3);
BEGIN

    -- 1. Bloqueia inserções manuais nos identificadores e determina o valor do "prefixo"
    IF TG_TABLE_NAME = 'caminho' THEN
        IF NEW.identificador_caminho IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_caminho" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'cam';
    ELSIF TG_TABLE_NAME = 'obstaculo' THEN
        IF NEW.identificador_obstaculo IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_obstaculo" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'obs';
    ELSIF TG_TABLE_NAME = 'area_interativa' THEN
        IF NEW.identificador_area_interativa IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_area_interativa" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        prefixo := 'ari';
    ELSE
        RAISE EXCEPTION 'Trigger usada em tabela incorreta: %', TG_TABLE_NAME;
    END IF;


    -- 2. Insere na tabela tipo_elemento_espacial e obtém o ID
    INSERT INTO tipo_elemento_espacial (tipo)
    VALUES (prefixo)
    RETURNING identificador_elemento_espacial INTO novo_id;


    -- 3. Atribui o ID gerado à nova linha da tabela filha
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

COMMENT ON FUNCTION public.gerar_id_tabelas_elemento_espacial() IS
'Usada como BEFORE INSERT nas tabelas caminho, obstaculo e area_interativa.
Gera ID automaticamente inserindo entrada em tipo_elemento_espacial e atribui ao NEW.identificador_{nome_da_tabela}';



CREATE FUNCTION public.gerar_id_tabelas_item()
RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    novo_id   ID;
    tipo     CHAR(3);
BEGIN
    -- 1. Bloqueia inserções manuais nos identificadores
    IF TG_TABLE_NAME = 'acessorio' THEN
        IF NEW.identificador_acessorio IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_acessorio" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'ace';
    ELSIF TG_TABLE_NAME = 'arma' THEN
        IF NEW.identificador_arma IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_arma" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'arm';
    ELSIF TG_TABLE_NAME = 'fruta' THEN
        IF NEW.identificador_fruta IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_fruta" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'fru';
    ELSIF TG_TABLE_NAME = 'consumivel' THEN
        IF NEW.identificador_consumivel IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_consumivel" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'con';
    ELSIF TG_TABLE_NAME = 'nao_consumivel' THEN
        IF NEW.identificador_nao_consumivel IS NOT NULL THEN
            RAISE EXCEPTION
                'A coluna "identificador_nao_consumivel" é gerada automaticamente; não forneça valor manualmente.';
        END IF;
        tipo := 'ncn';
    ELSE
        RAISE EXCEPTION 'Trigger usada em tabela não esperada: %', TG_TABLE_NAME;
    END IF;



    -- 3. Insere entrada em tipo_item e obtém ID
    INSERT INTO tipo_item (tipo)
    VALUES (tipo)
    RETURNING identificador_item INTO novo_id;


    -- 4. Atribui o ID gerado à nova linha
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

COMMENT ON FUNCTION public.gerar_id_tabelas_item() IS
'Usada como BEFORE INSERT nas tabelas acessorio, arma, fruta, consumivel e nao_consumivel.
Gera ID automaticamente inserindo entrada em tipo_item e atribui ao NEW.identificador_{nome_da_tabela}';



CREATE FUNCTION tentar_coletar_item()
RETURNS TRIGGER AS $$
DECLARE
  tentativa_antiga TIMESTAMP;
BEGIN
  SELECT data_da_tentativa INTO tentativa_antiga
  FROM recompensa_de_exploracao
  WHERE identificador_area_interativa = NEW.identificador_area_interativa
    AND identificador_jogador = NEW.identificador_jogador;

  IF tentativa_antiga IS NOT NULL AND now() - tentativa_antiga < interval '15 minutes' THEN
    RAISE EXCEPTION 'Você precisa esperar 15 minutos para interagir com esta área novamente.';
  END IF;

  RETURN NEW; -- Permite o INSERT seguir
END;
$$ LANGUAGE plpgsql;
