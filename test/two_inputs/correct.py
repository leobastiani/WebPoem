#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    driver = GoogleChrome()
    import os
    goTo("file:///"+os.getcwd()+"/index.htm")
    findInput("Two Inputs").fill("123", "456")
    findElement("Enviar").click()
    assert search("Me encontre")