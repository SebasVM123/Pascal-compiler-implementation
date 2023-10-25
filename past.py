from dataclasses import dataclass
from multimethod import multimeta
from typing import List

class Visitor(metaclass=multimeta):
    ...

# Clases abstractas
@dataclass
class Node:
    def accept(self, v: Visitor, *args, **kwargs):
        return v.visit(self, *args, **kwargs)

@dataclass
class Local(Node):
    ...

@dataclass
class Stmt(Node):
    ...

@dataclass
class Expr(Node):
    ...

# Clases reales
@dataclass
class Ident(Expr):
    id: str

@dataclass
class Number(Expr):
    value: str
    type: str

@dataclass
class Binary(Expr):
    op: str
    left: Expr
    right: Expr

@dataclass
class Unary(Expr):
    op: str
    fact: Expr

@dataclass
class Assign(Stmt):
    id: str
    expr: Expr

@dataclass
class ReturnStmt(Stmt):
    value: Expr

@dataclass
class IfStmt(Stmt):
    relation: Expr
    then: Stmt

@dataclass
class Skip(Stmt):
    ...
@dataclass
class Break(Stmt):
    ...

@dataclass
class WhileStmt(Stmt):
    relation: Expr
    stmt: Stmt

@dataclass
class Read(Stmt):
    value: str

@dataclass
class Write(Stmt):
    value: Expr

@dataclass
class Print(Stmt):
    text = str

@dataclass
class VarDecl(Local):
    id: str
    datatype: str

class FuncDecl(Local):
    name: str
    parmlist: List(Parm)
    locallist: List[Local]
    stmtlist: List(Stmt)

@dataclass
class Parm(Node):
    id: str
    datatype: str

@dataclass
class Func(Node):
    name: str
    parmlist: List(Parm)
    locallist: List(Local)
    stmtlist: List(Stmt)

@dataclass
class Program(Node):
    funclist = List(Func)