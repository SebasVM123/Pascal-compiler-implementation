'''
parser.py

Analizador Sintáctico para el lenguaje PL0
'''
import sly
from rich import print
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

    @_('funclist func')
    def funclist(self, p):
        return p.funclist + [p.func]
    
    @_('func')
    def funclist(self, p):
        return [p.func]

    @_('FUN ID "(" [ parmlist ] ")" [ locallist ] BEGIN stmtlist END')
    def func(self, p):
        return Func(p[1],p.parmlist,p.locallist,p.stmtlist)
       
    @_('parmlist "," parm')
    def parmlist(self, p):
        return p.parmlist + [p.parm]
    
    @_('parm')
    def parmlist(self, p):
        return [p.parm]

    @_('ID ":" datatype')
    def parm(self, p):
        return Parm(p[0],p[2])

    @_('INT "[" expr "]"',
       'FLOAT "[" expr "]"')
    def datatype(self, p): 
        return ArrayType(p[0],p.expr)
    
    @_('INT')
    def datatype(self, p):
        return TypeInt(p[0])
    
    @_('FLOAT')
    def datatype(self, p):
        return TypeFloat(p[0])

    @_('local ";"')
    def locallist(self, p):
        return [p.local]
    
    @_('local ";" locallist')
    def locallist(self, p):
        return [p.local] + p.locallist

    @_('parm')
    def local(self, p):
        return p.parm
    
    @_('func')
    def local(self, p):
        return p.func

    @_('stmt')
    def stmtlist(self, p):
        return [p.stmt]
    
    @_('stmt ";" stmtlist')
    def stmtlist(self, p):
        return [p.stmt] + p.stmtlist

    @_('PRINT "(" literal ")"')
    def stmt(self, p):
        return Print(p.literal)

    @_('WRITE "(" expr ")"')
    def stmt(self, p):
        return Write(p.expr)

    @_('READ "(" location ")"')
    def stmt(self, p):
        return Read(p.location)

    @_('WHILE relation DO stmt')
    def stmt(self, p):
        return WhileStmt(p[1],p[3])

    @_('BREAK')
    def stmt(self, p):
        return Break()

    @_('IF relation THEN stmt [ ELSE stmt ]')
    def stmt(self, p):
        return IfStmt(p[1],p[3])

    @_('BEGIN stmtlist END')
    def stmt(self, p):
        return BlockCode(p.stmtlist)

    @_('location ASSIGNOP expr')
    def stmt(self, p):
        return Assign(p.location, p.expr)

    @_('RETURN expr')
    def stmt(self, p):
        return ReturnStmt(p[1])

    @_('SKIP')
    def stmt(self, p):
        return Skip()

    @_('ID "(" exprlist ")"')
    def stmt(self, p):
        return Call(p[0],p.exprlist)

    @_('STRING', 'ICONST', 'FCONST')
    def literal(self, p):
        return p[0]

    @_('ID')
    def location(self, p):
        return SimpleLocation(p.ID)

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

    @_('ICONST')
    def expr(self, p):
        return p[0]
    
    @_('FCONST')
    def expr(self,p):
        return p[0]

    @_('ID')
    def expr(self, p):
        return SimpleLocation(p.ID)

    @_('ID "[" expr "]"') 
    def expr(self, p):
        return ArrayAccess(p.ID, p.expr)

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
        'relation OR relation')
    def relation(sel, p):
        return Logical(p[1],p[0],p[2])

    @_('NOT relation')
    def relation(self, p):
        return Unary(p[0],p[1])
        
    @_('"(" relation ")"',)
    def relation(sel, p):
        return p.relation

    @_('exprlist "," expr')
    def exprlist(self, p):
        return p.exprlist + [p.expr]

    @_('expr')
    def exprlist(self, p):
        return [p.expr]
    
def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test2/' + argv[1]).read()
    parser = Parser()
    Nodo=parser.parse(lex.tokenize(txt))
    Arbol=AST()
    Arbol.printer(Nodo)
    


if __name__ == '__main__':
    from sys import argv
    main(argv)
