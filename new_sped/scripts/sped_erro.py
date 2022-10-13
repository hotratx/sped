# from ast import Break
# from tkinter.tix import Tree
# from turtle import isvisible
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import pyautogui
from datetime import date
from tqdm import tqdm
import re


def certificado():

    try:

        select_cert = 'Selecionar.png'

        pyautogui.press(['tab'], 15)
        img = pyautogui.locateOnScreen(select_cert)
        pyautogui.click(img)

    except:

        print('Não foi possível localizar o certificado')


def sped():

    file = '../datas/dados_clientes.xlsx'
    dados = pd.read_excel(file)

    link = 'https://webas.sefaz.pi.gov.br/eageat/jsp/login/login.jsf?codigoCliente=6afdbe8a113e1d6d3b7f436732f'

    data_atual = date.today()

    if data_atual.month < 10:

        data_ini = '0' + str(data_atual.month - 1) + str(data_atual.year)
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

        sleep(6)

        try:

            page.wait_for_selector(
                'xpath=//*[@id="formMain:j_id5"]/div/div/div/ul/li[1]/a')

            page.click(
                'xpath=//*[@id="formMain:j_id5"]/div/div/div/ul/li[1]/a')
            page.click(
                'xpath=//*[@id="formMain:j_id5"]/div/div/div/ul/li[1]/ul/li[9]/a')
            page.is_visible(
                'xpath=//*[@id="app"]/div/nav/div[1]/div[2]/div[5]/a/div[2]/div')
            page.click(
                'xpath=//*[@id="app"]/div/nav/div[1]/div[2]/div[8]/a/div[2]/div')

            for x, num in enumerate(tqdm(dados['N'])):
                ie = dados.loc[x, 'IE']

                ie_efd = ie[0:12]
                ie_efd = str(ie_efd).replace('.', "").replace('-', "")

                value_x = page.locator(
                    '//*[@id="app"]/div/main/div/div/div/form').nth(0)

                value_y = value_x.inner_html()
                regex = re.compile(r'id=\"input-(\d*)')
                value_x = regex.findall(value_y)
                value_input_ie = value_x[0]
                value_input_ini = value_x[1]
                value_input_fin = value_x[2]

                page.fill(f'xpath=//*[@id="input-{value_input_ie}"]', ie_efd)

                ie_efd_value = page.locator(
                    f'xpath=//*[@id="list-{value_input_ie}"]/div/div').inner_text()

                page.is_visible(
                    f'xpath=//*[@id="list-{value_input_ie}"]/div/div')

                if ie_efd_value == 'Não há dados disponíveis':

                    dados.loc[x, 'PERIODO'] = 'SEM PROCURAÇÃO OU SERVIÇO'
                    dados.loc[x, 'DATA ENTREGA'] = 'SEM PROCURAÇÃO OU SERVIÇO'
                    dados.loc[x, 'TIPO'] = 'SEM PROCURAÇÃO OU SERVIÇO'
                    dados.loc[x, 'STATUS'] = 'SEM PROCURAÇÃO OU SERVIÇO'

                    page.click(
                        'xpath=//*[@id="app"]/div[1]/main/div/div/div/form/div/div[2]/div/div/button[1]/span')

                else:

                    page.click(
                        f'xpath=//*[@id="list-{value_input_ie}"]/div/div')

                    page.fill(
                        f'xpath=//*[@id="input-{value_input_ini}"]', str(data_ini))
                    page.fill(
                        f'xpath=//*[@id="input-{value_input_fin}"]', str(data_ini))

                    page.click(
                        'xpath=//*[@id="app"]/div[1]/main/div/div/div/form/div/div[2]/div/div/button[2]/span')

                    # alterações

                    d = ['EPE', 'IS', 'CNPJ', 'P', 'DE']
                    table = page.locator('xpath=//tbody')
                    html = table.inner_html()
                    soup = BeautifulSoup(html, "html.parser")
                    trs = soup.find_all('tr')
                    for tr in trs:
                        data = {}
                        tds = tr.find_all('td')
                        for name, td in zip(d, tds[1:]):
                            data[name] = td.contents[0]

                        dados.loc[x, 'GRUPO'] = data.get('CNPJ')
                        dados.loc[x, 'TIPO'] = data.get('P')
                        dados.loc[x, 'INCONSISTENCIA'] = data.get('DE')

                    sleep(2)

                    page.click(
                        'xpath=//*[@id="app"]/div[1]/main/div/div/div/form/div/div[2]/div/div/button[1]/span')

        except:

            print('Site indisponível')

        dados.to_excel('lista_out.xlsx', index=False)


#-------------------------------------------------------------------------------------------------#


sped()


