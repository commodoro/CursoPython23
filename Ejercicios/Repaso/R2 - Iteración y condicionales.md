# Ejercicios de repaso de iteración y condicionales.

> Todos estos ejercicios se pueden realizar únicamente con iteración y condicionales.

> Intenta hacer funciones para tareas sencillas.

### Ejercicio 1.

Realiza un programa que imprima la suma de todos los números primos que van del 1 al 100 y diga cuántos hay.

### Ejercicio 2.

Realiza un programa que permita calcular la media y la desviación típica de datos introducidos por consola.
- El programa debe pedir datos al usuario mediante la función `input()` hasta que introduzca 'stop'.
- No uses estructuras de datos como listas o diccionarios.
- Puedes usar el módulo `math` para obtener las función de raíz cuadrada (`sqrt`).

Media:

$$ \mu = \frac{1}{N}\sum_{i=1}^{N}{x_i} $$

Desviación estándar:

$$ \sigma = \sqrt{\frac{1}{N}((\sum_{i=1}^{N}{x_{i}^{2}})-N\mu^{2})}$$

### Ejercicio 3.

Realiza una función que dada una circunferencia de radio $R$ y centro ($x_c$, $y_c$) le pasemos un punto ($x_p$, $y_p$) y nos diga si queda dentro, fuera o tangente a la circunferencia. Haz que el programa pida la circunferencia y después los puntos separados por punto coma. Por ejemplo:

```bash
Introduzca circunferencia [R,x,y]: 3,0,2
Introduzca puntos [x,y;...]: 1,3;0,5;2,-4
----- Informe -----
Punto (+1.0, +3.0) : Dentro
Punto (+0.0, +5.0) : Tangente
Punto (+2.0, -4.0) : Fuera
```

- Utiliza una precisión de 0.01 unidades.
- La distancia entre dos puntos se calcula:  

$$ D(p_1, p_2) = \sqrt{(x_2 - x_1)^2 + (y_2-y_1)^2} $$

### Ejercicio 4.

Crea un programa que realice la simulación de una inversión a interés compuesto.

- El programa debe pedir:
  - La tasa de interés anual.
  - Un capital inicial $C$.
  - Información de si se realizan nuevos depósitos al principio o al final de cada periodo y la cantidad. 
  - El número de años que se calcula.

Haz que se imprima una tabla con información al final de cada año y un resumen final. El capital de un periodo ($n$) a otro se calcula en función de la tasa de interés ($r$) como:

$$ C_{n+1} = C_{n} \cdot (1+r) $$

Ten en cuenta si se añaden fondos antes o después de realizar el cálculo. A continuación un ejemplo:

- Capital inicial: 10.000€
- Inversión anual: 2.500€ (al principio del periodo).
- Periodo: 25 años
- Rentabilidad (interés): 7% anual

Debe dar de resultado al final:

- Inversión total: 72.500€. 
- Capital final: 223.465€. 
- Rendimiento total: 308,23%
