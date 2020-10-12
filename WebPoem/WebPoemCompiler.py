#!python3
#encoding=utf-8
from __future__ import print_function, division, absolute_import

import chardet
import re
import sys


DEBUG = sys.flags.debug or False
def debug(*args):
    '''funciona como print, mas só é executada se sys.flags.debug == 1'''
    if not DEBUG:
        return ;
    print(*args)


def WebPoemCompiler(filePath, outputPath):
    debug('WebPoemCompiler')
    debug("filePath:", filePath)
    debug("outputPath:", outputPath)

    #####################
    # variáveis globais #
    #####################
    # conteúdo do arquivo que vamos tratar
    global content
    # título do arquivo
    global title
    # identação sempre começa em 0
    global identacaoAtual
    identacaoAtual = 0

    # vamos filtrar as linhas importantes
    with open(filePath, 'rb') as file:
        fileContentBinary = file.read()
    debug("fileContentBinary:", fileContentBinary)
    encoding = chardet.detect(fileContentBinary)['encoding']
    debug("encoding:", encoding)
    content = fileContentBinary.decode(encoding)
    debug("content:", content)
    debug('########################')
    debug('# Início da compilação #')
    debug('########################')
    # padroniza as quebras de linhas com \n apenas
    content = content.replace('\r', '')

    # a primeira linha é o título
    sec = re.match(r'([^\n]+)\n', content, re.S + re.M)
    title = sec.group(1)
    content = content[len(sec.group(0)):]
    debug("title:", title)
    output = 'WebPoem.title = '+tokenize(title)+'\n'

    # vê a quantidade de espaços ou tabs no início da
    # linha
    output = ident(output+consume())
    debug("output:", output)
    output = readFile('py/header.py') + output
    with open(outputPath, 'w', encoding='utf-8') as file:
        file.write(output)
    return title


def readFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        return file.read()

# para depurar o conteudo do arquivo
# jogo ele numa linha só
def onLine(content):
    return content.replace('\n', '')

# esta função
# faz um regex em content
# e consume
def _matchContent(regex, content):
    ret = re.match(regex, content)
    content = content[len(ret.group()):]
    return ret, content
def matchContent(regex):
    global content
    ret, content = _matchContent(regex, content)
    return ret

# consome o conteúdo do arquivo
def consume():
    global content
    global StatementAtual
    global identacaoAtual
    debug('content:', onLine(content))

    if content == '':
        return ''

    ident = len(matchContent(r'^\n*( *)').group(1)) // 4

    if ident < identacaoAtual:
        return ''

    for fnAndStt in Statements:
        fn = fnAndStt[0]
        objs = fnAndStt[1:]
        debug("fn.__name__:", fn.__name__)
        for s in objs:
            debug("s:", s)

            # para cada nova tentativa de statement
            # eu reseto o statement atual
            StatementAtual = {}

            newContent = s.match(content)
            debug("newContent:", newContent)
            if isinstance(newContent, str):
                content = newContent
                ret = fn()
                return ret.rstrip()
        debug('')

def consumeByIdent():
    global content
    global identacaoAtual
    ret = ''
    while True:
        match = re.match(r'^\n*( *)([^\n]+)\n', content)
        ident = len(match.group(1)) // 4
        if ident < identacaoAtual:
            return ret
        # devo consumir
        line = match.group()
        ret += line
        content = content[len(line):]

# transforma isso:
# asd
# asd
# nisso:
#   asd
#   asd
def ident(string):
    lines = string.split('\n')
    return '\n'.join(['    '+x for x in lines])

# incrementa a identação atual
# e consome o arquivo
def incrIdent():
    global identacaoAtual
    identacaoAtual += 1
    return ident(consume())
# igual a de cima
# mas decrementa
def decrIdent():
    global identacaoAtual
    identacaoAtual -= 1
    return consume()


def tokenize(val):
    if val[0] == '{':
        # é um python code
        _, _, ret = parenteses(val)
        return ret
    if val[0] in '"\'':
        return val
    else:
        return '"'+val+'"'

