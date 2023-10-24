from dataclasses import dataclass
from multimethod import multimeta
from typing import List

# Clase Visitor
class Visitor(metaclass=multimeta):
  ...

# Clases Abstractas

@dataclass
class Node:
  def accept(self, v:Visitor, *args, **kwargs):
    return v.visit(self, *args, **kwargs)

@dataclass 
class Func(Node):
  ...

@dataclass
class Stmt(Node):
  ...

@dataclass
class Expr(Node):
  ...

@dataclass 
class Parm(Node):
  ...

@dataclass
class Local(Node):
  ...

# Clases concretas
@dataclass
class Program(Func):
  funclist : List[Func]
  
@dataclass 
class FuncExpr(Func):
  parmlist  : List[Parm]
  locallist : List[Local]
  stmtlist  : List[Stmt] 

@dataclass
class StmtExpr(Stmt):
  expr : Expr

@dataclass
class Logical(Expr):
  op    : str
  left  : Expr
  right : Expr

@dataclass
class Binary(Expr):
  op    : str
  left  : Expr
  right : Expr
  
@dataclass 
class Unary(Expr):
  op: str
  expr: Expr
    
@dataclass
class Literal(Expr):
  value : str 
  
@dataclass
class Location(Expr):
  id   : str
  dim  : Expr
  
@dataclass
class Call(Expr):
  name   : str
  exprlist  : List[Expr]
  
@dataclass
class Casting(Expr):
  typename   : str
  expr  : Expr

@dataclass
class Assign(Stmt):
  id   : str
  expr : Expr

@dataclass
class IConst(Expr):
  value : int
  
@dataclass
class FConst(Expr):
  value : float

@dataclass
class Ident(Expr):
  id : str