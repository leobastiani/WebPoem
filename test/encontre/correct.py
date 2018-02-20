#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "encontre"
    driver = GoogleChrome()
    goTo("http://localhost:3000/"+WebPoem.title+"/index.htm")
    assert search("Me encontre")
    assert not search("Não me encontre")