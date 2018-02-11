#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import

from WebPoem import *
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('output', nargs='?')
    args = parser.parse_args()
    if args.output:
        # apenas compilo
        WebPoemCompiler(args.file, args.output)
    else:
        # apenas executo
        WebPoemExec(args.file)