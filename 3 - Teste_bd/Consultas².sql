-- CONSULTA: Top 10 operadoras com maiores despesas no último ano
SELECT o.razao_social, d.registro_ans, SUM(d.evento_sinistro) AS total_despesas
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.ano = EXTRACT(YEAR FROM CURRENT_DATE) - 1 -- Último ano
GROUP BY o.razao_social, d.registro_ans
ORDER BY total_despesas DESC
LIMIT 10;
