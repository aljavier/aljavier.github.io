title: Fuentes dañadas luego de actualizar Arch Linux
date: 2017-04-30
tags: arch linux, fuentes dañadas, arch linux update
slug: fuentes-estropeadas-update-archlinux

Desde hace un tiempo no actualizaba mi Arch Linux, al actualizarlo a la fecha de esta entrada
del blog, me he encontrado con la sorpresa de que una vez reiniciado el sistema cuando abrí una terminal
las fuentes tipográficas que uso allí se veían bastante mal. Uso como terminal **urxvt** y como fuente 
tengo **terminus**.

Al parecer el problema es que aproximadamente desde enero por ahí del año actual (2017) los de *Arch Linux*
o los de *X server* decidieron renombrar algunas fuentes tipográficas entre ellas se encuentra *terminus*. Si llegaste
hasta este post es probable que es porque te haya pasado similar aunque con otra fuente. 

Para darnos cuenta si realmente el problema es porque la fuente ha sido renombrada corremos el siguiente comando:

	fc-list : family | sort

En la salida de ese comando podremos ver el nombre de todas las fuentes instaladas, ahí podremos verificar si la fuente
en cuestión ha sido renombrada. También podemos filtrar la salida, por ejemplo, como en mi caso mi fuente de terminal es la *terminus* uso el siguiente comando:

	fc-list : family | grep -i terminus

La salida del comando de arriba en mi caso fue la siguiente:

	xos4 Terminus

Esto indica que la fuente ha sido renombrada de **terminus** a **xos4 Terminus**.

Si en tu caso el problema es como el mio con la terminal *urxvt*, lo que resta es ir al archivo de configuración
**Xresources** y cambiar el nombre de la fuente por el nuevo nombre. Luego simplemente restaría correr el siguiente comando:

	xrdb -merge ~/.Xresources

Y voilà! 

**Update (24, Mayo de 2017):** Aparentemente han decidido revertir el cambio de nombre (al menos en el caso de la 
fuente Terminus puedo asegurar) y ahora es nuevamente **Terminus**, así que bien el caso podrìa ser ahora cambiar de
**xos4 Terminus** a **Terminus** nuevamente.

**Update (15, Junio de 2017):** Parece que estan aburridos, ahora el nombre de la fuente es nuevamente *xos4 Terminus*.
