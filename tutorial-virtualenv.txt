title: Virtualenv: Entornos virtuales de desarrollo para Python 
tags: python, virtualenv
date: 2013-08-16
slug: tutorial-virtualenv

Instalación
-----------

**Debian/Ubuntu**  
     
    apt-get install virtualenv

**Arch Linux** 

    pacman -S virtualenv
 
Se creo el directorio donde guardar todos los entornos virtuales:
     
    ~/virtualenv

Para crear un entorno virtual cualquiera:
     
    virtualenv ~/virtualenv/nombre

En el caso que no se quiera usar ningún paquete instalado en el sistema seria así:
    
     virtualenv ~/virtualenv/nombre --no-site-packages

El entorno se carga de esta forma:
    
     source ~/virtualenv/nombre/bin/activate

Y cambia el prompt a algo como:
    
     (nombre)tu_prompt

Y se desactiva el entorno con:
    
     deactivate

Para listar los paquetes instalados en el entorno usamos yolk acá:
    
     sudo easy_install yolk

Tuve problemas con yolk, así que mejor use pip que es una alternativa a easy_install por cierto, y que tiene soporte para desinstalar y listar paquetes entre otras.
    
     pip list

**Referencias**

* <http://simononsoftware.com/virtualenv-tutorial/>
* <http://www.virtualenv.org/en/latest/>
 
