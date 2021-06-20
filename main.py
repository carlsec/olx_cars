from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import requests
import numpy as np
import datetime
import time
import os

list_fuels = ['Gasolina', 'Flex', 'Diesel', 'Gás Natural', 'Etanol']
list_types = ['SUV', 'Sedã', 'Passeio', 'Hatch', 'Pick-up', 'Van/Utilitário', 'Conversível']
list_poten = ['1.8', '1.6', '1.0','1.7', '2.0 - 2.9', '1.5', '1.4', '1.3', '4.0 ou mais']
list_directions = ['Hidráulica', 'Elétrica', 'Mecânica']
list_changes = ['Manual', 'Automático', 'Semi-Automático']
list_colors = ['Branco', 'Prata', 'Verde', 'Azul', 'Amarelo', 'Vermelho', 'Preto', 'Cinza']
list_doors = ['4 portas', '2 portas']


def search_links():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless") #2
    chrome_options.add_argument("--no-sandbox") #2
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=chrome_options)
    
    links = []
    for pagina in tqdm(range(1)):
        url = 'https://sp.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios?o={}&sf=1'.format(pagina)
        response = driver.get(url=url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        html_splited = html.split("sc-1fcmfeb-2 juiJqh")
        for anuncio in html_splited:
                try: #5
                    soup = BeautifulSoup(anuncio, 'html.parser')
                    elemento_link = soup.find("a", {"data-lurker-detail":"list_id"}) #4
                    link = elemento_link.get("href") #6
                except:
                    None
                else:
                    links.append(link) #7
    return links


def apro(content, list_=None):
    for i in range(len(content)):
        text = content[i].text
        res = text in list_
        if res == True:
            return text
    return ''


def number(content):
    for i in range(len(content)):
        text = content[i].text
        try:
            number = int(text)
            return number
        except:
            text = ''
    return ""


def fipe_brand(name_brand, fipe_json):
    try:
        for n in range(len(fipe_json)):
            fipe_brand = fipe_json[n]['fipe_name'].upper()
            if name_brand == fipe_brand:
                return fipe_json[n]['id']
        return 'Not'
    except:
        return ''
        
        
def fipe_carr(name_carr, r_carros):
    try:
        for n in range(len(r_carros)):
            fipe_carr = r_carros[n]['fipe_name'].upper()
            #print(fipe_carr)
            point_fipe_carr = fipe_carr[-1]
            point_name_carr = name_carr[-1]
            
            if point_fipe_carr == '.':
                point_fipe_carr = True
            else:
                point_fipe_carr = False
            
            if point_name_carr == '.':
                point_name_carr = True
            else:
                point_name_carr = False
                
                
            if point_fipe_carr == True and point_name_carr == False:
                fipe_carr = fipe_carr[:-1]
            elif point_fipe_carr == False and point_name_carr == True:
                name_carr = name_carr[:-1]
                
            if name_carr == fipe_carr:
                return r_carros[n]['id']
            
        return 'Not'
    except:
        return ''
    
    
def fipe_model(model_carr, fipe_json):
    try:
        for n in range(len(fipe_json)):
            fipe_carr = fipe_json[n]['name']
            #print(model_carr, fipe_carr)
            if model_carr == fipe_carr:
                return fipe_json[n]['id']
        return 'Not'
    except:
        return ''
    
    
def fipe(model_carr, fipe_json):
    try:
        for n in range(len(fipe_json)):
            fipe_carr = fipe_json[n]['name']
            #print(model_carr, fipe_carr)
            if model_carr == fipe_carr:
                return fipe_json[n]['id']
        return 'Not'
    except:
        return ''
    
    
def search_data(links):
    titles = []
    prices = []
    models = []
    brands = []
    yers = []
    fuels = []
    kms = []
    directions = []
    changes = []
    types = []
    poten = []
    colors = []
    doors = []
    link_url = []
    dates = []

    c = 0

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless") #2
    chrome_options.add_argument("--no-sandbox") #2
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=chrome_options)

    for u in tqdm(links[:3]):
    #print(c)
        try:
            response = driver.get(url=u)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
        
            title = soup.find("h1", {"class":"sc-1q2spfr-0 fSThqK sc-ifAKCX cmFKIN"})
            price = soup.find("h2", {"class":"sc-1leoitd-0 cIfjkh sc-ifAKCX cmFKIN"})
            date = soup.find("span", {"class":"sc-1oq8jzc-0 jvuXUB sc-ifAKCX fizSrB"})
            content = soup.find("div", {"class":"sc-hmzhuo sc-1g2w54p-1 fEpzkb sc-jTzLTM iwtnNi"})        
            model = content.findAll("a")[0].text 
            brand = content.findAll("a")[3].text
            yer = content.findAll("a")[4].text
            fuel = content.findAll("a")[5].text
        
            content2 = soup.findAll("span", {"class":"sc-ifAKCX cmFKIN"})
        
            typy = apro(content2, list_types)
            pote = apro(content2, list_poten)
            direction = apro(content2, list_directions)
            change = apro(content2, list_changes)
            color = apro(content2, list_colors)
            door = apro(content2, list_doors)
            km = number(content2)
        except:
            titles.append("")
            prices.append("")
            models.append("")
            brands.append("")
            yers.append("")
            fuels.append("")
            types.append("")
            poten.append("")
            kms.append("")
            directions.append("")
            changes.append("")
            colors.append("")
            doors.append("")
            link_url.append("")
            dates.append("")
        else:
            titles.append(title.text)
            prices.append(price.text)
            models.append(model)        
            brands.append(brand)
            yers.append(yer)
            fuels.append(fuel)
            types.append(typy)
            poten.append(pote)
            kms.append(km)
            directions.append(direction)
            changes.append(change)
            colors.append(color)
            doors.append(door)
            link_url.append(u)
            dates.append(date.text)
        c += 1
        
        matrix = {
        'Titulo': titles,
        'Preco': prices,
        'Modelo': models, 
        'Fabricante': brands,
        'Ano': yers,
        'Combustivel': fuels,
        'Tipo do Veiculo': types,
        'Potencia': poten,
        'Km Rodado': kms,
        'Direção': directions,
        'Cambio': changes,
        'Cor': colors,
        'Portas': doors,
        'Link': link_url,
        'Dates': dates
        } #8
        df = pd.DataFrame(data=matrix) #9
        df['fipe'] = np.arange(len(df))
        
    return df


