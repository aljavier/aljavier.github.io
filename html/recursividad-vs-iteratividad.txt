title: Recursividad versus iteratividad
date: 2013-11-01
tags: python, recursividad, time, iteratividad, fibonacci, factorial

Una `función recursiva` es aquella que se llama a sí mismo, normalmente, un número 
finito de veces. Por su lado, la `iteratividad` ejecuta unas determinadas acciones
un determinado numero de veces tambien, pero de forma secuencial.

El contraste esta cuando queremos ejecutar una determinada acción una cantidad de veces, que bien podríamos hacerlo con recursividad o iteratividad, aunque escoger la mejor opción es la interrogante aquí.

Cuando usamos recursividad estamos haciendo caso al método "divide y vencerás", ya que 
dividimos el problema en partes mas pequeñas para su resolución. Cuando se emplea una 
función recursiva básicamente se divide la función en dos partes: 1) `paso recursivo`, es la parte que hace la llamada recursiva, por tanto también se llama `llamada recursiva`, 2) `caso base` que igualmente podrían ser más de uno, es aquí cuando el método en verdad devuelve un resultado, por lo que se podría decir que es lo único que se resuelve en una función recursividad.

A continuación veremos un ejemplo de función recursiva para buscar el factorial de un número entero positivo. El factorial de un numero se define como

	n * (n-1) (n-2) * ... * 1

Teniendo en cuenta que 1! y 0! es igual a 1, primero presentaré la solución con una función iterativa:

	:::python
	#!/usr/bin/env python
	# Función factorial usando un método iterativo

	def factorial(n):
		retorno = 1
		for x in range(1,n+1):
			retorno *=x
		return retorno

	def main():
    		for x in range(11):
	    	print "%d! =  %d" % (x,factorial(x))

	if __name__ == "__main__":
		main()

Ahora veamos el método recursivo que en efecto produce el mismo resultado

	:::python
	#/usr/bin/env python
	# Factorial función recursiva

	def factorial(n):
		if n <= 1:
			return 1
		else:
			return n * factorial(n-1)

	def main():
		for x in range(11):
			print "%d! = %d" % (x, factorial(x))

	if __name__ == "__main__":
		main()

**En este caso n =< 1 es lo que llamamos `caso base` y `n * factorial(n-1)` es el `paso recursivo` o `llamada recursiva`.**

La secuencia de llamadas recursivas y retornos para el factorial de 5 va como se muestra en lo adelante.
<pre>	
	+----+		        +----+  valor final = 120
	| 5! |	            | 5! |
	+----+		        +-^--+
	  |                   |
	  |                   |
      V                   |       se devuelve 5! = 5 * 24 = 120
	 +-------+          +--------+
  	 | 5 * 4!|          | 5 * 4! |
	 +-------+          +-----^--+
	       | 		          |
	       |		          |
	       V	 	          |     se devuelve 4! = 4 * 6 = 24
	     +-------+      +---------+
	     | 4 * 3!|		| 4 * 3!  |
	     +-------+		+------^--+
		   | 		           |			
		   |		           |
		   V		           |   se devuelve 3! = 3 * 2 = 6
		+-------+	     +--------+
		| 3 * 2!|        | 3 * 2! |
		+-------+	     +-----^--+
		      |                |
		      |                |
		      V                |   se devuelve 2! = 2 * 1 = 2
		    +-------+         +--------+
		    | 2 * 1 |         | 2 * 1! |
		    +-------+         +-----^--+
			  |                     | 
			  |                     |
			  V                     |   se devuelve 1
			+------+             +-------+
			|  1   |             |   1   |
			+------+	         +-------+
   Secuencia de llamadas recursivas		Valores devueltos de cada llamada
</pre>

**Ojo, que la secuencia de las llamadas recursivas esta ilustrada de arriba para abajo y los valores devueltos de abajo para arriba.**

Ejecutamos ambos scripts (uno a uno claro) precedido por el comando `time` para medir el tiempo de ejecución de ambos scripts, time esta por defecto creo en todas las distros GNU/Linux - sí, supongo que usas Linux, no? no?.

	time python factorial.py

Debo decir, que estoy usando Python 2.7, veamos ahora la salida de ambos programas.

Función recursiva

	0! = 1
	1! = 1
	2! = 2
	3! = 6
	4! = 24
	5! = 120
	6! = 720
	7! = 5040
	8! = 40320
	9! = 362880
	10! = 3628800

	real	0m0.025s
	user	0m0.017s
	sys	    0m0.007s

Función iterativa

	0! =  1
	1! =  1
	2! =  2
	3! =  6
	4! =  24
	5! =  120
	6! =  720
	7! =  5040
	8! =  40320
	9! =  362880
	10! =  3628800

	real	0m0.027s
	user	0m0.020s
	sys	    0m0.003s

Como pueden ver la diferencia es muy poca, pero aún así las hay. Hay muchas cosas que se pueden decir al respecto ahora, pero mejor veamos otro ejemplo más.

Ahora será con la sucesión de fibonacci, veamos la función recursiva primero.

	#/usr/bin/env python
	# Función fibonacci recursiva

	def fibonacci(n):
		if n == 0 or n == 1:
			return n
		else:
			return fibonacci(n-1) + fibonacci(n-2)

	def main():
		for x in range(11):
			print "Fibonnaci de %d es %d" % (x, fibonacci(x))

	if __name__ == "__main__":
		main()

Aquí el `caso base` es n == 0 or n == 1, ya que es cuando sabemos con seguridad el valor que debemos devolver, el cual es el mismo parámetro.

