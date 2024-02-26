// Ejercicio 1
// Usando método Factoría
/*
 1. Ejercicio 1. Patrón Factoría Abstracta en Java
Descripción
Programa utilizando hebras la simulación de 2 carreras simultáneas con el mismo número
inicial (N ) de bicicletas. N no se conoce hasta que comienza la carrera. De las carreras de
montaña y carretera se retirarán el 20 % y el 10 % de las bicicletas, respectivamente, antes de terminar. Ambas carreras duran exactamente 60 s. y todas las bicicletas se retiran a la
misma vez.
Deberán seguirse las siguientes especificaciones:
Se implementará el patrón de diseño Factoría Abstracta junto con el patrón de diseño
Método Factoría.

Se implementarán las modalidades montaña/carretera como las dos familias/estilos de
productos
Se definirá la interfaz Java FactoriaCarreraYBicicleta para declarar los métodos de
fabricación públicos:
• crearCarrera que devuelve un objeto de alguna subclase de la clase abstracta
Carrera y
• crearBicicleta que devuelve un objeto de alguna subclase de la clase abstracta
Bicicleta.
La clase Carrera tendrá al menos un atributo ArrayList<Bicicleta>, con las bicicletas
que participan en la carrera. La clase Bicicleta tendrá al menos un identificador único
de la bicicleta en una carrera. Las clases factoría específicas heredarán de Facto-
riaCarreraYBicicleta y cada una de ellas se especializará en un tipo de carreras y
bicicletas: las carreras y bicicletas de montaña y las carreras y bicicletas de carrete-
ra. Por consiguiente, tendremos dos clases factoría específicas: FactoriaMontana y
FactoriaCarretera, que implementarán cada una de ellas los métodos de fabricación
crearCarrera y crearBicicleta.
Se definirán las clases Bicicleta y Carrera como clases abstractas que se especiali-
zarán en clases concretas para que la factoría de montaña pueda crear productos
BicicletaMontana y CarreraMontana y la factoría de carretera pueda crear producto
BicicletaCarretera y CarreraCarretera.

 */

 import java.util.ArrayList;
 import java.util.Random;
 import java.util.concurrent.TimeUnit;
 
 // Interfaz FactoriaCarreraYBicicleta
 interface FactoriaCarreraYBicicleta {
    Random rand = new Random();
    int NUM_BICICLETAS = 10 * rand.nextInt(100);
    Carrera crearCarrera();
    Bicicleta crearBicicleta();
 }
 
 // Clase abstracta Carrera
 abstract class Carrera {
     ArrayList<Bicicleta> bicicletas = new ArrayList<Bicicleta>();
     abstract void retirarBicicletas();
 }
 
 // Clase abstracta Bicicleta
 abstract class Bicicleta {
     int id;
 }
 
 // Clase Factoría Bicicleta de Montaña
 class FactoriaMontana implements FactoriaCarreraYBicicleta {
 
     public Carrera crearCarrera() {
         return new CarreraMontana(NUM_BICICLETAS);
     }
 
     public Bicicleta crearBicicleta() {
         return new BicicletaMontana();
     }
 }
 
 // Clase Factoría Bicicleta de Carretera
 class FactoriaCarretera implements FactoriaCarreraYBicicleta {
     public Carrera crearCarrera() {
         return new CarreraCarretera(NUM_BICICLETAS);
     }
 
     public Bicicleta crearBicicleta() {
         return new BicicletaCarretera();
     }
 }
 
// Clase Carrera de Montaña
class CarreraMontana extends Carrera {
    public CarreraMontana(int numBicicletas) {
        for (int i = 0; i < numBicicletas; i++) {
            bicicletas.add(new BicicletaMontana());
        }
    }

    // Se retirarán el 20% de las bicicletas
    public void retirarBicicletas() {
        int n = bicicletas.size() / 5;
        for (int i = 0; i < n; i++) {
            bicicletas.remove(0);
        }
    }
}

// Clase Carrera de Carretera
class CarreraCarretera extends Carrera {
    public CarreraCarretera(int numBicicletas) {
        for (int i = 0; i < numBicicletas; i++) {
            bicicletas.add(new BicicletaCarretera());
        }
    }

    // Se retirarán el 10% de las bicicletas
    public void retirarBicicletas() {
        int n = bicicletas.size() / 10;
        for (int i = 0; i < n; i++) {
            bicicletas.remove(0);
        }
    }
}

 
 // Clase Bicicleta de Montaña
 class BicicletaMontana extends Bicicleta {
     public BicicletaMontana() {
         Random rand = new Random();
         id = rand.nextInt(1000);
     }
 }
 
 // Clase Bicicleta de Carretera
 class BicicletaCarretera extends Bicicleta {
     public BicicletaCarretera() {
         Random rand = new Random();
         id = rand.nextInt(1000);
     }
 }
 
 public class Ejercicio1 {
    public static void main(String[] args) {
        FactoriaCarreraYBicicleta factoriaMontana = new FactoriaMontana();
        FactoriaCarreraYBicicleta factoriaCarretera = new FactoriaCarretera();
        // Empezar las carreras
        // Creamos una hebra para cada carrera
        Thread hiloMontana = new Thread(new Runnable() {
            public void run() {
                Carrera carreraMontana = factoriaMontana.crearCarrera();
                int numBicicletas = carreraMontana.bicicletas.size();
                System.out.println("Número de bicicletas en la carrera de montaña: " + numBicicletas);
                try {
                    TimeUnit.SECONDS.sleep(60);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                carreraMontana.retirarBicicletas();
                float numBicicletasRest = carreraMontana.bicicletas.size();
                System.out.println("Porcentaje de bicicletas retiradas en la carrera de montaña: " + (numBicicletas - numBicicletasRest) / numBicicletas * 100 + "%");
            }
        });
        Thread hiloCarretera = new Thread(new Runnable() {
            public void run() {
                Carrera carreraCarretera = factoriaCarretera.crearCarrera();
                int numBicicletas = carreraCarretera.bicicletas.size();
                System.out.println("Número de bicicletas en la carrera de carretera: " + numBicicletas);
                try {
                    TimeUnit.SECONDS.sleep(60);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                carreraCarretera.retirarBicicletas();
                float numBicicletasRest = carreraCarretera.bicicletas.size();
                System.out.println("Porcentaje de bicicletas retiradas en la carrera de carretera: " + (numBicicletas - numBicicletasRest) / numBicicletas * 100 + "%");

            }
        });
        System.out.println("-------------------");
        hiloMontana.start();
        hiloCarretera.start();
        try {
            hiloMontana.join();
            hiloCarretera.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

 
