#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "prompt"
    driver = GoogleChrome()
    goTo("http://localhost:3000/"+WebPoem.title+"/index.htm")
    findElement("Clique em mim").click()
    with NewWindow():
        send_keys("123")
        findElement("OK").click()
    assert search("Me encontre")
