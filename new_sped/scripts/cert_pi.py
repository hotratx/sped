# +------------------------------------------------------------------+
# |                                               Certidões_Piauí.py |
# |                                    Copyright 2022, Roger Holanda |
# |                                              rogergtsh@gmail.com |
# +------------------------------------------------------------------+

__author__ = "Roger Holanda <rogergtsh@gmail.com>"
__status__ = "development"
__version__ = "1.0.0.0"
__date__ = "20/09/2022"

# -----------------------------------------------------------------------
# Módulos a serem importados
# -----------------------------------------------------------------------

# import string
# from time import sleep
# from turtle import update
from playwright.sync_api import sync_playwright
import pandas as pd
from tqdm import tqdm
import psycopg2

# -----------------------------------------------------------------------
# Variáves Globais
# -----------------------------------------------------------------------

user_DB = str("postgres")
password_DB = str("@RRcontas2022")
host_DB = str("127.0.0.1")
port_DB = str("5432")
database_DB = str("Cont-X")

link = 'https://webas.sefaz.pi.gov.br/certidaonft-web/index.xhtml'
file = 'lista nova.xlsx'
dados = pd.read_excel(file)



# -----------------------------------------------------------------------
# Programa principal
# -----------------------------------------------------------------------

def cert_pi():

    conn = psycopg2.connect(user = user_DB, password = password_DB, host = host_DB, port = port_DB, database = database_DB)
    conn.autocommit = False
    cursor = conn.cursor()

    postgresql_select_query = 'SELECT company_id, company_name, company_cpf_cnpj FROM public.company ORDER BY "company_id";'
    cursor.execute(postgresql_select_query)
    company_list = cursor.fetchall()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        with page.expect_navigation():
             page.goto(link)

#---------------------Solicitar certidão dívida ativa---------------------

        page.locator('xpath=//*[@id="mainMenuForm:mainMenuBar"]/ul/li[1]/a/span[2]').click()
        page.locator('xpath=//*[@id="mainMenuForm:mainMenuBar"]/ul/li[1]/ul/li[2]/a/span[2]').click()
     
        for x, num in enumerate(tqdm(dados['N'])):
            cnpj_cpf = dados.loc[x, 'CNPJ-CPF']
    

            cnpj_cpf = str(cnpj_cpf).replace('.', "").replace('/', "").replace('-', "").replace(' ', "")
            cont = len(str(cnpj_cpf))

            try:
            
                page.is_visible('xpath=//*[@id="tabView:tabContent_tabItem1:formSolicitar:tipoPessoa_label"]')
                page.locator('xpath=//*[@id="tabView:tabContent_tabItem1:formSolicitar:tipoPessoa_label"]').click()

                if cont == 14:
                    page.locator('xpath=//*[@id="tabView:tabContent_tabItem1:formSolicitar:tipoPessoa_0"]').click()

                elif cont == 11:
                    page.locator('xpath=//*[@id="tabView:tabContent_tabItem1:formSolicitar:tipoPessoa_1"]').click()
            
                page.wait_for_timeout(500)
            
                page.locator('xpath=//*[@id="tabView:tabContent_tabItem1:formSolicitar:j_id-2093731013_1a130daa"]').fill("")
                page.locator('xpath=//*[@id="tabView:tabContent_tabItem1:formSolicitar:j_id-2093731013_1a130daa"]').fill(str(cnpj_cpf))                      
                page.locator('xpath=//*[@id="tabView:tabContent_tabItem1:formSolicitar:solicitarBtn"]/span[2]').click()  
                page.is_visible('xpath=//*[@id="tabView:tabContent_tabItem1:formSolicitar:messages"]/div/span')

                aviso_da = page.locator('xpath=//*[@id="tabView:tabContent_tabItem1:formSolicitar:messages"]/div').inner_text()

               
                dados.loc[x, 'D.A SOLICIT'] = aviso_da
                
                page.wait_for_timeout(200)

            except Exception:

                dados.loc[x, 'D.A SOLICIT'] = 'ERRO'
                
                
                page.wait_for_timeout(200)

        page.locator('xpath=//*[@id="tabView"]/div[1]/ul/li/span').click()