def format_data(df):
    for i in range(len(df)):
        name_model = df['Modelo'][i]
        name_brand = df['Fabricante'][i]
    
        name_model = name_model.replace(name_brand + " ", "")
        df['Modelo'][i] = name_model
    
        price_car = df['Preco'][i]
        try:
            price_car = price_car.split('.')
            price_car1 = price_car[0].replace("R$", "")
            price_car = price_car1 + price_car[1]
            df['Preco'][i] = int(price_car)
        except:
            df['Preco'][i] = ''
    return df


def format_date(df):
    for i in range(len(df)):
        try:
            date_name = df['Dates'][i] # Publicado em 19/06 às 15:57
            date_name = date_name.split(" ")
            day, month = date_name[2].split("/")
            year = datetime.date.today().year
            date_name = datetime.datetime(year, int(month), int(day), 0)
            df['Dates'][i] = date_name
        except:
            df['Dates'][i] = ''
    regra = datetime.timedelta(days=-1)
    date_now = datetime.datetime.now()
    date_regra = date_now + regra
    
    date_regra = datetime.datetime(date_regra.year, date_regra.month, date_regra.day)
    #print(date_regra)
    return df, date_regra


def search_fipe(df):
    marcas = requests.get('http://fipeapi.appspot.com/api/1/carros/marcas.json')
    r_marcas = marcas.json()
    c = 1
    for i in tqdm(range(len(df))):
        if c >= 57:
            c = 0
            time.sleep(45)
        name_model = df['Modelo'][i]
        name_brand = df['Fabricante'][i]
    
        fuel = df['Combustivel'][i]
        yer = df['Ano'][i]
    
        name_model_car = yer + ' ' + 'Gasolina'
    
        try:

            id_marca = int(fipe_brand(name_brand, r_marcas))
            #df2['id_marca'][i] = id_marca
    
            carros = requests.get(f'http://fipeapi.appspot.com/api/1/carros/veiculos/{id_marca}.json')
            r_carros = carros.json()
    
            id_carro = fipe_carr(name_model, r_carros)
            #df2['id_carro'][i] = id_carro
        
            modelo = requests.get(f'http://fipeapi.appspot.com/api/1/carros/veiculo/{id_marca}/{id_carro}.json')
            r_modelo = modelo.json()
        
            id_modelo = fipe_model(name_model_car, r_modelo)
            #df2['id_modelo'][i] = id_modelo
        
            fipe = requests.get(f'http://fipeapi.appspot.com/api/1/carros/veiculo/{id_marca}/{id_carro}/{id_modelo}.json')
            r_fipe = fipe.json()

            df['fipe'][i] = r_fipe['preco']
        
        except:
            #df2['id_marca'][i] = ''
            #df2['id_carro'][i] = ''
            #df2['id_modelo'][i] = ''
            df['fipe'][i] = ''
        
        c += 3
        
    return df


def format_fipe(df):
    df = df[df['fipe'] != '' ].reset_index(drop=True).fillna('0')
    df = df[df['Preco'] != '' ].reset_index(drop=True).fillna('0')
    
    for i in range(len(df)):
        price_fipe = df['fipe'][i]
        price_fipe = price_fipe.replace("R$ ", "")
        price_fipe = price_fipe.replace(".", "")
        price_fipe = price_fipe.split(",")
    
        df['fipe'][i] = price_fipe[0]
    df['fipe'] = df['fipe'].astype(int)
    df['Preco'] = df['Preco'].astype(int)
        
    df = df[df['fipe'] != 0].reset_index(drop=True)
    df = df[df['Preco'] != 0].reset_index(drop=True)
    
    return df


def rate(df):
    rate = []

    for i in range(len(df)):
        price_fipe = df['fipe'][i]
        price =  df['Preco'][i]
    
        if price_fipe > price:
            v = ((price_fipe - price)/price_fipe)*100
            rate.append(v)
        else:
            rate.append(0)
    df['rate'] = rate
    df['rate'] = df['rate'].astype(int)
    
    return df


def main():
    links = search_links()
    links = search_links()
    df = search_data(links)
    df = format_data(df.copy())
    df, start_date = format_date(df.copy())
    df = search_fipe(df.copy())
    df = format_fipe(df.copy())
    df = rate(df.copy())
    
    data = pd.read_csv('data.csv')
    data = pd.concat([data, df], axis=0, ignore_index=True).reset_index(drop=True)
    data = data.sort_values(by=['rate'], ascending=False)
    data = data.drop_duplicates()
    data['Dates'] = pd.to_datetime(data['Dates'])
    data = data[(data['Dates'] > start_date)]
    data.to_csv('data.csv', index=False)