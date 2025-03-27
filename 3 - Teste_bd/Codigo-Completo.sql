-- TAREFA 3.3 - Criação das Tabelas

-- Tabela de Operadoras
CREATE TABLE operadoras (
    id_operadora SERIAL PRIMARY KEY,
    registro_ans VARCHAR(10) UNIQUE NOT NULL,
    cnpj VARCHAR(18) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    modalidade VARCHAR(100) NOT NULL,
    uf VARCHAR(2) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    data_registro DATE NOT NULL
);

-- Tabela de Demonstrativos Contábeis
CREATE TABLE demonstrativos_contabeis (
    id SERIAL PRIMARY KEY,
    ano INT NOT NULL,
    trimestre INT NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    registro_ans VARCHAR(10) NOT NULL,
    evento_sinistro DECIMAL(15,2) NOT NULL,
    receita_total DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans) ON DELETE CASCADE
);

-- TAREFA 3.4 - Importação dos Arquivos CSV para as Tabelas

-- 3.4.1 Importação de Operadoras (PostgreSQL)
-- PostgreSQL: Importação de Dados Cadastrais das Operadoras Ativas
COPY operadoras(registro_ans, cnpj, razao_social, modalidade, uf, municipio, data_registro)
FROM 'C:/Users/USUARIO/Downloads/operadoras_de_plano_de_saude_ativas.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- MySQL: Importação de Dados Cadastrais das Operadoras Ativas
-- MySQL: Importação de Dados Cadastrais das Operadoras Ativas
LOAD DATA INFILE 'C:/Users/USUARIO/Downloads/operadoras_de_plano_de_saude_ativas.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
IGNORE 1 LINES
(registro_ans, cnpj, razao_social, modalidade, uf, municipio, data_registro);

-- 3.4.2 Importação dos Demonstrativos Contábeis (PostgreSQL)
-- PostgreSQL: Importação dos Demonstrativos Contábeis
COPY demonstrativos_contabeis(ano, trimestre, registro_ans, evento_sinistro, receita_total)
FROM 'C:/Users/USUARIO/Downloads/demonstracoes_contabeis.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- MySQL: Importação dos Demonstrativos Contábeis
LOAD DATA INFILE 'C:/Users/USUARIO/Downloads/demonstracoes_contabeis.csv'
INTO TABLE demonstrativos_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
IGNORE 1 LINES
(ano, trimestre, registro_ans, evento_sinistro, receita_total);

-- TAREFA 3.5 - Consultas Analíticas

-- 3.5.1 Top 10 Operadoras com Maiores Despesas no Último Trimestre
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

-- 3.5.2 Top 10 Operadoras com Maiores Despesas no Último Ano
SELECT o.razao_social, d.registro_ans, SUM(d.evento_sinistro) AS total_despesas
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.ano = EXTRACT(YEAR FROM CURRENT_DATE) - 1 -- Último ano
GROUP BY o.razao_social, d.registro_ans
ORDER BY total_despesas DESC
LIMIT 10;

-- TAREFA 3.6 - Índices para Otimizar Consultas

-- Índice para otimizar as consultas por registro_ans
CREATE INDEX idx_demonstrativos_registro_ans ON demonstrativos_contabeis(registro_ans);

-- Índice para otimizar consultas por ano e trimestre
CREATE INDEX idx_demonstrativos_ano_trimestre ON demonstrativos_contabeis(ano, trimestre);