#---------------------Solicitar certidão tributária---------------------

        page.locator('xpath=//*[@id="mainMenuForm:mainMenuBar"]/ul/li[2]/a/span[2]').click()
        page.locator('xpath=//*[@id="mainMenuForm:mainMenuBar"]/ul/li[2]/ul/li[2]/a/span[2]').click()


        for x, num in enumerate(tqdm(dados['N'])):
            cnpj_cpf = dados.loc[x, 'CNPJ-CPF']
            ie = dados.loc[x, 'IE']

            cnpj_cpf = str(cnpj_cpf).replace('.', "").replace('/', "").replace('-', "").replace(' ', "")
            ie = str(ie).replace('.', "").replace('/', "").replace('-', "").replace(' ', "")
            cont = len(str(cnpj_cpf))

            try:
            
                page.is_visible('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:tipoPessoa_label"]')
                page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:tipoPessoa_label"]').click()

                if cont == 14:
                    page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:tipoPessoa_0"]').click()
                elif cont == 11:
                    page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:tipoPessoa_1"]').click()

                page.wait_for_timeout(500)

                page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:contribuinteCpfCnpjId"]').fill("")
                page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:contribuinteCpfCnpjId"]').fill(str(cnpj_cpf))

                if ie == 'SINSCRIÇÃO':
                    page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:solicitarBtn"]/span[2]').click()
                else:
                    page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:contribuinteIncricaoId"]').fill("")
                    page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:contribuinteIncricaoId"]').fill(str(ie))
                    page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:solicitarBtn"]/span[2]').click()
                      
                aviso_t = page.locator('xpath=//*[@id="tabView:tabContent_tabItem2:formSolicitar:messages"]/div').inner_text()
            
                dados.loc[x, 'T. SOLICIT'] = aviso_t
                page.wait_for_timeout(200)

            except Exception:

                dados.loc[x, 'T. SOLICIT'] = 'ERRO'
                
                page.wait_for_timeout(200)

        page.locator('xpath=//*[@id="tabView"]/div[1]/ul/li/span').click()


 #---------------------Consulta certidão dívida ativa---------------------   

        for x, num in enumerate(tqdm(dados['N'])):
            cnpj_cpf = dados.loc[x, 'CNPJ-CPF']

            cnpj_cpf = str(cnpj_cpf).replace('.', "").replace('/', "").replace('-', "").replace(' ', "")
            cont = len(str(cnpj_cpf))
         
            try:

                page.click('xpath=//*[@id="mainMenuForm:mainMenuBar"]/ul/li[1]/a/span[2]')
                page.click('xpath=//*[@id="mainMenuForm:mainMenuBar"]/ul/li[1]/ul/li[1]/a/span[2]')

                page.wait_for_load_state()
  
                num_x = num + 2

                page.click(
                    f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:CertidaoNegativaTv:formConsulta:tipoPessoa_label"]')

                if cont == 11:
                    page.click(
                        f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:CertidaoNegativaTv:formConsulta:tipoPessoa_1"]')
                elif cont == 14:
                    page.click(
                        f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:CertidaoNegativaTv:formConsulta:tipoPessoa_0"]')

                page.wait_for_timeout(400)

                page.click(
                    f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:CertidaoNegativaTv:formConsulta'
                    f':j_id803287465_4bc2e83"]')

                page.fill(f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:CertidaoNegativaTv:formConsulta'
                          f':j_id803287465_4bc2e83"]', str(cnpj_cpf))
                page.wait_for_load_state()
                
                page.click(f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:CertidaoNegativaTv:formConsulta'
                           f':j_id803287465_4bc2ee9"]/span[2]')

                page.wait_for_load_state()

                page.is_visible(f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:CertidaoNegativaTv'
                                             f':formConsulta:j_id803287465_4bc2ec4_data"]/tr[1]/td[2]')

                status = page.locator(f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:CertidaoNegativaTv'
                                          f':formConsulta:j_id803287465_4bc2ec4_data"]/tr[1]/td[4]').inner_text()

                dados.loc[x, 'DÍVIDA ATIVA'] = status

                page.locator('xpath=//*[@id="tabView"]/div[1]/ul/li/span').click()

            except Exception:

                dados.loc[x, 'DÍVIDA ATIVA'] = 'ERRO'

                page.locator('xpath=//*[@id="tabView"]/div[1]/ul/li/span').click()


#---------------------Consulta certidão tributária---------------------

        for x, num in enumerate(tqdm(dados['N'])):
            cnpj_cpf = dados.loc[x, 'CNPJ-CPF']

            cnpj_cpf = str(cnpj_cpf).replace('.', "").replace('/', "").replace('-', "").replace(' ', "")
            cont = len(str(cnpj_cpf))

            try:

                page.click('xpath=//*[@id="mainMenuForm:mainMenuBar"]/ul/li[2]/a/span[2]')
                page.click('xpath=//*[@id="mainMenuForm:mainMenuBar"]/ul/li[2]/ul/li[1]/a/span[2]')

                page.wait_for_load_state()

                num_x = num + 13

                page.click(
                    f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:certidaoSituacaoTv:formConsultar:tipoPessoa_label"]')

                if cont == 14:
                    page.click(
                        f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:certidaoSituacaoTv:formConsultar:tipoPessoa_0"]')
                elif cont == 11:
                    page.click(
                        f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:certidaoSituacaoTv:formConsultar:tipoPessoa_1"]')

                page.wait_for_timeout(400)

                page.click(
                    f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:certidaoSituacaoTv:formConsultar'
                    f':contribuinteCpfCnpjId"]')

                page.fill(
                    f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:certidaoSituacaoTv:formConsultar'
                    f':contribuinteCpfCnpjId"]',
                    str(cnpj_cpf))

                page.wait_for_load_state()

                page.click(
                    f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:certidaoSituacaoTv:formConsultar:buscarBtn'
                    f'"]/span[2]')

                page.wait_for_load_state()

                page.is_visible(f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:certidaoSituacaoTv:formConsultar'
                                    f':resultsDataTable_data"]/tr[1]/td[2]')

                status = page.locator(
                        f'xpath=//*[@id="tabView:tabContent_tabItem{num_x}:certidaoSituacaoTv:formConsultar'
                        f':resultsDataTable_data"]/tr[1]/td[4]').inner_text()

                dados.loc[x, 'TRIBUTÁRIA'] = status

                page.locator('xpath=//*[@id="tabView"]/div[1]/ul/li/span').click()

            except Exception:

                dados.loc[x, 'TRIBUTÁRIA'] = "ERRO"

                page.locator('xpath=//*[@id="tabView"]/div[1]/ul/li/span').click()


#-------------------------------------------------------------------------


def main():

    cert_pi()
    dados.to_excel('lista_out.xlsx', index=False)

# ------------------------------------------------------------------------
if __name__ == "__main__":
    main()
# ------------------------------------------------------------------------





