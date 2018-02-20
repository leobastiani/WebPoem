#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import

from WebPoem import *
import sys
import argparse
from pathlib import Path
import glob

def isWildcard(file):
    return file.find('*') != -1 or file.find('?') != -1

def toFile(file):
    # retorna sempre uma lista de string
    if isWildcard(file):
        return glob.glob(file)
    path = Path(file)
    if not path.exists():
        return []
    if path.is_dir():
        return [str(x) for x in path.glob('*.txt')]
    return [file]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    parser.add_argument('--output', '-o', type=str, nargs='?')
    args = parser.parse_args()
    files = args.files
    files = sum([toFile(f) for f in args.files], [])
    if args.output:
        # apenas compilo
        WebPoemCompiler(files[0], args.output)
    else:
        # apenas executo
        for file in files:
            WebPoemExec(file)