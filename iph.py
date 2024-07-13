import requests
from bs4 import BeautifulSoup
import re
import mailtrap as mt
from datetime import datetime, timezone, timedelta
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import time
import telepot
import secrets

def update_document_content(document_id, new_content):
    # Prima rimuovi tutto il contenuto esistente
    document = service.documents().get(documentId=document_id).execute()
    end_index = document['body']['content'][-1]['endIndex']
    requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': end_index - 1
                }
            }
        },
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': new_content
            }
        }
    ]

    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    return result

def aggiorna_file():
    global new_content
    global contenuto_file_iniziale
    
    if not new_content == '':
        da_mettere = new_content + contenuto_file_iniziale
        da_mettere = da_mettere.replace(' ', '')
        da_mettere = da_mettere.replace('\n', '')
            
        if len(da_mettere) > 25000:
            da_mettere = da_mettere[:25000]
        
        contat = 0
        while contat <= 5:
            contat += 1
            try:
                update_document_content(DOCUMENT_ID, da_mettere)
                contenuto_file_iniziale = contenuto()
                print("Aggiornamento riuscito")
                break
            except:
                time.sleep(1)
                print("Aggiornamento NON riuscito")
            

def contenuto():
    contat = 0
    contenuto_file = ''
    while contat <= 5:
        contat += 1
        try:
            document = service.documents().get(documentId=DOCUMENT_ID).execute()
            content = document.get('body').get('content')
            for element in content:
                if 'paragraph' in element:
                    elements = element['paragraph']['elements']
                    for e in elements:
                        contenuto_file += e['textRun']['content']
            print("Lettura riuscita")
            break
        except:
            time.sleep(1)
            print("Lettura NON riuscita")
            
    return contenuto_file


def manda_mail(link_annuncio, titolo='Annuncio interessante'):

    now = datetime.now()

    inizio_ora_legale = datetime(now.year, 3, 31)
    fine_ora_legale = datetime(now.year, 10, 27)

    if inizio_ora_legale <= now <= fine_ora_legale:
        ora_attuale = datetime.now(timezone(timedelta(hours=2)))
    else:
        ora_attuale = datetime.now(timezone(timedelta(hours=1)))

    formato_leggibile = str(ora_attuale.strftime("%H:%M"))

    mail = mt.Mail(
        sender=mt.Address(email="mailtrap@demomailtrap.com", name="Tracker Subito.it"),
        to=[mt.Address(email=MAIL_MIA)],
        subject=titolo,
        text='Orario: ' + formato_leggibile + '\n\nLink annuncio: ' + link_annuncio + '\n\nValutazione Swappie: https://swappie.com/it/vendere/iphone/',
        category="Integration Test",
        )

    client = mt.MailtrapClient(token=API_MAIL)
    client.send(mail)
  

API_MAIL = os.getenv('API_MAIL')
MAIL_MIA = os.getenv('MAIL_MIA')
TOK = os.getenv('TOK')
TG_TOK = os.getenv('TG_TOK')
CHAT_ID = os.getenv('CHAT_ID')
LINK_INIZIALE = os.getenv('LINK_INIZIALE')
LINK_INIZIALE_2 = os.getenv('LINK_INIZIALE_2')
TOK = json.loads(TOK)

pmax = "=" + str(secrets.randbelow(1200) + 750)
pmin = "=" + str(secrets.randbelow(19) + 20)

LINK_INIZIALE = LINK_INIZIALE.replace('=1000', pmax)
LINK_INIZIALE_2 = LINK_INIZIALE_2.replace('=1000', pmax)

LINK_INIZIALE = LINK_INIZIALE.replace('=30', pmin)
LINK_INIZIALE_2 = LINK_INIZIALE_2.replace('=30', pmin)

SCOPES = ['https://www.googleapis.com/auth/documents']
creds = service_account.Credentials.from_service_account_info(TOK, scopes=SCOPES)
DOCUMENT_ID = '1RrJzZSB8OUbmt-vtt-ifk8bKeeC2mUdQQY1d2u6QSp0'
service = build('docs', 'v1', credentials=creds)

bot = telepot.Bot(TG_TOK)

new_content = ''
contenuto_file_iniziale = ''

page = requests.get(LINK_INIZIALE)
soup = BeautifulSoup(page.text, 'html.parser')
product_list_items_1 = soup.find_all('div', class_=re.compile(r'item-card'))

