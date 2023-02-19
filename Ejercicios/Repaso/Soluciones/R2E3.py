import math

def introducir_circulo():
    'Introducimos radio y centro del círculo'
    entrada = input('Introduzca circunferencia [R,x,y]: ')
    r, x, y = entrada.split(',')
    return float(r), float(x), float(y)

def introducir_puntos():
    'Introducimos los puntos separados por ";" '
    entrada = input('Introduzca puntos [x,y-...]: ')
    return entrada

def extraer_coordenadas(punto):
    'Sacamos x e y de un punto en formato texto (str)'
    x, y = punto.split(',')
    return float(x), float(y)    

def distancia_puntos(x_1, y_1, x_2, y_2):
    'Calcula la distancia entre dos puntos'
    return math.sqrt((x_2-x_1)**2+(y_2-y_1)**2)

def posicion_relativa(distancia, radio, precision=0.01):
    'La posición rel. depende de lo lejos que esté un punto del centro.'
    if abs(distancia-radio) < precision:
        return 'Tangente'
    return 'Fuera' if distancia - radio > 0 else 'Dentro'
    
def main():
    'Programa principal.'
    radio_circulo, x_circulo, y_circulo = introducir_circulo()
    puntos = introducir_puntos()
    print('----- Informe -----')
    for punto in puntos.split(';'):
        x_punto, y_punto = extraer_coordenadas(punto)
        distancia = distancia_puntos(x_circulo, y_circulo, x_punto, y_punto)
        posicion = posicion_relativa(distancia, radio_circulo)
        print(f'Punto ({x_punto:+.1f}, {y_punto:+.1f}) : {posicion}' )

main()