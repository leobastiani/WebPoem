#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "timeout"
    driver = GoogleChrome()
    goTo("http://localhost:3000/"+WebPoem.title+"/index.htm")
    assert search("Me encontre")