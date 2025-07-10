/**********************************************************************************************
* FUNÇÃO TRIGGER PARA VALIDAR EFEITOS
* ─ Disparada ANTES do INSERT ou UPDATE na tabela efeito.
* ─ Verifica se o valor é válido para efeitos que exigem valor numérico.
* ─ Garante que efeitos de status não tenham valor definido.
* ─ Lança exceção se as condições não forem atendidas.
**********************************************************************************************/

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