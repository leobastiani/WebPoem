#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "two_inputs"
    driver = GoogleChrome()
    goTo("http://localhost:3000/two_inputs/index.htm")
    findInput("Two Inputs").fill("123", "456")
    findElement("Enviar").click()
    assert search("Me encontre")