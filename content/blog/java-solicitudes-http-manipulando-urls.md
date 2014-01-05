title: Manipulando URLs y haciendo solicitudes HTTP con Java
tags: java, URL, networking, HTTP
date: 2014-01-03


Interactuar con formularios web desde una que otra aplicación que yo mismo
programe siempre me ha parecido bastante interesante y en efecto es algo que 
que uso de vez en vez, más con el lenguaje Python que con cualquier otro, pero se da que en
uno que otro caso pueda ser interesante usar Java para estas cosas, quizás porque
quiero hacer algo parecido en alguna aplicación que por una u otra razón haya
decidido programar en Java. 

En esta entrada vamos a usar las clases [URLConnection](http://docs.oracle.com/javase/6/docs/api/java/net/URLConnection.html "URLConnection")
y [HttpURLConnection](http://docs.oracle.com/javase/6/docs/api/java/net/HttpURLConnection.html "HttpURLConnection") 
para interactuar con formularios web y para acceder y manipular URLs, para definir
una [URL](https://es.wikipedia.org/wiki/Uniform_Resource_Locator "Uniform Resource Locator")
en Java usamos la clase [URL](http://docs.oracle.com/javase/7/docs/api/java/net/URL.html "java.net.URL") 
lo cual por igual tiene algunos métodos que podrían ser útiles y pueden ser consultados
en la documentación oficial. 

Por otro lado, las clases URLConnection y HttpURLConnection no tienen mucha diferencia
entre si y básicamente se podría usar cualquiera si la vamos a usar para el protocolo
http, ya que URLConnection es una clase muy HTTP-céntrica como dice la documentación
oficial, la misma es útil para establecer un enlace de comunicación entre una aplicación
y una URL, que bien podría ser una de un ftp, servidor de archivos u otra. En cambio, 
HttpURLConnection es una subclase directa de URLConnection para establecer conexiones
con un servidor web, que no es lo mismo que ftp u otro.

Entrando en materia iniciamos con lo mas básico, la URL. Para crear una _URL absoluta_
es tan simple como esto:

	:::java
	URL myURL = new URL("http://example.com/");

La URL podría ser cualquiera, sin importar si apunta a un recurso en el servidor, como
lo seria `http://example.com/pdf/java-book.pdf`. Ahora crear URLs relativas a una URL base
como seria: http://example.com/pages/, lo haríamos del siguiente modo:

	:::java
	URL baseURL = new URL("http://example.com/pages/");
	URL page1URL = new URL(baseURL, "page1.html");
	URL page2URL = new URL(baseURL, "page2.html");

La forma general de este `constructor` es como sigue:

	::java
	URL(URL baseURL, String relativeURL);

El resultado es obvio, ahora bien si el primer parámetro(URL base) es `null` el segundo
parámetro(URL relativa) sera tratada como una URL absoluta. Si por otro lado, haya o no
un primer elemento valido y el segundo es una URL absoluta entonces el constructor ignorará
el primer argumento(URL base).

Igual podríamos hacer lo siguiente:

	:::java
	URL page1BottomURL = new URL(page1URL, "#BOTTOM");

Así tendríamos un objeto URL apuntando específicamente al contenido en `http://example.com/pages/page1.hyml#BOTTOM`.

Existen como dos constructores más, que pueden consultarse en la documentación
oficial, en todo caso los aquí presentados me parecen los mas útiles.

Otra cosa que si quisiéramos encodear los caracteres especiales en nuestra URL(como podrían
ser espacios en blancos y demás) podríamos usar la clase 
[URI](http://docs.oracle.com/javase/7/docs/api/java/net/URI.html "URI"), suponiendo
que la URL completa es `http://example.com/hellow word/`:

	:::java
	URI uri = new URI("http","example.com", "/hello word/","");
	// Para convertirla a URL
	URL URL = uri.toURL();

>> **Nota:** Las clases URLConnection, HttpURLConnection, URL, URI y URLEncoder(la cual veremos 
más adelante) se encuentran en el paquete `java.net`.

Los objetos URL lanzan una excepción del tipo `MalformedURLException` si los argumentos del constructor
son del tipo `null` o algún protocolo desconocido. Algo importante, es que los objetos del tipo `URL` 
no se le puede cambiar el estado una vez creados, es decir, no se le pueden cambiar sus atributos una vez
han sido creados.

Leyendo directamente desde una URL
------------------------------------

Leer directamente desde una URL es bastante simple, una vez ya tenemos un objeto URL creado podemos
llamar al método `openStream()` para obtener un stream del cual se podrá leer el contenido de la URL.
El método `openStream()` como se puede imaginar devuelve un objeto `InputStream`([paquete java.io.InputStream](http://docs.oracle.com/javase/7/docs/api/java/io/InputStream.html "InputStream")).

Veamos el siguiente ejemplo que ilustra claramente como leer directamente desde una URL:

	:::java
	import java.io.BufferedReader;
	import java.io.InputStreamReader;
	import java.net.URL;


	public class URLReader {
		public static void main(String[] args) throws Exception{
			URL URL = new URL("http://aljavier.github.io");
			BufferedReader in = new BufferedReader(new InputStreamReader(URL.openStream()));
		
			String inputLine;
			while((inputLine = in.readLine()) != null)
				System.out.println(inputLine);
			in.close();
		}
	}

El código es tan simple que se explica así mismo, primero instanciamos la URL, luego obtenemos un `Stream` de URL
invocando su método `openStream()`, pasamos el objeto devuelto por dicho método(cuyo objeto es un `InputStream`) a un
objeto del tipo `InputStreamReader` y de igual forma éste al constructor de `BufferedReader`, para así de esa forma 
poder leer el contenido devuelvo por el sitio web como si leyéramos de un simple archivo.

Conectándose a una URL
----------------------

Anteriormente habíamos visto como poder obtener un sitio web, leyendo directamente desde su URL, ahora veremos como
conectarnos a una URL de tal forma que podamos establecer parámetros y propiedades para las solicitudes que haremos
al website según sean nuestras necesidades.

Una vez ya tengamos un objeto `URL` creado podemos llamar a su método `OpenConnection()` para obtener un objeto 
`URLConnection` o una de sus subclases de protocolos específicos(como HttpURLConnection).  La conexión hacia la maquina
y/o recurso remoto representado por el objeto `URL` solo se inicia cuando se llama al método `connect()` del objeto
`URLConnection`, con esto iniciamos un enlace de conexión entre nuestro aplicación Java y la URL a través de la red. Cabe
decir que en algunos casos no es necesario llamar explícitamente el método `connect`, ya que este es ejecutado de forma
implícita cuando se ejecutan métodos como `getInputStream`, `getOutputStream` entre otros.

Veamos el siguiente ejemplo que esta en la documentación oficial tal cual(como casi todos en este post), el mismo
abre una conexión al sitio `example.com`:

	:::java
	try {
 	   URL myURL = new URL("http://example.com/");
    	URLConnection myURLConnection = myURL.openConnection();
    	myURLConnection.connect();
	} 
		catch (MalformedURLException e) { 
    	// new URL() failed
    	// ...
	} 
		catch (IOException e) {   
    	// openConnection() failed
    	// ...
	}

Una vez conectado correctamente a nuestra URL estamos listo para usar URLConnection y ejecutar acciones como
leer y/o escribir a esa conexión.

Leyendo desde un objeto URLConnection
--------------------------------------------------------

A continuación veremos que leer desde URLConnection, primeramente como siempre creamos un objeto `URL`, luego 
un objeto `URLConnection` y después de esto leemos el flujo de datos(o stream) con BufferedReader. El siguiente
código lo ilustra de forma clara:

	:::java
	import java.io.BufferedReader;
	import java.io.InputStreamReader;
	import java.net.URL;
	import java.net.URLConnection;

	public class URLConnectionReader {
		public static void main(String[] args) throws Exception{
			URL my_URL = new URL("http://aljavier.github.io");
			URLConnection uc = my_URL.openConnection();
		
			BufferedReader in = new BufferedReader(new InputStreamReader(
					uc.getInputStream()));
			String inputLine;
			while((inputLine = in.readLine()) != null)
				System.out.println(inputLine);
			in.close();
		}
	}

El código anterior hace lo mismo que el otro anterior que lee directamente desde URL y este mas arriba, de modo
que ambas formas pueden usadas, no obstante, tiene sus ventajas usar `URLConnection`, por ejemplo, que podemos
realizar otras acciones además de leer, como es escribir a esa URL(como enviar datos a un formulario POST, ver más abajo).

Escribiendo a un objeto URLConnection
-----------------------------------------

Es de esta forma que podemos por ejemplo enviar datos a un formulario web. Según la documentación oficial para un programa
Java interactuar con proceso del lado servidor este simplemente escribir a un `URL`(sí al objeto), de esta forma proveyendo los
datos al servidor. Para esto, sigue los siguiente pasos:

1. Crear un **URL**.
2. Obtener el objeto **URLConnection**.
3. Establecer capacidad de envío(output) en el URLConnection.
4. Abrir una conexion al recurso.
5. Obtener un `output stream` de la conexión.
6. Escribir al `output stream`.
7. Cerrar el `output stream`.

Para el siguiente ejemplo, ya que necesitamos un formulario con el cual interactuar tengo un servidor web en localhost corriendo
con el siguiente formulario:

	:::html
	<?php
	if($_POST){
			if(isset($_POST['nombre'])){
				echo "Hey, un grato saludo mister ".$_POST['nombre']."!\n";
			}else{
				echo "Hey, que onda mister Anónimo!\n";
			}
	}
	?>
	<!DOCTYPE html>
	<html lang="es">
		<head>
			<title> Formulario Simple</title>
		</head>
		<body>
			<form id="datos" action="" method="POST">
				<label for="nombre">Nombre:</label>
				<input id="nombre" name="nombre" type="text"/>
				<input type="submit" value="Enviar"/>
			</form>
		</body>
	</html>

El archivo anterior le he llamado en mi servidor `form.php`, ahora veamos el código que interactúa con el mismo usando URLConnection:

	:::java
	import java.io.BufferedReader;
	import java.io.InputStreamReader;
	import java.io.OutputStreamWriter;
	import java.net.URL;
	import java.net.URLConnection;
	import java.net.URLEncoder;

	public class URLWriter {

		public static void main(String[] args) throws Exception{
			String userAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0";
			String address = "http://localhost/form.php";
			String forSending = "Batman";
		    String charset = "UTF-8";
            
            // El metodo encode() de URLEncoder se encarga de encodear la cadena que enviaremos
			// al servidor, sustituyendo espacios y caracteres especiales
			String stringToSend = URLEncoder.encode(forSending, charset);
		
			// 1. Creamos objeto URL
			URL URL = new URL(address);
			// 2. Obtenemos el objeto URLConnection llamando a openConnection() en URL
			URLConnection connection = URL.openConnection();
			// Establecemos algunas propiedas de envió, como es el User-Agent
			connection.addRequestProperty("User-Agent", userAgent);
			
			// 3. Esto es importantisímo, es aqui donde establecemos la capacidad de envió.
			connection.setDoOutput(true);
		
			// 4. Abrimos una conexión al recurso para poder escribir/enviar datos al formulario
			// Nota que no se llama explícitamente a connect() porque llamados a getOutputStream()
			OutputStreamWriter out = new OutputStreamWriter(
					connection.getOutputStream());
			out.write("nombre=" + stringToSend); // "nombre" es el campo del formulario web
			out.close();
		
			// Aquí leemos el resultado que nos devolvió el servidor, en efecto, lo que
			// respondió form.php y luego de enviar los datos
			BufferedReader in = new BufferedReader(
					new InputStreamReader(
							connection.getInputStream()));
			String response;
			while((response = in.readLine()) != null)
				System.out.println(response);
			in.close();
		}
	}

El servidor, nos responde perfectamente con algo como:

	Hey, un grato saludo mister Batman!

Con el código html de la pagina más abajo, si hubiese puesto el php en un solo archivo aparte
solo tendría la respuesta de mas arriba, en todo caso, la idea del post es clara no? :|

Obviamente, lo que tengo mas arriba es un ejemplo sencillo básicamente tal cual esta en la documentación
oficial, para ilustrar el como funciona todo esto, pero lo correcto seria crear alguna clase que podamos
reutilizar y manejar un poco de mejor manera el manejo de las excepciones.

Escribiendo a un objeto HttpURLConnection
------------------------------------------------------

Ahora vamos a mostrar el mismo ejemplo pero usando `HttpURLConnection` esta vez, no tiene mucho misterio
ya que esta es una subclase directa de `URLConnection` que bien sobreescribe y agrega algunos métodos, pero
que comparten otros cuantos.

	:::java
	import java.io.BufferedReader;
	import java.io.InputStreamReader;
	import java.io.OutputStreamWriter;
	import java.net.HttpURLConnection;
	import java.net.URL;
	import java.net.URLEncoder;

	public class URLWritterHttp {
		public static void main(String[] args) throws Exception{
			String userAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0";
			String address = "http://localhost/form.php";
			String forSending = "Batman";
		    String charset = "UTF-8";

			String stringToSend = URLEncoder.encode(forSending, charset);
		
			URL URL = new URL(address);
			HttpURLConnection connection = (HttpURLConnection)URL.openConnection();
			connection.addRequestProperty("User-Agent", userAgent);
		
			//Para poder escribir datos a la URL
			connection.setDoOutput(true);
		
			// Indicamos el tipo de request, POST en este caso
			connection.setRequestMethod("POST");

			// Indicamos un timeout de 10 segundos
			connection.setReadTimeout(10*1000);
		
			OutputStreamWriter out = new OutputStreamWriter(
					connection.getOutputStream());
			out.write("nombre=" + stringToSend);
			out.close();
		
			BufferedReader in = new BufferedReader(
					new InputStreamReader(
							connection.getInputStream()));
			String response;
			while((response = in.readLine()) != null)
				System.out.println(response);
			in.close();
		}
	}

Como puede verse los cambios son muy pocos, como dije antes aunque HttpURLConnection es una clase especifica para comunicaciones
con el protocolo http, la clase URLConnection es muy http-céntrica. En este ultimo ejemplo agregue un timeout, además
puede verse como el HttpURLConnection tiene un método `setRequestMethod()` que permite especificar el tipo de método
de envío(los más usados son POST y GET, pero también existen PUT, HEAD y otros).


**Referencias**
+ [Oracle docs - Java SE - Working with URLs](http://docs.oracle.com/javase/tutorial/networking/urls/index.html "Working with URLs") 

**Más información**
+ [StackOverflow - How to use URLConnection to fire and handle HTTP requests](http://stackoverflow.com/questions/2793150/how-to-use-java-net-URLconnection-to-fire-and-handle-http-requests "stackoverflow ")
