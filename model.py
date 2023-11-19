from dataclasses import dataclass, field
from multimethod import multimeta
from typing import List
from rich.tree import Tree
from rich.console import Console
from rich import print
import inspect

class Visitor(metaclass=multimeta):
    ...

# Clases abstractas
@dataclass
class Node:
    def accept(self, v: Visitor, *args, **kwargs):
        if args:
            if args[0].context is not None:
                print(self)
                print(f'Context: {args[0].context.name}, Entries: {list(args[0].entries.keys())}')
                #print(list(args[0].entries.values()))
                print('-' * 100)
        return v.visit(self, *args, **kwargs)

@dataclass
class DataType(Node):
    ...

@dataclass
class Stmt(Node):
    ...

@dataclass
class Expr(Node):
    ...

# DataType ------------------------------------------
@dataclass
class SimpleType(DataType):
    name: str

@dataclass
class ArrayType(DataType):
    name: str
    dim: Expr

# Expressions ---------------------------------------
@dataclass
class Literal(Expr):
    ...

@dataclass
class Integer(Literal):
    value: int
    dtype: DataType = SimpleType('int')

@dataclass
class Float(Literal):
    value: float
    dtype: DataType = SimpleType('float')
    
@dataclass
class Location(Expr):
    ...

@dataclass
class SimpleLocation(Location):
    name: str


@dataclass
class ArrayLocation(Location):
    name: str
    index: Expr

@dataclass
class TypeCast(Expr):
    name: str
    expr: Expr

@dataclass
class FuncCall(Expr):
    name: str
    arglist: Expr

    def __post_init__(self):
        if isinstance(self.arglist, list):
            self.arglist = ArgList(self.arglist)

@dataclass
class Binary(Expr):
    op: str
    left: Expr
    right: Expr
 

@dataclass
class Logical(Expr):
    op: str
    left: Expr
    right: Expr

@dataclass
class Unary(Expr):
    op: str
    fact: Expr

# Statements ----------------------------------
@dataclass
class Declaration(Stmt):
    ...

@dataclass
class VarDefinition(Declaration):
    name: str
    dtype: DataType
    init : bool = field(init=False, default=False)

@dataclass
class Parameter(Declaration):
    name: str
    dtype: DataType

@dataclass
class FunDefinition(Declaration):
    name: str
    parmlist: Declaration
    varlist: Declaration
    stmtlist: Stmt
    dtype: DataType = field(init=False, default=None)
    
    def __post_init__(self):
        if isinstance(self.parmlist, list):
            self.parmlist = ParmList(self.parmlist)
        if isinstance(self.varlist, list):
            self.varlist = VarList(self.varlist)
        if isinstance(self.stmtlist, list):
            self.stmtlist = StmtList(self.stmtlist)

@dataclass
class Print(Stmt):
    value: str

@dataclass
class Write(Stmt):
    expr: Expr

@dataclass
class Read(Stmt):
    location: Expr

@dataclass
class While(Stmt):
    relation: Expr
    stmt: Stmt

@dataclass
class Break(Stmt):
    ...

@dataclass
class IfStmt(Stmt):
    relation: Expr
    thenstmt: Stmt
    elsestmt: Stmt

@dataclass
class Skip(Stmt):
    ...

@dataclass
class Return(Stmt):
    value: Expr

@dataclass
class Assign(Stmt):
    location: Location
    expr: Expr

# Contenedores ----------------------------------
@dataclass
class Program(Stmt):
    funclist: List[FunDefinition] = field(default_factory=list)

@dataclass
class StmtList(Stmt):
    stmtlist: List[Stmt] = field(default_factory=list)

@dataclass
class VarList(Stmt):
    varlist: List[Declaration] = field(default_factory=list)

@dataclass
class ParmList(Stmt):
    parmlist: List[Declaration] = field(default_factory=list)

@dataclass
class ArgList(Stmt):
    arglist: List[Expr] = field(default_factory=list)
