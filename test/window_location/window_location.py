#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "window_location"
    driver = GoogleChrome()
    import os
    goTo("http://localhost:3000/"+WebPoem.title+"/index.htm")
    assert search("Me encontre")
