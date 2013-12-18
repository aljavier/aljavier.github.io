title: Diccionarios con HashMap y TreeMap en Java
tags: java, HashMap, TreeMap, diccionarios, generics
date: 2013-06-20

Las colecciones nos permiten agrupar un conjunto de objetos del mismo tipo o al menos lo ideal es eso, que sean del mismo tipo ya que pueden agrupar objetos diferentes pero no es aconsejable, le quita las ventajas de usar los llamados [genéricos](http://docs.oracle.com/javase/tutorial/extra/generics/index.html "genéricos") y haciendo así perdemos un poco el control sobre el tipo de objeto que manejamos.

Hay muchos objetos que entran en la categoría de collection en java, pero como siempre hay unos mas usados que otros, tenemos; *ArrayList, List, HashMap, TreeMap, TreeSet*, etc. Los dos primeros almacenan objetos o mas bien referencia a objetos estilo los vectores, es decir que nos permite acceder por medio de su posición en el mismo, los otros dos siguientes entran en la categoría de diccionarios y el ultimo es como los vectores también pero elimina automáticamente los objetos idénticos. En esta entrada solo explicaré HashMap y TreeMap.

Para los ejemplos tengo una clase llamada Person.

	:::java
	public class Person {
		 private String nombre;
		 private String apellido;
		 private int edad;
		 
		 public Person(){}
		  
		 public Person(String nombre, String apellido, int edad) {
			  super();
			  this.nombre = nombre;
			  this.apellido = apellido;
			  this.edad = edad;
			 }

		 public String getNombre() {
		  	return nombre;
		 }

		 public void setNombre(String nombre) {
		  	this.nombre = nombre;
		 }

		 public String getApellido() {
		 	 return apellido;
		 }

		 public void setApellido(String apellido) {
			  this.apellido = apellido;
		 }

		 public int getEdad() {
		 	 return edad;
		 }

		 public void setEdad(int edad) {
			  this.edad = edad;
		 }
	}

HashMap
-------

Los diccionarios nos permiten acceder a los elementos por medio de una clave que elijamos nosotros, en vez de una posición como eventualmente son los arrays o vectores. La clase HashMap se encuentra en el paquete **java.util.HashMap**.

Podemos inicializar un objeto de este tipo de la siguiente manera (cabe decir que HashMap también tiene otras tipos de constructores):

	HashMap<Key,Value > dictionary = new HashMap<Key, Value>();

Tanto en `Key` como en `Value` lo que debemos especificar es el tipo, *Key* es la clave del diccionario y *Value* es el valor del mismo. 


	HashMap<Integer, Person> dictionary = new HashMap<Integer, Person>();


En el ejemplo arriba vemos perfectamente que *dictionary* almacenará objetos del tipo *Person* con una clave numérica tipo *Integer*.

Podemos agregar los objetos al diccionario con el método put, el cual recibe dos parámetros; clave, valor, en ese orden. De igual forma tenemos el método get el cual recibe un parámetro como clave del objeto a buscar, si encuentra un objeto con la clave pasada como parámetro nos devuelve el objeto sino devuelve null. Veamos:

	:::java
	import java.util.HashMap;

	public class MainClass {

		public static void main(String[] args) {
			HashMap<Integer, Person> dictionary = new HashMap<Integer, Person>();
			Person person1 = new Person("Juan", "Pineda", 19);
			Person person2 = new Person("Alex", "Rodriguez", 35);
			Person person3 = new Person("Juan", "Guerra", 40);
			Person person4 = new Person("Mike", "Martinez", 60);
			dictionary.put(person1.getEdad(), person1);
			dictionary.put(person2.getEdad(), person2);
			dictionary.put(person3.getEdad(), person3);
			dictionary.put(person4.getEdad(), person4);

			// Obtenemos el objeto con clave igual a la edad de person3
			Person x = dictionary.get(person3.getEdad());
			  
			System.out.println("Nombre: " + x.getNombre());
			System.out.println("Apellido: " + x.getApellido());
			System.out.println("Edad: " + x.getEdad());
		}
	}

Obtuvimos como salida del programa:

	Nombre: Juan
	Apellido: Guerra
	Edad: 40

HashMap tiene entre otros los siguiente métodos:

**Object remove(Object key)**: Este método borra el objeto de clave key en el diccionario.

	dictionary.remove(person4.getEdad()); 

**boolean containsValue(Object value)**: Devuelve *true* si el diccionario contiene una referencia a ese objeto pasado como parámetro, en caso contrario devuelve *false*.

	if(dictionary.containsValue(person2)){ // devuelve true
		System.out.println("Si existe!");
	}else{
		System.out.println("No existe!");
	}

**boolean containsKey(Object key)**: Devuelve *true* si el diccionario contiene una referencia a un objeto con la clave pasada como parámetro, en caso contrario devuelve *false*.

	if(dictionary.containsKey(person2.getEdad())){
		System.out.println("Si existe!");
	}else{
		System.out.println("No existe!");
	} 


**void clear()**: Este método vacía el diccionario y lo deja tal cual como estaba al momento de instanciarse.

	dictionary.clear(); // vacía el diccionario 

**boolean isEmpty**: Devuelve *true* si el diccionario esta vacío o *false* en caso contrario.

	if(dictionary.isEmpty()){ 
		System.out.println("Esta vacío");
	}else{
		System.out.println("No esta vacío!!!");
	}

**int size()**: Este método devuelve la cantidad de objetos/claves en el diccionario.

	System.out.println("Cantidad de objetos en el diccionario: " + dictionary.size());

**Collection<Value> values()**: Este método devuelve todos los objetos contenidos en el diccionario.

	for(Person p : dictionary.values()){
		    System.out.println("Nombre" + p.getNombre());
		    System.out.println("Apellido: " + p.getApellido());
		    System.out.println("Edad: " + p.getEdad());
		    System.out.println();
	}

Tienen otros métodos de HashMap así también como otros tipos de constructores en [este link](http://docs.oracle.com/javase/6/docs/api/java/util/HashMap.html "docs oracle").

TreeMap
-------

De este no podemos decir mucho, ya que es idéntico al HashMap incluso tiene los mismos métodos explicados anteriormente, entre otros, pero hay ciertas diferencias:

>> Cuando iteramos un objeto TreeMap los objetos son extraídos de la colección en forma ascendente según sus claves, ya que TreeMap ordena los objetos según la clave.

De modo que la gran diferencia es que TreeMap ordena los objetos según la clave en forma ascendente, pero HashMap teóricamente nos devolverá los objetos en la secuencia que fueron introducidos. Entonces ¿Por qué no sólo usar TreeMap? Ah pues el caso es que cuando usamos un objeto definido por el usuario como clave (digamos una clase creada por nosotros) TreeMap no sabe como ordenar la colección, así que solo lo hace si es con datos primitivos (Integer, String, etc).

Tienen más información sobre TreeMap en [este link de acá](http://docs.oracle.com/javase/6/docs/api/java/util/TreeMap.html)

