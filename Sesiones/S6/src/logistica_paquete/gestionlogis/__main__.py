from .gestion import gestor_pedidos
from . import io 
import argparse


def main():
    parser = argparse.ArgumentParser(description='Gestiona pedidos.', prog='gestorlogis')

    parser.add_argument('pedidos', help='Los pedidos en formato json.')
    parser.add_argument('salida', help='Donde quieres el informe.')
    parser.add_argument('-v','--verbose', help='Imprime la salida por pantalla.', action='store_true')
    argumentos = parser.parse_args()
        
    lista_pedidos = io.cargar_pedidos(argumentos.pedidos)
    camiones = gestor_pedidos(lista_pedidos)    

    if argumentos.verbose:
        print(*camiones, sep='\n')
        print("Total:", len(camiones), "camiones.")

    io.redactar_informe(camiones, argumentos.salida)

main()
