# checker.py
import sys

from rich.console import Console

from plex import Lexer
from pparser import Parser
from AST import AST
from model import *
from typesys import *


def error(code: int, name: str = None, type1: str = None, type2: str = None):
    console = Console()
    if code == 1:
        console.print(f'[red]Type Error: variable {name} used but no defined.[/red]')
    elif code == 2:
        console.print(f'[red]Type Error: array variable {name} used without specifying an index.[/red]')
    elif code == 3:
        console.print(f'[red]Type Error: variable {name} has no indices because it was not defined as an array.[/red]')
    elif code == 4:
        console.print(f'[red]Type Error: expected {type1} in assignment of {name} but a {type2} was given.[/red]')

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
                super().__init__(f'In function "{env.context}": Parameter "{name}" has already been defined before')
            elif isinstance(env.entries[name], VarDefinition):
                super().__init__(f'In function "{env.context}": Variable "{name}" has already been defined before')
            elif isinstance(env.entries[name], FunDefinition):
                super().__init__(f'In function "{env.context}": Function "{name}" has already been defined before')


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

    def get(self, name):
        '''
        Recupera el símbolo con el nombre dado de la tabla de
        símbolos, recorriendo hacia arriba a traves de las tablas
        de símbolos principales si no se encuentra en la actual.
        '''
        if name in self.entries:
            return self.entries[name]
        elif self.parent:
            return self.parent.get(name)
        return None


class Checker(Visitor):

    @classmethod
    def check(cls, n: Node):
        vis = cls()
        n.accept(vis)

    def visit(self, n: Program):
        # Crear un nuevo contexto (Symtab global)
        # Visitar cada una de las declaraciones asociadas
        global_env = Symtab(context='Program')
        for func in n.funclist:
            func.accept(self, global_env)

    def visit(self, n: FunDefinition, env: Symtab):
        # Agregar el nombre de la funcion a Symtab
        # Crear un nuevo contexto (Symtab)
        # Visitar ParamList, VarList, StmtList
        # Determinar el datatype de la funcion (revisando instrucciones return)
        env.add(n.name, n)

        print(n, env.context, env.entries.keys())
        print('-' * 100)

        local_env = Symtab(context=n.name, parent=env)

        if n.parmlist:
            for parm in n.parmlist.parmlist:
                parm.accept(self, local_env)
        if n.varlist:
            for var in n.varlist.varlist:
                var.accept(self, local_env)
        for stmt in n.stmtlist.stmtlist:
            stmt.accept(self, local_env)

    def visit(self, n: Parameter, env: Symtab):
        # Agregar el nombre del parametro a Symtab
        env.add(n.name, n)
        print(n, env.context, env.entries.keys())
        print('-' * 100)

    def visit(self, n: VarDefinition, env: Symtab):
        # Agregar el nombre de la variable a Symtab
        env.add(n.name, n)
        print(n, env.context, env.entries.keys())
        print('-' * 100)

    # Declaraciones ------------------------------------------------------
    def visit(self, n: Print, env: Symtab):
        ...

    def visit(self, n: Write, env: Symtab):
        # Buscar la Variable en Symtab
        print(n, env.context, env.entries.keys())
        print('-' * 100)

    def visit(self, n: Read, env: Symtab):
        # Visitar la variable
        print(n, env.context, env.entries.keys())
        print('-' * 100)

    def visit(self, n: While, env: Symtab):
        # Visitar la condicion del While (Comprobar tipo bool)
        # Visitar las Stmts
        pass

    def visit(self, n: Break, env: Symtab):
        # Esta dentro de un While?
        pass

    def visit(self, n: IfStmt, env: Symtab):
        # Visitar la condicion del IfStmt (Comprobar tipo bool)
        # Visitar las Stmts del then y else
        pass

    def visit(self, n: Return, env: Symtab):
        # Visitar la expresion asociada
        # Actualizar el datatype de la funcion
        pass

    def visit(self, n: Skip, env: Symtab):
        ...

    def visit(self, n: Assign, env: Symtab):
        # Visitar el location (devuelve datatype) y marcar ese location como inicializado en VarDefinition
        # Visitar la expresión (devuelve datatype)
        # Comparar ambos tipo de datatype
        print(n, env.context, env.entries.keys())
        print('-' * 100)

        if (location_dtype := n.location.accept(self, env)) is not None:
            var_def = env.get(n.location.name)
            var_def.init.append(n.location)

        expr_dtype = n.expr.accept(self, env)

        if location_dtype != expr_dtype:
            error(4, name=n.location.name, type1=location_dtype, type2=expr_dtype)

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
        print(n, env.context, env.entries.keys())
        print('-' * 100)
        dtype = None
        if var_def := env.get(n.name):
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
        print(n, env.context, env.entries.keys())
        print('-' * 100)
        dtype = None
        if var_def := env.get(n.name):
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
        pass

    def visit(self, n: FuncCall, env: Symtab):
        # Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
        # Visitar la lista de Argumentos
        # Comparar el numero de argumentos con parametros
        # Comparar cada uno de los tipos de los argumentos con los parametros
        # Retornar el datatype de la funcion
        pass

    def visit(self, n: Binary, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        # Visitar el hijo derecho (devuelve datatype)
        # Comparar ambos tipo de datatype
        pass

    def visit(self, n: Logical, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        # Visitar el hijo derecho (devuelve datatype)
        # Comparar ambos tipo de datatype
        pass

    def visit(self, n: Unary, env: Symtab):
        # Visitar la expression asociada (devuelve datatype)
        # Comparar datatype
        pass

    # Contenedores -----------------------------------------------

    def visit(self, n: VarList, env: Symtab):
        # Visitar cada una de las variables asociadas
        pass

    def visit(self, n: ParmList, env: Symtab):
        # Visitar cada una de los parametros asociados
        pass

    def visit(self, n: ArgList, env: Symtab):
        # Visitar cada una de los argumentos asociados
        pass

    def visit(self, n: StmtList, env: Symtab):
        # Visitar cada una de las instruciones asociadas
        pass


def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test3/' + argv[1]).read()
    parser = Parser()
    nodo = parser.parse(lex.tokenize(txt))
    Checker.check(nodo)
    # semantico.visit(nodo, Tabla)


if __name__ == '__main__':
    from sys import argv

    main(argv)
