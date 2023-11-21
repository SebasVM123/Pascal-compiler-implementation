# context.py
'''
Clase de alto nivel que contiene todo sobre el análisis/ejecución de un programa PL0.

Sirve como repositorio de información sobre el programa, incluido el código fuente, informe de errores, etc.
'''
# from interp  import Interpreter
from model import Node
from plex import Lexer
from pparser import Parser


class Context:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        # self.interp = Interpreter(self)
        self.source = ''
        self.ast = None
        self.have_errors = False

    def lex(self):
        pass