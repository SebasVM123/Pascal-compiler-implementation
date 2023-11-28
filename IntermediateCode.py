# IntermediateCode.py
import sys

from rich.console import Console

from plex import Lexer
from pparser import Parser
from AST import AST
from model import *
from typesys import *


class IntermediateCode(Visitor):
    intermediate_code = {}
    registers = {}

    @classmethod
    def generator(cls, n: Node):
        vis = cls()
        n.accept(vis)

    def visit(self, n: Program):
        for func in n.funclist:
            func.accept(self)

    def visit(self, n: FunDefinition):
        self.intermediate_code[n.name] = []
        if n.parmlist:
            n.parmlist.accept(self, n.name)
        if n.varlist:
            n.varlist.accept(self, n.name)

        n.stmtlist.accept(self, n.name)

        print(self.intermediate_code)

    def visit(self, n: Parameter, namefunc):
        p = 1
        while f'R{p}' in self.registers.values():
            p = p + 1

        self.registers[n.name] = f'R{p}'
        self.intermediate_code[namefunc].append(f"('LOADI', '{n.name}', 'R{p}')")

    def visit(self, n: VarDefinition, namefunc):
        p = 1
        while f'R{p}' in self.registers.values():
            p = p + 1

        self.registers[n.name] = f'R{p}'
        self.intermediate_code[namefunc].append(f"('LOADI', '{n.name}', 'R{p}')")

    # Declaraciones ------------------------------------------------------
    def visit(self, n: Print, namefunc):
        pass

    def visit(self, n: Write, namefunc):
        ...

    def visit(self, n: Read, namefunc):
        ...

    def visit(self, n: While, namefunc):
        ...

    def visit(self, n: Break, namefunc):
        ...

    def visit(self, n: IfStmt,namefunc):
        n.relation.accept(self,namefunc)
        n.thenstmt.accept(self,namefunc)
        if n.elsestmt:
            n.elsestmt.accept(self,namefunc)

    def visit(self, n: Return, namefunc):
        RD = n.value.accept(self, namefunc)
        self.intermediate_code[namefunc].append(f"('RET', '{RD}')")

    def visit(self, n: Skip, namefunc):
        ...

    def visit(self, n: Assign, namefunc):
        p = 1
        while f'R{p}' in self.registers.values():
            p = p + 1

        register = (n.location.accept(self, namefunc))

        self.registers[register] = f'R{p}'
        self.intermediate_code[namefunc].append(f"('STOREI', '{register}', '{self.registers[register]}')")
        n.expr.accept(self,namefunc)




    # Expresiones ---------------------------------------------
    def visit(self, n: Integer, namefunc):
        # Devolver datatype
        p = 1
        while f'R{p}' in self.registers.values():
            p = p + 1
        self.registers[n.value] = f'R{p}'
        self.intermediate_code[namefunc].append(f"('MOVI', '{n.value}', '{self.registers[n.value]}')")
        return f'R{p}'

    def visit(self, n: Float, namefunc):
        p = 1
        while f'R{p}' in self.registers.values():
            p = p + 1
        self.registers[n.value] = f'R{p}'
        self.intermediate_code[namefunc].append(f"('MOVI', '{n.value}', '{self.registers[n.value]}')")
        return f'R{p}'

    def visit(self, n: SimpleLocation, namefunc):
        return n.name

    def visit(self, n: ArrayLocation, namefunc):
        ...

    def visit(self, n: TypeCast, namefunc):
        ...

    def visit(self, n: FuncCall, namefunc):
        p = 1
        while f'R{p}' in self.registers.values():
            p = p + 1

        self.registers[n.name] = f'R{p}'
        listargs = n.arglist.accept(self,namefunc)

        args = ''
        for i in listargs:
            if 'R' in i:
                for key,value in self.registers.items():
                    if value == i:
                        if args:
                            args = f"'{args}', '{i}'"
                        else:
                            args = f'{i}'
            else:
                if args:
                    args = f"'{args}', '{self.registers[i]}'"
                else:
                    args = f'{self.registers[i]}'

        self.intermediate_code[namefunc].append(f"('CALL', '{n.name}', '{args}', '{self.registers[n.name]}')")
        return f'R{p}'

    def visit(self, n: Binary, namefunc):
        p = 1
        while f'R{p}' in self.registers.values():
            p = p + 1
        if n.op == '/':
            op = f'DIVI'
        elif n.op == '*':
            op = f'MULI'
        elif n.op == '+':
            op = f'ADDI'
        elif n.op == '-':
            op = f'SUBI'

        RD = self.registers[f'Resultop{p}'] = f'R{p}'

        left = n.left.accept(self, namefunc)
        right = n.right.accept(self, namefunc)
        if 'R' not in left:
            left = self.registers[left]
        if 'R' not in right:
            right = self.registers[right]

        self.intermediate_code[namefunc].append(f"('{op}', '{left}', '{right}', '{RD}')")
        return RD

    def visit(self, n: Logical, namefunc):
        p = 1
        while f'R{p}' in self.registers.values():
            p = p + 1
        if n.op == '>':
            op = f'GT'
        elif n.op == '<':
            op = f'LT'
        elif n.op == '>=':
            op = f'GE'
        elif n.op == '<=':
            op = f'LE'
        elif n.op == 'and':
            op = f'AND'
        elif n.op == 'or':
            op = f'OR'

        RD = self.registers[f'Resultop{p}'] = f'R{p}'

        left = n.left.accept(self, namefunc)
        right = n.right.accept(self, namefunc)
        if 'R' not in left:
            left = self.registers[left]
        if 'R' not in right:
            right = self.registers[right]

        self.intermediate_code[namefunc].append(f"('{op}', '{left}', '{right}', '{RD}')")

        return RD

    def visit(self, n: Unary, namefunc):
        p = 1
        while f'R{p}' in self.registers.values():
            p = p + 1
        if n.op == '/':
            op = f'DIVI'
        elif n.op == '*':
            op = f'MULI'
        elif n.op == '+':
            op = f'ADDI'
        elif n.op == '-':
            op = f'SUBI'
        elif n.op == 'not':
            op = f'NOT'

        RD = self.registers[f'Resultop{p}'] = f'R{p}'

        fact = n.fact.accept(self, namefunc)

        if 'R' not in fact:
            fact = self.registers[fact]

        self.intermediate_code[namefunc].append(f"('{op}', '{fact}', '{RD}')")
        return RD

    # Contenedores -----------------------------------------------
    def visit(self, n: ParmList, namefunc):
        parmlist = []
        for parm in n.parmlist:
            parmlist.append(parm.accept(self, namefunc))
        return parmlist

    def visit(self, n: VarList, namefunc):
        for var in n.varlist:
            return var.accept(self, namefunc)

    def visit(self, n: StmtList, namefunc):
        for stmt in n.stmtlist:
            stmt.accept(self, namefunc)

    def visit(self, n: ArgList, namefunc):
        arglist = []
        for arg in n.arglist:
            arglist.append(arg.accept(self, namefunc))
        return arglist


def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test3/' + argv[1]).read()
    parser = Parser()
    nodo = parser.parse(lex.tokenize(txt))
    IntermediateCode.generator(nodo)


if __name__ == '__main__':
    from sys import argv

    main(argv)
