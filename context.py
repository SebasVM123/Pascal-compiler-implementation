# context.py
'''
Clase de alto nivel que contiene todo sobre el análisis/ejecución de un programa PL0.

Sirve como repositorio de información sobre el programa, incluido el código fuente, informe de errores, etc.
'''
from prettytable import PrettyTable

# from interp  import Interpreter
from model import Node
from plex import Lexer
from pparser import Parser
from AST import AST


class Context:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        # self.interp = Interpreter(self)
        self.source = ''
        self.ast = None
        self.have_errors = False

    def print_lexer(self, source):
        tokens_table = PrettyTable()
        tokens_table.align = 'l'
        tokens_table.field_names = ['TOKEN', 'LEXEMA', 'LINENO']

        for tok in self.lexer.tokenize(source):
            tokens_table.add_row([tok.type, tok.value, tok.lineno])

        self.have_errors = self.lexer.have_errors

        print(tokens_table)

        return self.lexer.errors

    def print_AST(self, source):
        ast = self.parser.parse(self.lexer.tokenize(source))
        if not self.lexer.have_errors:
            if not self.parser.have_errors:
                AST.printer(ast)
            else:
                self.have_errors = True
                return self.parser.errors
        else:
            self.have_errors = True
            return self.lexer.errors
