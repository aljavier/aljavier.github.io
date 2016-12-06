title: Patrón de diseño Strategy
tags: Strategy pattern, design patterns, design principles, java 
date: 2014-07-16
slug: strategy-pattern

Los patrones de diseño(design patterns en ingles) en síntesis son técnicas que resuelven problemas conocidos
de diseño de software. Por lo que no tenemos que rompernos la cabeza buscándole una 
solución a dichos problemas, sino que podemos asirnos de los distintos patrones que 
ya otros genios del área han figurado. 

Existen unos cuantos principios de diseño(design principles en ingles) que nos ayudan a programar
mucho mejor si los mantenemos en mente, esto es crear códigos extensibles y de fácil
mantenimiento, sobre los mismos suelen basarse los patrones de diseño. 

A continuación presento tres *principios de diseño*:

1.)
> **Identifica los aspectos de tu aplicación que varían y separalo de aquellos que permanecen
iguales.**

Un ejemplo, en un vídeo juego una clase *Character* tiene un método *fight()* los personajes siempre 
van a pelear en este hipotético juego que es un genero de pelea por así decir, de modo que usaran algún 
tipo de arma pero el personaje a su vez puede cambiar de armas varias veces, por tanto, si implementamos 
la lógica del arma dentro de la clase *Character* no podríamos extender esa característica del juego luego 
si quisiéramos agregar algo nuevo en cuanto a las armas, sin tener que modificar el código de la clase, 
violando así otro principio llamado [open/closed principle][1].

2.)
> **Programa orientado a una interfaz, no a una implementación.**

Interfaz aquí no se refiere exactamente a una interfaz como tienen Java o C#, es decir, que interfaz aquí
se refiere tanto a un *interface* como seria en los lenguajes antes mencionado o igualmente podría ser una
clase abstracta, la cuestión es que este principio nos exhorta a usar en nuestras aplicaciones un super tipo
o supertype en vez de una clase concreto. 

Me explico mejor, supongamos que  siguiendo con el ejemplo anterior en nuestra aplicación usualmente usaremos 
2 armas: Cuchillo(Knife) y hacha(Axe). Entonces podría darse el caso que en algún momento quisiéramos agregar 
al juego nuevas armas, si en la propiedad de la arma en el personaje
fuere una arma concreta, digamos que se llame Knife, de modo que tendríamos en la clase `Character` algo como
`Knife knife = new Knife()` haciendo así seria imposible agregar nuevas armas al juego sin modificar esta clase.

De modo que ahí estaríamos usando una `implementación` que aquí se refiere a usar una clase concreta, en cambio,
si creamos una Interfaz o una clase abstracta como plantilla de la cual extenderán o implementaran todas las
demás armas y que el campo en la clase *Character* vendría siendo precisamente esa clase padre, por lo que en el
cliente donde instanciemos *Character* podríamos pasarle cualquier clase como arma que sea del tipo de la 
anterior clase padre, así pudiendo extender esta para crear nuevas sin tener que modificar el código existente.

3.)
> **Favorece `composición` sobre herencia.**

Hay que entender bien esto aquí, porque herencia aun sigue siendo la mejor opción en algunos casos, así que
hay que entender digamos el contexto. Este principio se refiere a que si quieres agregar una funcionalidad(o 
un mínimo de las funcionalidades de esta) de otra clase a otra en vez de usar herencia que te limitaría en 
muchas cosas, ya que de por si la relación de tu clase con la que heredes seria del tipo ["IS-A"][2](es decir, 
que es del mismo tipo en otras palabras la extiende o implementa), encima que no se soporta la herencia múltiple 
en algunos lenguajes, así que vaye imaginándose, además de eso todo el código que no necesitas de la misma. 
Lo otro es, que `composición` aquí se refiere a que la clase en cuestión contenga la otra clase, por lo que 
igual seria valido `composición` o `agregación` en términos 
estrictos de UML. 


Patrón de diseño Strategy (Strategy pattern)
-------------------------------------------

Define una familia de protocolos, encapsula cada uno de ellos y los hace intercambiables. Strategy
permite al algoritmo variar independientemente de los clientes que lo usen. 

