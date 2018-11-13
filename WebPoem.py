#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import

from WebPoem import *
import sys
import argparse
from pathlib import Path
import glob
import os

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

    if len(files) == 1:
        # testa para saber se é uma navegação contínua
        file = files[0]
        if not Path(file).exists():
            os.makedirs(file)
        if Path(file).is_dir():
            @WebPoemMain
            def main():
                WebPoem.title = file
                WebPoem.keepData(file)
                driver = GoogleChrome()
                import code
                code.interact(local=dict(globals(), **locals()))

    files = sum([toFile(f) for f in args.files], [])
    if args.output:
        # apenas compilo
        WebPoemCompiler(files[0], args.output)
    else:
        # apenas executo
        for file in files:
            WebPoemExec(file)