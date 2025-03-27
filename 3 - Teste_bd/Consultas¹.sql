-- CONSULTA: Top 10 operadoras com maiores despesas no último trimestre
SELECT o.razao_social, d.registro_ans, SUM(d.evento_sinistro) AS total_despesas
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.ano = EXTRACT(YEAR FROM CURRENT_DATE) -- Último ano
AND d.trimestre = (
    SELECT MAX(trimestre) 
    FROM demonstrativos_contabeis 
    WHERE ano = EXTRACT(YEAR FROM CURRENT_DATE)
)
GROUP BY o.razao_social, d.registro_ans
ORDER BY total_despesas DESC
LIMIT 10;
