'''
parser.py

Analizador Sintáctico para el lenguaje PL0
'''
import sly
from rich import print
from plex import Lexer
from model import *

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
        return FunDefinition(p.ID, p.parmlist, p.locallist, p.stmtlist)
       
    @_('parmlist "," parm')
    def parmlist(self, p):
        return p.parmlist + [p.parm]
    
    @_('parm')
    def parmlist(self, p):
        return [p.parm]

    @_('ID ":" datatype')
    def parm(self, p):
        return Parameter(p.ID, p.datatype)

    @_('INT "[" expr "]"',
       'FLOAT "[" expr "]"')
    def datatype(self, p): 
        return ArrayType(p[0], p.expr)
    
    @_('INT', 'FLOAT')
    def datatype(self, p):
        return SimpleType(p[0])

    @_('local ";"')
    def locallist(self, p):
        return [p.local]
    
    @_('local ";" locallist')
    def locallist(self, p):
        return [p.local] + p.locallist

    @_('vardecl')
    def local(self, p):
        return p.vardecl

    @_('ID ":" datatype')
    def vardecl(self, p):
        return VarDefinition(p.ID, p.datatype)
    
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
        return While(p.relation, p.stmt)

    @_('BREAK')
    def stmt(self, p):
        return Break()

    @_('IF relation THEN stmt')
    def stmt(self, p):
        return IfStmt(p.relation, p.stmt)

    @_('BEGIN stmtlist END')
    def stmt(self, p):
        return StmtList(p.stmtlist)

    @_('SKIP')
    def stmt(self, p):
        return Skip()

    @_('RETURN expr')
    def stmt(self, p):
        return Return(p.expr)

    @_('location ASSIGNOP expr')
    def stmt(self, p):
        return Assign(p.location, p.expr)

    @_('ID "(" exprlist ")"')
    def stmt(self, p):
        return FuncCall(p.ID, p.exprlist)

    @_('STRING')
    def literal(self, p):
        return p.STRING

    @_('ID')
    def location(self, p):
        return SimpleLocation(p.ID)

    @_('ID "[" expr "]"')
    def location(self, p):
        return ArrayLocation(p.ID, p.expr)

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
        return Integer(p[0],SimpleType('int'))
    
    @_('FCONST')
    def expr(self,p):
        return Float(p[0],SimpleType('float'))

    @_('ID')
    def expr(self, p):
        return SimpleLocation(p.ID)

    @_('ID "[" expr "]"') 
    def expr(self, p):
        return ArrayLocation(p.ID, p.expr)

    @_('ID "(" [ exprlist ] ")"')
    def expr(self, p):
        return FuncCall(p.ID, p.exprlist)

    @_('INT "(" expr ")"', 'FLOAT "(" expr ")"',)
    def expr(self, p):
        return TypeCast(p[0], p.expr)
        
    @_('expr LT expr',
        'expr LE expr',
        'expr GT expr',
        'expr GE expr',
        'expr ET expr',
        'expr DF expr',
        'relation AND relation',
        'relation OR relation')
    def relation(sel, p):
        return Logical(p[1], p[0], p[2])

    @_('NOT relation')
    def relation(self, p):
        return Unary(p[0], p[1])
        
    @_('"(" relation ")"',)
    def relation(sel, p):
        return p.relation

    @_('exprlist "," expr')
    def exprlist(self, p):
        return p.exprlist + [p.expr]

    @_('expr')
    def exprlist(self, p):
        return [p.expr]

    def error(self, p):
        print(p)
    
def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test3/' + argv[1]).read()
    parser = Parser()
    Nodo = parser.parse(lex.tokenize(txt))
    Arbol = AST()
    Arbol.printer(Nodo)


if __name__ == '__main__':
    from sys import argv
    main(argv)
