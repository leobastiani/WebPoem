#!python3
#encoding=utf-8
from __future__ import print_function, division

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
    global lines
    global identacaoAtual
    identacaoAtual = 0

    # vamos filtrar as linhas importantes
    with open(filePath, 'rb') as file:
        fileContentBinary = file.read()
    debug("fileContentBinary:", fileContentBinary)
    encoding = chardet.detect(fileContentBinary)['encoding']
    debug("encoding:", encoding)
    fileContent = fileContentBinary.decode(encoding)
    debug("fileContent:", fileContent)
    debug('########################')
    debug('# Início da compilação #')
    debug('########################')
    # padroniza as quebras de linhas com \n apenas
    fileContent = fileContent.replace('\r', '')
    # linhas juntas, sem quebras excessivas
    fileContent = re.sub('\n+', '\n', fileContent)
    lines = fileContent.split('\n')

    # a primeira linha é o título
    titulo = lines.pop(0)
    debug("titulo:", titulo)
    debug("lines:", lines)

    # vê a quantidade de espaços ou tabs no início da
    # linha
    output = ident(Lines())
    debug("output:", output)
    output = readFile('py/header.py') + output
    with open(outputPath, 'w', encoding='utf-8') as file:
        file.write(output)


def readFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        return file.read()


def Lines():
    line, identacao = getNewLine()
    if line is None:
        return ''

    global StatementAtual
    StatementAtual = {}

    global identacaoAtual
    if identacao != identacaoAtual:
        identacaoAtual -= 1
        return ''

    return Line(line, identacao)


def getNewLine():
    global lines

    if len(lines) == 0:
        return None, None

    line = lines.pop(0)
    identacaoChars = re.match(r'^(\s+)', line)
    if identacaoChars is None:
        # quantidade de identacao feita até o momento
        identacao = 0
    else:
        identacaoChars = identacaoChars.group()
        if identacaoChars[0] == ' ':
            # é com espaços
            identacao = int(len(identacaoChars) / 4)
        else:
            # é com tabs
            identacao = len(identacaoChars)
    # nesse ponto, a identacao deve ser a quantidade de identacao
    # dada na linha
    # atualizo a linha
    line = line.strip()
    return line, identacao


def goBackLine(line, identacao):
    global lines
    lines.insert(0, '\t'*identacao + line)


def ident(string):
    lines = string.split('\n')
    return '\n'.join(['    '+x for x in lines])

def incrIdent():
    global identacaoAtual
    identacaoAtual += 1
    return identacaoAtual

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
    return 'driver = '+GoogleChrome+'()\n'+Lines()

def goTo():
    line, _ = getNewLine()
    return 'goTo("'+line+'")\n'+Lines()

def preencha():
    # agora vem o campo
    lineCampo, identacao = getNewLine()
    
    if identacao == identacaoAtual + 1:
        # nome do campo DOIS_PONTO
        campo = re.match(r'^(.+):$', lineCampo)

        if campo is None:
            raise 'Tratar o caso em que não tem : no fim da linha'

        campo = campo.group(1)

        # agora obtenho os valores
        valores = []
        # a primeira linha tem que ter
        lineValor, identacao = getNewLine()

        valores.append(lineValor)
        debug("valores:", valores)

        while True:
            # com a mesma identação
            lineValor, identacao = getNewLine()
            debug("identacaoAtual:", identacaoAtual)
            debug("identacao:", identacao)
            if identacao < identacaoAtual + 2:
                goBackLine(lineValor, identacao)
                break
            valores.append(lineValor)

        def quotes(v):
            if v[0] == '{':
                _, _, v = parenteses(v, '{')
                return v
            return '"'+v+'"'

        valoresStr = ', '.join([quotes(v) for v in valores])

        return 'findInput("'+campo+'").fill('+valoresStr+')\n'+Lines()

    # nesse caso, volto a tratar as linhas
    goBackLine(lineCampo, identacao)
    return Lines()

def acaoToWebPoem(acao):
    if acao == 'CLIQUE':
        acao = '.click()'
    else:
        acao = ''

    return acao

def acao():
    debug("StatementAtual:", StatementAtual)

    if StatementAtual['input'] == 'mim':
        return 'element.click()\n'+Lines()

    return 'findElement("'+StatementAtual['input']+'")'+acaoToWebPoem(StatementAtual['ACAO'])+'\n'+Lines()

def definicao():
    debug("StatementAtual:", StatementAtual)
    input_nome  = StatementAtual['input_nome']
    input_valor = StatementAtual['input_valor']
    return input_nome+' = findElement("'+input_valor+'")\n'+Lines()

def comentario():
    debug("StatementAtual:", StatementAtual)
    return '#'+StatementAtual['line']+'\n'+Lines()

def copyline():
    debug("StatementAtual:", StatementAtual)
    line = StatementAtual['line']
    fecha = line[len(line)-1]
    if fecha != '}':
        raise 'Não fechei o parênteses'
    line = line[:len(line)-1]
    return line+'\n'+Lines()

def doWhile():
    input_nome = StatementAtual['input']
    acao = acaoToWebPoem(StatementAtual['ACAO'])

    incrIdent()
    middle = ident(Lines())

    ret = '''while True:
    Clickable = findElement("'''+input_nome+'''")
'''+middle+'''
    if not Clickable.isClickable():
        break
    Clickable'''+acao+'\n'
    return ret

def While():
    debug("StatementAtual:", StatementAtual)

    incrIdent()

    inp = StatementAtual['input']
    if StatementAtual.get('ENQUANTO') == 'ENQUANTO':
        return 'while '+inp+':\n'+ident(Lines())

    return 'for element in '+inp+':\n'+ident(Lines())

