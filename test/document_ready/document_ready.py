#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "document_ready"
    driver = GoogleChrome()
    goTo("http://localhost:3000/document_ready/index.htm")
    assert search("Me encontre")