-- Importação dos Dados Cadastrais das Operadoras Ativas para MySQL
LOAD DATA INFILE 'C:/Users/USUARIO/Downloads/operadoras_de_plano_de_saude_ativas.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
IGNORE 1 LINES
(registro_ans, cnpj, razao_social, modalidade, uf, municipio, data_registro);
-- Importação dos Demonstrativos Contábeis para MySQL
LOAD DATA INFILE 'C:/Users/USUARIO/Downloads/demonstracoes_contabeis.csv'
INTO TABLE demonstrativos_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
IGNORE 1 LINES
(ano, trimestre, registro_ans, evento_sinistro, receita_total);