##################################################
# Funções para serem executadas pelos statements #
##################################################
def navegue():
    # Navegue com o Google Chrome
    debug("StatementAtual:", StatementAtual)
    if StatementAtual['NAVEGADOR'] == 'Chrome':
        GoogleChrome = 'GoogleChrome'
    else:
        raise 'Outros navegadores não foram implementados ainda.'
    return 'driver = '+GoogleChrome+'()\n'+consume()

def goTo():
    link = matchContent(r'\n*\s*([^\n]+)').group(1)
    return 'goTo("'+link+'")\n'+consume()

def preencha():
    ret = []
    # agora vem os campos
    # mudo a identação atual
    # para pegar os campos
    global identacaoAtual

    # as funções que estarão
    # no arquivo compilado
    if 'PREENCHA' in StatementAtual:
        func = 'findInput'
        fill = 'fill'
    elif 'SELECIONE' in StatementAtual:
        func = 'findInput'
        fill = 'select'

    identacaoAtual += 1
    campoAndValue = consumeByIdent()
    identacaoAtual -= 1

    campoAndValue = campoAndValue.split('\n')
    campoAndValue = [x for x in campoAndValue if x != '']

    def getIdent(line):
        return len(re.match(r'^\n*( *)', line).group(1)) // 4

    idents = [getIdent(x) for x in campoAndValue]

    def getCampoValues():
        i = 0
        limit = len(idents)
        while i < limit:
            j = i+1
            values = []
            while j < limit and idents[j] > idents[i]:
                values.append(campoAndValue[j].strip())
                j+=1
            yield [campoAndValue[i].strip(), values]
            i = j+1

    # transforma [x1, x2, ...]
    # em [(x1, x2), ...]
    for campo, valores in getCampoValues():
        debug("campo:", campo)
        debug("valores:", valores)

        for i, valor in enumerate(valores):
            valores[i] = tokenize(valor)

        ret.append(func+'("'+campo+'").'+fill+'('+', '.join(valores)+')')
    # filtra os valores que não possuem nada
    return '\n'.join(ret) + '\n' + consume()

def acaoToWebPoem(acao):
    if acao == 'CLIQUE':
        acao = '.click()'
    else:
        acao = ''

    return acao

def callFunction():
    global StatementAtual

    if 'input' in StatementAtual:
        inp = tokenize(StatementAtual['input'])
    else:
        inp = ''

    if 'PAUSE' in StatementAtual:
        func = 'pause'
    elif 'DIGITE' in StatementAtual:
        func = 'send_keys'

    return func+'('+inp+')\n'+consume()


def acao():
    debug("StatementAtual:", StatementAtual)

    if StatementAtual['input'] == 'mim':
        return 'element.click()\n'+consume()

    return 'findElement("'+StatementAtual['input']+'")'+acaoToWebPoem(StatementAtual['ACAO'])+'\n'+consume()

def definicao():
    debug("StatementAtual:", StatementAtual)
    input_nome  = StatementAtual['input_nome']
    input_valor = StatementAtual['input_valor']
    return input_nome+' = findElement('+tokenize(input_valor)+')\n'+consume()

def comentario():
    debug("StatementAtual:", StatementAtual)
    return '#'+StatementAtual['line']+'\n'+consume()

def pythonCode():
    debug("StatementAtual:", StatementAtual)
    return StatementAtual['input']+'\n'+consume()

def doWhile():
    input_nome = StatementAtual['input']
    acao = acaoToWebPoem(StatementAtual['ACAO'])

    return '''while True:
    Clickable = findElement("'''+input_nome+'''")
'''+incrIdent()+'''
    if not Clickable.isClickable():
        break
    Clickable'''+acao+'\n'+decrIdent()

def While():
    debug("StatementAtual:", StatementAtual)

    inp = StatementAtual['input']
    if StatementAtual.get('ENQUANTO') == 'ENQUANTO':
        return 'while '+inp+':\n'+incrIdent()+'\n'+decrIdent()

    return 'for element in '+inp+':\n'+incrIdent()+'\n'+decrIdent()

def encontre():
    debug("StatementAtual:", StatementAtual)
    if 'NÃO' in StatementAtual:
        nao = 'not '
    else:
        nao = ''
    return 'assert '+nao+'search("'+StatementAtual['input']+'")\n'+consume()

