#========================================================================================#
#--------------------------------Información del proyecto--------------------------------#
# Proyecto: Scraper Flashscore Peruvian League (SFsPL)
# Autor: Gianfranco Soria Alosilla
# @: gianfranco.soria@pucp.edu.pe  
# GitHub: Gianfranso.Soria
#========================================================================================#

#----------------------------------------------------------------------------------------#
# 0. Importar librerias necesarias
#........................................................................................#
import os
import sys
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

#----------------------------------------------------------------------------------------#
# 1. Fijar directorio de trabajo
#........................................................................................#
os.chdir(r'C:\Users\PC-1\Documents\GitHub\Scraper-BD-Liga1Betsson\Scrapers')
print(os.getcwd())

#----------------------------------------------------------------------------------------#
# 2. Fijar parámetros
#........................................................................................#

# 2.0 Varibles y parámetros
url='https://www.flashscore.pe/futbol/peru/liga-1-2022/resultados/'
button_cookies="//*[@id='onetrust-accept-btn-handler']"
scroll="//*[@id='live-table']/div[1]/div/div/a"
cod_xpath="//*[@id='live-table']/div[1]/div/div"
max_rep=5
intentos_rep=0
#****************************************************************************************#
# 2.1 Configuración de opciones para el webdriver
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')              # Modo headless, sin abrir ventana de navegador
chrome_options.add_argument('--disable-notifications') # Deshabilitar notificaciones
chrome_options.add_argument('--start-maximized')       # Maximizar la ventana del navegador
chrome_options.add_argument('--disable-infobars')      # Deshabilitar infobars
chrome_options.add_argument('--no-sandbox')            # Ejecutar sin sandbox
chrome_options.add_argument('--disable-dev-shm-usage') # Deshabilitar uso de memoria compartida /dev/shm
chrome_options.add_argument('--disable-gpu')           # Deshabilitar aceleración de GPU
#****************************************************************************************#

#----------------------------------------------------------------------------------------#
# 3. Iniciar navegador
#........................................................................................#

# 3.0 Abrir la página
driver=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), 
                        options=chrome_options)
driver.get(url)

# 3.1 Esperar a que el botón de aceptar cookies sea visible y cliqueable
wait=WebDriverWait(driver, 50)
try:
    accept_cookies_button = wait.until(
        EC.element_to_be_clickable((By.XPATH,button_cookies))
    )
    accept_cookies_button.click()
except:
    print('No se pudo hacer clic en el botón de aceptar cookies.')
    driver.close()
    sys.exit()
time.sleep(2)

# 3.2 Scroll página
while intentos_rep<max_rep:
    scroll_click=None
    try:
        scroll_click=driver.find_element(By.XPATH, scroll)
    except:
        pass

    if scroll_click:
        scroll_click.click()
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        intentos_rep+=1
        time.sleep(0.5)
    else:
        intentos_rep+=1

#----------------------------------------------------------------------------------------#
# 4. Extraer códigos de cada partido
#........................................................................................#

content_cod=driver.find_element(By.XPATH,cod_xpath)
soup_cod=content_cod.get_attribute('innerHTML')
buscar1_cod='<div id="g_1_'
buscar2_cod='title="¡Haga click para detalles del partido!"'
result1_cod=[_.start() for _ in re.finditer(buscar1_cod,soup_cod)]
result2_cod=[_.start() for _ in re.finditer(buscar2_cod,soup_cod)]
result_buscar_cod=[0]*len(result1_cod)
for i in range(len(result1_cod)):
    result_buscar_cod[i]=str(soup_cod[result1_cod[i]+13:result2_cod[i]-2])

#----------------------------------------------------------------------------------------#
# 5. 
#........................................................................................#

driver.get('https://www.flashscore.pe/partido/'+f'{result_buscar_cod[1]}'+'/#/resumen-del-partido/resumen-del-partido')
time.sleep(1)
driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
time.sleep(2)
html=driver.page_source
soup=BeautifulSoup(html, 'html.parser')
elements=soup.find_all(class_="smv__verticalSections section")
texto_completo = ""

for element in elements:
    text = '\n'.join(element.stripped_strings)
    texto_completo += text + '\n'
texto_completo=texto_completo.split('\n')

elements.text.splitlines()
resumen_match_soup[276:]
print(resumen_match)
print('Fin del programa...')    



