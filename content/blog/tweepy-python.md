title: Tweepy: Manejando la API de Twitter desde Python
tags: twitter, python, tweepy
slug: tweepy-api-twitter-para-python
date: 2014-05-23

Hace poco me había surgido la idea de hacer un script en `Python` para `Twitter`, con
la idea de mantener un registro de las personas que me dieran unfollow. Ya había usado
hace tiempo la librería de la que hoy vengo a hablar que es nada mas y nada menos que
[Tweepy](http://www.tweepy.org/) una librería de Python para acceder a la `API` de Twitter.

Como casi todo en el fabuloso mundo del lenguaje de programación Python, Tweepy es relativamente
intuitiva y de fácil uso. Lo primero que necesitamos es instalar la librería, que como la mayoría de librerías puedes instalar con `pip` o `easy_install` o usando el instalador 
desde el código fuente, el típico `python setup.py install`.

**Instalación con pip:**

	pip search tweepy # para buscar si esta en los repositorios
	pip install tweepy

**Instalación con easy_install:**
   
	easy_install tweepy

**Instalación desde código fuente:**

	python setup.py install

*Nota: Necesitas permiso de super usuario para eso.*

Este no esta pensado para ser un tutorial extenso o bastante detallado(debo admitir que 
yo mismo no es que tenga un conocimiento tan pronunciado sobre esta librería) sino mas bien una breve introducción, en todo caso la documentación oficial es buena.

Así que para empezar, tener en cuenta que necesitaras registrar tu app en Twitter, específicamente en [este link](https://apps.twitter.com/), luego de registrarte y elegir los 
permisos correspondientes para tu app en `API Keys` puedes encontrar tu `API key` y `API 
secret`. Como cambiar permiso y demás, no es algo que explicare, supongo que esta bastante intuitivo la interfaz del `Twitter Application Manager`.

Una vez obtengas el API key y el API secret(en lo adelante `consumer_key` y `consumer_secret`, respectivamente) ya podemos iniciar con lo mas básico, que es la `autenticación`(claro, luego de import la librería con `import tweepy`):

	:::python
	consumer_key = raw_input("Introduzca el consumer_key >>> ")
	consumer_secret = raw_input("Introduzca el consumer_secret >>> ")
   
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

	# Ahora necesitamos el access token para los permmisos
	redirect_url = auth.get_authorization_url()
	print "Puede obtener el access token en este link >>> ", redirect_url
	verifier = raw_input("Introduzca el codigo verificador: ")
   
	# Obtenemos y pasamos al objeto 'auth' el token con el codigo antes provisto
	auth.get_access_token(verifier)

	# Obtenemos un objeto api que necesitaremos para hacer los requests a Twitter
	api = tweepy.API(auth)   # Pasando el objeto 'auth' como parámetro


Esa es una posible forma de hacerlo, obviamente no querrás introducir esos mismos datos
cada vez que inicias la aplicación, por eso lo ideal seria guardar el `access_token` y el
`consumer_key` así como el `consumer_secret` en un archivo o base de datos(no de fácil acceso
a todo mundo, por seguridad), en ese caso para el access_token tendrías que setear su valor
de esta manera:

	auth.set_access_token(key, secret)

Si haces lo siguiente puedes obtener el key y el secret del token así:

	:::python
	acces_token = auth.get_access_token()
	key = acces_token.key
	secret = access_token.secret

De ahí almacenas esos datos en algún medio de persistencia(archivo, base de datos) y seteas cada vez esos valores conforme quieras.

Para ilustrar el uso de la librería procederé a hacer una especie de `Hello World` usando algunos ejemplos combinados de la documentación oficial:

	:::python
	import tweepy

	consumer_key = raw_input("Introduzca consumer key >>> ")
	consumer_secret = raw_input("Introduzca consumer secret >>> ")
   
	# Autentificamos la app
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
   
	# Obtenemos autorización del usuario para acceder/usar su perfil desde nuestra app
	redirect_url = aut.get_authorization_url()
	print "Autorize esta app para usar su perfil en >>> ", redirect_url
	verifier = raw_input("Ahora introduzca el codigo de verificación aquí >>> ")

	# Seteamos la autorización
	auth.get_access_token(verifier)

	# Obtenemos nuestro objeto 'api'
	api = tweepy.API(auth)

	# Si quisiéramos obtener para guardar en algún lado el token de acceso
	# podríamos obtenerlo así
	# key = auth.access_token.key
	# secret = auth.access_token.secret
   

	# Ahora leamos nuestro timeline
	public_tweets = api.home_timeline()
	for tweet in public_tweets:
	    print "[+] %s" % tweet.text

	# Obteniendo información de un usuario en especifico
	user = api.get_user('twitter')
	print "Nombre publico o nick: %s" % user.scree_name
	print "Cantidad de seguidores: %s" % user.followers_count
	print " <<<<< LISTA DE AMIGOS >>>>>"
	for friend in user.friends():
        print friend.screen_name

	# Seguir a todo el que me sigue
	for follower in tweepy.Cursor(api.followers).items():
    	follower.follow()
  		print "Ahora siguiendo a >>> %s" follower.screen_name

Algo muy útil que no se ilustra en el codigo anterior son los [objetos Cursores](http://tweepy.readthedocs.org/en/v2.3.0/cursor_tutorial.html) para limitar la cantidad de resultados, por ejemplo en el 
codigo anterior para seguir a todo mundo podríamos haber limitado la cantidad de personas 
a seguir que nos devolviera el api a 10 de la siguiente manera:

	:::python
    for follower in tweepy.Cursor(api.followers).items(10)
        follower.follow

Muchas otras cosas se pueden hacer, buscar usuarios, como la búsqueda que se realiza en el mismo twitter 
con el botón buscar, navegar a través de su lista de amigos, sus fotos de perfil, websites, etc.. Cosas
que podrían ser muy útil para practicar `análisis de datos` con Python.

Por el momento es todo, lo que puedan necesitar sobre esta api en la documentación oficial lo encuentran. 

Shalom!

**Referencias**
* [Tweepy Documentation](http://tweepy.readthedocs.org/en/v2.3.0/index.html)

	