def newWindow():
    return 'with NewWindow():\n'+incrIdent()+'\n'+decrIdent()

def keepData():
    return 'WebPoem.keepData()\n'+consume()

def openInNewWindow():
    return 'with OpenInNewWindow(findElement("'+StatementAtual['input']+'")):\n'+incrIdent()+'\n'+decrIdent()

def salve():
    return 'save()\n'+consume()

def enviar():
    return 'send()\n'+consume()

def espere():
    inputTime = StatementAtual['input']
    debug("inputTime:", inputTime)

    # removo os espaços
    inputTime = re.sub(r'\s+', '', inputTime)
    inputTime = inputTime.lower()

    # pega os tempos
    inputTime = re.findall(r'(\d+)([a-z]+)?', inputTime)
    # exemplo de inputTime
    # [('10', 'm'), ('5', 's'), ('100', 'ms')]
    # ou
    # [(5, '')]
    inputTime = [unidade+'('+time+')' for time, unidade in inputTime]
    inputTime  = '+'.join(inputTime)

    return 'sleep('+inputTime+')\n'+consume()

###################
# Fim das funções #
###################

class Statement:
    termos = {
        # todos são expressões regulares
        # faltam um \b no final
        'NAVEGUE': ['navegue', 'navegação'],
        'ACESSE': ['acesse'],
        'NÃO': ['NÃO', 'NAO'],
        'PREENCHA': ['preencha', 'preencher'],
        'SELECIONE': ['selecione', 'selecionar'],
        'PREP': ['com', 'de'],
        'ARTIGO': ['o', 'a', 'uma', 'um'],
        'ACAO': {
            'CLIQUE': ['clique', 'clicar'],
        },
        'NO': ['em', 'na', 'no'],
        'É': ['é'],
        'ENQUANTO': ['enquanto'],
        'PARA CADA': ['para cada'],
        'MODO': ['modo'],
        'CONTINUA': ['contínua'],
        'NOVA': ['nova'],
        'ABRA': ['abra'],
        'JANELA': ['janela', 'aba'],
        'ESPERE': ['espere'],
        'PAUSE': ['pause'],
        'ENVIAR': ['enviar'],
        'ENCONTRE': ['encontre', 'encontrar'],
        'SALVE': ['salve'],
        'CONSEGUIR': ['puder'],
        'DIGITE': ['digite'],
        'NAVEGADOR': {
            'Chrome': ['Google Chrome', 'Chrome'],
            'IE': ['Internet Explorer'],
        },
        '.': [r'\.'],
        ':': [':'],
        '#': ['#'],
        '{': [r'\{'],
        '\n': [r'\n'],
    }

    def __init__(self, *statements):
        self.statements = statements

    def match(self, content):
        debug("content:", onLine(content))
        debug("self.statements:", self.statements)

        for s in self.statements:
            content = Statement.matchRegex(s, content)
            if content is False:
                return None
            # remove os espaços do início da string
            # isso não prejudica a identação
            # pq antes da identação tem um \n
            content = re.sub(r'^ +', '', content)
        return content

    def __str__(self):
        return str(self.statements)

    @staticmethod
    def matchRegex(statement, content):
        if content == '':
            return False

        termos = Statement.termos.get(statement)
        debug('')
        debug("statement:", repr(statement))
        debug("termos:", repr(termos))
        debug("content:", repr(onLine(content)))

        if termos is None:
            # retorna a própria linha
            if statement.startswith('input'):
                if content[0] in '${[("\'':
                    # é uma entrada igual o seletor
                    # do jQuery
                    if content[0] == '$':
                        # começa com $
                        content = content[1:]
                    # obtém o termo entre parênteses
                    startParenteses, endParenteses, _ = parenteses(content)

                    if startParenteses != 0:
                        raise 'Erro na seleção de $'

                    ret = content[startParenteses+1:endParenteses]
                    content = content[endParenteses+1:]
                    debug("ret:", ret)
                    debug("content:", onLine(content))
                else:
                    # caso genérico
                    ret, content = _matchContent(r'\n*([^\n]+)', content)
                    ret = ret.group(1)

            StatementAtual[statement] = ret
            return content

        # padroniza tudo
        if not isinstance(termos, dict):
            # de list
            # para dict
            aux = {}
            aux[statement] = termos
            termos = aux

        for t in termos:
            debug("t:", t)
            matches = termos[t]
            debug("matches:", matches)
            for m in matches:
                match = re.match(r'^'+m, content, flags=re.IGNORECASE)
                debug("match:", match)
                if match is None:
                    continue
                match = match.group()
                StatementAtual[statement] = t
                debug("match:", match)
                content = content[len(match):]
                return content

        return False


