# context.py
'''
Clase de alto nivel que contiene todo sobre el análisis/ejecución de un programa PL0.

Sirve como repositorio de información sobre el programa, incluido el código fuente, informe de errores, etc.
'''
from prettytable import PrettyTable

# from interp  import Interpreter
from model import *
from plex import Lexer
from pparser import Parser
from AST import AST
from checker import Checker
from ir_code import IntermediateCode

from prettytable import PrettyTable


class Context:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.checker = Checker()
        # self.interp = Interpreter(self)
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

    def print_symtab(self, source):
        symtabs = self.checker.check(self.parser.parse(self.lexer.tokenize(source)))

        errors = None

        if not self.lexer.have_errors:
            if not self.parser.have_errors:
                if self.checker.have_errors:
                    self.have_errors = True
                    errors = self.checker.errors
            else:
                self.have_errors = True
                errors = self.parser.errors
        else:
            self.have_errors = True
            errors = self.lexer.errors

        for symtab in symtabs:
            symtab_table = PrettyTable()
            symtab_table.align = 'l'
            symtab_table.field_names = ['SYMBOL NAME', 'SYMBOL TYPE']
            for symbol_name, symbol_type in zip(symtab.entries.keys(), symtab.entries.values()):
                if isinstance(symbol_type, FunDefinition):
                    symtab_table.add_row([symbol_name, 'FunDefinition'])
                elif isinstance(symbol_type, Parameter):
                    symtab_table.add_row([symbol_name, 'Parameter: ' + str(symbol_type.dtype)])
                elif isinstance(symbol_type, VarDefinition):
                    symtab_table.add_row([symbol_name, 'VarDefinition: ' + str(symbol_type.dtype)])

            if symtab.context:
                print('SCOPE: ', symtab.context.name)
            else:
                print('SCOPE: Global')
            print(symtab_table)
            print()

        return errors

    def genIr(self, source):
        node = self.parser.parse(self.lexer.tokenize(source))

        errors = None

        if not self.lexer.have_errors:
            if not self.parser.have_errors:
                self.checker.check(node)
                if not self.checker.have_errors:
                    IntermediateCode.generator(node)
                else:
                    self.have_errors = True
                    errors = self.checker.errors
            else:
                self.have_errors = True
                errors = self.parser.errors
        else:
            self.have_errors = True
            errors = self.lexer.errors

        print(errors)
