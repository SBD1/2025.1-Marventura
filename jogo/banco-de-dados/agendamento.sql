CREATE EXTENSION IF NOT EXISTS pgagent;

CREATE OR REPLACE FUNCTION reviver_lacaios() RETURNS void AS $$
BEGIN
  UPDATE estado_lacaio
  SET 
    vida_atual = lacaio.vida,
    identificador_area_atual = estado_lacaio.identificador_area_origem,
    data_da_morte = NULL
  FROM lacaio
  WHERE estado_lacaio.identificador_lacaio = lacaio.identificador_lacaio
    AND estado_lacaio.data_da_morte IS NOT NULL
    AND now() - estado_lacaio.data_da_morte >= interval '5 minutes';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION reviver_chefe() RETURNS void AS $$
BEGIN
  UPDATE estado_chefe
  SET vida_atual = c.vida,
      identificador_area_atual = c.identificador_area,
      data_da_morte = NULL
  FROM chefe c
  WHERE estado_chefe.identificador_chefe = c.identificador_chefe
    AND data_da_morte IS NOT NULL
    AND now() - data_da_morte >= interval '15 minutes';
END;
$$ LANGUAGE plpgsql;

-- Este script é executado no banco 'postgres' para criar os jobs pgAgent

DO $$
DECLARE
    jid integer;
    scid integer;
BEGIN
    -- Excluir jobs existentes para idempotência
    -- É bom limpar antes de recriar para evitar duplicatas se o script rodar várias vezes
    DELETE FROM pgagent.pga_schedule WHERE jscjobid IN (SELECT jobid FROM pgagent.pga_job WHERE jobname IN ('tarefa_reviver_lacaios', 'tarefa_reviver_chefe'));
    DELETE FROM pgagent.pga_jobstep WHERE jstjobid IN (SELECT jobid FROM pgagent.pga_job WHERE jobname IN ('tarefa_reviver_lacaios', 'tarefa_reviver_chefe'));
    DELETE FROM pgagent.pga_job WHERE jobname IN ('tarefa_reviver_lacaios', 'tarefa_reviver_chefe');

    -- Criando uma nova tarefa para lacaios
    INSERT INTO pgagent.pga_job(
        jobjclid, jobname, jobdesc, jobhostagent, jobenabled
    ) VALUES (
        1::integer, 'tarefa_reviver_lacaios'::text, 'Tarefa para reviver lacaios mortos a cada minuto.'::text, ''::text, true
    ) RETURNING jobid INTO jid;

    -- Etapas para a tarefa de lacaios
    INSERT INTO pgagent.pga_jobstep (
        jstjobid, jstname, jstenabled, jstkind,
        jstconnstr, jstdbname, jstonerror,
        jstcode, jstdesc
    ) VALUES (
        jid, 'Executar reviver_lacaios'::text, true, 's'::character(1),
        ''::text, 'Marventura'::name, 'f'::character(1),
        'SELECT reviver_lacaios();'::text, ''::text
    ) ;

    -- Horários para tarefa de lacaios (a cada minuto)
    INSERT INTO pgagent.pga_schedule(
        jscjobid, jscname, jscdesc, jscenabled,
        jscstart, jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths
    ) VALUES (
        jid, 'Agendamento Lacaios Minuto'::text, ''::text, true,
        now(), -- Iniciar agora
        -- Minutos: tudo verdadeiro (a cada minuto)
        '{t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t}'::bool[]::boolean[],
        -- Horas: tudo verdadeiro (a cada hora)
        '{t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t}'::bool[]::boolean[],
        -- Dias da semana: tudo verdadeiro (todos os dias da semana)
        '{t,t,t,t,t,t,t}'::bool[]::boolean[],
        -- Dias do mês: tudo verdadeiro (todos os dias do mês)
        '{t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t}'::bool[]::boolean[],
        -- Meses: tudo verdadeiro (todos os meses)
        '{t,t,t,t,t,t,t,t,t,t,t,t}'::bool[]::boolean[]
    ) RETURNING jscid INTO scid;

    -- Criando uma nova tarefa para chefes
    INSERT INTO pgagent.pga_job(
        jobjclid, jobname, jobdesc, jobhostagent, jobenabled
    ) VALUES (
        1::integer, 'tarefa_reviver_chefe'::text, 'Tarefa para reviver chefes mortos a cada minuto.'::text, ''::text, true
    ) RETURNING jobid INTO jid;

    -- Etapas para a tarefa de chefes
    INSERT INTO pgagent.pga_jobstep (
        jstjobid, jstname, jstenabled, jstkind,
        jstconnstr, jstdbname, jstonerror,
        jstcode, jstdesc
    ) VALUES (
        jid, 'Executar reviver_chefe'::text, true, 's'::character(1),
        ''::text, 'Marventura'::name, 'f'::character(1),
        'SELECT reviver_chefe();'::text, ''::text
    ) ;

    -- Horários para tarefa de chefes (a cada minuto)
    INSERT INTO pgagent.pga_schedule(
        jscjobid, jscname, jscdesc, jscenabled,
        jscstart, jscminutes, jschours, jscweekdays, jscmonthdays, jscmonths
    ) VALUES (
        jid, 'Agendamento Chefe Minuto'::text, ''::text, true,
        now(), -- Iniciar agora
        -- Minutos: tudo verdadeiro (a cada minuto)
        '{t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t}'::bool[]::boolean[],
        -- Horas: tudo verdadeiro (a cada hora)
        '{t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t}'::bool[]::boolean[],
        -- Dias da semana: tudo verdadeiro (todos os dias da semana)
        '{t,t,t,t,t,t,t}'::bool[]::boolean[],
        -- Dias do mês: tudo verdadeiro (todos os dias do mês)
        '{t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t}'::bool[]::boolean[],
        -- Meses: tudo verdadeiro (todos os meses)
        '{t,t,t,t,t,t,t,t,t,t,t,t}'::bool[]::boolean[]
    ) RETURNING jscid INTO scid;
END
$$;