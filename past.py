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

@dataclass
class DataType(Node):
    ...

# Clases reales
class TypeInt(DataType):
    value : int

class TypeFloat(DataType):
    value : float

# Expressions ---------------------------------------
@dataclass
class Logical(Expr):
    op: str
    left: Expr
    right: Expr

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
class Casting(Expr):
    datatype: DataType
    exprlist: List[Expr]

@dataclass
class Call(Expr):
    id : str
    exprlist: List[Expr]

@dataclass
class Location(Expr):
    id : str
    dim : int

'''@dataclass
class Grouping(Expr):
    exprlist: List[Expr]'''

# Statements ----------------------------------
@dataclass
class BlockCode(Stmt):
    stmtlist: List[Stmt]

@dataclass
class Assign(Stmt):
    id: Location
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
    location: Location

@dataclass
class Write(Stmt):
    value: Expr

@dataclass
class Print(Stmt):
    text = str

@dataclass
class Parm(Node):
    id: str
    datatype: DataType

@dataclass
class VarDecl(Local):
    id: str
    datatype: DataType

class FuncDecl(Local):
    name: str
    parmlist: List[Parm]
    locallist: List[Local]
    stmtlist: List[Stmt]

@dataclass
class Func(Node):
    name: str
    parmlist: List[Parm]
    locallist: List[Local]
    stmtlist: List[Stmt]

@dataclass
class Program(Node):
    funclist : List[Func]


from rich.tree import Tree
from rich.console import Console

class AST(Visitor):
    @classmethod
    def printer(cls, n:Node):
        vis = cls()
        return n.accept(vis)

    def visit(self, n:Program):
        print(1)