Graficando el conjunto de llamadas sucesivas para fibonacci(3) tenemos:
<pre>
			      +---------------+
		          |	fibonacci(3)  |
			      +---------------+
				     |
				     |	
				     V
	      -----------------------^---------------------------
		return fibonacci(2)      +      fibonacci(1)
		      --------------           --------------
			     /                              \
			    /			                     \
               /                                  \
	------------------^------------------        -------------
         return fibonacci(1)  +  fibonacci(0)           return 1
                ------------     ------------          
		     |		                |
		     |                      |
		     |                      |
		-----^-----          -------^------
		 return 1	            return 0
</pre>
Más fácil de entender así no? 

Ahora veamos la salida de ambos programas, tanto el que tiene usa la función recursiva como el que usa la función iterativa.

Función recursiva

	Fibonnaci de 0 es 0
	Fibonnaci de 1 es 1
	Fibonnaci de 2 es 1
	Fibonnaci de 3 es 2
	Fibonnaci de 4 es 3
	Fibonnaci de 5 es 5
	Fibonnaci de 6 es 8
	Fibonnaci de 7 es 13
	Fibonnaci de 8 es 21
	Fibonnaci de 9 es 34
	Fibonnaci de 10 es 55

	real	0m0.028s
	user	0m0.023s
	sys	0m0.003s

Función iterativa
	Fibonacci de 0 es 0
	Fibonacci de 1 es 1
	Fibonacci de 2 es 1
	Fibonacci de 3 es 2
	Fibonacci de 4 es 3
	Fibonacci de 5 es 5
	Fibonacci de 6 es 8
	Fibonacci de 7 es 13
	Fibonacci de 8 es 21
	Fibonacci de 9 es 34
	Fibonacci de 10 es 55

	real	0m0.024s
	user	0m0.017s
	sys	0m0.003s

Ahh, pues ya tenemos dos ejemplos con los cuales poder ir haciendo conclusiones, como podemos ver en algunos casos la recursividad es más rápida y en otros casos la iteratividad es más rápida. Pero se puede ver claramente que el problema esta cuando hacemos demasiadas llamadas al mismo método, se consume mucha memoria, es el problema aquí con la función recursiva fibonacci, hacemos bastantes llamadas al mismo método, de hecho personas con más conocimientos que el wannabe que escribe esto aconsejan a no usar recursividad en casos así, porque se carga bastante el sistema. 

Así que donde se hacen bastante llamadas a un mismo método el resultado podría no ser muy óptimo, en otros casos si, por eso vemos que con el factorial el método recursivo es en efecto más rápido.

La recursividad así como la iteración se basan en una instrucción de control: la iteración utiliza una instrucción de repetición (for, while o do...while), mientras que la recursividad utiliza una instrucción de selección (if, if...else o switch), de modo que ambas implican repetición, sólo que difieren en el como lo hacen.

Del libro Java Como programar de Deitel nos aconsejan lo siguiente:

>Cualquier problema que se pueda resolver mediante la recursividad, se puede también mediante la iteración(sin recursividad). Por lo general, se prefiere un método recursivo a uno iterativo cuando el primero refleja con más naturalidad el problema, y se produce un programa más fácil de entender y de depurar. A menudo, puede implementarse un método recursivo con menos lineas de código. Otra razón por la que es preferible elegir un método recursivo es que uno iterativo podría no ser aparente.

>Evite usar la recursividad en situaciones en las que se requiera un alto rendimiento. Las llamadas recursivas requieren tiempo y consumen memoria adicional.

Dicho esos sabios consejos, podemos sacar de ahí que un método recursivo implica bien menos código pero a veces no es aconsejable por cuestiones de rendimiento, aunque ahí dice que podría ser además más obvio y legible yo diría que más podaría confundir a veces, pero bueno básicamente es saber donde utilizarlos son muy buenos recursos, solo toca analizar bien, porque si nos afecta bastante el rendimiento pues usar un método iterativo es la mejor opción.

Un último ejemplo, usamos una función recursiva y una iterativa en diferentes programas, para calcular la potencia de un número.

Primero veamos la solución iterativa:

	:::python
	#!/usr/bin/env python
	# Exponenciacion iterativo

	def exponenciacion(base, exponente):
		retorno = base
		for x in range(exponente-1):
			retorno = retorno*base
		return retorno

	def main():
		for x in range(1,10):
			for z in range(1,10):
				print "%{0}^%{1} = %{2}".format(x, z, exponenciacion(x, z))
			print ""

	if __name__ == "__main__":
		main()

Fácil, ahora veamos la solución recursiva:

	:::python
	#!/usr/bin/env python
	# Exponenciacion recursivo

	def exponenciacion(base, exponente):
		if exponente == 1:
			return base
		else:
			return base * exponenciacion(base, exponente-1)

	def main():
		for x in range(1,10):
			for z in range(1,10):
				print "%{0}^%{1} = %{2}".format(x, z, exponenciacion(x, z))
			print ""

	if __name__ == "__main__":
		main()

Ahora es el momento de ver el tiempo de ejecución de ambos, la salida del comando `time`, no mostraré la salida de los programas porque es algo amplía como se puede deducir del código.

Tiempo ejecución función recursiva:

	real	0m0.025s
	user	0m0.020s
	sys	0m0.003s

Tiempo ejecución función iterativa:

	real	0m0.027s
	user	0m0.020s
	sys	0m0.003s

Nuevamente aquí la recursividad ganó en cuanto a rapidez, por la misma razón que antes, no tiene muchas llamadas al mismo método, en casos así funciona fluido. El marcador final en cuando a rapidez: recursividad 2 - iteratividad 1!



