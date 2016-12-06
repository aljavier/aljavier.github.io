title: Redirecciones y expansiones en bash
tags: bash, shell, scripting
slug: bash-redirecciones-y-expansiones
date: 2013-06-10

Veremos algo bien breve y sencillo para muchos, pero además muy importante principalmente a la hora de escribir bash scripts. Hablamos de las redirecciones, las expansiones aritméticas y las expansiones de llaves.

Redirecciones
-------------

A la hora de escribir un script en bash la mayoría de veces necesitaremos usar estas, al menos para redireccionar los posibles errores que pueda lanzar una determinada expresión.

Como muchos ya saben en Linux todo es un archivo, es así que la <a href="http://es.wikipedia.org/wiki/Entrada_est%C3%A1ndar" target="_blank">Entrada y Salida estándar</a>&nbsp; son los archivos que se encuentran en /dev/stdin y dev/sdout respectivamente. Pero también tenemos el archivo stderr en /dev/stderr, pero estos además tienen un <a href="http://es.wikipedia.org/wiki/Descriptor_de_archivo" target="_blank">descriptor de archivo</a> (un numero) que nos permite referirnos a estos de ese modo. Sus descriptores son como sigue:</div>

   | Valor entero | Nombre                  |
   |--------------|-------------------------|
   |      0       | Entrada estándar(stdin) |
   |      1       | Salida estándar(stdout) |
   |      2       | Error estándar(stderr)  |


Normalmente si queremos redireccionar la salida de un comando, los cuales usan la salida estándar por defecto, a un archivo por ejemplo, es tan simple como hacer esto:
	
	ls -l /usr/bin > programas.txt

