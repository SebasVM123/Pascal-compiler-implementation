# checker.py
'''
Revision de Variables

Recorre el AST para determinar el alcance adecuado para cada simbol.

TODO: Podría agregar más manejo de errores.  Mejor manejo de mensajes de error.

En este proyecto necesita realizar comprobaciones semánticas en su programa.
Este problema es multifacético y complicado. Para que el cerebro no explote un poco menos, debes tomarlo con calma y en porciones pequeñas.
La esencia básica de lo que debe hacer es la siguiente:

1. Nombres y Simbolos:

    Todos los identificadores deben ser definidos antes de que ellos sean usados. Esto incluye variables, constantes y nombres de tipo. Pro ejemplo, esta clase de codigo genera un error:

        fun main()
        begin
            a := 3    /* Error. 'a' no definida.
        end

2. Tipos de literales y constantes

    Todos los símbolos literales se escriben implícitamente y se les debe asignar un tipo de "int" o "float". Este tipo se utiliza para establecer el tipo de constantes. Por ejemplo:

        fun main()
            const a = 42;         // Tipo "int"
            const b = 4.2;        // Tipo "float"
        begin
            skip
        end

3. Comprobar el tipo del operador

    Los operadores binarios sólo operan con operandos de un tipo compatible.
    De lo contrario, obtendrá un error de tipo. Por ejemplo:

        fun main()
            a : int;
            b : float;
            c : int;
            d : int;
            e : int;
        begin
            a := 2;
            b := 3.14;
            c := a + 3;    // OK
            d := a + b;    // Error.  int + float
            e := b + 4.5;  // Error.  int = float
        end

    Además, debe asegurarse de que solo se permitan operadores compatibles.

4.  Asignacion.

    Los lados izquierdo y derecho de una operación de asignación deben declararse como del mismo tipo.

        fun main()
            a : int;
        begin
            a = 4 + 5;     // OK
            a = 4.5;       // Error. int = float
        end

    Los valores sólo se pueden asignar a declaraciones de variables, no a constantes.

        fun main()
            a : int;
            const b = 42;
        begin
            a := 37;        // OK
            b := 37;        // Error. b is const
        end

Estrategia de implementacion:
------------------------
Utilizará la clase `Visitor` definida en pl0/model.py para recorrer el árbol de análisis. Definirá varios métodos para diferentes tipos de nodos AST. Por ejemplo, si tienes un nodo Binary, escribirás un método como este:

    def visit(self, n:Binary):
        ...

Para comenzar, haga que cada método simplemente imprima un mensaje:

    def visit(self, n:Binary):
        print('visit:', n)
        n.left.accept(self)
        n.right.accept(self)

Esto al menos le indicará que el método se está activando. Pruebe algunos ejemplos de código simples y asegúrese de que todos sus métodos se estén ejecutando realmente cuando recorra el árbol de análisis.

Pruebas
-------
Los archivos test3/*.pl0 contienen diferentes cosas que debes verificar. Se dan instrucciones específicas en cada archivo de prueba.

Consejos generales
------------------
Lo principal en lo que debe pensar al verificar es en la corrección del programa. ¿Tiene sentido esta declaración u operación que está viendo en el árbol de análisis? De lo contrario, es necesario generar algún tipo de error. Utilice sus propias experiencias como programador como guía (piense en lo que causaría un error en su lenguaje de programación favorito).

Un desafío será la gestión de muchos detalles complicados.
Tienes que realizar un seguimiento de símbolos, tipos y diferentes tipos de capacidades.
No siempre está claro cómo organizar mejor todo eso. Por lo tanto, espere andar un poco a tientas al principio.


::: AST :::
    |
    +-- Node
            |
            +-- DataType
            |   |
            |   +-- SimpleType : 'int', 'float'
            |   |
            |   +-- ArrayType : 'int[]', 'float[]'
            |
            +-- Expression
            |   |
            |   +-- Literal
            |   |   |
            |   |   +-- Integer : 12, 34, 23
            |   |   |
            |   |   +-- Float : 3.14, 1.618
            |   |
            |   +-- Location
            |   |   |
            |   |   +-- SimpleLocation : 'a', 'b', 'casa',
            |   |   |
            |   |   +-- ArrayLocation
            |   |
            |   +-- TypeCast
            |   |
            |   +-- Assign
            |   |
            |   +-- FuncCall
            |   |
            |   +-- Binary
            |   |
            |   +-- Logical
            |   |
            |   +-- Unary
            |
            +-- Statement
                    |
                    +-- Declaration
                    |   |
                    |   +-- FuncDefinition
                    |   |
                    |   +-- VarDefinition
                    |   |
                    |   +-- Parameter
                    |
                    +-- Print
                    |
                    +-- Write
                    |
                    +-- Read
                    |
                    +-- While
                    |
                    +-- Break
                    |
                    +-- IfStmt
                    |
                    +-- Return
                    |
                    +-- Skip
                    |
                    +-- Program
                    |
                    +-- StmtList
                    |
                    +-- VarList
                    |
                    +-- ParmList
                    |
                    +-- ArgList

'''
#checker.py
from model import *
from plex import Lexer
from pparser import Parser
from rich import print
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
        pass

    def __init__(self, parent=None):
        '''
        Crea una tabla de símbolos vacia con la tabla de
        simbolos padre dada.
        '''
        self.entries = {}
        self.parent = parent
        if self.parent:
            self.parent.children.append(self)
        self.children = []

    def add(self, name, value):
        '''
        Agrega un simbol con el valor dado a la tabla de simbolos.
        El valor suele ser un nodo AST que representa la declaración
        o definición de una función, variable (por ejemplo, Declaración
        o FuncDeclaration)
        '''
        if name in self.entries:
            raise Symtab.SymbolDefinedError()
        self.entries[name] = value

    def get(self, name):
        '''
        Recupera el símbol con el nombre dado de la tabla de
        simbol, recorriendo hacia arriba a traves de las tablas
        de simbol principales si no se encuentra en la actual.
        '''
        if name in self.entries:
            return self.entries[name]
        elif self.parent:
            return self.parent.get(name)
        return None
    
    def current_func(self):
        if self.parent:
            return list(self.parent.entries.keys())[0]
        else:
            return None
    
