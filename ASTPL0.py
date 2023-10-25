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
class Stmt(Node):
  ...

@dataclass
class Expr(Node):
  ...

# Clases Concretas

@dataclass
class Parm(Expr):
  ID: str
  datatype: Type

@dataclass
class Func(Stmt):
  name: str
  parmlist: List[Parm]

@dataclass
class Program(Stmt):
  funclist: List[Func]