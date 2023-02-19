
def is_prime(numero):
    'Calcula si es primo.'
    for candidato in range(2, numero):
        if numero % candidato == 0:
            return False
    return True

def main():
    'Programa principal.'
    suma_primos = 0
    numero_primos = 0
    for numero in range(1, 101):
        if is_prime(numero):
            suma_primos += numero
            numero_primos += 1
    
    print('La suma de los primos de 1 a 100 es', suma_primos)
    print('El número de primos de 1 a 100 es', numero_primos)


main()