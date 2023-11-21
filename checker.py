# checker.py
import sys

from rich.console import Console

from plex import Lexer
from pparser import Parser
from AST import AST
from model import *
from typesys import *


def error(code: int, name: str = None, value1: str = None, value2: str = None):
    console = Console()
    if code == 1:
        console.print(f'[red]Name Error: variable {name} used but no defined.[/red]')
    elif code == 2:
        console.print(f'[red]Attribute Error: array variable {name} used without specifying an index.[/red]')
    elif code == 3:
        console.print(f'[red]Attribute Error: variable {name} has no indices because it was not defined as an array.'
                      f'[/red]')
    elif code == 4:
        console.print(f'[red]Type Error: invalyd assignment of {value2} expression to a {value1} variable {name}[/red]')
    elif code == 5:
        console.print(f'[red]Type Error: unsupported operand type for "{name}": "{value1}" and "{value2}"[/red]')
    elif code == 6:
        console.print(f'[red]Error: Break Statement must be within a While Statement[/red]')
    elif code == 7:
        console.print(f'[red]Name Error: function {name} called but no defined.[/red]')
    elif code == 8:
        console.print(f'[red]Type Error: in call of {name}: expected {value1} arguments but {value2} were given.[/red]')
    elif code == 9:
        console.print(f'[red]Type Error: type of argument passed in call of {name} does not match with the type '
                      f'expected.[/red]')
    elif code == 10:
        console.print(f'[red]Name Error: main function not found[/red]')

    print('-' * 100)

# ---------------------------------------------------------------------
#  Tabla de Simbolos
# ---------------------------------------------------------------------
class Symtab:
    '''
    Una tabla de símbolos.  Este es un objeto simple que sólo
    mantiene una hashtable (dict) de nombres de simbolos y los
    nodos de declaracion o definición de funciones a los que se
    refieren.
    Hay una tabla de simbolos separada para cada elemento de
    código que tiene su propio contexto (por ejemplo cada función,
    clase, tendra su propia tabla de simbolos). Como resultado,
    las tablas de simbolos se pueden anidar si los elementos de
    código estan anidados y las búsquedas de las tablas de
    simbolos se repetirán hacia arriba a través de los padres
    para representar las reglas de alcance léxico.
    '''

    class SymbolDefinedError(Exception):
        '''
        Se genera una excepción cuando el código intenta agregar
        un simbol a una tabla donde el simbol ya se ha definido.
        Tenga en cuenta que 'definido' se usa aquí en el sentido
        del lenguaje C, es decir, 'se ha asignado espacio para el
        simbol', en lugar de una declaración.
        '''
        def __init__(self, env, name):
            sys.tracebacklimit = 0

            if isinstance(env.entries[name], Parameter):
                super().__init__(f'In function {env.context.name}: Parameter {name} has already been defined before')
            elif isinstance(env.entries[name], VarDefinition):
                super().__init__(f'In function {env.context.name}: Variable {name} has already been defined before')
            elif isinstance(env.entries[name], FunDefinition):
                super().__init__(f'In function {env.context.name}: Function {name} has already been defined before')


    def __init__(self, context=None, parent=None):
        '''
            Crea una tabla de símbolos vacia con la tabla de
            simbolos padre dada.
        '''
        self.entries = {}
        self.parent = parent
        if self.parent:
            self.parent.children.append(self)
        self.children = []

        self.context = context

    def add(self, name, value):
        '''
        Agrega un simbol con el valor dado a la tabla de simbolos.
        El valor suele ser un nodo AST que representa la declaración
        o definición de una función, variable (por ejemplo, Declaración
        o FuncDeclaration)
        '''
        if name in self.entries:
            raise Symtab.SymbolDefinedError(self, name)
        self.entries[name] = value

    def get_var(self, name):
        '''
        Recupera el símbolo con el nombre dado de la tabla de
        símbolos, recorriendo hacia arriba a traves de las tablas
        de símbolos principales si no se encuentra en la actual.
        '''
        if name in self.entries:
            if not isinstance(self.entries[name], FunDefinition):
                return self.entries[name]
        elif self.parent:
            return self.parent.get_var(name)
        return None

    def get_fun(self, name):
        '''
        Recupera el símbolo con el nombre dado de la tabla de
        símbolos, recorriendo hacia arriba a traves de las tablas
        de símbolos principales si no se encuentra en la actual.
        '''
        if name in self.entries:
            if isinstance(self.entries[name], FunDefinition):
                return self.entries[name]
        elif self.parent:
            return self.parent.get_fun(name)
        return None


