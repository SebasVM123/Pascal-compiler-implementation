'''
plex.py

Analizador Lexico para el lenguaje PL0
'''
import sly
from prettytable import PrettyTable


class Lexer(sly.Lexer):

    have_errors = False
    errors = []

    tokens = {
        # Palabras Reservadas
        FUN, BEGIN, END, SKIP, BREAK, WHILE, DO,
        IF, THEN, PRINT, WRITE, READ, RETURN, ELSE,

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
    }
    literals = '+-*/=,;():[]"'

    # ignora espacios en blanco
    ignore = ' \t\r'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # expresiones regulares
    @_(r'"([^"\n\\]*(\\.?[^"\n\\]*)*)"([ ]*("([^"\n\\]*(\\.?[^"\n\\]*)*)")*)*')
    def STRING(self, t):
        t.value = t.value.replace('\\"', '&escquote&')

        if t.value[-1] != '"':
            return self.error(t, error_type=4)

        splited_string = t.value.split('"')[1::2]

        t.value = '"' + ''.join(splited_string) + '"'
        t.value = t.value.replace('&escquote&', '\\"')

        escape_characters = {'"', 'n', '\\'}

        i = 0
        unknown_escapechar_error = False
        while i < len(t.value):
            if t.value[i] == '\\':
                if i + 1 < len(t.value) and t.value[i + 1] not in escape_characters:
                    unknown_escapechar_error = True
                    return self.error(t, error_type=5, extra_info=t.value[i + 1])
                i += 2
            else:
                i += 1

        if not unknown_escapechar_error:
            return t

    @_(r'"([^"\n\\]*(\\.?[^"\n\\]*)*)')
    def UNCLOSED_STRING(self, t):
        return self.error(t, error_type=4)

    keywords = {'and', 'begin', 'break', 'do', 'else', 'end', 'float', 'fun', 'if', 'int', 'not', 'or', 'print',
                'read', 'return', 'skip', 'then', 'while', 'write'}

    @_(r'(\d*\.\d+)(e(-|\+)?\d+)?|[0-9]\d*e(-|\+)?\d+')
    def FCONST(self, t):
        if t.value[0] == '.':
            return self.error(t, error_type=6)
        elif t.value[0] == '0' and t.value[1] in '0123456789':
            return self.error(t, error_type=1, extra_info='float')
        else:
            return t

    @_(r'\d*[a-zA-Z_]+(\w|_)*')
    def ID(self, t):
        if t.value[0] in '0123456789':
            return self.error(t, error_type=3)
        else:
            if t.value in self.keywords:
                t.type = t.value.upper()
            return t

    @_(r'\d+')
    def ICONST(self, t):
        if len(t.value) > 1 and t.value[0] == '0':
            return self.error(t, error_type=1, extra_info='integer')
        else:
            t.value = int(t.value)
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

    @_(r'\/\*([^*]|(\*+[^*/]))*$')
    def BAD_COMMENT(self, t):
        self.lineno += t.value.count('\n')
        return self.error(t, error_type=2)

    def error(self, t, error_type=0, extra_info=None):
        self.have_errors = True

        if error_type == 0:
            error_message = f'LEXICAL ERROR: Illegal character "{t.value[0]}" in line: {t.lineno}'
            self.index += 1
        elif error_type == 1:
            error_message = (f'LEXICAL ERROR: Leading zeros not supported in {extra_info} {t.value}, '
                             f'line: {t.lineno}')
        elif error_type == 2:
            error_message = f'LEXICAL ERROR: Unclosed comment at line: {t.lineno}'
        elif error_type == 3:
            error_message = f'LEXICAL ERROR: {t.value} is not a valid name, line {t.lineno}'
        elif error_type == 4:
            error_message = f'LEXICAL ERROR: Unclosed string at line {t.lineno}'
        elif error_type == 5:
            error_message = f'LEXICAL ERROR: {extra_info} is not a valid escape character in line {t.lineno}'
        elif error_type == 6:
            error_message = (f'LEXICAL ERROR: {t.value} must have integer part in line {t.lineno}. '
                             f'Did you mean 0{t.value}?')

        self.errors.append(error_message)


'''def print_lexer(source):
    lex = Lexer()
    tokens_table = PrettyTable()
    tokens_table.align = 'l'
    tokens_table.field_names = ['TOKEN', 'LEXEMA', 'LINENO']

    for tok in lex.tokenize(source):
        tokens_table.add_row([tok.type, tok.value, tok.lineno])

    print(tokens_table)

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
    main(argv)'''
