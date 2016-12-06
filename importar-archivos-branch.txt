title: Git: Importar archivos desde un directorio en otro branch
date: 2016-12-06
tags: git trick, git tip

En una ocasión tuve la necesidad de importar todos los archivos en un directorio
de un branch en git, desde el **branch master**. Si por alguna razón sólo queremos 
importar un directorio desde otro branch (supongamos que no se quiera hacer un merge
por alguna razón), podríamos hacerlo así:

    git checkout nombre_branch -- nombre_directorio
    
Con eso se preservarían los *commits* desde **nombre_branch**.

En mi caso necesitaba copiar los archivos de ese directorio en *nombre_branch* hacia
el branch master, pero no el directorio, sino sólo los archivos dentro de él. Supongamos que tenía en 
*nombre_branch* un directorio llamado *html_dir* y quería copiar el contenido ahí dentro
al directorio de master dónde me encontraba en ese momento. Esos archivos ahí eran
*.html* y dos directorios uno *css* y el otro *images*. Entonces usaría el siguiente comando:

    git checkout nombre_branch -- html_dir && 
    find html \( -name "*.html" -o -type d -name "css" -o -type d -name "images" \)  \
    | xargs cp -r -t .

Al final lo que necesitaba era borrar en el directorio raíz del branch master
dónde me encontraba todos los archivos *.html* y los directrios *css* e *images* con su contenido.
Entonces luego importar desde la rama *nombre_branch* todos los archivos _html_ y 
sus directorios hijos _css_ e _images_ con su contenido al directorio raíz de master.

Con un poco de bash, ayuda de StackOverflow y unos cuantos errores después (borré archivos
por error que no quería borrar!) lo hice de esta manera 

    :::bash
    git rm *.html && git rm -r css && git rm -r images 

    git checkout source -- html && 
    find html \( -name "*.html" -o -name "*.txt" -o -type d -name "css" -o -type d -name "images" \)  \
    | xargs cp -r -t . && git rm -rf html && echo -e "\nDone!\n"

**Nota 1**: /!\ Advertencia /!\ La secuencia de arriba borrará archivos de tu directorio actual, usar con 
precaución. Aunque en todo caso, si estan en un repositorio remoto puedes recuperarlo fácilmente.

**Nota 2**: Con esos comandos NO se preservaría el historial de *commits* que ya tenían en la rama 
desde la que importamos. Es probablemente una muy mala idea hacer las cosas así. 

En este ejemplo he reemplazado *nombre_branch* por *source*, que era el nombre del branch
desde dónde quería importar los archivos. De igual manera, he reemplazado *nombre_directorio*
por *html*, que era el nombre del directorio en la situación que se me presentó.

Lo gracioso, es que luego de quemar algunas neuronas para ese comando llegué
a la conclusión que iba a hacer las cosas de otra manera. Lo documento aquí porque 
puede serle útil a alguien o a mi mismo en otra ocasión. Aunque era un requerimiento
extraño, como dije antes es probablemente muy mala idea hacer algo como esto de esta manera :-]