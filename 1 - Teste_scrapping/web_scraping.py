import requests
from bs4 import BeautifulSoup
import zipfile
import os

# URL para extração
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Criando a sessão
session = requests.Session()

# Accessando o Site
response = session.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Procurando os links dos pdf's
pdf_links = []
for link in soup.find_all('a', href=True):
    if 'Anexo' in link.text and (link['href'].endswith('.pdf')):
        pdf_links.append(link['href'])

# Baixando PDFs
pdf_files = []
for pdf_link in pdf_links:
    pdf_response = session.get(pdf_link)
    pdf_name = pdf_link.split('/')[-1]
    pdf_files.append(pdf_name)
    with open(pdf_name, 'wb') as f:
        f.write(pdf_response.content)

# Criando o arquivo ZIP
zip_filename = "anexos.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for pdf_file in pdf_files:
        zipf.write(pdf_file)

# Movendo o ZIP para o Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
os.rename(zip_filename, os.path.join(desktop_path, zip_filename))

print(f"Download Concluido e arquivos salvos em {desktop_path}")
