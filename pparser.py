'''
parser.py

Analizador Sintáctico para el lenguaje PL0
'''
import sly
from plex import Lexer

class Parser(sly.Parser):
    debugfile = 'pl0.txt'

    tokens = Lexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', ET, DF),
        ('left', LT, GT, LE, GE),
        ('right', NOT),
        )
    
    
    # definición de reglas
    @_('funclist')
    def program(self, p):
        pass
    @_('[ funclist ] func')
    def funclist(self, p):
        pass
    @_('FUN ID "(" [ parmlist ] ")" [ locallist ] BEGIN stmtlist END')
    def func(self, p):
        pass
    @_('[ parmlist "," ] parm')
    def parmlist(self, p):
        pass
    @_('ID ":" datatype')
    def parm(self, p):
        pass
    @_('INT [ "[" expr "]" ]',
       'FLOAT [ "[" expr "]" ]')
    def datatype(self, p):
        pass
    @_('locallist ";" { local ";" }','local')
    def locallist(self, p):
        pass
    @_('parm', 'func')
    def local(self, p):
        pass
    @_('stmt { ";" stmt }')
    def stmtlist(self, p):
        pass
    @_('STRING','ICONST', 'FCONST')
    def literal(self, p):
        pass
    @_('PRINT "(" literal ")"',
       'WRITE "(" expr ")"',
       'READ "(" location ")"',
       'WHILE relation DO stmt',
       'BREAK',
       'IF relation THEN stmt',
       'BEGIN stmtlist END',
       'location ASSIGNOP expr',
       'RETURN expr',
       'SKIP',
       'ID "(" exprlist ")"')
    def stmt(self, p):
        pass
    @_('ID [ "[" expr "]" ]')
    def location(self, p):
        pass
    @_('expr { "," expr }')
    def exprlist(self, p):
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
    @_('ID "(" exprlist ")"',
       'ID "[" exprlist "]"',
       'ID',
       'ICONST',
       'FCONST',
       '"(" relation ")"',
       'INT "(" expr ")"',
       'FLOAT "(" expr ")"',
       '"-" term',
       '"+" term',
       '"(" expr ")"')
    def term(self, p):
        pass
    @_('expr LT expr',
       'expr LE expr',
       'expr GT expr',
       'expr GE expr',
       'expr ET expr',
       'expr DF expr',
       'relation AND relation',
       'relation OR relation',
       'NOT relation')
    def relation(self, p):
        pass
    
    
def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test2/' + argv[1]).read()
    parser = Parser()
    parser.parse(lex.tokenize(txt))

if __name__ == '__main__':
    from sys import argv
    main(argv)