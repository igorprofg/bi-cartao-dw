--CONSULTA 1:

SELECT 
    CASE 
        WHEN f.num_parcela = 1 THEN 'À vista'
        ELSE 'Parcelado'
    END AS tipo_compra,
    COUNT(*) AS quantidade,
    SUM(f.valor_brl) AS total_gasto
FROM fato_transacao f
GROUP BY tipo_compra;

--CONSULTA 2:

SELECT 
    CASE 
        WHEN f.num_parcela = 1 THEN 'À vista'
        ELSE 'Parcelado'
    END AS tipo_compra,
    COUNT(*) AS quantidade,
    SUM(f.valor_brl) AS total_gasto
FROM fato_transacao f
WHERE f.valor_brl > 0
GROUP BY tipo_compra;