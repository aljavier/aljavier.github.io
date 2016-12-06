title: Instalación de Teamviewer en Arch Linux x86_64
tags: Arch Linux, teamviewer, pacman
slug: instalacion-teamviewer-archlinux-x86_64
date: 2013-10-07

Para instalar Teamviewer en Arch Linux x86_64 (vamos 64 bits), hay que tener en cuenta unas cuantas cosas; teamviewer se ejecuta en 
GNU/Linux emulando un entorno Windows, de modo que en verdad se ejecuta el binario para Windows usando wine, el mismo no requiere
que tengas wine instalado porque usa una versión portable, el asunto es que teamviewer requiere de un sin número de librerías 32 bits
para funcionar y por defecto la que tendrás en tu sistema si es de 64 bits pues serán la de esa arquitectura, obviamente.

Desconozco en verdad si instalando desde AUR se resuelven todos estos problemas de dependencias aún en sistemas de 64 bits, por lo que he leído
me parece que no, en todo caso yo preferí descargar el source desde la web oficial de [teamviewer](https://www.teamviewer.com/en/index.aspx)  y hacer todo yo mismo.

Como Arch Linux no esta oficialmente soportada por Teamviewer nos descargamos el source del susodicho software:

	:::bash
	wget http://download.teamviewer.com/download/teamviewer_linux.tar.gz

Procedemos a descomprimirlo y lo enviamos de una vez a /opt:

   	tar zxvf teamviewer_linux.tar.gz -C /opt

*Nota: Si estas con la cuenta de usuario normal necesitas permiso de super usuario para mover el teamviewer a /opt, en mi caso uso `sudo`.*

En mi caso fue necesario cambiar de owner la carpeta del teamviewer a mi usuario normal, ya que uso *sudo* para poder moverlo a /opt:

   	chown -R usuario /opt/teamviewer8

Donde *usuario* es tu usuario normal obviamente.

Luego de esto para no tener que escribir la ruta completa cada vez que quiera ejecutarlo hize un link simbólico del mismo:

  	ln -s /opt/teamviewer8/teamviewer /usr/local/bin/teamviewer

Si usas gnome o algún entorno gráfico de escritorio posiblemente preferirás crear algún lanzador en el menú del mismo, en mi caso solo uso manejador de ventanas
así que no requiero de hacer eso, específicamente ando usando DWM ahora mismo.

Otra vez te recuerdo, que para el anterior comando necesitas permisos de super usuario.

Ahora si ejecutas *teamviewer* en una terminal podrás ver el siguiente error:

	[10:37] [jota@arch-linux ~ \ ]$ teamviewer 

	Init...
	Checking setup...
	Launching TeamViewer...
	Daemon not running!
	Starting network process... pid 6697
	Network process already started (or error)

Pensarás que es un problema del daemon e irás a ejecutar *kill -9 6697* entonces te responderá que no hay ningún proceso con ese pid corriendo, claro el pid posiblemente sera distinto...bueno eso hubieras hecho
si antes no te lo hubiera pronosticado no? En fin...

Llegue a leer por ahí que matando el proceso del daemon de teamviewer y ejecutándolo de nuevo se resolvía, pero no en nuestro caso. Como decía al principio es un problema de 
librerías, estamos ejecutando un software que requiere librerías para sistemas de 32 bits y nosotros solo tenemos librerías de 64 bits actualmente.  Para corroborar esto ejecuta lo 
esto:

	/opt/teamviewer8/tv-setup --checklibs

En mi caso la salida fue lo siguiente:

	    -=-   TeamViewer tar.gz check   -=-      

	In order to use the tar.gz version of TeamViewer, 
	you have to make sure that the necessary libraries are installed.
	NOTE: All needed libraries are 32 bit libraries, even if you are on a 64 bit system!


	Writing raw output to /opt/teamviewer8/logfiles/tv_sys_check.log
	Analyzing ...

		libSM.so.6 => not found
		libX11.so.6 => not found
		libX11.so.6 => not found
		libXau.so.6 => not found
		libXdamage.so.1 => not found
		libXext.so.6 => not found
		libXfixes.so.3 => not found
		libXrender.so.1 => not found
		libXtst.so.6 => not found
		libasound.so.2 => not found
		libfreetype.so.6 => not found
		libgcc_s.so.1 => not found
		libgcc_s.so.1 => not found
		libz.so.1 => not found

	The libraries listed above seem to be missing
	Find and install the corresponding packages.

Pueden ver el *NOTE* arriba? Dice explícitamente que todas las librerías requeridas son de 32 bits, seguro que ya tenemos todas estas librerías instaladas o la mayoría de ellas
pero para 64 bits.

Lo primero que debemos hacer en nuestro caso si aún no tenemos habilitados el repositorio `multilib` es habilitarlo, entonces ya luego podremos instalar librerías de 32 bits. En mi caso 
yo lo tenia comentado desde el día que instalé el Arch Linux, así que solo tuve que descomentarlo, así que si lo tienes comentado descomentalo y sino lo tienes agregalo, de la siguiente forma:

Abre con tu editor de texto favorito (por ejemplo vim) el archivo **/etc/pacman.conf** y agrega o descomenta (según sea tu caso)  la siguiente linea:

	[multilib]
	Include = /etc/pacman.d/mirrorlist

Ahora queda sincronizar los repositorios:

	pacman -Sy

Podrás ver como ahora tienes el repositorio multilib agregado. 

Ahora es el momento de instalar las librerías que requiere el teamviewer, esto es medio tricky a veces, porque algunas librerías no tienen el mismo nombre que nos dice el comando que corrimos antes,
además que como es en un sistema de 64 bits la mayoría de estas llevaran como prefijo *lib32-*, pero ya que yo he hecho todo esto no tendrás que andar buscando los nombres de esas librerías y demás,
que en todo caso serian mas `pacman -Ss nombre_librería` que cualquier otra cosa y algunas búsquedas por la red en algunos casos.

Procedemos a instalar las librerías del siguiente modo:

	pacman -S lib32-libxau lib32-libsm lib32-libx11 lib32-libxdamage lib32-libxext lib32-libxfixes lib32-libxrender lib32-libxtst lib32-alsa-lib lib32-gcc-libs lib32-zlib lib32-libxft

Espero que no se me este quedando ninguna, pero luego de haber instalado las librerías arribas, ya debes estar ready para ejecutar teamviewer sin problemas. Veamos, primero ejecutamos nuevamente 
*/opt/teamviewer8/tv-setup --checklibs* ahora deberíamos recibir como salida lo siguiente:

       		-=-   TeamViewer tar.gz check   -=-      

   	In order to use the tar.gz version of TeamViewer, 
   	you have to make sure that the necessary libraries are installed.
   	NOTE: All needed libraries are 32 bit libraries, even if you are on a 64 bit system!


   	Writing raw output to /opt/teamviewer8/logfiles/tv_sys_check.log
   	Analyzing ...

   	All dependencies seem to be satisfied!   

En caso que tu salida sea diferente y que aun te este diciendo que faltan algunas librerías, pues busca en los repos con `pacman -Ss nombre_librería` e instala la que pertenece al repositorio `multilib`
que generalmente tendrá como prefijo `lib32-`. Si no encuentras la librería ahí busca en Internet que podaría ser que el nombre sea diferente en Arch.

Ya no queda más que simplemente ejecutar teamviewer nuevamente.

![Teamviewer](images/misc/teamviewer.png "Teamviewer en Arch Linux x86_64")

`Versión de Teamviewer`: *8.0.20931*

`uname -a`: *Linux arch-linux 3.11.3-1-ARCH #1 SMP PREEMPT Wed Oct 2 01:38:48 CEST 2013 x86_64 GNU/Linux*


