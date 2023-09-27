'''
plex.py

Analizador Lexico para el lenguaje pascal
'''
import sly

class Lexer(sly.Lexer):
    tokens = {
        # Palabras Reservadas
        FUN, BEGIN, END, SKIP, BREAK, WHILE, DO,
        IF, THEN, PRINT, WRITE, READ, RETURN, 
        
        # Operadores de Relacion
        LT, LE, GT, GE, ET, DF,
        
        #Operadores logicos
        AND, OR, NOT,
        
        # Literales
        INTEGER, FLOAT, STRING, NEWLINE, ASSIGNOP,
        
        # Datatype
        INTTYPE, FLOATTYPE,

        # Otros Simbolos
        ID,
    }
    literals = '+-*/=,;():[]"'

    # ignora espacios en blanco
    ignore = ' \t\r'

    # expresiones regulares
    STRING = r'".*"'

    @_(r'[a-zA-Z_]+(\w|_)*')
    def ID(self, t):
        if t.value.upper() in self.tokens and t.value.upper() != 'ID':
            t.type = t.value.upper()
        return t

    FUN    = r'fun'
    BEGIN  = r'begin'
    END    = r'end'
    SKIP   = r'skip'
    BREAK  = r'break'
    WHILE  = r'while'
    DO     = r'do'
    IF     = r'if'
    THEN   = r'then'
    PRINT  = r'print'
    WRITE  = r'write'
    READ   = r'read'
    RETURN = r'return'

    #operadores de relacion
    LE= r'<='
    LT= r'<'
    GE= r'>='
    GT= r'>'
    ET= r'=='
    DF= r'!='
    
    #operadores logicos
    AND = r'and'
    OR = r'or'
    NOT = r'not'

    ASSIGNOP = r':='

    INTTYPE = r'int'
    FLOATTYPE = r'float'

    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += t.value.count('\n')
    
    @_(r'(\d+\.\d*|\d*\.\d+)(E-?\d+)?|[1-9]\d*E-?\d+')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTEGER(self, t):
        t.value = int(t.value)
        return t

    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1

def main(argv):
    '''if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)'''
    
    lex = Lexer()
    #txt = open(argv[1]).read()
    txt = open('test2.pl0').read()

    for tok in lex.tokenize(txt):
        print(tok)


if __name__ == '__main__':
    from sys import argv
    main(argv)