#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "window_load"
    driver = GoogleChrome()
    goTo("http://localhost:3000/window_load/index.htm")
    assert search("Me encontre")