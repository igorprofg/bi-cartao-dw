SELECT c.nome_categoria, SUM (f.valor_brl) AS total_gasto
FROM  fato_transacao f 
INNER JOIN dim_categoria c ON f.id_categoria = c.id_categoria
GROUP BY c.nome_categoria
ORDER BY total_gasto DESC
LIMIT 10;