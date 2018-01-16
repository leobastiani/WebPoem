#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.GoogleChrome()
    goTo("http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/")
    numId = 2004
    while numId > 0:
        findInput("Ex: 1475").fill(numId)
        send()
        save()
        numId -= 1
        