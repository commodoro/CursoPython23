

from math import sqrt


def calculo_estadisticas():
    "Programa principal."
    numero_muestras = 0
    sumatorio = 0
    sumatorio_cuadrado = 0

    while True:
        entrada = input('Indroduzca valor numérico (o "stop" para acabar): ')
        if entrada == 'stop':
            break
        valor = float(entrada)
        numero_muestras += 1
        sumatorio += valor
        sumatorio_cuadrado += valor**2

    media = (1/numero_muestras)*sumatorio
    sd = sqrt((1/numero_muestras)*(sumatorio_cuadrado-numero_muestras*media**2))

    print('Número de muestras', numero_muestras)
    print('Valor medio:', media)
    print('Desviación estándar', sd)


calculo_estadisticas()