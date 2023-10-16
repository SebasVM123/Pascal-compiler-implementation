'''
parser.py

Analizador Sintáctico para el lenguaje PL0
'''
import sly
from plex import Lexer

class Parser(sly.Parser):
    debugfile = 'pl0.txt'

    tokens = Lexer.tokens

    # definición de reglas
    @_('funclist')
    def program(self, p):
        pass

    @_('funclist func', 'func')
    def funclist(self, p):
        pass

    @_('FUN ID "(" { args } ")" ')
    def func(self, p):
        pass

    @_('args "," arg', 'arg', '')
    def args(self, p):
        pass

    @_('ID ":" datatype')
    def arg(self, p):
        pass

    @_('integer', 'float')
    def datatype(self, p):
        pass

    @_('INT [ "[" ICONST "]" ]')
    def integer(self, p):
        pass

    @_('FLOAT [ "[" ICONST "]" ]')
    def float(self, p):
        pass


txt = 'fun hola(a:int, b:float)'

lex = Lexer()
parser = Parser()
parser.parse(lex.tokenize(txt))