class Checker(Visitor):

    @classmethod
    def check(cls, n: Node):
        vis = cls()
        n.accept(vis)

    def visit(self, n: Program):
        # Crear un nuevo contexto (Symtab global)
        # Visitar cada una de las declaraciones asociadas
        global_env = Symtab()
        for func in n.funclist:
            func.accept(self, global_env)

        if 'main' not in global_env.entries:
            error(10)

    def visit(self, n: FunDefinition, env: Symtab):
        # Agregar el nombre de la funcion a Symtab
        # Crear un nuevo contexto (Symtab)
        # Visitar ParamList, VarList, StmtList
        # Determinar el datatype de la funcion (revisando instrucciones return)
        env.add(n.name, n)

        print(n, 'Program', env.entries.keys())
        print('-' * 100)

        local_env = Symtab(context=n, parent=env)

        if n.parmlist:
            n.parmlist.accept(self, local_env)
        if n.varlist:
            n.varlist.accept(self, local_env)
        n.stmtlist.accept(self, local_env)

    def visit(self, n: Parameter, env: Symtab):
        # Agregar el nombre del parametro a Symtab
        env.add(n.name, n)

    def visit(self, n: VarDefinition, env: Symtab):
        # Agregar el nombre de la variable a Symtab
        env.add(n.name, n)

    # Declaraciones ------------------------------------------------------
    def visit(self, n: Print, env: Symtab):
        ...

    def visit(self, n: Write, env: Symtab):
        # Buscar la Variable en Symtab

        n.expr.accept(self, env) # Dentro de Write solo van variables?

    def visit(self, n: Read, env: Symtab):
        # Visitar la variable

        n.location.accept(self, env)

    def visit(self, n: While, env: Symtab):
        # Visitar la condicion del While (Comprobar tipo bool)
        # Visitar las Stmts

        n.relation.accept(self, env)
        in_while = True
        if isinstance(n.stmt, StmtList):
            for stmt in n.stmt.stmtlist:
                if isinstance(stmt, Break):
                    stmt.accept(self, env, in_while)
                else:
                    stmt.accept(self, env)
        elif isinstance(n.stmt, Break):
            n.stmt.accept(self, env, in_while)
        else:
            n.stmt.accept(self, env)

    def visit(self, n: Break, env: Symtab, in_while: bool = False):
        # Esta dentro de un While?

        if not in_while:
            error(6)
    def visit(self, n: IfStmt, env: Symtab):
        # Visitar la condicion del IfStmt (Comprobar tipo bool)
        # Visitar las Stmts del then y else

        n.relation.accept(self, env)
        n.thenstmt.accept(self, env)

    def visit(self, n: Return, env: Symtab):
        # Visitar la expresion asociada
        # Actualizar el datatype de la funcion

        dtype = n.value.accept(self, env)
        if dtype is not None:
            env.context.dtype = dtype

    def visit(self, n: Skip, env: Symtab):
        ...

    def visit(self, n: Assign, env: Symtab):
        # Visitar el location (devuelve datatype) y marcar ese location como inicializado en VarDefinition
        # Visitar la expresión (devuelve datatype)
        # Comparar ambos tipo de datatype

        # Solo evalua la expresion si la variable está definida y su tipo de variable concuerda
        if (location_dtype := n.location.accept(self, env)) is not None:
            # Solo compara los tipos si la expresion no tiene errores de tipo

            if (expr_dtype := n.expr.accept(self, env)) is not None:
                if location_dtype != expr_dtype:
                    error(4, name=n.location.name, value1=location_dtype, value2=expr_dtype)

    # Expresiones ---------------------------------------------
    def visit(self, n: Integer, env: Symtab):
        # Devolver datatype

        return n.dtype.name

    def visit(self, n: Float, env: Symtab):
        # Devolver datatype

        return n.dtype.name

    def visit(self, n: SimpleLocation, env: Symtab):
        # Buscar en Symtab y extraer datatype (No se encuentra?)
        # Comprobar que el tipo de variable (simple o array) concuerda con el tipo de variable definido
        # Devuelvo el datatype

        dtype = None
        if var_def := env.get_var(n.name):
            if isinstance(var_def.dtype, SimpleType):
                dtype = var_def.dtype.name
            else:
                error(2, n.name)
        else:
            error(1, n.name)

        return dtype

    def visit(self, n: ArrayLocation, env: Symtab):
        # Buscar en Symtab y extraer datatype (No se encuentra?)
        # Devuelvo el datatype

        dtype = None
        if var_def := env.get_var(n.name):
            if isinstance(var_def.dtype, ArrayType):
                dtype = var_def.dtype.name
            else:
                error(3, n.name)
        else:
            error(1, n.name)

        return dtype

    def visit(self, n: TypeCast, env: Symtab):
        # Visitar la expresion asociada
        # Devolver datatype asociado al nodo

        n.expr.accept(self, env)
        dtype = n.name
        return dtype

    def visit(self, n: FuncCall, env: Symtab):
        # Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
        # Visitar la lista de Argumentos
        # Comparar el numero de argumentos con parametros
        # Comparar cada uno de los tipos de los argumentos con los parametros
        # Retornar el datatype de la funcion
        dtype = None
        if (fun := env.get_fun(n.name)) is not None:
            parms_num = len(fun.parmlist.parmlist) if fun.parmlist else 0
            args_num = len(n.arglist.arglist) if n.arglist else 0

            if parms_num != args_num:
                error(8, n.name, parms_num, args_num)
            else:
                all_matched = True
                for parm, arg in zip(fun.parmlist.parmlist, n.arglist.arglist):
                    parm_type = parm.dtype.name
                    arg_type = arg.accept(self, env)

                    if arg_type is not None:
                        if parm_type != arg_type:
                            error(9, name=n.name)
                            all_matched = False
                            break
                if all_matched:
                    dtype = fun.dtype
                    print(dtype)
        else:
            error(7, n.name)

        return dtype

    def visit(self, n: Binary, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        # Visitar el hijo derecho (devuelve datatype)
        # Comparar ambos tipo de datatype
        

        left_dtype = n.left.accept(self, env)
        right_dtype = n.right.accept(self, env)
        # Compara los tipos de datos si la parte izquierda y derecha no tienen errores
        dtype = check_binary_op(n.op, left_dtype, right_dtype)
        if left_dtype is not None and right_dtype is not None:
            # Si los tipos de datos son distintos lanza un error
            if dtype is None:
                error(5, name=n.op, value1=left_dtype, value2=right_dtype)

        return dtype

    def visit(self, n: Logical, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        # Visitar el hijo derecho (devuelve datatype)
        # Comparar ambos tipo de datatype
        

        left_dtype = n.left.accept(self, env)
        right_dtype = n.right.accept(self, env)
        dtype = check_binary_op(n.op, left_dtype, right_dtype)

        # Compara los tipos de datos si la parte izquierda y derecha no tienen errores
        if left_dtype is not None and right_dtype is not None:
            # Si los tipos de datos son distintos lanza un error
            if dtype is None:
                error(5, name=n.op, value1=left_dtype, value2=right_dtype)

        return dtype

    def visit(self, n: Unary, env: Symtab):
        # Visitar la expression asociada (devuelve datatype)
        # Comparar datatype

        fact_dtype = n.fact.accept(self, env)
        dtype = check_unary_op(n.op, fact_dtype)

        return dtype

    # Contenedores -----------------------------------------------
    def visit(self, n: ParmList, env: Symtab):
        # Visitar cada una de los parametros asociados
        for parm in n.parmlist:
            parm.accept(self, env)

    def visit(self, n: VarList, env: Symtab):
        # Visitar cada una de las variables asociadas
        for var in n.varlist:
            var.accept(self, env)

    def visit(self, n: StmtList, env: Symtab):
        # Visitar cada una de las instruciones asociadas
        for stmt in n.stmtlist:
            stmt.accept(self, env)

    def visit(self, n: ArgList, env: Symtab):
        # Visitar cada una de los argumentos asociados
        for arg in n.arglist:
            arg.accept(self, env)


def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test3/' + argv[1]).read()
    parser = Parser()
    nodo = parser.parse(lex.tokenize(txt))
    Checker.check(nodo)


if __name__ == '__main__':
    from sys import argv

    main(argv)
