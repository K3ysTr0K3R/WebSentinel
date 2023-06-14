import requests
from bs4 import BeautifulSoup
from lib.ConsoleHandler import *

class Scanner:
    def __init__(self):
        self.msg = ConsoleHandler()

website_url = 'https://www.silkbank.com.pk'

response = requests.get(website_url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: href.endswith('.pdf'))
    for link in pdf_links:
        pdf_url = link['href']
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code == 200:
            filename = pdf_url.split('/')[-1]
            with open(filename, 'wb') as file:
                file.write(pdf_response.content)
            print(f"[*] [URL] [{website_url}] [PDF] [{filename}] [SAVED]")
        else:
            print(f"[~] Failed to fetch {pdf_url}")
else:
    print(f"[~] Cant connect to {website_url}")
    exit()
