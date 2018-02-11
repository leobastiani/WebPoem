#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import

from .WebPoemCompiler import WebPoemCompiler
import os
import imp
import tempfile

def WebPoemExec(filePath):
        filePath = filePath
        # exemplo: ('sucupira1', '.py')
        basename_ext = os.path.splitext(filePath)
        # exemplo: 'sucupira1'
        basename_without_extension = basename_ext[0]
        # ext pode ser 'py' ou outro arquivo como 'txt'
        ext = basename_ext[1][1:]
        # é um arquivo compilado se
        # sua extensão for py
        compiled = ext == 'py'

        if compiled:
            # solução de:
            # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
            imp.load_source(basename_without_extension, filePath)
        else:
            # preciso compilar
            outputPath = tempfile.mktemp(suffix='.py', dir='.')
            WebPoemCompiler(filePath, outputPath)
            WebPoemExec(outputPath)
            os.remove(outputPath)