page = requests.get(LINK_INIZIALE_2)
soup = BeautifulSoup(page.text, 'html.parser')
product_list_items_2 = soup.find_all('div', class_=re.compile(r'item-card'))

product_list_items_tot = product_list_items_1 + product_list_items_2

for item in product_list_items_tot:
    
    a_tag = item.find('a', class_='SmallCard-module_link__hOkzY')
    link_annuncio = a_tag['href'] if a_tag else 'N/A'
    
    price_tag = item.find('p', class_='index-module_price__N7M2x')
    prezzo = price_tag.text.strip() if price_tag else 'N/A'
    prezzo = prezzo.replace('.', '')
    prezzo = prezzo.replace(',', ' ')
    prezzo = int(prezzo.split('€')[0])

    title_tag = item.find('h2', class_='index-module_sbt-text-atom__ifYVU')
    titolo_annuncio = title_tag.text.strip() if title_tag else 'N/A'

    if not "cerco" in titolo_annuncio.lower() and not "malfunzionante" in titolo_annuncio.lower() and not "non funzionante" in titolo_annuncio.lower() and not "lcd" in titolo_annuncio.lower() and not "rotta" in titolo_annuncio.lower() and not "schermo" in titolo_annuncio.lower() and not "scocca" in titolo_annuncio.lower() and not "fotocamera" in titolo_annuncio.lower() and not "fotocamere" in titolo_annuncio.lower() and not "display" in titolo_annuncio.lower() and not "scheda madre" in titolo_annuncio.lower() and not "bloccato" in titolo_annuncio.lower() and not "cover per" in titolo_annuncio.lower() and not "guasto" in titolo_annuncio.lower() and not "rotto" in titolo_annuncio.lower() and not "ricambi" in titolo_annuncio.lower() and not "da aggiustare" in titolo_annuncio.lower() and not "no wifi" in titolo_annuncio.lower() and not "display" in titolo_annuncio.lower():
        if "cover" in titolo_annuncio.lower():
            if not "con cover" in titolo_annuncio.lower() and not "regalo" in titolo_annuncio.lower() and not "+" in titolo_annuncio.lower() and not "pi" in titolo_annuncio.lower():
                continue
        if "custodia" in titolo_annuncio.lower():
            if not "con custodia" in titolo_annuncio.lower() and not "regalo" in titolo_annuncio.lower() and not "+" in titolo_annuncio.lower() and not "pi" in titolo_annuncio.lower():
                continue
        if "iphone 11" in titolo_annuncio.lower() or "iphon 11" in titolo_annuncio.lower():
            min = 39
            max = 121
        elif "iphone 12" in titolo_annuncio.lower() or "iphon 12" in titolo_annuncio.lower():
            if "mini" in titolo_annuncio.lower():
                min = 39
                max = 151
            elif "pro" in titolo_annuncio.lower():
                if "max" in titolo_annuncio.lower():
                    min = 220
                    max = 340
                else:
                    min = 39
                    max = 221
            else:
                min = 39
                max = 216
            
        elif "iphone 13" in titolo_annuncio.lower() or "iphon 13" in titolo_annuncio.lower():
            if "mini" in titolo_annuncio.lower():
                min = 170
                max = 241
            elif "pro" in titolo_annuncio.lower():
                if "max" in titolo_annuncio.lower():
                    min = 289
                    max = 421
                else:
                    min = 199
                    max = 320
            else:
                min = 199
                max = 311
                
        elif "iphone 14" in titolo_annuncio.lower() or "iphon 14" in titolo_annuncio.lower():
            if "pro" in titolo_annuncio.lower():
                if "max" in titolo_annuncio.lower():
                    min = 309
                    max = 451
                else:
                    min = 289
                    max = 431
            else:
                min = 209
                max = 321
        else:
            continue
            
        if prezzo > min and prezzo < max:

            if not contenuto_file_iniziale:
                contenuto_file_iniziale = contenuto()
                print(contenuto_file_iniziale)
            
            if not link_annuncio in contenuto_file_iniziale + new_content:
                #manda_mail(link_annuncio, titolo_annuncio)
                bot.sendMessage(CHAT_ID, titolo_annuncio + ' a ' + str(prezzo) + '€' + ': '+ link_annuncio)
                new_content = link_annuncio + new_content
                aggiorna_file()

delay = secrets.randbelow(10) + 5
time.sleep(delay)
    
    