@dataclass
class Integer(Literal):
    value : int
    type : DataType = field(default_factory=SimpleType('int'))

@dataclass
class Float(Literal):
    value : float
    type : DataType = field(default_factory=SimpleType('float'))
    

@dataclass
class SimpleLocation(Location):
    name: str
    dtype : DataType = field(init=False)

class Checker(Visitor):
    loop_stack=[]
    def visit(self, n: Literal, env: Symtab):
        # Devolver datatype
        return n.dtype.name
    def visit(self, n: Location, env: Symtab):
        # Buscar en Symtab y extraer datatype (No se encuentra?)
        # Devuelvo el datatype
        if env.get(n.name):
            return env.get(n.name).datatype.name
        else:
            print("Error location")
    
    def visit(self, n: TypeCast, env: Symtab):
        # Visitar la expresion asociada
        # Devolver datatype asociado al nodo
        self.visit(n.expr,env)
        return n.name
    def visit(self, n: Assign, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        # Visitar el hijo derecho (devuelve datatype)
        # Comparar ambos tipo de datatype
        Left=self.visit(n.location,env)
        Right=self.visit(n.expr,env)
        if Left == Right:
            return Left
        else:
            print("Error assign")
            return None
    
    def visit(self, n: FuncCall, env: Symtab):
        # Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
        # Visitar la lista de Argumentos
        # Comparar el numero de argumentos con parametros
        # Comparar cada uno de los tipos de los argumentos con los parametros
        # Retornar el datatype de la funcion   
        datatype=env.get(n.name).dtype
        if env.get(n.name):
            pass
        self.visit(n.arglist,env)
        if len(n.arglist.arglist) == len(env.get(n.name).parmlist.parmlist):
            pass
        else:
            print("error funcall")
        return datatype

    def visit(self, n: Binary, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        # Visitar el hijo derecho (devuelve datatype)
        # Comparar ambos tipo de datatype
        TLeft=self.visit(n.left,env)
        TRight=self.visit(n.right,env)
        if TLeft == TRight:
            return TLeft
        else:
            print("Error Binary")
            
    def visit(self, n: Logical, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        # Visitar el hijo derecho (devuelve datatype)
        # Comparar ambos tipo de datatype
        TLeft=self.visit(n.left,env)
        TRight=self.visit(n.right,env)
        if TLeft == TRight:
            return bool
        else:
            print("error logical",n.left,TRight)

    def visit(self, n: Unary, env: Symtab):
        # Visitar la expression asociada (devuelve datatype)
        # Comparar datatype
        datatype= self.visit(n.fact, env)
        return datatype
        
    def visit(self, n: FunDefinition, env: Symtab):
        # Agregar el nombre de la funcion a Symtab
        # Crear un nuevo contexto (Symtab)
        # Visitar ParamList, VarList, StmtList
        # Determinar el datatype de la funcion (revisando instrucciones return)
        env.add(n.name,FunDefinition(name=n.name,parmlist=n.parmlist,varlist=n.varlist,stmtlist=n.stmtlist))
        env.get(n.name).dtype: DataType = field(init=False)
        TFunc=Symtab(env)
        if n.parmlist:
            for parm in n.parmlist.parmlist:
                self.visit(parm,TFunc)
        if n.varlist:
            for var in n.varlist.varlist:
                self.visit(var,TFunc)
        for stmt in n.stmtlist.stmtlist:
            self.visit(stmt,TFunc)
            if isinstance(stmt,Return):
                env.get(n.name).dtype = self.visit(stmt,TFunc)
        
    def visit(self, n: VarDefinition, env: Symtab):
        # Agregar el nombre de la variable a Symtab
        env.add(n.name,VarDefinition(name=n.name,datatype=n.datatype))

    def visit(self, n: Parameter, env: Symtab):
        # Agregar el nombre del parametro a Symtab
        env.add(n.name,Parameter(name=n.name,datatype=n.datatype))
     
        
    def visit(self, n: Print, env: Symtab):
        ...		

    def visit(self, n: Write, env: Symtab):
        # Buscar la Variable en Symtab
        if env.get(n.expr.name):
            pass
        else: 
            print("error en write")  
        
    def visit(self, n: Read, env: Symtab):
        # Buscar la Variable en Symtab
        if env.get(n.location.name):
            ...
        else:
            print("Error en read")
   
        
    def visit(self, n: While, env: Symtab):
        # Visitar la condicion del While (Comprobar tipo bool)
        # Visitar las Stmts
        self.visit(n.relation,env)
        self.loop_stack.append("while")
        self.visit(n.stmt,env)
        self.loop_stack.pop()
    
    def visit(self, n: Break, env: Symtab):
        # Esta dentro de un While?
        if "while" in self.loop_stack:
            pass
        else:
            print("Error: Break fuera de un bucle while.")
     
    def visit(self, n: IfStmt, env: Symtab):
        # Visitar la condicion del IfStmt (Comprobar tipo bool)
        # Visitar las Stmts del then y else
        if self.visit(n.relation,env) == bool:
            return bool
        else:
            print("Error no bool")
        self.visit(n.thenstmt,env)
        if n.elsestmt:
            self.visit(n.elsestmt,env)
    
    def visit(self, n: Return, env: Symtab):
        # Visitar la expresion asociada
        # Actualizar el datatype de la funcion
        # Obtener el tipo de la expresión asociada
        datatype = self.visit(n.value, env)
        # Actualizar el datatype de la función
        name = env.current_func()
        env.get(name).dtype = datatype
        return datatype  # Agregamos el retorno del tipo
        
    def visit(self, n: Skip, env: Symtab):
        ...

    def visit(self, n: Program, env: Symtab):
        # Crear un nuevo contexto (Symtab global)
        # Visitar cada una de las declaraciones asociadas        
        EnvProgram=Symtab()
        for func in n.funclist:
            self.visit(func,EnvProgram)
        if 'main' in list(EnvProgram.entries.keys()):
            pass
        else:
            print("No tiene main")
            
    def visit(self, n: StmtList, env: Symtab):
        # Visitar cada una de las instruciones asociadas
        for stmt in n.stmtlist:
            self.visit(stmt,env)
    def visit(self, n: VarList, env: Symtab):
        # Visitar cada una de las variables asociadas
        for var in n.varlist:
            self.visit(var,env)
    def visit(self, n: ParmList, env: Symtab):
        # Visitar cada una de los parametros asociados
        for parm in n.parmlist:
            self.visit(parm,env)
    def visit(self, n: ArgList, env: Symtab):
        # Visitar cada una de los argumentos asociados
        for arg in n.arglist:
            self.visit(arg,env)
  
def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    lex = Lexer()
    txt = open('test3/errors/' + argv[1]).read()
    parser = Parser()
    Nodo = parser.parse(lex.tokenize(txt))
    semantico=Checker()
    Tabla= Symtab()
    semantico.visit(Nodo,Tabla)



if __name__ == '__main__':
    from sys import argv
    main(argv)
