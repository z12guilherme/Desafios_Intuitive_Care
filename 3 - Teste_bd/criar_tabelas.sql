-- Criação da tabela para armazenar as Operadoras de Plano de Saúde Ativas
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

-- Criação da tabela para armazenar os Demonstrativos Contábeis
CREATE TABLE demonstrativos_contabeis (
    id SERIAL PRIMARY KEY,
    ano INT NOT NULL,
    trimestre INT NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    registro_ans VARCHAR(10) NOT NULL,
    evento_sinistro DECIMAL(15,2) NOT NULL,
    receita_total DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans) ON DELETE CASCADE
);
