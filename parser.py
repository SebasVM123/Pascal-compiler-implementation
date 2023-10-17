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
    
    @_('{ stmtlist } ";" stmt')
    def stmtlist(self, p):
        pass
    
    @_('WHILE relation DO stmt',
       'IF relation THEN stmt',
       'location ASSIGNOP expr',
       'PRINT "(" STRING ")"',
       'WRITE "(" expr ")"',
       'READ "(" location ")"',
       'RETURN expr',
       'ID "(" exprlist ")"',
       'SKIP',
       'BREAK',
       'BEGIN stmtlist END')
    def stmt(self, p):
        pass
    
    @_('ID','ID "[" expr "]"')
    def location(self, p):
        pass
    
    @_('logic_or')
    def relation(self, p):
        pass
    
    @_('logic_or OR { logic_and }')
    def logic_or(self, p):
        pass
    
    @_('logic_and AND { logic_not }')
    def logic_and(self, p):
        pass
    
    @_('NOT logic_not', 'equality')
    def logic_not(self, p):
        pass
    
    @_('equality DF comparison',
       'equality ET comparison',
       'comparison')
    def equality(self, p):
        pass
    
    @_('comparison GT expr',
       'comparison GE expr',
       'comparison LT expr',
       'comparison LE expr',
       'expr')
    def comparison(self, p):
        pass
    
    @_('factor "+" expr',
       'factor "-" expr',
       'factor')
    def expr(self, p):
        pass
    
    @_('term "*" factor',
       'term "/" factor',
       'term')
    def factor(self, p):
        pass
    
    @_('{ exprlist } "," expr')
    def exprlist(self, p):
        pass
    
    @_('ID  "(" exprlist ")"',
       'ID  "[" exprlist "]"',
       'ID',
       'INT',
       'FLOAT',
       '"(" relation ")"',
       'INT "(" expr ")"',
       'FLOAT "(" expr ")"',
       '"-" term',
       '"+" term')
    def term(self, p):
        pass
    

txt = 'fun hola(a:int, b:float)'

lex = Lexer()
parser = Parser()
parser.parse(lex.tokenize(txt))