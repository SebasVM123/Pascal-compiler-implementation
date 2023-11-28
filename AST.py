from model import *


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
        tree.add(n.dtype.accept(self))
        return tree

    def visit(self, n: VarDefinition):
        tree = Tree("VarDefinition" + "(" + n.name + ")")
        tree.add(n.dtype.accept(self))
        return tree

    # Declaraciones -------------------------------------------------
    def visit(self, n: Print):
        tree = Tree("Print " + n.value)
        return tree

    def visit(self, n: Write):
        tree = Tree("Write")
        tree.add(n.expr.accept(self))
        return tree

    def visit(self, n: Read):
        tree = Tree("Read")
        tree.add(n.location.accept(self))
        return tree

    def visit(self, n: While):
        tree = Tree("While")
        hijo1 = tree.add("Relation")
        hijo2 = tree.add("Stmt")
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

    def visit(self, n: IfStmt):
        tree = Tree("IfStmt")
        hijo1 = tree.add("relation")
        hijo2 = tree.add("then")
        hijo3 = tree.add("else")
        hijo1.add(n.relation.accept(self))
        if isinstance(n.thenstmt, StmtList):
            for stmt in n.thenstmt.stmtlist:
                hijo2.add(stmt.accept(self))
        else:
            hijo2.add(n.thenstmt.accept(self))

        if isinstance(n.elsestmt, StmtList):
            for stmt in n.elsestmt.stmtlist:
                hijo3.add(stmt.accept(self))
        elif n.elsestmt:
            hijo3.add(n.elsestmt.accept(self))

        return tree

    def visit(self, n: Return):
        tree = Tree("Return")
        tree.add(n.value.accept(self))
        return tree

    def visit(self, n: Skip):
        tree = Tree("Skip")
        return tree

    def visit(self, n: Assign):
        tree = Tree("assign ")
        hijo1 = tree.add("Name (" + n.location.name + ")")
        hijo2 = tree.add("Expr")
        hijo2.add(n.expr.accept(self))
        return tree

    # Expresiones ---------------------------------------------------------------
    def visit(self, n: Integer):
        tree = Tree('Int: ' + str(n.value))
        return tree

    def visit(self, n: Float):
        tree = Tree('Float: ' + str(n.value))
        return tree

    def visit(self, n: SimpleLocation):
        tree = Tree("Simpleloc (" + n.name + ")")
        return tree

    def visit(self, n: ArrayLocation):
        tree = Tree("ArrayLoc (" + n.name + ")")
        tree.add(n.index.accept(self))
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
        else:
            hijo1.add(label=n.expr)
        return tree

    def visit(self, n: Binary):
        tree = Tree("Binary (" + str(n.op) + ")")
        hijo1 = tree.add("expr_left")
        hijo1.add(n.left.accept(self))
        hijo2 = tree.add("expr_right")
        hijo2.add(n.right.accept(self))
        return tree

    def visit(self, n: Logical):
        tree = Tree("Logical (" + str(n.op) + ")")
        hijo1 = tree.add("expr_left")
        hijo1.add(n.left.accept(self))
        hijo2 = tree.add("expr_right")
        hijo2.add(n.right.accept(self))
        return tree

    def visit(self, n: Unary):
        tree = Tree("Unary " + str(n.op))
        tree.add(n.fact.accept(self))
        return tree

    # Datatype -------------------------------------------------------------------------
    def visit(self, n: SimpleType):
        tree = Tree(str(n.name))
        return tree

    def visit(self, n: ArrayType):
        tree = Tree("ArrayType (" + n.name + ")")
        hijo1 = tree.add("Dim")
        hijo1.add(n.dim.accept(self))
        return tree
