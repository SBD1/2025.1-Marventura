SELECT
    i.identificador_ilha,
    i.nome,
    CASE
        WHEN p.identificador_ilha IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS visitada
FROM
    ilha i
LEFT JOIN
    progresso_ilha p
    ON i.identificador_ilha = p.identificador_ilha AND p.jogador_id = %s
ORDER BY i.nome;
