SELECT d.dia_semana,
COUNT(f.id_transacao) AS qtd_transacoes,
SUM(f.valor_brl) AS total_gasto
FROM fato_transacao f
JOIN dim_data d ON f.id_data = d.id_data
GROUP BY d.dia_semana
ORDER BY total_gasto DESC;