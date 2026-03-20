SELECT t.nome_titular,
COUNT(f.id_transacao) AS qtd_transacoes,
SUM(f.valor_brl) AS total_gasto,
AVG(f.valor_brl) AS media_por_transacao
FROM fato_transacao f
JOIN dim_titular t ON f.id_titular = t.id_titular
WHERE f.valor_brl > 0
GROUP BY t.nome_titular
ORDER BY total_gasto DESC;