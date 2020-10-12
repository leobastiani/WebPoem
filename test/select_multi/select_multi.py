#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "select_multi"
    driver = GoogleChrome()
    goTo("http://localhost:3000/"+WebPoem.title+"/index.htm")
    findInput("Selecione todos").select("123", "456", "789")
    findElement("Enviar").click()
    assert search("Me encontre")
