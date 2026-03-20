SELECT t.nome_titular,
SUM(f.valor_brl) AS total_estornos
FROM fato_transacao f
JOIN dim_titular t ON f.id_titular = t.id_titular
WHERE f.valor_brl < 0
GROUP BY t.nome_titular;