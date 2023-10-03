# Implementación de un lexer para un compilador de PL0
## About
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
corresponde a todos los nombre de los test que están en **\test1**. No es necesario especificar la ruta relativa,
solo el nombre del test. 

### Dependencias
El programa depende de la librería *sly* para el análisis léxico y de la librería *prettytable* para la impresión
de los resultados en formato de tabla. Si desea instalar automaticamente las dependencias ejecute
`pip install -r requirements.txt`.

## Autores
* Alicia Valencia Acevedo
* Sebastián Velásquez Múnera

