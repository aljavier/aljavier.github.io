title: Error en Python: Unsupported locale setting
slug: unsupported-locale-setting
tags: python, locale, ubuntu, unsupported locale setting
date: 2016-12-01


Supongamos que tenemos el siguiente código en Python:

    :::python
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    
    import locale
    
    locale.setlocale(locale.LC_TIME, 'es_DO.UTF-8')
    
La última línea nos sirve para cambiar las [locales](https://wiki.archlinux.org/index.php/Locale_(Espa%C3%B1ol)) en GNU/Linux.
De manera que no sólo nos cambie el idioma sino que también nos cambia el formato de fechas y otros cosas relacionadas
que varía por idioma y región.

El caso es que si no tenemos instalado esa *locale* que le pasamos al método *setlocale*, que en nuestro caso es *es_DO.UTF-8*,
entonces nos lanzará un error parecido al siguiente:

    Traceback (most recent call last):
     File "script.py", line 6, in <module>
     locale.setlocale(locale.LC_TIME, LOCALE)
    File "/usr/lib/python2.7/locale.py", line 579, in setlocale
     return _setlocale(category, locale)
    locale.Error: unsupported locale setting
    
En Ubuntu podemos resolver esto de la siguiente manera. Primero verificamos que el *locale* no existe en 
nuestro sistema corriendo el siguiente comando en un terminal:

    locale -a
    
En mi caso esto retornó lo siguiente:

    C
    C.UTF-8
    POSIX
    
Realmente no tenemos ese *locale* instalado. Entonces procemos a instalarlo de la siguiente manera, en una terminal:

    sudo locale-gen es_DO.UTF-8
    
Claro, `es_DO.UTF-8` debe ser sustituido por el *locale* que se quiera instalar. Una vez instalado esto ya podemos
ejecutar nuestro script sin ningún problema.

