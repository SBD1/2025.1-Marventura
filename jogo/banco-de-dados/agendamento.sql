CREATE EXTENSION IF NOT EXISTS pg_cron;

CREATE OR REPLACE FUNCTION reviver_lacaios() RETURNS void AS $$
BEGIN
  UPDATE estado_instancia_lacaio
  SET vida_atual = l.vida,
      identificador_area_atual = il.identificador_area,
      data_da_morte = NULL
  FROM instancia_lacaio il
  JOIN lacaio l ON il.identificador_lacaio = l.identificador_lacaio
  WHERE estado_instancia_lacaio.identificador_instancia_lacaio = il.identificador_instancia_lacaio
    AND data_da_morte IS NOT NULL
    AND now() - data_da_morte >= interval '5 minutes';
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

-- Lacaio: checagem por minuto
SELECT cron.schedule('revive_lacaios_job', '*/1 * * * *', $$ SELECT reviver_lacaios(); $$);

-- Chefe: checagem por minuto
SELECT cron.schedule('revive_chefe_job', '*/1 * * * *', $$ SELECT reviver_chefe(); $$);

-- Teste manual
UPDATE estado_instancia_lacaio
SET data_da_morte = now() - interval '6 minutes',
	identificador_area_atual = 'are034'
WHERE identificador_progresso = 'pro001' AND identificador_instancia_lacaio = 'ins001';

SELECT reviver_chefe();