A continuación un diagrama UML de un juego de Aventuras(el que intencionalmente use antes para las explicaciones
mas arriba), el mismo utiliza Strategy para ofrecer la flexibilidad de poder agregar cuantas armas se quieren
y poder cambiarlas en tiempo de ejecución, observar como se reflejan los tres principios de diseño de los que
se hablo antes.

![Diagrama Strategy Pattern][4]

El diagrama se explica así mismo, notar que *Character* es una clase abstracta y que usamos el método *setWeapon()*
para poder cambiar de arma(estrategia) en runtime el cual definimos en la misma clase padre *Character* ya que
posiblemente no haya necesidad de sobreescribirlo jamas.

Ahora veremos el código en Java, puede escribirse fácilmente en otros lenguajes, lo importante es tomar el concepto,
claro evidentemente no todos los lenguajes permiten hacer esto, la wikipedia sobre los requisitos para 
implementar el Strategy pattern dice:

> *The essential requirement in the programming language is the ability to store a reference to some code in a data 
structure and retrieve it. This can be achieved by mechanisms such as the native function pointer, the first-class 
function, classes or class instances in object-oriented programming languages, or accessing the language implementation's 
internal storage of code via reflection.*

***Character.java***
	
	:::java
	public abstract class Character{
		WeaponBehavior weapon;

		public Character(WeaponBehavior weapon){
			this.setWeapon(weapon);
		}

		public abstract void fight();

		public void setWeapon(WeaponBehavior weapon){
			this.weapon = weapon;
		}
	}

***King.java***

	:::java
	public class King extends Character{
	
		public King(WeaponBehavior weapon){
			super(weapon);
			System.out.println("El Rey ha entrado al juego...inclinate!");
		}

		public void fight(){
			System.out.println("El rey da un paso hacia un lado como "
						+ "en el ajedrez y de repente...");
			weapon.useWeapon();
		}
	}	

***Queen.java***
	
	:::java
	public class Queen extends Character{

			public Queen(WeaponBehavior weapon){
				super(weapon);
				System.out.println("La Reina ha entrado al juego...inclinate!");
			}

			public void fight(){
				System.out.println("Como toda mujer(o casi) aruña, grita y muerde...y de momento...");
				weapon.useWeapon();
			}
	}

***Knight.java***

	:::java
	public class Knight extends Character{
	
		public Knight(WeaponBehavior weapon){
			super(weapon);
			System.out.println("Un noble caballero ha entrado al juego!");
		}

		public void fight(){
			System.out.println("El Caballero de repente...");
			weapon.useWeapon();
		}
	}

***Troll.java***

	::java
	public class Troll extends Character{
	
		public Troll(WeaponBehavior weapon){
			super(weapon);
			System.out.println("Un infame troll ha entrado al juego!");
		}

		public void fight(){
			System.out.println("Y el troll cual criatura malvada...");
			weapon.useWeapon();
		}
	}

***WeaponBehavior.java***
	
	:::java
	public interface WeaponBehavior{
	
		public void useWeapon();
	}

***KnifeBehavior.java***
	
	:::java
	public class KnifeBehavior implements WeaponBehavior{ 
	
		public KnifeBehavior(){
			System.out.println("Cuchillo activado...");
		}

		public void useWeapon(){ 
			System.out.println("Fuaa!!! Cuchillo arriba, cuchillo abajo...y un brazo menos!");
		}
	}

***SwordBehavior.java***
	
	:::java
	public class SwordBehavior implements WeaponBehavior{
	
		public SwordBehavior(){
			System.out.println("Espada activada...");
		}

		public void useWeapon(){
			System.out.println("Saca la espada como un samurai, directo al corazon"
							+ " y baaaaam! El enemigo es historia");
		}
	}

***AxeBehavior.java***
	
	:::java
	public class AxeBehavior implements WeaponBehavior{
	
		public AxeBehavior(){
			System.out.println("Hacha activada...");
		}

		public void useWeapon(){
			System.out.println("Agarra el hacha por el palo, la hala en forma " 
							+ "de media luna y buuum! Enemigo abatido!");
		}
	}

