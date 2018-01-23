#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    driver = GoogleChrome()
    import os
    goTo("file:///"+os.getcwd()+"/test/sleep/index.htm")
    sleep(ms(100))
    assert search("Me encontre") == True
    