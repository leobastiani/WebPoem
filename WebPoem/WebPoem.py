#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import

from selenium import webdriver
from selenium.webdriver.common.by import By

import selenium.webdriver.chrome.webdriver
from selenium.common.exceptions import TimeoutException
import os
import sys

DEBUG = sys.flags.debug or False
def debug(*args):
    '''funciona como print, mas só é executada se sys.flags.debug == 1'''
    if not DEBUG:
        return ;
    print(*args)


class WebPoem:
    driver = None
    alert = None
    title = ''

def WebPoemMain(main, *args, **kwargs):
    try:
        main()
        print(WebPoem.title, 'OK')
    except Exception as e:
        print(WebPoem.title, 'FAIL')
        pause()
        raise e
    finally:
        driver.quit()

def pause():
    print('Aperte ENTER para encerrar.')
    input()

###############
# navegadores #
###############
def GoogleChrome():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_extension('./extension/dist/WebPoem.crx')

    WebPoem.driver = selenium.webdriver.chrome.webdriver.WebDriver(chrome_options=options)
    # define driver como global
    global driver
    driver = WebPoem.driver

    driver.set_page_load_timeout(30)
    driver.set_script_timeout(10 * 60 * 1000)
    # para acessar nas funções abaixo
    return WebPoem.driver

def goTo(url):
    try:
        driver.get(url)
    except TimeoutException as e:
        pass


def send_keys(val):
    if WebPoem.alert:
        return WebPoem.alert.send_keys(val)

def WebPoemJs(js, *args):
    return driver.execute_script("return " + js, *args);


def find(by, str):
    try:
        return driver.find_elements(by, str)
    except:
        return []

def isStdName(str):
    return bool(re.fullmatch(r'[\w\-\.# >\d\(\):]+', str))


# tentativa de encontrar um elemento
# por funções simples, sem precisar chamar o javascript
def _findElement(str):
    # não faço nada enquanto estou no meio de uma requisição
    # ajax
    wait()

    if isStdName(str):
        # procuro um elemento com esse ID
        els = find(By.ID, str)
        if len(els) != 0:
            return Elements(els)

        # tenta com name
        els = find(By.NAME, str)
        if len(els) != 0:
            return Elements(els)

        # tenta com o class name
        els = find(By.CLASS_NAME, str)
        if len(els) != 0:
            return Elements(els)

        # tenta com o seletor de css
        els = find(By.CSS_SELECTOR, str)
        if len(els) != 0:
            return Elements(els)

    # não encontrei
    return []

def findElement(str):
    if WebPoem.alert:
        if str == 'OK':
            return WebPoem.alert
    
    # tentativa pelo simples
    simples = _findElement(str)
    if len(simples) != 0:
        return simples

    # agora é a minha própria tentativa
    # procura um elemento que o tenha esse texto
    # primeiro, vamos tratar esse texto
    return Elements(WebPoemJs("window.WebPoem.findElement('" + str + "')"))

def findInput(str):
    # tentativa pelo simples
    simples = _findElement(str)
    if len(simples) != 0:
        return simples

    # agora é a minha própria tentativa
    # procura um elemento que o tenha esse texto
    # primeiro, vamos tratar esse texto
    return Elements(WebPoemJs("window.WebPoem.findInput(window.WebPoem.findElement('" + str + "'))"))

def execFile(fileName):
    with open('js/'+fileName+'.js', 'r', encoding='utf-8') as file:
        driver.execute_script('return '+file.read())


def wait():
    driver.execute_async_script('return WebPoem.wait().then(arguments[0]);')


count = 1
def save():
    wait()

    global count

    if not os.path.exists('saves'):
        os.mkdir('saves')

    while os.path.exists('saves/'+str(count)+'.txt'):
        count += 1

    with open('saves/'+str(count)+'.txt', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    count += 1


def send():
    wait()
    if Elements.last is not None:
        Elements.last.send_keys(Keys.ENTER)


#####################
# funções de tempo: #
#    h, m, s, ms    #
#####################
def ms(x):
    return x / 1000

def s(x):
    return x

def m(x):
    return x * 60

def h(x):
    return 60 * m(x)
############################
# fim das funções de tempo #
############################


def Number(str):
    nums = Numbers(str)
    if len(nums) == 0:
        return 0
    return nums[-1]

def Numbers(str):
    numbers = re.findall(r'[\d,\.]+', str)

    def numberfy(n):
        if n.find(',') == -1:
            # não tem vírgula
            return float(n)

        # aqui qr dizer q tem vírgula
        if n.find('.') == -1:
            # só tem vírgula
            return float(n.replace(',', '.'))

        # tem os dois
        # vejo qual deles está mais próximo
        # do final da string
        ponto = re.search(r'([\.,])\d+$', n).group(1)
        if ponto == '.':
            # remove as vírgulas
            # e retorna
            return float(n.replace(',', ''))

        # a vírgula separa
        # o inteiro dos décimos
        return float(n.replace('.', '').replace(',', '.'))

    return [numberfy(x) for x in numbers]


def search(s):
    wait()
    text = driver.find_element(By.TAG_NAME, 'body').text
    return text.find(s) != -1

import re
from WebPoem.Elements import Elements
from WebPoem.NewWindow import NewWindow
from selenium.webdriver.common.keys import Keys
