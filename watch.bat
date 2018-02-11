@ECHO OFF
call env\python3\Scripts\activate
echo O Watch ira compilar o arquivo test.txt para compiled.py
pause
nodemon -e py,txt -i test.py --exec "cls && WebPoem test.txt compiled.py"