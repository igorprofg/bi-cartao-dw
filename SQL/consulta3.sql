SELECT d.ano,d.mes,
SUM(f.valor_brl) AS total_gasto
FROM fato_transacao f
JOIN dim_data d ON f.id_data = d.id_data
GROUP BY d.ano, d.mes
ORDER BY d.ano, d.mes;