# from tkinter.tix import Tree
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import pyautogui
from datetime import date
from tqdm import tqdm
import re




def certificado():

    select_cert = 'Selecionar.png'
    
    pyautogui.press(['tab'], 15)
    img = pyautogui.locateOnScreen(select_cert)
    pyautogui.click(img)
    

def sped():
       
    file = 'lista_out.xlsx'
    dados = pd.read_excel(file)

    link = 'https://webas.sefaz.pi.gov.br/eageat/jsp/login/login.jsf?codigoCliente=fb958a088fb0dce174deef135f0a69e5'

    data_atual = date.today()

    if data_atual.month < 10:

        data_ini = '0' + str(data_atual.month -1) + str(data_atual.year) 
    else:
        data_ini = str(data_atual.month - 1) + str(data_atual.year)


    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        with page.expect_navigation():
            page.goto(link)
            
        page.click('xpath=//*[@id="form"]/div/main/section/article/p[5]/a/img')

        sleep(3)

        certificado()

        sleep(10)

       # page.is_visible('xpath=//*[@id="formMain:j_id5"]/div/div/div/ul/li[1]/a')
        page.click('xpath=//*[@id="formMain:j_id5"]/div/div/div/ul/li[1]/a')
        page.click('xpath=//*[@id="formMain:j_id5"]/div/div/div/ul/li[1]/ul/li[8]/a')
        page.go_back()
        page.is_visible('xpath=//*[@id="formMain:j_id5"]/div/div/div/ul/li[1]/a')
        page.click('xpath=//*[@id="formMain:j_id5"]/div/div/div/ul/li[1]/a')
        page.click('xpath=//*[@id="formMain:j_id5"]/div/div/div/ul/li[1]/ul/li[9]/a')
        page.is_visible('xpath=//*[@id="app"]/div/nav/div[1]/div[2]/div[5]/a/div[2]/div')
        page.click('xpath=//*[@id="app"]/div/nav/div[1]/div[2]/div[5]/a/div[2]/div')


        for x, num in enumerate(tqdm(dados['N'])):
            cnpj_cpf = dados.loc[x, 'CNPJ-CPF']

            cnpj_cpf_efd = cnpj_cpf[0:10]
            cnpj_cpf_efd = str(cnpj_cpf_efd).replace('.', "")

            value_x = page.locator("//div[@class='v-select__slot']").nth(1)
            value_y = value_x.inner_html()
            regex = re.compile(r'id=\"input-(\d*)')
            value_x = regex.search(value_y)
            value_x = value_x.groups()[0]


            page.fill(f'xpath=//*[@id="input-{value_x}"]', cnpj_cpf_efd)

            cnpj_cpf_value = page.locator(f'xpath=//*[@id="list-{value_x}"]/div/div').inner_text()

            page.is_visible(f'xpath=//*[@id="list-{value_x}"]/div/div')


            if cnpj_cpf_value == 'Não há dados disponíveis':

                dados.loc[x, 'PERIODO'] = 'SEM PROCURAÇÃO'
                dados.loc[x, 'DATA ENTREGA'] = 'SEM PROCURAÇÃO'
                dados.loc[x, 'TIPO'] = 'SEM PROCURAÇÃO'
                dados.loc[x, 'STATUS'] = 'SEM PROCURAÇÃO'                
            
            else:

                page.click(f'xpath=//*[@id="list-{value_x}"]/div/div')
                
                page.fill('xpath=//*[@id="input-80"]', str(data_ini))          
                page.fill('xpath=//*[@id="input-83"]', str(data_ini))
            
                page.click('xpath=//*[@id="app"]/div[1]/main/div/div/div/div[3]/form/div/div[7]/div/div/div/div/button[2]/span')

                sleep(3)

                # alteracoes
                
                d = ['EPE', 'IS', 'CNPJ', 'P', 'DE', 'DR', 'A', 'F', 'S']
                table = page.locator('xpath=//tbody')
                html = table.inner_html()
                soup = BeautifulSoup(html, "html.parser")
                trs = soup.find_all('tr')
                for tr in trs:
                    data = {}
                    tds = tr.find_all('td')
                    for name, td in zip(d, tds[1:]):
                        data[name] = td.contents[0]

                    dados.loc[x, 'PERIODO'] = data.get('P')
                    dados.loc[x, 'DATA ENTREGA'] = data.get('DR')
                    dados.loc[x, 'ENTREGA'] = data.get('F')
                    dados.loc[x, 'STATUS'] = data.get('S')

            page.click('xpath=//*[@id="app"]/div/main/div/div/div/div[3]/form/div/div[7]/div/div/div/div/button[1]')                
            sleep(1)
            
    dados.to_excel('lista_out.xlsx', index=False)


#-------------------------------------------------------------------------------------------------#




# sped()

