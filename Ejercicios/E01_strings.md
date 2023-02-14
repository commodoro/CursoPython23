# E1: Extraer Información.

Recibimos cada pocos minutos mensaje desde una estación meteorológica con este formato:

> "temp:00X-hum:X-lluvia:[si|no]"

Es decir, la temperatura en kelvin con precisión de un grado, la humedad en porcentaje relativo (10-99) y ‘si’ o ‘no’ cuando hay lluvia. 

Un ejemplo de mensaje puede ser: “temp:290-hum:54-lluvia:si” 

Extrae la información y muestra por pantalla la misma información con mejor formato y la temperatura en grados centígrados.