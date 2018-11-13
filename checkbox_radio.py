#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "checkbox_radio"
    driver = GoogleChrome()
    goTo("http://localhost:3000/"+WebPoem.title+"/index.htm")
    findInput("Marque a opção 2 e 3").check("2", "3")
    findInput("Marque a opção 1").check("1")
    findElement("Enviar").click()
    assert search("Me encontre")