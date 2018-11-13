#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import
from WebPoem import *

@WebPoemMain
def main():
    WebPoem.title = "open_new_window"
    driver = GoogleChrome()
    goTo("http://localhost:3000/"+WebPoem.title+"/index.htm")
    with OpenInNewWindow(findElement("link1")):
        assert search("Me Encontre")
    with OpenInNewWindow(findElement("link2")):
        assert search("Me Encontre")