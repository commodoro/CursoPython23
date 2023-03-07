import json
from . import logistica

def cargar_pedidos(ruta_json: str):
    "Carga los pedidos desde un archivo json."
    with open(ruta_json, 'r') as pedidos_json:
        data = json.load(pedidos_json)
    return [logistica.Pedido.from_dict(pedido_dict) for pedido_dict in data]


def redactar_informe(camiones: list[logistica.Camion], ruta_salida: str):
    "Redacta el informe de los camiones."

    with open(ruta_salida, 'w') as archivo:
        todas_rutas = [tuple(camion.ruta) for camion in camiones]
        rutas = set(todas_rutas)
        for ruta in rutas:
            print(f'----------------------------------------', file=archivo)
            print(f'Ruta: {ruta}', file=archivo)
            print(f'----------------------------------------', file=archivo)
            for camion in filter(lambda cam: tuple(cam.ruta) == ruta, camiones):
                print(camion, file=archivo)
        print(f'----------------------------------------', file=archivo)
        print("Total:", len(camiones), "camiones.", file=archivo)