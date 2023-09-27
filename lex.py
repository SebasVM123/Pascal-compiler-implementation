# lexer.py

import sly


class Lexer(sly.Lexer):
    # Definición de Símbolos
    tokens = {
        # Palabras Reservadas:
        BEGIN, END, PRINT, IF, THEN,

        # Identificador
        IDENT,

        # Comentario
        COMMENT,
    }
    literals = '+-*/=,;()'

    # Espacios en Blanco
    ignore = ' \t\r'

    # Expresiones Regulares
    BEGIN = r'begin'
    END = r'end'
    PRINT = r'print'
    IF = r'if'
    THEN = r'then'

    IDENT = r'[a-zA-Z][a-zA-Z0-9]*'

    COMMENT = '//.*'

    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\d*\.\d+')
    def RCONST(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def ICONST(self, t):
        t.value = int(t.value)
        return t

    @_(r'".+"')
    def SCONST(self, t):
        t.value = str(t.value)
        return t

    def error(self, t):
        print(f"Caracter ilegal '{t.value[0]}'")
        self.index += 1


if __name__ == "__main__":
    #file_name = input('Ingrese el nombre del archivo: ')

    with open('test.txt') as file:
        lex = Lexer()
        for tok in lex.tokenize(file.read()):
            print(tok)