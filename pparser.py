'''
parser.py

Analizador Sintáctico para el lenguaje PL0
'''
import sly
from plex import Lexer
from past import *

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
        return Program(p.funclist)

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

    @_('PRINT "(" literal ")"')
    def stmt(self, p):
        ...

    @_('WRITE "(" expr ")"')
    def stmt(self, p):
        ...

    @_('READ "(" location ")"')
    def stmt(self, p):
        ...

    @_('WHILE relation DO stmt')
    def stmt(self, p):
        ...

    @_('BREAK')
    def stmt(self, p):
        ...

    @_('IF relation THEN stmt')
    def stmt(self, p):
        ...

    @_('BEGIN stmtlist END')
    def stmt(self, p):
        ...

    @_('location ASSIGNOP expr')
    def stmt(self, p):
        return Assign(p.location, p.expr)

    @_('RETURN expr')
    def stmt(self, p):
        ...

    @_('SKIP')
    def stmt(self, p):
        ...

    @_('ID "(" exprlist ")"')
    def stmt(self, p):
        ...

    @_('STRING', 'ICONST', 'FCONST')
    def literal(self, p):
        return p[0]

    @_('ID')
    def location(self, p):
        return Location(p.ID, 0)

    @_('ID "[" expr "]"')
    def location(self, p):
        return Location(p.ID, p.expr)

    @_('expr "+" expr',
        'expr "-" expr',
        'expr "*" expr',
        'expr "/" expr',
    )
    def expr(self, p):
        return Binary(p[1], p.expr0, p.expr1)

    @_('"-" expr %prec UNARY',
        '"+" expr %prec UNARY',
    )
    def expr(self, p):
        return Unary(p[0], p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('ICONST', 'FCONST')
    def expr(self, p):
        return p[0]

    @_('ID')
    def expr(self, p):
        return Location(p.ID, 0)

    @_('ID "[" expr "]"')
    def expr(self, p):
        return Location(p.ID, p.expr)

    @_('ID "(" [ exprlist ] ")"')
    def expr(self, p):
        return Call(p.ID, p.exprlist)

    @_('INT "(" expr ")"', 'FLOAT "(" expr ")"',)
    def expr(self, p):
        return Casting(p[0], p.expr)

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

    @_('exprlist "," expr')
    def exprlist(self, p):
        return p.exprlist + [p.expr]

    @_('expr')
    def exprlist(self, p):
        return [p.expr]





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
        
    end
'''
txt = open('test2/fun2.pl0').read()
parser = Parser()
parser.parse(lex.tokenize(txt))