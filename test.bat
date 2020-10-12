@ECHO OFF

set WEBPOEM=%*
py -3 -m unittest discover -v
