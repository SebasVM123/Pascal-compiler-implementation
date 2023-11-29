# COMPILADOR PL0
## Implementación de un lexer para un compilador de PL0
### About
### Tipos de errores o excepciones:
* Error 0 (por defecto): Caracter ilegal.
* Error 1: Ceros a la izquierda en enteros o flotantes.
* Error 2: Comentario sin cerrar.
* Error 3: Nombre de variable no valido (cuando empiezan con numeros).
* Error 4: String sin comilla de cierre.
* Error 5: Caracter de escape no válido (solo admite \\\", \n y \\\\).
* Error 6: Flotante sin parte entera.

### Manejo de entradas que deban ser ignoradas
El lexer ignora espacios en blanco (" \t") y carriage return. Además también ignora los saltos de línea.
Los comentarios deben ser ignorados pero de momento los acepta como tokens para que se puedan visualizar en la salida.
Comentarios sin cerrar no se aceptan como tokens.

### Salida
El programa imprimirá los errores en rojo siempre especificando la línea en la que se encuentra el error.
Luego imprimirá una tabla que mostrará cada token con su tipo, valor y línea.

### Ejecución
Para ejecutar el lexer use el siguiente comando en la terminal `python plex.py [testname].pl0` donde *testname*
corresponde a cada uno de los nombre de los test que están en **\test1**. No es necesario especificar la ruta relativa,
solo el nombre del test. 

## Implementación de un analizador sintáctico para un compilador de PLO
### About 
### Tipos de errores
Cuenta con un tipo de error en el que se puede ver en que linea se encuentra y lo que lo esta causando.

### Salida
Cuando el programa se ejecuta, verifica si hay errores en el código fuente. Si los hay, los muestra en la pantalla con un mensaje adecuado. Si no los hay, construye un árbol de sintaxis abstracta que representa la estructura del programa.

### Ejecución
Para ejecutar el parser use el siguiente comando en la terminal `python pparser.py [testname].pl0` donde *testname*
corresponde a cada uno de los nombres de los test que están en **\test2**. No es necesario especificar la ruta relativa,
solo el nombre del test.

## Implementación de un analizador semántico para un compilador de PL0
### About
### Tipos de errores
* Error 1: Uso de variable sin definir.
* Error 2: Vector sin index especificado.
* Error 3: Variable no  definida como vector es usada como si lo fuera.
* Error 4: Asignación incorrecta (Diferentes tipos).
* Error 5: Operación incorrecta (Diferentes tipos).
* Error 6: Break usado sin un while que lo anteceda.
* Error 7: Llamado a una función que no esta definida.
* Error 8: Numero incorrecto de argumentos al hacer el llamado a función.
* Error 9: Tipo de argumento incorrecto (Cuando se hace el llamado a función).
* Error 10: Función *main* no definida.
* Error 11: Tipo de index incorrecto.

### Salida
Cuando el programa se ejecuta, verifica si hay errores en el código fuente. Si los hay, los muestra en la pantalla con un mensaje adecuado. Si no los hay, construye una tabla de sintaxis.

### Ejecución
Para ejecutar el checker use el siguiente comando en la terminal `python checker.py [testname].pl0` donde *testname*
corresponde a cada uno de los nombre de los test que están en **\test3**. No es necesario especificar la ruta relativa,
solo el nombre del test.

## Implementación de un Generador de codigo intermedio para compilador de PL0
### Salida
Cuando el programa se ejecuta produce una secuencia de instrucciones de bajo nivel que equivalen al codigo fuente original. Estas instrucciones se muestran en la pantalla.

### Ejecución
Para ejecutar el generador de codigo intermedio use el siguiente comando en la terminal `python ir_code.py foldername/[testname].pl0` donde *foldername* corresponde a la carpeta en la que se encuentre el archivo y *testname*
corresponde al test que quiera probar.

### Dependencias
El programa depende de diferentes librerías para su ejecución un ejemplo de estas es *sly* para el análisis léxico y *prettytable* para la impresión
de los resultados en formato de tabla. Si desea instalar automaticamente las dependencias ejecute
`pip install -r requirements.txt`.

## Autores
* Alicia Valencia Acevedo
* Sebastián Velásquez Múnera 

