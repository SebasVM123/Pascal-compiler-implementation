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
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', NOT, UNARY),
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

    @_('local ";"',
       'local ";" locallist')
    def locallist(self, p):
        pass

    @_('parm',
       'func')
    def local(self, p):
        pass

    @_('stmt',
       'stmt ";" stmtlist')
    def stmtlist(self, p):
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

    @_('STRING', 'ICONST', 'FCONST')
    def literal(self, p):
        pass

    @_('expr "+" expr',
        'expr "-" expr',
        'expr "*" expr',
        'expr "/" expr',
        '"-" expr %prec UNARY',
        '"+" expr %prec UNARY',
        '"(" expr ")"',
        'ICONST',
        'FCONST',
        'ID',
        'ID "[" expr "]"',
        'ID "(" [ exprlist ] ")"',
        'INT "(" expr ")"',
        'FLOAT "(" expr ")"',
    )
    def expr(self, p):
        ...

    @_('ID [ "[" expr "]" ]')
    def location(self, p):
        pass

    @_('expr LT expr',
        'expr LE expr',
        'expr GT expr',
        'expr GE expr',
        'expr ET expr',
        'expr DF expr',
        'relation AND relation',
        'relation OR relation',
        'NOT relation',
        '"(" relation ")"',
    )
    def relation(self, p):
        ...

    @_('expr { "," expr }')
    def exprlist(self, p):
        pass


lex = Lexer()
txt = '''
    fun hola ()
        z: int;
        f: float;
        fun bar(x:int, y:int)
            a:int;
            begin
                y := 40;
                x := 30
            end;
    begin
        
    endd
'''
txt = open('test2/write1.pl0').read()
parser = Parser()
parser.parse(lex.tokenize(txt))