import unittest
from WebPoem import *
from WebPoem.WebPoemCompiler import *
import imp
import os
import shutil
import glob
from pathlib import Path
import sys
import argparse

try:
    parser = argparse.ArgumentParser()
    parser.add_argument('test_case', nargs='?', default='*')
    parser.add_argument('--no-compile', '-nc', action='store_true')
    parser.add_argument('--no-exec', '-ne', action='store_true')
    parser.add_argument('--compile-only', '-c', '-co', action='store_true')
    parser.add_argument('--exec-only', '-e', '-eo', action='store_true')
    parser.add_argument('--redifine', '-r', action='store_true',
        help='redefine todos os arquivos correct.py que servem para comparar o resultado gerado pelo compilador'
    )
    parser.add_argument('--all', '-a', action='store_true',
        help='executa todos os tipos de testes, inclui os testes não-locais'
    )

    argv = os.environ['WEBPOEM'] if 'WEBPOEM' in os.environ else ''
    args = parser.parse_args(argv.split())
    folders = Path('test').glob(args.test_case)

    cwd = os.getcwd()
    for folder in folders:
        def testFunction():
            name = str(folder.relative_to('test'))
            src     = folder / (name+'.txt')
            dest    = folder / (name+'.py')
            correct = folder / 'correct.py'
            index   = folder / 'index.htm'
            # copia o arquivo para a raiz
            if not src.exists():
                return
            print('Testing:', src)
            # quero saber
            # se esse teste
            # é local ou não
            isLocalTest = index.exists()

            # para saber se vai compilar, segue a tabela
            # exec_only    no_compile       vai_compilar
            #     0             0       ==        1
            #     0             1       ==        0
            #     1             0       ==        0
            #     1             1       ==        0
            if not args.exec_only and not args.no_compile:
                title = WebPoemCompiler(str(src), str(dest))
            else:
                title = name

            if args.redifine:
                # quando estou redefinindo
                # apenas o arquivo gerado pelo compilador
                shutil.copy(str(dest), str(correct))
            elif not correct.exists():
                print('O arquivo correct.py não existe para o caso de teste "'+name+'"')
                print('Execute o caso de teste com a opção --redifine')
            else:
                # não estou redifinindo
                # verifica se os arquivos são iguais
                with open(str(correct), 'r', encoding='utf-8') as fileCorrect:
                    with open(str(dest), 'r', encoding='utf-8') as fileDest:
                        assert fileCorrect.read() == fileDest.read()

            # agora eu verifico se eu quero executar
            # seguindo a msma lógica do "se quero compilar"
            if not args.compile_only and not args.no_exec:
                if isLocalTest or args.all:
                    WebPoemExec(str(dest))

            if os.path.exists(title):
                shutil.rmtree(title)

        # chamo essa função que acabei de criar
        testcase = unittest.FunctionTestCase(
            testFunction,
            description=str(folder)
        )
        testcase.runTest()

except SystemExit as e:
    pass
