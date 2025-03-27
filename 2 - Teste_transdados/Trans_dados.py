import pdfplumber
import pandas as pd
import zipfile
import os
import getpass
import shutil

# Definir o caminho do PDF corretamente
pdf_path = r"C:\Users\USUARIO\Desktop\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"

# Verificar se o arquivo existe
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"O arquivo {pdf_path} não foi encontrado.")

# Extração de dados do PDF
data = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            data.extend(table)

# Criar um DataFrame, verificando se há dados
if not data:
    raise ValueError("Nenhuma tabela foi extraída do PDF.")

df = pd.DataFrame(data[1:], columns=data[0])  # Usar a primeira linha como cabeçalho

# Substituir abreviações
df.replace({'OD': 'Ortopedia', 'AMB': 'Ambulatório'}, inplace=True)

# Salvar para CSV
csv_filename = "rol_procedimentos.csv"
df.to_csv(csv_filename, index=False)

# Criar o arquivo ZIP
user_name = getpass.getuser()
zip_filename = f"Teste_{user_name}.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    zipf.write(csv_filename)

# Mover o ZIP para a área de trabalho
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
shutil.move(zip_filename, os.path.join(desktop_path, zip_filename))

print(f"Arquivo ZIP salvo em: {desktop_path}")
