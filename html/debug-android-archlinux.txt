title: Debug de aplicaciones Android en Arch Linux
tags: android, debug, arch linux
date: 2016-05-02
slug: debug-android-archlinux

Si estas iniciando a desarrollar aplicaciones **Android** usando **Arch Linux** lo más probable es que ya te habrás
dado cuenta que el *Android Studio*, el *Eclipse* o el *adb* si lo usas directamente no reconocen tu dispositivo 
Android si lo has conectado, por lo que no puedes hacer debug/test de tus aplicaciones. Esto se debe a que el conocido
y controvertido **Systemd** que implementan casi todas las distros GNU/Linux desde hace un tiempo, pone ciertas
restricciones de seguridad para que el dispositivo pueda ser reconocido.

No hay necesidad de temer, simplemente en Arch Linux como se tiene la cultura de ser minimalista hay que hacer las cosas
un poco más "mecánicamente". A continuación se explica como hacerlo.

Habilitar **USB debugging** en el dispositivo Android en *Setting*  buscar **System > Developer Options**.

Buscar el *vendor id* y *product id* del dispositivo. Para eso conectamos el dispositivo (si ya no lo esta) 
con un cable usb a la computadora y tecleamos en una terminal:
	
	lex@localhost ~/$ lsusb

Veremos un dispositivo con el nombre de la marca del dispositivo y probablemente el modelo del mismo, entre otros posibles
dispositivos si los hay. Donde dice ID hay dos palabras separadas por ":" (sin las comillas) el primero es el *vendor id* y el segundo es 
el *product id*.

Creamos el archivo de *Android Rules* en la ruta **/etc/udev/rules.d/**:

	vim /etc/udev/rules.d/51-android.rules

Yo uso *vim*, puedes usar el editor de texto que quieras. Por cada dispositivo que queramos agregar insertamos una línea
como la siguiente:

	SUBSYSTEM=="usb", ATTR{idVendor}=="id_vendor", ATTR{Product}=="id_product", MODE="0666"

Claro, reemplazando **id_vendor** y **id_product** por sus respectivos valores en nuestro dispositivo, aquellos
que vimos en la salida de **lsusb**.


Una vez hecho esto guardas el archivo y corres el siguiente comando:

	sudo udevadm control --reload-rules

Desconecta el dispositivo android y conéctalo nuevamente. Una vez hecho esto, en un terminal escribes:

	adb devices

Y deberías ver tu dispositivo listado. 

Nota: El dispositivo en cuestión esta en inglés, por eso "setting" en vez de "configuración" y así sucesivamente. De modo que,
si el dispositivo esta en español tomar en cuenta hacer las traducciones para poder seguir la guía.

**Más información:**
+ [Android - Wiki Arch Linux](https://wiki.archlinux.org/index.php/Android)
