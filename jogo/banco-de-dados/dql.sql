SELECT receita.identificador_receita AS Receita, consumivel.nome AS Nome
FROM receita JOIN consumivel ON receita.consumivel_produzido = consumivel.identificador_consumivel
