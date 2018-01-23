import unittest
from WebPoem import *
from WebPoem.WebPoemCompiler import *
import imp


def setUp():
    print('setup')


def testSomething():
    assert 'oi' == 'oi'


def deleteSomethingDB():
    pass


testcase = unittest.FunctionTestCase(
    testSomething,
    setUp=setUp,
    tearDown=deleteSomethingDB,
    description='oi'
)



import glob
from pathlib import Path

folders = Path('test').glob('*')

print('Testes do compilador:\n')


# defina essa variável para True
# para redefinir todas os arquivos
# correct.py
redifine = True

for folder in folders:
    def testFunction():
        name = str(folder.relative_to('test'))
        src     = folder / (name+'.txt')
        dest    = folder / (name+'.py')
        correct = folder / 'correct.py'
        index   = folder / 'index.htm'

        if not src.exists():
            return

        print(src)
        WebPoemCompiler(str(src), str(dest))

        if redifine or not correct.exists():
            import shutil
            shutil.copy(str(dest), str(correct))
        
        else:
            # verifica se os arquivos são iguais
            with open(str(correct), 'r', encoding='utf-8') as fileCorrect:
                with open(str(dest), 'r', encoding='utf-8') as fileDest:
                    assert fileCorrect.read() == fileDest.read()

        if index.exists():
            # solução de:
            # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
            infile = str(dest.absolute())
            basename = os.path.basename(infile)
            basename_without_extension = basename[:-3]
            imp.load_source(basename_without_extension, infile)
        

    testcase = unittest.FunctionTestCase(
        testFunction,
        description=str(folder)
    )

    testcase.runTest()
