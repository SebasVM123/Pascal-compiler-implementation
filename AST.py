from rich.tree import Tree
from rich.console import Console
from past import *
from plex import Lexer
from pparser import Parser

class AST(Visitor):
    @classmethod
    def printer(cls, n:Node):
        vis = cls()
        tree= n.accept(vis)
        console = Console()
        console.print(tree)
        
    def visit(self, n:Program):
        tree = Tree("Program")
        hijo = tree.add("funclist")
        for func in n.funclist:
            hijo.add(func.accept(self))
        return tree
    
    def visit(self,n: Func):
        tree = Tree("funclist" + "(" + n.name + ")")
        hijo = tree.add("parmlist")
        hijo2 = tree.add ("locallist")
        hijo3 = tree.add ("stmtlist")

        if isinstance(n.parmlist,list):
            for parm in n.parmlist: 
                hijo.add(parm.accept(self))
        if isinstance(n.locallist,list):
            for local in n.locallist:
                hijo2.add(local.accept(self))
        if isinstance(n.stmtlist,list):
            for stmt in n.stmtlist:
                hijo3.add(stmt.accept(self))
        return tree
    
    def visit(self, n: Parm):
        tree = Tree("parm" + "(" + n.id + ")")
        tree.add(label=str(n.datatype))
        return tree
    
    #Nodos DATATYPE
    def visit(self, n: SimpleType):
        tree = Tree(str(n.value))
        return tree
    def visit(self, n: SimpleType):
        tree = Tree(str(n.value))
        return tree
    
    #Nodos de EXPRESSION
    def visit(self, n:Logical):
        tree = Tree("Logical " + str(n.op))
        hijo1=tree.add("expr_left")
        hijo1.add(n.left.accept(self))
        hijo2=tree.add("expr_right")
        hijo2.add(n.right.accept(self))
        return tree
    
    def visit(self, n: Binary):
        tree = Tree("Binary " + str(n.op))
        hijo1=tree.add("expr_left")
        hijo1.add(n.left.accept(self))
        hijo2=tree.add("expr_right")
        hijo2.add(n.right.accept(self))
        return tree
    
    def visit(self, n: Unary):
        tree = Tree("Unary " + str(n.op))
        tree.add(n.fact.accept(self))
        return tree
    
    def visit(self, n: Casting):
        tree = Tree("Casting")
        hijo1=tree.add("Exprlist")
        for expr in n.exprlist:
            hijo1.add(expr.accept(self))
        return tree
    
    def visit(self, n: Call):
        tree = Tree("Call " + n.id)
        hijo1= tree.add("Exprlist")
        if isinstance(n.exprlist,list):
            for expr in n.exprlist:
                hijo1.add(expr.accept(self))
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
        hijo1.add(n.index.accept(self))
        return tree
    
    #Node STMTS
    def visit(self, n: BlockCode):
        tree = Tree("BlockCode")
        hijo1 = tree.add("Stmtlist")
        for stmt in n.stmtlist:
            hijo1.add(stmt.accept(self))
        return tree
    def visit(self, n: Assign):
        tree = Tree("assign " + str(n.id))
        hijo2 = tree.add("Expr")
        if n.expr == Expr:
            hijo2.add(n.expr.accept(self))
        else:
            hijo2.add(label=str(n.expr))
        return tree
    def visit(self, n: ReturnStmt):
        tree = Tree("Return")
        tree.add(n.value.accept(self))
        return tree
    def visit(self, n: IfStmt):
        tree = Tree("IfStmt")
        hijo1=tree.add("relation")
        hijo2=tree.add("then")
        hijo1.add(n.relation.accept(self))
        hijo2.add(n.then.accept(self))
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
        hijo1.add(n.relation.accept(self))
        hijo2.add(n.stmt.accept(self))
        return tree
    def visit(self, n: Read):
        tree = Tree("Read")
        tree.add(n.location.accept(self))
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
        hijo1.add(n.expr.accept(self))
        return tree

def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test2/' + argv[1]).read()
    parser = Parser()
    Nodo=parser.parse(lex.tokenize(txt))
    Arbol=AST()
    Arbol.printer(Nodo)
    


if __name__ == '__main__':
    from sys import argv
    main(argv)
