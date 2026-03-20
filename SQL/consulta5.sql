SELECT e.nome_estabelecimento,
SUM(f.valor_brl) AS total_gasto
FROM fato_transacao f
JOIN dim_estabelecimento e ON f.id_estabelecimento = e.id_estabelecimento
GROUP BY e.nome_estabelecimento
ORDER BY total_gasto DESC
LIMIT 10;