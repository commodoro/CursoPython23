import json
from gestion import gestor_pedidos
import logistica


def cargar_pedidos(ruta_json: str):
    "Carga los pedidos desde un archivo json."
    with open(ruta_json, 'r') as pedidos_json:
        data = json.load(pedidos_json)
    return [logistica.Pedido.from_dict(pedido_dict) for pedido_dict in data]


def main():
    lista_pedidos = cargar_pedidos('pedidos.json')
    camiones = gestor_pedidos(lista_pedidos)    

    print(*camiones, sep='\n')
    print("Total:", len(camiones), "camiones.")

main()
