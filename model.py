from dataclasses import dataclass, field
from multimethod import multimeta
from typing import List
from rich.tree import Tree
from rich.console import Console

class Visitor(metaclass=multimeta):
    ...

# Clases abstractas
@dataclass
class Node:
    def accept(self, v: Visitor, *args, **kwargs):
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

@dataclass
class Float(Literal):
    value: float

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
    datatype: DataType

@dataclass
class Parameter(Declaration):
    name: str
    datatype: DataType

@dataclass
class FunDefinition(Declaration):
    name: str
    parmlist: Declaration
    varlist: Declaration
    stmtlist: Stmt

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
    stmt: Stmt

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


class AST(Visitor):
    @classmethod
    def printer(cls, n: Node):
        vis = cls()
        tree = n.accept(vis)
        console = Console()
        console.print(tree)

    def visit(self, n: Program):
        tree = Tree("Program")
        hijo = tree.add("funclist")

        for func in n.funclist:
            hijo.add(func.accept(self))
        return tree

    def visit(self, n: FunDefinition):
        tree = Tree("func" + "(" + n.name + ")")
        hijo1 = tree.add("parmlist")
        hijo2 = tree.add("locallist")
        hijo3 = tree.add("stmtlist")

        if n.parmlist:
            for parm in n.parmlist.parmlist:
                hijo1.add(parm.accept(self))
        if n.varlist:
            for var in n.varlist.varlist:
                hijo2.add(var.accept(self))
        for stmt in n.stmtlist.stmtlist:
            hijo3.add(stmt.accept(self))

        return tree

    def visit(self, n: Parameter):
        tree = Tree("Parameter" + "(" + n.name + ")")
        tree.add(n.datatype.accept(self))
        return tree

    def visit(self, n: VarDefinition):
        tree = Tree("VarDefinition" + "(" + n.name + ")")
        tree.add(n.datatype.accept(self))
        return tree

    # Nodos DATATYPE
    def visit(self, n: SimpleType):
        tree = Tree(str(n.name))
        return tree

    # Nodos de EXPRESSION
    def visit(self, n: Logical):
        tree = Tree("Logical (" + str(n.op) + ")")
        hijo1 = tree.add("expr_left")
        hijo1.add(n.left.accept(self))
        hijo2 = tree.add("expr_right")
        hijo2.add(n.right.accept(self))
        return tree

    def visit(self, n: Binary):
        tree = Tree("Binary (" + str(n.op) + ")")
        hijo1 = tree.add("expr_left")
        hijo1.add(n.left.accept(self))
        hijo2 = tree.add("expr_right")
        hijo2.add(n.right.accept(self))
        return tree

    def visit(self, n: Unary):
        tree = Tree("Unary " + str(n.op))
        tree.add(n.fact.accept(self))
        return tree

    def visit(self, n: TypeCast):
        tree = Tree("TypeCast")
        tree.add(n.expr.accept(self))
        return tree

    def visit(self, n: FuncCall):
        tree = Tree("Call " + n.name)
        hijo1 = tree.add("Exprlist")
        if isinstance(n.arglist, list):
            for expr in n.arglist:
                hijo1.add(expr.accept(self))
        return tree

    def visit(self, n: SimpleLocation):
        tree = Tree(n.name)
        return tree

    def visit(self, n: ArrayLocation):
        tree = Tree(n.name)
        tree.add(n.index.accept(self))
        return tree

    # Node STMTS
    def visit(self, n: Assign):
        tree = Tree("assign ")
        hijo1 = tree.add("Name (" + n.location.name + ")")
        hijo2 = tree.add("Expr")
        hijo2.add(n.expr.accept(self))
        return tree

    def visit(self, n: Float):
        tree = Tree('Float: ' + str(n.value))
        return tree

    def visit(self, n: Integer):
        tree = Tree('Int: ' + str(n.value))
        return tree

    def visit(self, n: Return):
        tree = Tree("Return")
        tree.add(n.value.accept(self))
        return tree

    def visit(self, n: IfStmt):
        tree = Tree("IfStmt")
        hijo1 = tree.add("relation")
        hijo2 = tree.add("then")
        hijo1.add(n.relation.accept(self))
        if isinstance(n.stmt, StmtList):
            for stmt in n.stmt.stmtlist:
                hijo2.add(stmt.accept(self))
        else:
            hijo2.add(n.stmt.accept(self))
        return tree

    def visit(self, n: Break):
        tree = Tree("Break")
        return tree

    def visit(self, n: Skip):
        tree = Tree("Skip")
        return tree

    def visit(self, n: While):
        tree = Tree("While")
        hijo1 = tree.add("Relation")
        hijo2 = tree.add("Stmt")
        hijo1.add(n.relation.accept(self))
        if isinstance(n.stmt, StmtList):
            print(n.stmt)
            for stmt in n.stmt.stmtlist:
                hijo2.add(stmt.accept(self))
        else:
            hijo2.add(n.stmt.accept(self))
        return tree

    def visit(self, n: Read):
        tree = Tree("Read")
        tree.add(n.location.accept(self))
        return tree

    def visit(self, n: Write):
        tree = Tree("Write")
        tree.add(n.expr.accept(self))
        return tree

    def visit(self, n: Print):
        tree = Tree("Print " + n.value)
        return tree

    def visit(self, n: ArrayType):
        tree = Tree("ArrayType (" + n.name + ")")
        hijo1 = tree.add("Dim")
        hijo1.add(n.dim.accept(self))
        return tree