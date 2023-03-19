# Ejercicio 5: Alguicultura.

Definición de API:

> La interfaz de programación de aplicaciones, conocida también por la sigla API, en inglés, *application programming interface*, es un conjunto de subrutinas, funciones y procedimientos (o métodos, en la programación orientada a objetos) que ofrece cierta biblioteca para ser utilizado por otro software como una capa de abstracción. 
>  
> Wikipedia.

Una API, en resumen, sirve para comunicar diferentes softwares entre sí. Por ejemplo, una librería gráfica comunica el sistema de gráficos del sistema operativo con nuestro programa, permitiendo mostrar figuras o imágenes por pantalla. 

Otro uso de las API -y cada vez más importante- es la **transferencia de información entre dos sistemas**. Pensemos, por ejemplo, en una red de sensores para unas piscinas de cultivo de algas. Cada piscina podría tener, por ejemplo, sensores de temperatura de agua, ph, salinidad y refracción (para la pureza del agua). Una API nos podría proveer de la información de los sensores para el control de la planta o para el análisis de la explotación simplemente con una petición de información.

Una forma de intercambiar la información es mediante métodos HTTP (como la web normal) y formato JSON. En concreto, este sistema recibe el nombre de [REST API](https://es.wikipedia.org/wiki/Transferencia_de_Estado_Representacional). Usar el mismo método de comunicación que la web nos permite recibir la información desde cualquier lugar utilizando la infraestructura existente y manejar la información desde cualquier lenguaje o sistema (al ser abierto y popular, prácticamente todos los lenguajes implementan librerías de cliente http). Ejemplo de una petición HTTP en el sistema antes descrito puede ser por ejemplo:

```bash
GET /explotacion/piscinas/1 HTTP/1.1
Host: alguicultura.com:8080
User-Agent: Python
Authorization: Basic Y29tbW9kb3JvOjEyMzQ1Ng==
Accept: */*
```

Haríamos una **petición GET** (tipo usado pedir información) para acceder a los datos de las piscinas (`explotacion/piscinas`), más concretamente la piscina número `1`. Podríamos pedir la información de todas las piscinas con `/explotacion/piscinas` o la informacón de solo los sensores de la piscina con `/explotacion/piscinas/1/sensores`. **Las REST APIs se basan en estas rutas para representar el estado del sistema**.

En cuento al resto de la información, el `Host` es la dirección a la que enviamos la petición (por ejemplo `google.es` sería el host de Google) y la `Authorization` es información de usuario y contraseña codificada. El resto se le envía al servidor para que proceda con la petición.

La respuesta a esta petición concreta puede ser algo como:

```bash
HTTP/1.0 200 OK
Date: Fri, 24 Feb 2023 23:21:36 GMT
Server: WSGIServer/0.2 CPython/3.10.6
Content-Type: application/json; charset=UTF-8
Content-Length: 239

{
  "id": 1,
  "sensors": {
    "ph": 7.2,
    "temp": 15.1,
    "sali": 20.5,
    "refr": 6.8
  },
  "set_points": {
    "ph": 7.1,
    "temp": 21.0,
    "sali": 24.1,
    "refr": 8.8
  },
  "last_feeding": 1676970000,
  "release_date": "10/01/23",
  "species": "dulse",
  "capacity(L)": 5600
}
``` 

La respuesta se compone de un código de retorno (el 200 en este caso), información del servidor y la respuesta (en este caso texto en json). 

Cuando navegamos por internet a través del navegador hacemos el mismo tipo de peticiones pero el navegador actúa como una gran capa de asbtracción y simplemente introducimos direcciones y obtenemos la visualización de las respuestas.

Obviamente, el ejemplo que hemos visto es muy simple: sin seguridad en el transporte de los datos (no usa HTTP) y con poca información. Las API REST pueden manejar miles de `recursos` (llamamos recursos a las diferentes peticiones de información que podemos enviar/recibir).

Bien pero, ¿cómo podemos hacer peticiones con Python? Para realizar peticiones HTTP a un servidor existe el módulo `http.client` en la Python Standard Library, sin embargo el módulo `requests` provee de una interfaz más amigable y se recomienda su uso para este caso. Para instalar `requests`:

En Windows:
```
py -m pip install requests
```

En Linux/Mac:
```
python3 -m pip install requests
```

La petición en Python sería entonces:

```python
import requests

host = 'alguicultura.com' # La url
port = 8080            # Puerto de conexión
ruta = 'explotacion/piscinas/3'

url = f'http://{host}:{port}/{ruta}'

respuesta = requests.get(url, auth=('user', 'password'))
datos_piscina = respuesta.json()
```

En data tendríamos los datos en formato `dict` (pasados desde json). Ahora podemos acceder a los datos descargados de la piscina:

```python
datos_piscina['sensores']['ph'] # -> 6.2
```

> La documentación de la librería [`requests`](https://docs.python-requests.org/en/latest/user/quickstart/).

De esta manera podemos obtener toda la información que necesitemos sobre los sensores de las piscinas. Esta forma es cómoda, pero se puede hacer algo tediosa para manejar todos los recursos de la aplicación. Para ello le podemos añadir una capa de abstacción mediante Programación Orientada a objetos. Por ejemplo:

```python
import requests
import json

class Piscina:
    (...)

class Algicultivo:
    (...)

if __name__ == '__main__':
    url = (...)
    usuario = (...)
    instalacion = Algicultivo(url, usuario)
    pisc3 = instalacion.get_piscina(3) # pisc3 es de clase Piscina
    print(pisc3.get_ph())
```

En la primera parte de este ejercicio vamos a crear esta capa de abstracción. Los datos del servidor son los siguientes:

```python
host = "pcasocieee.upct.es"
port = 50600
```

Los recursos disponibles son:

    GET
    -> explotacion
        -> piscinas
            -> #[0-5]            <- Número de 0 a 5
                -> sensores
                    -> ph
                    -> temp
                    -> refr
                    -> sali
                -> set_points

Es decir, podemos pedir la ruta `/explotacion`, `/explotacion/piscinas`, `explotacion/piscinas/0`, etc. Recomiendo que hagas una petición a todos los recursos para ver el formato de la respuesta (siempre es JSON, pero es importante ver la estructura de la respuesta).

> Existe una aplicación llamada [Insomnia](https://insomnia.rest/) que te permite jugar con la API desde una interfaz gráfica más cómoda. Instálalo y sigue el vídeo tutorial de la web para cargar la plantilla y hacer llamadas a la API. 

> Debes crear un usuario para poder utilizar la API. Para ello cuentas con el recurso `POST /users/register` al que tendrás que pasarle los datos mediante json: `requests.post(url, json={"username":"[tu usuario]", "password": "[tu contraseña]"})`

El primer objetivo es:

1. En un módulo, crea al menos una clase  `Algicultivo` que gestiones las peticiones HTTP y una clase `Piscina` que sirva para acceder a los datos de las piscinas. También puedes crear otras clases si te ayuda a abstraer mejor el problema (como Sensor). Las clases deben tener, como mínimo, los siguientes métodos:
    - `Algicultivo.info()`: devuelve en una cadena de texto con información sobre la explotación.
    - `Algicultivo.load()`: devuelve los datos del recurso 'piscinas' en un diccionario.
    - `Algicultivo.get_piscina(n)`: devuelve los datos de la piscina número `n` en un objeto de `Piscina`.
    - `Alguicultivo.__getitem__(piscina)`: igual que `get_piscina(n)` pero a través de los operadores `[]`.
    - `Piscina.info()`: devuelve una cadena de texto con info sobre la piscina (sin los datos sobre los sensores).
    - Las propiedades `Piscina.ph`, `Piscina.temp`, etc. Para acceder y escribir en todos los datos de los sensores/setpoints de la piscina (se leen los sensores y se escribe sobre los setpoints).

Las API REST también se pueden usar para escribir valores en los recursos. Imaginemos que la explotación alguícola está totalmente automatizada y queremos marcar valores de consigna (*set points*) de PH, temperatura, pureza y salinidad. O que queramos liberar alimento a las piscinas. Para ello, en el ejemplo que usamos también está definido los siguientes recursos:

    POST
    -> explotacion/piscinas/#[0-5]/set_points
    -> explotacion/piscinas/#[0-5]/feed


Es decir, por ejemplo puedes usar hacer peticiones `POST` en el recurso `explotacion/piscinas/0/set_points`, `explotacion/piscinas/0/feed`, etc. Pero no puedes hacer peticiones `POST`a `/explotacion` o `/set/piscinas` porque no son valores en los que puedas escribir. 

Nótese que usamos un método diferente para escribir (POST en vez de GET). Con `requests` para pasar información en formato JSON cuando hacemos una petición solo tenemos que pasar un diccionario al argumento `json`. Por ejemplo, para enviar mediante POST a '/set/piscinas/0' datos en JSON:

```python
set_points = {'ph': 7.25, 'temp': 20.2}
respuesta = requests.post(url, json=set_points, auth=usuario)
```

> Véase que no es necesario introducir todos los *setpoints* a la vez. Se actualizarán los que se introduzca. 

Los siguientes objetivos del ejercicio son:

2. Modificar la clase 'Alguicultivo' de forma que se puedan envíar al servidor los valores de consigna de los reguladores de piscinas. Al menos uno de los métodos debe aceptar por argumento una instancia de la clase `Piscina` modificada.
3. Añade otro método para poder alimentar las piscinas mediante el recurso `POST explotacion/piscinas/0/feed`. Este recurso no necesita datos en `json`.
4. Para finalizar el ejercicio crea un nuevo script en la carpeta y, usando las clases y funciones del módulo, crea una aplicación de consola con una interfaz parecida a esta:

    ```
    [Iniciando]
    Introduce nombre de usuario: xxx
    Introduce contraseña: xxx
    Introduce Host: xxx

    --- Alguicultivo ---
    Selecciona la opción:
    1 - Resumen explotación.
    2 - Resumen piscina.
    3 - Cambiar consigna.
    4 - Alimentar.
    5 - Auto-análisis.
    6 - Salir.
    >> 
    ```
    Las opciones realizan las siguientes acciones:
    1. **Resumen explotación**: Devuelve un informe de la explotación por pantalla.
    2. **Resumen piscina**: Pregunta la piscina y devuelve un informe de la piscina (sensores y setpoints includos).
    3. **Cambiar Consigna**: Pregunta la piscina, el sensor y después el valor que cambiar.
    4. **Alimentar**: Pregunta la piscina y la alimenta.
    5. **Auto-análisis**: Realiza un informe de todas las piscinas resaltando las indicidencias. Incidencias son:
        - Leves. 
          - Que los valores de los sensores difieran 0.2 unidades de su setpoint. 0.5 para la temperatura.
          - Que la piscina no se alimente desde hace 1 día.
        - Moderados.
          - Que los valores de los sensores difieran 0.5 unidades de su setpoint. 1.0 para la temperatura.
          - Que la piscina no se alimente desde hace 2 días.
        - Graves.
          - Que los valores de los sensores difieran 0.8 unidades de su setpoint. 1.5 para la temperatura.
        - Que la piscina no se alimente durante 3 días.
    6. **Salir**: Se cierra el programa. Se debe repetir el menú mientras no acabe el programa.

Notas/consejos:

- Las respuestas (`response`) de las peticiones HTTP tienen un código de respuesta que nos indica si la petición se ha realizado correctamente. Las respuestas correctas siempre nos dan el código `200`. En el caso contrario, revisa la respuesta para comprobar el mensaje de error.

Con `request`: 
```python
respuesta = requests.post(...)  # Por ejemplo
respuesta.status_code  # -> Si es 200, todo ok.
``` 

- El tiempo está definido en timpo POSIX, es decir, segundos desde el 1 de enero de 1970. Puedes pasarlo a fecha y hora con el módulo `time` de la Python Standard Library. 

- La clase `Alguicultivo` representa los datos que están en el servidor y debería contener métodos para acceder a ellos (mediante la API). `Piscina` sin embargo es más un contenedor de datos

- Se puede acceder a todos los recursos GET simplemente poniendo en la barra de direcciones del navegador web el host con el puerto y la ruta. Prueba por ejemplo: http://pcasocieee.upct.es:50600/explotacion

- Es muy recomendable hacer pruebas en la consola o en un script en programación estructurada (funciones y variables globales) antes de encapsular en una clase. Primero entiende los procesos detrás del REST API y luego implementa tu solución. ¡Ánimo!