def encontre():
    debug("StatementAtual:", StatementAtual)
    return 'assert search("'+StatementAtual['input']+'") == True\n'+Lines()

def newWindow():
    incrIdent()
    return 'with NewWindow():\n'+ident(Lines())

def salve():
    return 'save()\n'+Lines()

def enviar():
    return 'send()\n'+Lines()

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

    return 'sleep('+inputTime+')\n'+Lines()

###################
# Fim das funções #
###################

# trata uma linha
def Line(line, identacao):
    for fnAndStt in Statements:
        fn = fnAndStt[0]
        objs = fnAndStt[1:]

        for s in objs:
            matched = s.match(line)
            debug("matched:", matched)
            if matched:
                ret = fn()
                return ret

identacaoAtual = 0
StatementAtual = {}

class Statement:
    termos = {
        # todos são expressões regulares
        # faltam um \b no final
        'NAVEGUE': ['navegue'],
        'ACESSE': ['acesse'],
        'PREENCHA': ['preencha'],
        'PREP': ['com'],
        'ARTIGO': ['o', 'a', 'uma', 'um'],
        'ACAO': {
            'CLIQUE': ['clique', 'clicar'],
        },
        'NO': ['em', 'na', 'no'],
        'É': ['é'],
        'ENQUANTO': ['enquanto'],
        'PARA CADA': ['para cada'],
        'NOVA': ['nova'],
        'JANELA': ['janela'],
        'ESPERE': ['espere'],
        'ENVIAR': ['enviar'],
        'ENCONTRE': ['encontre', 'encontrar'],
        'SALVE': ['salve'],
        'CONSEGUIR': ['puder'],
        'NAVEGADOR': {
            'Chrome': ['Google Chrome', 'Chrome'],
            'IE': ['Internet Explorer'],
        },
        '.': [r'\.'],
        ':': [':'],
        '#': ['#'],
        '{': [r'\{'],
    }

    def __init__(self, *statements):
        self.statements = statements

    def match(self, line):

        debug("line:", line)
        debug("self.statements:", self.statements)

        for s in self.statements:
            line = StatementMatch(s, line)
            if line is False:
                return False
            line = line.strip()
        return True
    

def parenteses(line, abre='('):
    if   abre == '(': fecha = ')'
    elif abre == '{': fecha = '}'

    i = 0
    while line[i] != abre:
        i += 1
    start = i
    abertos = 1
    while True:
        i+=1
        if line[i] == abre:
            abertos += 1
        elif line[i] == fecha:
            abertos -= 1
            if abertos == 0:
                break
    return start, i, line[start+1:i]

def StatementMatch(statement, line):
    if line == '':
        return line

    termos = Statement.termos.get(statement)
    debug('')
    debug("statement:", '"'+str(statement)+'"')
    debug("termos:", '"'+str(termos)+'"')
    debug("line:", '"'+str(line)+'"')

    if termos is None:
        # retorna a própria linha
        if statement.startswith('input'):
            if line[0] == '$' or line[0] == '(':
                # é uma entrada igual o seletor
                # do jQuery
                if line[0] == '$':
                    # começa com $
                    line = line[1:]
                # obtém o termo entre parênteses
                startParenteses, endParenteses, _ = parenteses(line)

                if startParenteses != 0:
                    raise 'Erro na seleção de $'

                ret = line[startParenteses+2:endParenteses-1]
                line = line[endParenteses+1:]
                debug("ret:", ret)
                debug("line:", line)

            elif line[0] == '"' or line[0] == '\'':
                # a linha começa com aspas
                startChar = line[0]
                start = 1
                end = start + 1
                ret = None
                # percorre por end
                while end < len(line):
                    if line[end] == startChar:
                        # encontrei
                        ret = line[start:end]
                        line = line[end+1:]
                        break
                    elif line[end] == '\\':
                        end += 1
                    end += 1

                if ret is None:
                    raise 'O par das aspas não foi encontrado.'

            else:
                # caso genérico
                ret = line[:len(line)-1]
                line = line[len(line)-1:]

        elif statement.startswith('line'):
            ret = line

        StatementAtual[statement] = ret
        return line

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
            match = re.match(r'^'+m, line, flags=re.IGNORECASE)
            debug("match:", match)
            if match is None:
                continue
            match = match.group()
            StatementAtual[statement] = t
            debug("match:", match)
            line = line[len(match):]
            return line

    return False


Statements = [
    
    # Navegue com o Google Chrome
    [ navegue,
        Statement('NAVEGUE', 'PREP', 'ARTIGO', 'NAVEGADOR', '.'),
    ],
    [ goTo,
        Statement('ACESSE', ':'),
    ],
    [ newWindow,
        Statement('NO', 'NOVA', 'JANELA', ':'),
    ],
    [ salve,
        Statement('SALVE', '.'),
    ],
    [ encontre,
        Statement('ENCONTRE', 'input', '.'),
    ],
    [ doWhile,
        Statement('ENQUANTO', 'CONSEGUIR', 'ACAO', 'NO', 'input', ':'),
    ],
    [ While,
        Statement('ENQUANTO', 'input', ':'),
        Statement('PARA CADA', 'input', ':'),
    ],
    [ preencha,
        Statement('PREENCHA', ':'),
    ],
    [ espere,
        Statement('ESPERE', 'input', '.'),
    ],
    [ enviar,
        Statement('ENVIAR', '.'),
    ],
    [ acao,
        Statement('ACAO', 'NO', 'input'),
    ],
    [ comentario,
        Statement('#', 'line'),
    ],
    [ copyline,
        Statement('{', 'line'),
    ],
    [ definicao,
        Statement('input_valor', 'É', 'ARTIGO', 'input_nome'),
    ]
    
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
                    newList.append(word + r'\b')

                termos[termo] = newList


addBarraB(Statement.termos)