def parenteses(line):
    chars = [
        ('(', ')'),
        ('[', ']'),
        ('{', '}'),
        ('"', '"'),
        ("'", "'"),
    ]

    for abre, fecha in chars:
        if line[0] == abre:
            i = 0
            abertos = 1
            while True:
                i+=1
                if line[i] == '\\':
                    i+=1
                # o fecha tem que vir antes
                # pq no caso
                # das aspas
                # eu eu tenho que tratar
                # que estou fechando
                elif line[i] == fecha:
                    abertos -= 1
                    if abertos == 0:
                        break
                elif line[i] == abre:
                    abertos += 1
            return 0, i, line[1:i]

Statements = [
    # Statements não é um dict
    # porque eu preciso seguir essa ordem
    # na hora de testar os statements
    # por isso ele é uma lista
    # e segue esse padrão
    # [ FuncaoReferenteParaTratar, ...listaDeStatements]

    # Navegue com o Google Chrome
    [ navegue,
        Statement('NAVEGUE', 'PREP', 'ARTIGO', 'NAVEGADOR'),
    ],
    [ goTo,
        Statement('ACESSE'),
    ],
    [ openInNewWindow,
        Statement('ABRA', 'NO', 'NOVA', 'JANELA', 'input'),
    ],
    [ newWindow,
        Statement('NO', 'NOVA', 'JANELA'),
    ],
    [ keepData,
        Statement('MODO', 'PREP', 'NAVEGUE', 'CONTINUA'),
    ],
    [ salve,
        Statement('SALVE'),
    ],
    [ callFunction,
        Statement('DIGITE', 'input'),
        Statement('PAUSE'),
    ],
    [ encontre,
        Statement('NÃO', 'ENCONTRE', 'input'),
        Statement('ENCONTRE', 'input'),
    ],
    [ doWhile,
        Statement('ENQUANTO', 'CONSEGUIR', 'ACAO', 'NO', 'input'),
    ],
    [ While,
        Statement('ENQUANTO', 'input'),
        Statement('PARA CADA', 'input'),
    ],
    [ preencha,
        Statement('PREENCHA'),
        Statement('SELECIONE'),
    ],
    [ espere,
        Statement('ESPERE', 'input'),
    ],
    [ enviar,
        Statement('ENVIAR'),
    ],
    [ acao,
        Statement('ACAO', 'NO', 'input'),
    ],
    [ definicao,
        Statement('input_valor', 'É', 'ARTIGO', 'input_nome'),
    ],
    [ pythonCode,
        Statement('input'),
    ],

]


# adiciona um \b em todos
# os Statement.termos

def addBarraB(termos):
    for termo in termos:
        if re.match(r'\w+', termo):
            l = termos[termo]

            # não é uma lista
            if isinstance(l, dict):
                addBarraB(l)
            else:
                # é uma lista
                newList = []
                for word in l:
                    # bypass do acento
                    # solução
                    # trasforma
                    # exêmplo em ex[eê]mplo
                    for semAcento in acentos:
                        chsAcentos = acentos[semAcento]
                        for ch in chsAcentos:
                            word = word.replace(ch, '['+semAcento+ch+']')
                    # fim dele
                    newList.append(word + r'\b')

                termos[termo] = newList

acentos = {
    'a': 'áàâã',
    'e': 'éê',
    'i': 'íî',
    'o': 'õôõ',
    'u': 'úü',
    'c': 'ç',
}

addBarraB(Statement.termos)
