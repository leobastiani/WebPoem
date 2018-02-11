#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "sleep"
    driver = GoogleChrome()
    goTo("http://localhost:3000/sleep/index.htm")
    assert search("Me encontre")