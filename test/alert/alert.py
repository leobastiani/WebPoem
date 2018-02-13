#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "alert"
    driver = GoogleChrome()
    import os
    goTo("http://localhost:3000/"+WebPoem.title+"/index.htm")
    with NewWindow():
        findElement("OK").click()
    with NewWindow():
        findElement("OK").click()
    assert search("Me encontre")