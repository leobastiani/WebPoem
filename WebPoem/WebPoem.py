#!python3
#encoding=utf-8
from __future__ import print_function, division

from selenium import webdriver
from selenium.webdriver.common.by import By

import selenium.webdriver.chrome.webdriver
import os


class WebPoem:
    @staticmethod
    # navegadores:
    def GoogleChrome():
        WebPoem.driver = selenium.webdriver.chrome.webdriver.WebDriver()
        # define driver como global
        global driver
        driver = WebPoem.driver
        # para acessar nas funções abaixo
        return WebPoem.driver


def WebPoemMain(main, *args, **kwargs):
    try:
        main()
    except Exception as e:
        print('Aperte ENTER para encerrar.')
        input()
        raise e
    finally:
        driver.quit()

def goTo(url):
    driver.get(url)

def WebPoemJs(js, *args):
    try:
        return driver.execute_script("return " + js, *args);
    except Exception:
        execFile('WebPoem')
        return WebPoemJs(js, *args)


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
    waitAjax()

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


def waitAjax():
    try:
        obj = driver.execute_async_script('return window.WebPoem.waitAjax(arguments[0])')
    except Exception:
        execFile("WebPoem")
        return waitAjax()


count = 1
def save():
    global count

    if not os.path.exists('saves'):
        os.mkdir('saves')

    while os.path.exists('saves/'+str(count)+'.txt'):
        count += 1

    with open('saves/'+str(count)+'.txt', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    count += 1


def send():
    if Elements.last is not None:
        Elements.last.send_keys(Keys.ENTER)


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

import re
from WebPoem.Elements import Elements
from WebPoem.NewWindow import NewWindow
from selenium.webdriver.common.keys import Keys