***BowAndArrowBehavior.java***
	
	:::java
	public class BowAndArrowBehavior implements WeaponBehavior{
	
		public BowAndArrowBehavior(){
			System.out.println("");
		}

		public void useWeapon(){
			System.out.println("Se sube a un alto, agarra su arco, flecha en mano,"
							+ "todo listo, suelta y baaaaam\n a la cabeza del enemigo!"
							+ " Totalmente enfermo!");
		}
	}

Por último, una clase para probar todo esto ***MainClass.java***
	
	:::java
	public class MainClass{

		public static void main(String[] args){
			// Declaramos e instanciamos los personajes
			Character c1 = new King(new KnifeBehavior());
			Character c2 = new Queen(new KnifeBehavior());
			Character c3 = new Knight(new KnifeBehavior());
			Character c4 = new Troll(new KnifeBehavior());
	
			System.out.println();

			// Y a pelear!!! - Instancia de King
			c1.fight(); //  Primero con la arma por defecto que es el cuchillo
			c1.setWeapon(new AxeBehavior()); // Y en runtime cambiamos el arma a Hacha 
			c1.fight(); // Atacamos con nuestra flamante nueva arma

			System.out.println();

			// Lo mismo que en lo anterior con diferentes armas
			// Instancia de Queen
			c2.fight();
			c2.setWeapon(new SwordBehavior()); // Cambiamos el arma a espada
			c2.fight();
	
			System.out.println();
	
			// Instancia de Knight
			c3.fight();
			c3.setWeapon(new BowAndArrowBehavior()); // Cambiamos el arma a arco y flecha
			c3.fight();

			System.out.println();

			// Instancia de Troll
			c4.fight();
			c4.setWeapon(new SwordBehavior()); // Cambiamos el arma a espada
			c4.fight();
		}
	
	}

	
Cuando compilamos y corremos la clase MainClass esta tiene la siguienda salida:

	Cuchillo activado...
	El Rey ha entrado al juego...inclinate!
	Cuchillo activado...
	La Reina ha entrado al juego...inclinate!
	Cuchillo activado...
	Un noble caballero ha entrado al juego!
	Cuchillo activado...
	Un infame troll ha entrado al juego!

	El rey da un paso hacia un lado como en el ajedrez y de repente...
	Fuaa!!!! Cuchillo arriba, cuchillo abajo...y un brazo menos!
	Hacha activada...
	El rey da un paso hacia un lado como en el ajedrez y de repente...
	Agarra el hacha por el palo, la hala en forma de media luna y buuum! Enemigo abatido!

	Como toda mujer(o casi) aruña, grita y muerde...y de momento...
	Fuaa!!!! Cuchillo arriba, cuchillo abajo...y un brazo menos!
	Espada activada...
	Como toda mujer(o casi) aruña, grita y muerde...y de momento...
	Saca la espada como un samurai, directo al corazon y baaaaam! El enemigo es historia

	El Caballero de repente...
	Fuaa!!!! Cuchillo arriba, cuchillo abajo...y un brazo menos!

	El Caballero de repente...
	Se sube a un alto, agarra su arco, flecha en mano,todo listo, suelta y baaaaam
 	a la cabeza del enemigo! Totalmente enfermo!

	Y el troll cual criatura malvada...
	Fuaa!!!! Cuchillo arriba, cuchillo abajo...y un brazo menos!
	Espada activada...
	Y el troll cual criatura malvada...
	Saca la espada como un samurai, directo al corazon y baaaaam! El enemigo es historia

Esa fue una demostración del patrón de diseño Strategy...usando el lenguaje Java en esta
ocasión.

exit(0);

[+] **Referencias**

* [Wikipedia: Strategy Pattern][3]
* Eric Freeman, Elisabeth Freeman. *Head First Design Patterns*. (Chapter 1)













[1]: https://en.wikipedia.org/wiki/Open/closed_principle
[2]: https://en.wikipedia.org/wiki/IS-A
[3]: https://en.wikipedia.org/wiki/Strategy_pattern

[4]: images/strategy.png "Diagrama Strategy Pattern"
