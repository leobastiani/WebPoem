#!python3
#encoding=utf-8
from __future__ import print_function, division
from WebPoem.WebPoemCompiler import *

import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('usage: WebPoem entrada.txt saida.py')
        sys.exit(0)
    WebPoemCompiler(sys.argv[1], sys.argv[2])