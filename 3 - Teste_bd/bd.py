import os
import ftplib
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# Configurações
DATABASE_CONFIG = {
    'mysql': {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': '3306',
        'database': 'ans_db'
    },
    'postgresql': {
        'dialect': 'postgresql',
        'driver': 'psycopg2',
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': '5432',
        'database': 'ans_db'
    }
}

# 1. Download dos Arquivos via FTP
def download_ftp_files():
    ftp = ftplib.FTP('dadosabertos.ans.gov.br')
    ftp.login()
    
    # Diretórios
    base_dir = '/FTP/PDA/'
    operadoras_dir = 'operadoras_de_plano_de_saude_ativas/'
    demonstracoes_dir = 'demonstracoes_contabeis/'
    
    # Download Operadoras
    ftp.cwd(base_dir + operadoras_dir)
    with open('operadoras.csv', 'wb') as f:
        ftp.retrbinary('RETR operadoras_ativas.csv', f.write)
    
    # Download Demonstrações (últimos 2 anos)
    ftp.cwd(base_dir + demonstracoes_dir)
    years = sorted(ftp.nlst(), reverse=True)[:2]
    
    for year in years:
        ftp.cwd(year)
        files = ftp.nlst()
        for file in files:
            if file.endswith('.csv'):
                with open(f'demonstracoes_{year}.csv', 'wb') as f:
                    ftp.retrbinary(f'RETR {file}', f.write)
        ftp.cwd('..')
    
    ftp.quit()

# 2. Conexão com o Banco de Dados
def get_engine(db_type='mysql'):
    config = DATABASE_CONFIG[db_type]
    connection_string = (
        f"{config['dialect']}+{config['driver']}://"
        f"{config['user']}:{config['password']}@"
        f"{config['host']}:{config['port']}/"
        f"{config['database']}"
    )
    return create_engine(connection_string)

# 3. Criação das Tabelas
def create_tables(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS operadoras (
                cnpj VARCHAR(20) PRIMARY KEY,
                razao_social VARCHAR(255),
                data_registro_ans DATE,
                situacao VARCHAR(50)
            """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS demonstracoes (
                id SERIAL PRIMARY KEY,
                cnpj VARCHAR(20),
                data DATE,
                conta VARCHAR(255),
                valor DECIMAL(15,2),
                FOREIGN KEY (cnpj) REFERENCES operadoras(cnpj)
            )"""))
        conn.commit()

# 4. Importação dos Dados
def import_data(engine):
    # Operadoras
    df_operadoras = pd.read_csv('operadoras.csv', sep=';', encoding='latin1')
    df_operadoras.to_sql('operadoras', engine, if_exists='replace', index=False)
    
    # Demonstrações
    for file in os.listdir():
        if file.startswith('demonstracoes_'):
            df = pd.read_csv(file, sep=';', encoding='latin1')
            df.to_sql('demonstracoes', engine, if_exists='append', index=False)

# 5. Consultas Analíticas
def run_queries(engine):
    with engine.connect() as conn:
        # Último trimestre
        print("\nTop 10 - Último Trimestre:")
        result = conn.execute(text("""
            SELECT o.razao_social, SUM(d.valor) AS total
            FROM demonstracoes d
            JOIN operadoras o ON d.cnpj = o.cnpj
            WHERE d.conta LIKE '%EVENTOS/%MEDICO HOSPITALAR'
            AND d.data >= CURRENT_DATE - INTERVAL '3 MONTHS'
            GROUP BY o.razao_social
            ORDER BY total DESC
            LIMIT 10
        """))
        for row in result:
            print(f"{row.razao_social}: R${row.total:,.2f}")
        
        # Último ano
        print("\nTop 10 - Último Ano:")
        result = conn.execute(text("""
            SELECT o.razao_social, SUM(d.valor) AS total
            FROM demonstracoes d
            JOIN operadoras o ON d.cnpj = o.cnpj
            WHERE d.conta LIKE '%EVENTOS/%MEDICO HOSPITALAR'
            AND d.data >= CURRENT_DATE - INTERVAL '1 YEAR'
            GROUP BY o.razao_social
            ORDER BY total DESC
            LIMIT 10
        """))
        for row in result:
            print(f"{row.razao_social}: R${row.total:,.2f}")

# Execução Principal
if __name__ == "__main__":
    # Download dos dados
    print("Baixando arquivos...")
    download_ftp_files()
    
    # Configurar conexão
    engine = get_engine('mysql')  # Altere para 'postgresql' se necessário
    
    # Criar estrutura
    print("Criando tabelas...")
    create_tables(engine)
    
    # Importar dados
    print("Importando dados...")
    import_data(engine)
    
    # Executar consultas
    print("Executando análises...")
    run_queries(engine)