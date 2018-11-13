#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "sucupira exemplo 1"
    driver = GoogleChrome()
    goTo("https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/programa/listaPrograma.jsf")
    findInput("Instituição de Ensino Superior").fill("33003017")
    findElement("33003017 UNIVERSIDADE ESTADUAL DE CAMPINAS (UNICAMP)").click()
    findInput("Programa").fill("CIÊNCIA DA COMPUTAÇÃO")
    findElement("Consultar").click()
    Lupa = findElement('.glyphicon-search')
    while True:
        Clickable = findElement("Próxima")
        for element in Lupa[1:]:
            element.click()
            with NewWindow():
                save()
        if not Clickable.isClickable():
            break
        Clickable.click()