@ECHO OFF

set watch=F
if ["%*"] == ["--watch"] set watch=T
if ["%*"] == ["-w"] set watch=T

if ["%watch%"] == ["T"] (
	call nodemon --ignore test --watch extension\src --exec "cls && extension"
	goto:eof
)

rem o compilador comeca a partir daqui

rem call browserify extension\src\WebPoem.js -o extension\unpacked\WebPoem.unwrapped.js -t [ babelify --presets [ es2015 ] ]
call browserify extension\src\WebPoem.js -o extension\unpacked\WebPoem.unwrapped.js
cat extension\wrapper\header.js > extension\unpacked\WebPoem.js
cat extension\unpacked\WebPoem.unwrapped.js >> extension\unpacked\WebPoem.js
cat extension\wrapper\bottom.js >> extension\unpacked\WebPoem.js

pushd extension\unpacked
7z a ..\dist\WebPoem.zip WebPoem.js manifest.json
popd

pushd bin
buildcrx_winnt_x86.exe ..\extension\dist\WebPoem.zip ..\extension\dist\WebPoem.pem
popd
