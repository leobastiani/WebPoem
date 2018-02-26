# WebPoem
Se declare para seu navegador.

## Linux:
### Como instalar:
<!-- https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5 -->
```sh
# instalar o chromedriver
CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`
wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
rm ~/chromedriver_linux64.zip
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver
# instalar o selenium
sudo apt-get -y install python-pip
pip install selenium
# instalar as dependências do projeto
pip install -r requirements.txt
```

### Exemplo de uso:
```sh
# executando o caso de teste da plataforma sucupira
python WebPoem.py test/sucupira1/sucupira1.txt -o sucupira1.py
python sucupira1.py
```
