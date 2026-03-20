SELECT  t.nome_titular, d.ano, d.mes, SUM(f.valor_brl) AS total_gasto
FROM  fato_transacao f
INNER JOIN dim_titular t ON f.id_titular = t.id_titular
JOIN dim_data d ON f.id_data = d.id_data 
GROUP BY t.nome_titular, d.ano, d.mes
ORDER BY t.nome_titular, d.ano, d.mes;