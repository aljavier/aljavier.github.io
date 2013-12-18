title: Shadow passwords en Linux, ataque de diccionario con Python
tags: Linux, python, crypt, security
date:2013-12-18

Hace unos meses ya, leyendo el libro de Violent Python había un script
que alguien usó una vez para hackear una maquina Unix, haciendo un ataque
de diccionario para averiguar la password del archivo /etc/passwd, cuando
eso no usaban el ya famoso /etc/shadow.

El autor dejó como un reto al lector el actualizar el script para funcionar
con el actual formato de los sistemas Linux. En aquel entonces del script original
me parece que para el cifrado de las passwords usaban MD5, era por mucho mas fácil de
hacer un ataque de diccionario, ahora es un poco mas enredado, pero igual posible,
suponiendo que tienes acceso al archivo /etc/shadow o aun mejor a una copia de este.

Claro como ha de saberse, los ataques por diccionarios desesperan, esto siempre dependerá
del tipo de password usadas y demás. En todo caso, la idea era pasarla bien escribiendo
ese script en Python.

Según lo que nos interesa, veamos lo siguiente (si quieres entender mejor el fichero
shadow, mirate este [link](https://encrypted.google.com/search?hl=en&q=entendiendo%20%2Fetc%2Fshadow "Entendiendo /etc/shadow")):
<pre>
jota:$6$62vNvZQgN$RcwvBFj7NV9hNGXR3/1Gtb3Fd0HMN1:15951:0:99999:7:::
 |    |                 |
user id              hashed                       
</pre>


Volviendo a lo anterior, primero tenemos el *user*, luego de los dos puntos el hash, nuestra password
cifrada, pero los 3 primeros dígitos indican el tipo de hash con el que ha sido
cifrada.

Para entenderlo mejor, Wikipedia lo pone como sigue:

	$id$salt$hashed

En donde el id debe interpretarse  como sigue:

| id          |  algoritmo     |
|:------------|---------------:|
| $1$         | MD5            |
| $2$         | Blowfish       |
| $5$         | SHA-256        |
| $6$         | SHA-512        |

Si donde debería salir el $id$salt$hashed, es decir luego de `user:`, tenemos un "NP" significa
que no tiene password el user, si tiene un "!" significa que la cuenta esta bloqueada, si es "!!"
 quiere decir que la cuenta ha expirado.

Lo del *salt*, seguro es mas entendible leyendo lo que dice la wikipedia:

>>En criptografía, la sal comprende bits aleatorios que son usados como una de las entradas en una función derivadora de claves. La otra entrada es habitualmente una contraseña. La salida de la función derivadora de claves se almacena como la versión cifrada de la contraseña. La sal puede también ser usada como parte de una clave en un cifrado u otro algoritmo criptográfico. La función de derivación de claves generalmente usa una función hash. A veces el vector de inicialización, un valor generado previamente, es usado como sal.

Aclarando que "salt" en ingles es "sal" en español. Bien dicho eso, como ven, para generar los cifrados en el shadow,
se usa un salt como entrada aleatoria de datos para generar el hash, y la password como tal.

En python esto lo hacemos usando la librería crypt. Si tomas el hash mas el id como segundo parámetro y como primer parámetro una password en texto plano,
si la password en texto plano es la cifrada entonces el hash sera igual que el segundo parámetro de la función crypt.

Vamos a verlo de forma mas practica. Primera tenemos a un nuevo user llamado prueba:

	prueba:$6$kI8uI0MW$oj1B1xFlB35KuJY11ckxPCcU42K31hV7JFrsF/7dm1nbFDngu8.iJidAiAuxVmchDkIGEPY8WKrU/bctla3a1.:16057:0:99999:7:::

Por tanto de ahí tenemos que su hash mas el id del hash es el siguiente:

	$6$kI8uI0MW$oj1B1xFlB35KuJY11ckxPCcU42K31hV7JFrsF/7dm1nbFDngu8.iJidAiAuxVmchDkIGEPY8WKrU/bctla3a1.

Para ser mas explícito, el id es `$6$` y el la password cifrada (el hashed) es:

	kI8uI0MW$oj1B1xFlB35KuJY11ckxPCcU42K31hV7JFrsF/7dm1nbFDngu8.iJidAiAuxVmchDkIGEPY8WKrU/bctla3a1.

Usando la librería crypt de python y llamando al método crypt, podemos comprobar o intentar adivinar cual es la password, del siguiente modo:

	:::python
	crypt.crypt(palabra, id+salt)

Así que veamos cual es la password:

	:::python
	 crypt.crypt("passw0rd", "$6$kI8uI0MW$oj1B1xFlB35KuJY11ckxPCcU42K31hV7JFrsF/7dm1nbFDngu8.iJidAiAuxVmchDkIGEPY8WKrU/bctla3a1.")

Eso nos devuelve lo siguiente:

	'$6$kI8uI0MW$vrAM1PcLjFpMccU2OcVKnaWpZUYyZJax84o6KWoehvEpyP6/CHtZAfZifEtVPFXBZbCwArVhLjAtF9xHg98ko/'

Claramente es distinto al hash que pasamos como segundo parámetro, por tanto, "passw0rd", no es la
password cifrada aquí. Pero si ahora probamos del siguiente modo:

	:::python
	 crypt.crypt("123456789","$6$kI8uI0MW$oj1B1xFlB35KuJY11ckxPCcU42K31hV7JFrsF/7dm1nbFDngu8.iJidAiAuxVmchDkIGEPY8WKrU/bctla3a1.")

Nos devuelve como resultado:

	$6$kI8uI0MW$oj1B1xFlB35KuJY11ckxPCcU42K31hV7JFrsF/7dm1nbFDngu8.iJidAiAuxVmchDkIGEPY8WKrU/bctla3a1.

Es el mismo hash! Por lo tanto, 123456789, es la password real.


Así que hemos podido ver como generar el tipo de password que usa Linux para el /etc/shadow y así poder realizar
un ataque de diccionario. Claro, igualmente podemos usar esto para generar passwords más seguras en nuestras aplicaciones
tal como hace Linux con el /etc/shadow, es cuestión de tener en cuenta que el id es el tipo de cifrado, el salt es una palabra 
aleatoria. De eso modo la función crypt te devolvería un hash usando el cifrado que sea, según el id que pusiste. 
Por cierto, crypt no soporta Blowfish ($2$).

Ahora luego de esa leve explicación, les comparte el script completo que como dije antes habría hecho como upgrade
al que tiene el libro Violent Python que era para sistemas unix viejos. Pero les dejare el link en github, no lo pegare aquí porque es un poco extenso, no mucho pero algo.

Link a mi script [Unix Password Cracker](https://github.com/aljavier/violent-python-stuff/tree/master/UnixPasswordCracker "Unix Password Cracker") en github.

En verdad no es ningún cracker de passwords, ya que no es en el sentido estricto de la palabra ataque por fuerza bruta pura, sino simplemente ataque por diccionario, pero se ve mejor el nombre así :|

**Más información**

+ [Ataque de diccionario](https://es.wikipedia.org/wiki/Ataque_de_diccionario "Ataque de diccionario")
+ [Explicación sobre salt](https://es.wikipedia.org/wiki/Sal_(criptograf%C3%ADa) "salt")
+ [Librería crypt de python](http://docs.python.org/2/library/crypt.html "crypt")

También tienen mas info en el man de crypt si usas Linux: `man 3 crypt`. 
