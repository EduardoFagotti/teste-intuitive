import requests
from bs4 import BeautifulSoup
import os
import zipfile
from urllib.parse import urljoin  

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
headers = {'User-Agent': 'Mozilla/5.0'} 
pasta_downloads = "downloads"
os.makedirs(pasta_downloads, exist_ok=True)


response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')


pdf_links = []
for link in soup.select('ol a.internal-link[href$=".pdf"]'):  
    href = link.get('href')
    if 'Anexo_I' in href or 'Anexo_II' in href:  
        pdf_links.append(urljoin(url, href))  


for pdf_url in pdf_links:
    try:
        nome_arquivo = os.path.join(pasta_downloads, pdf_url.split('/')[-1])
        with open(nome_arquivo, 'wb') as f:
            f.write(requests.get(pdf_url, headers=headers).content)
        print(f"Baixado: {nome_arquivo}")
    except Exception as e:
        print(f"Falha ao baixar {pdf_url}: {str(e)}")


if os.listdir(pasta_downloads):
    with zipfile.ZipFile('anexos.zip', 'w') as zipf:
        for arquivo in os.listdir(pasta_downloads):
            zipf.write(os.path.join(pasta_downloads, arquivo), arquivo)
    print("\n✅ Concluído! Arquivos compactados em 'anexos.zip'")
else:
    print("\n❌ Nenhum PDF foi baixado. Verifique os links no HTML.")