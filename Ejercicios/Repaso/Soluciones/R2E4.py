


def calcular_periodo(capital, interes, nuevo, prev=True):
    '''Devuelve el capital tras un periodo. 
       Si `prev` == `True` se aplica el nuevo capital al  
       principio del periodo y si es `False` al final.'''
    return (capital+nuevo)*(1+interes) if prev else capital*(1+interes) + nuevo

def formulario():
    'Pregunta las condiciones del cálculo'
    capital_inicial = float(input('Introduca capital inicial: '))
    interes = float(input('Introduzca tasa de interés en %: '))/100
    pregunta_deposito = input('¿Deposito al principio o al final de los periodos? [p/f]: ') 
    prev_deposito = False if pregunta_deposito == 'f' else True
    deposito = float(input('¿Cuánto deposita cada año?: '))
    annos = int(input('Introduzca los años para el cálculo: '))
    return capital_inicial, interes, deposito, annos, prev_deposito


def main():
    'Programa principal'
    capital_inicial, interes, deposito, annos, prev_deposito = formulario()
    print('- Año -\t\t- Inicio -\t- Final -')
    capital = capital_inicial
    for anno in range(0, annos):
        final = calcular_periodo(capital, interes, deposito, prev_deposito)
        print(f'  {anno+1:02d}\t\t{capital:9.2f}€\t{final:9.2f}€')
        capital = final
    inversion_total = deposito*annos+capital_inicial
    print(f'Inversión total: {inversion_total:.2f}€')
    print(f'Capital final: {capital:.2f}€')
    print(f'Rendimiento total: {(capital/inversion_total)*100:.2f}%')

main()