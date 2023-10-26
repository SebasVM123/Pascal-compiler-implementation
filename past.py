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
@dataclass
class TypeInt(DataType):
    value : int
@dataclass
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
class SimpleLocation(Expr):
    id : str

@dataclass
class Location(Expr):
    id : str
    dim : int
    
@dataclass
class ArrayAccess(Expr):
    id : str
    index : Expr

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
    text : str

@dataclass
class Parm(Node):
    id: str
    datatype: DataType

'''@dataclass
class VarDecl(Local):
    id: str
    datatype: DataType'''
    
@dataclass
class ArrayType(DataType):
    name: str
    expr: Expr 
    

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
        tree=n.accept(vis)
        console = Console()
        console.print(tree)
        
    def visit(self, n:Program):
        tree = Tree("Program")
        hijo = tree.add("funclist")
        for func in n.funclist:
            hijo.add(self.visit(func))
        return tree
    
    def visit(self,n: Func):
        tree = Tree("funclist" + "(" + n.name + ")")
        hijo = tree.add("parmlist")
        hijo2 = tree.add ("locallist")
        hijo3 = tree.add ("stmtlist")
        for parm in n.parmlist:
            hijo.add(self.visit(parm))
        for local in n.locallist:
            hijo2.add(self.visit(local))
        for stmt in n.stmtlist:
            hijo3.add(self.visit(stmt))
        return tree
    
    def visit(self, n: Parm):
        tree = Tree("parm" + "(" + n.id + ")")
        tree.add(label=str(n.datatype))
        return tree
    
    #Nodos DATATYPE
    def visit(self, n: TypeInt):
        tree = Tree(str(n.value))
        return tree
    def visit(self, n: TypeFloat):
        tree = Tree(str(n.value))
        return tree
    
    #Nodos de EXPRESSION
    def visit(self, n:Logical):
        tree = Tree("Logical " + str(n.op))
        hijo1=tree.add("expr_left")
        hijo1.add(self.visit(n.left))
        hijo2=tree.add("expr_right")
        hijo2.add(self.visit(n.right))
        return tree
    
    def visit(self, n: Binary):
        tree = Tree("Binary " + str(n.op))
        hijo1=tree.add("expr_left")
        hijo1.add(self.visit(n.left))
        hijo2=tree.add("expr_right")
        hijo2.add(self.visit(n.right))
        return tree
    
    def visit(self, n: Unary):
        tree = Tree("Unary " + str(n.op))
        tree.add(self.visit(n.fact))
        return tree
    
    def visit(self, n: Casting):
        tree = Tree("Casting")
        hijo1=tree.add("Exprlist")
        for expr in n.exprlist:
            hijo1.add(self.visit(expr))
        return tree
    
    def visit(self, n: Call):
        tree = Tree("Call " + n.id)
        hijo1= tree.add("Exprlist")
        for expr in n.exprlist:
            hijo1.add(self.visit(expr))
        return tree
    
    def visit(self, n: SimpleLocation):
        tree = Tree(n.id)
        return tree
    
    def visit(self, n: Location):
        tree = Tree(n.id)
        tree.add(str(n.dim))
        return tree
    
    def visit(self, n: ArrayAccess):
        tree = Tree("ArrayAccess " + n.id)
        hijo1= tree.add("Expr")
        hijo1.add(self.visit(n.index))
        return tree
    
    #Node STMTS
    def visit(self, n: BlockCode):
        tree = Tree("BlockCode")
        hijo1 = tree.add("Stmtlist")
        for stmt in n.stmtlist:
            hijo1.add(self.visit(stmt))
        return tree
    def visit(self, n: Assign):
        tree = Tree("assign " + str(n.id))
        hijo2 = tree.add("Expr")
        if n.expr == Expr:
            hijo2.add(self.visit(n.expr))
        else:
            hijo2.add(label=str(n.expr))
        return tree
    def visit(self, n: ReturnStmt):
        tree = Tree("Return")
        tree.add(self.visit(n.value))
        return tree
    def visit(self, n: IfStmt):
        tree = Tree("IfStmt")
        hijo1=tree.add("relation")
        hijo2=tree.add("then")
        hijo1.add(self.visit(n.relation))
        hijo2.add(self.visit(n.then))
        return tree
    def visit(self, n: Skip):
        tree = Tree("Skip")
        return tree
    def visit(self, n: Break):
        tree = Tree("Break")
        return tree
    def visit(self, n: WhileStmt):
        tree = Tree("While")
        hijo1 =tree.add("Relation")
        hijo2 =tree.add("Stmt")
        hijo1.add(self.visit(n.relation))
        hijo2.add(self.visit(n.stmt))
        return tree
    def visit(self, n: Read):
        tree = Tree("Read")
        tree.add(self.visit(n.location))
        return tree
    def visit(self, n: Write):
        tree = Tree("Write " + n.value)
        return tree
    def visit(self, n: Print):
        tree = Tree("Print " + n.text)
        return tree
    def visit(self, n: ArrayType):
        tree = Tree("ArrayType " + n.name)
        hijo1= tree.add("Dim")
        hijo1.add(self.visit(n.expr))
        return tree