Ese es su uso mas simple, claro la salida estándar también podría redirigirse a otro comando usando [tuberia](http://es.tldp.org/COMO-INSFLUG/COMOs/Bash-Prog-Intro-COMO/Bash-Prog-Intro-COMO-4.html "tuberías bash")

Los operadores que usamos en redirecciones son los siguientes:

   | Operador      |   Descripción    
   |---------------|--------------------------------------------------------------------------------------------------------------------------------|
   |     >         | Redirecciona la salida al archivo que le sigue, si no existe se crea y si existe se sobre escribe.                             |
   |     >>        | Igual que al anterior con la excepción de que este añade la salida al final del archivo, es decir, no lo sobreescribe.         |
   |     2>&1      | Redirecciona la salida estándar y error estándar si hay alguno, del comando o programa al mismo archivo.(Este es mas bien  una combinación de operadores, no un operador en si).   |                                                                          |
   |     &>        | Lo mismo que el anterior, pero este funciona en versiones mas recientes, no en versiones muy viejas.(Este es mas bien una  combinación de operadores, no un operador en si)                                                                              .|

*Nota: Reconozco que lo anterior esta pobre-mente explicado y deja muchas cosas de lado, por eso recomiendo leer [en este link](http://0x945.wordpress.com/2011/05/01/bash-operadores-de-redireccion/) al respecto.

Algunas cosas de lo que vemos en esa tabla podría no quedar claro sin un ejemplo, así que veamos algunos ejemplos básicos: 

	 ls -l /usr/bin /usr/local/bin | uniq > programas.txt

Ahora se nos ha creado un archivo llamado programas.txt con una lista de los programas instalados en el sistema (claro exceptuando los que puedan haber en /opt).

	ls /opt >> programas.txt 

Ahora también se nos agrego al archivo los programas instalados en /opt.

	ls /etc/bin > lista.txt 2>&1

He puesto /etc/bin a sabiendas de que no existe, lo que hace lo de arriba es lo siguiente: Primero redirecciona la salida del comando ls a lista.txt, si se produce algún error(observa el 2, identificador de stderr) lo redirecciona a la salida estándar nuevamente, el cual ya ha sido redireccionado al archivo, de modo que, tanto si el comando es exitoso como si se produce un error se enviara al archivo.txt.

El orden es importante, si se cambia el orden de las redirecciones en este caso (el de este ejemplo), no funcionaria.

En la mayoría de los sistemas mas recientes (o en todos) podríamos hacer lo anterior con &> del siguiente modo:

	ls /etc/bin &> lista.txt

Sin duda, es mas sutil la ultima forma.

Pero lo mas usado según yo es redirigir la salida de errores que se puedan producir en un programa, comando o script a [/dev/null](http://es.wikipedia.org/wiki//dev/null). Este archivo es el black hole de Linux, es la nada, todo lo que va ahí simplemente se pierde.

Veamos el siguiente ejemplo:

	tar jcvf logs.tar.bz2  /var/log/messages 2> /dev/null

Ese tipo de uso es bastante común y útil, lo que hacemos ahí es redireccionar la salida de errores (observar el 2) a /dev/null, así no veríamos errores ni seria interrumpido el script por posibles salida de errores.

Expansiones aritméticas
------------------------

Esto es muy interesante y es bastante simple también, esto nos permite ejecutar operaciones aritméticas en la terminal! El formato es:
	
	$((expresion))

Los operadores aritméticos:

   | Operador |      Descripción     |
   |----------|----------------------|
   |    +     |          Suma        |
   |    -     |          Resta       |
   |    *     |   Multiplicación     |
   |    /     |   División           |
   |    %     |   Modulo o Resto     |
   |   **     |   Exponenciación     |

*Nota: Cabe aclarar que las expresiones aritméticas solo trabajan con números enteros, así que estos serán redondeados automáticamente 
aquí. Por ejemplo, si divides 7 entre 2, obtendra como resultado solo 3 y no la parte decimal.*

**Algunos ejemplos básicos:**

	[stallman@linux ~]$ echo "Suma de 5 + 4 = " $((5+4))
	Suma de 5 + 4 =  9

	[stallman@linux ~]$ echo "50 - 10 es " $((50 - 10))
	50 - 10 es  40

	[stallman@linux ~]$ echo "5 x 5 = " $((5*5))
	5 x 5 =  25

	[stallman@linux ~]$ echo "7 / 2 es "$((7/2))
	7 / 2 es 3

	[stallman@linux ~]$ echo "Resto de 7 / 2 es "$((7%2))
	Resto de 7 / 2 es 1

	[stallman@linux ~]$ echo "10^10 es: " $((10**10))
	10^10 es:  10000000000

Cabe decir, que el espacio que se pueda dejar entre la expresión no es relevante, es decir, $((2*2)) y $((2 * 2)) es igual, no da error ni resultados desiguales.

**Estas también soportan expresiones anidadas:**

	[stallman@linux ~]$ echo "(5+4)*10 = "$(($((5+4))*10))
	(5+4)*10 =  90

También se podría usar paréntesis simples (no dobles) cuando usemos subexpresiones como aquí, ejemplo:

	[stallman@linux ~]$ echo "5 + 4 * 10 = " $(((5+4)*10))
	5 + 4 * 10 = 90

Como ven ahí no tuvimos que usar en la subexpresion dobles paréntesis ni el signo de dolar $.

Expansiones de llaves
---------------------

Con estas puedes crear varios archivos por ejemplo, mejor veamos como funcionan luego podrán darles los usos que quieran.

Digamos que quieren imprimir todas las posibles combinaciones de dos palabras en el abecedario, entonces haríamos lo siguiente:

	echo {A..Z}{A..Z}

Entonces echo imprimirá todas las combinaciones de dos letras en el abecedario, haganlo en su terminal y verán el resultado, no lo pongo aquí porque es algo extenso.

Entonces ya tenemos una idea de como funciona, mas o menos funciona así {element1, elemento2, elemento3...elemtoN} es decir todos los elementos que quieren, también se puede con {A..Z} esto es desde A hasta Z, {a..z} igual que la anterior pero minúsculas, {0..9} si como lo has pensado, los números del 0 al 9, también puedes intercambiarlos: {Z..A}, {z..a} y {9..0}, etc., en fin, rangos.

Supongamos que tenemos una cámara de videovigilancia de la cual guardamos las grabaciones por mes, supongamos que queremos hacer directorios para guardar todas las grabaciones del año 2012, haríamos así:

	[stallman@linux ~]$ mkdir grabacion_2012-0{1..9} grabacion_2012-{10..12}


Y listo se ahorraron hacer todas esos directorios uno a uno.

Estas también permiten expresiones anidadas, ejemplo:

	[stallman@linux ~]$ echo a{A{0..9},B{A..Z}}z

Eso es todo por ahora, pueden profundizar en ese tema en el manual de bash.

Un saludo!

