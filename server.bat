@ECHO OFF

pushd test
python -m http.server 3000 --bind 127.0.0.1
popd