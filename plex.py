'''
plex.py

Analizador Lexico para el lenguaje pascal
'''
import sly
from prettytable import PrettyTable

class Lexer(sly.Lexer):
    tokens = {
        # Palabras Reservadas
        FUN, BEGIN, END, SKIP, BREAK, WHILE, DO,
        IF, THEN, PRINT, WRITE, READ, RETURN,

        # Operadores de Relacion
        LT, LE, GT, GE, ET, DF,

        # Operadores logicos
        AND, OR, NOT,

        # Literales
        ICONST, FCONST, STRING, ASSIGNOP,

        # Datatype
        INT, FLOAT,

        # Identificador
        ID,

        # Comentarios
        COMMENT
    }
    literals = '+-*/=,;():[]"'

    # ignora espacios en blanco
    ignore = ' \t\r'

    # expresiones regulares
    STRING = r'".*"'

    keywords = {'and', 'begin', 'break', 'do', 'else', 'end', 'float', 'fun', 'if', 'int', 'not', 'or', 'print',
                'read', 'return', 'skip', 'then', 'while', 'write'}

    @_(r'[a-zA-Z_]+(\w|_)*')
    def ID(self, t):
        if t.value in self.keywords:
            t.type = t.value.upper()
        return t

    FUN = r'fun'
    BEGIN = r'begin'
    END = r'end'
    SKIP = r'skip'
    BREAK = r'break'
    WHILE = r'while'
    DO = r'do'
    IF = r'if'
    THEN = r'then'
    PRINT = r'print'
    WRITE = r'write'
    READ = r'read'
    RETURN = r'return'

    # operadores de relacion
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    ET = r'=='
    DF = r'!='

    # operadores logicos
    AND = r'and'
    OR = r'or'
    NOT = r'not'

    ASSIGNOP = r':='

    INT = r'int'
    FLOAT = r'float'

    @_(r'\/\*([^*]|(\*+[^*/]))*\*+\/')
    def COMMENT(self, t):
        self.lineno += t.value.count('\n')
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    @_(r'(\d+\.\d+)(e(-|\+)?\d+)?|[0-9]\d*e(-|\+)?\d+')
    def FCONST(self, t):
        return t

    @_(r'\d+')
    def ICONST(self, t):
        if len(t.value) > 1 and t.value[0] == '0':
            self.error(t, error_type=1)
        else:
            t.value = int(t.value)
            return t

    def error(self, t, error_type=0):
        if error_type == 0:
            print(f'\033[91mERROR: Illegal character "{t.value[0]}" in line: {t.lineno}\033[0m')
            self.index += 1
        elif error_type == 1:
            print(f'\033[91mERROR: Leading zeros not supported in integer {t.value}, line: {t.lineno}\033[0m')


def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test1/' + argv[1]).read()

    tokens_table = PrettyTable()
    tokens_table.align = 'l'
    tokens_table.field_names = ['TOKEN', 'LEXEMA', 'LINENO']

    for tok in lex.tokenize(txt):
        tokens_table.add_row([tok.type, tok.value, tok.lineno])

    print(tokens_table)


if __name__ == '__main__':
    from sys import argv
    main(argv)