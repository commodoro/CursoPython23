"Se encarga de la gestión de los pedidos."

from functools import partial
import itertools
from typing import Mapping
from . import logistica
from collections import defaultdict


def asignar_camiones(lista_pedidos: list[logistica.Pedido]) -> list[logistica.Camion]:
    "Asigna camiones a una lista de pedidos. Ignora la ruta."
    camiones : list[logistica.Camion] = []
    for pedido in lista_pedidos:
        asignado = False
        for camion in camiones:
            if asignado := camion.agregar_pedido(pedido):  # ':=' operador 'walrus', asignar + comparar.
                break
        if not asignado:
            camiones.append(logistica.Camion())
            camiones[-1].agregar_pedido(pedido)
    return camiones


def unir_camiones(camion_origen: logistica.Camion, camion_dest: logistica.Camion) -> bool:
    "Une dos camiones en uno. None si no puede."
    if not ((camion_origen.peso + camion_dest.peso) <= logistica.Camion.PESO_MAXIMO):
        return False
    for pedido in camion_origen.pedidos:
        camion_dest.agregar_pedido(pedido)
    return True


def reducir_camion(camion: logistica.Camion, lista_camiones: list[logistica.Camion]) -> bool:
    "Intenta eliminar un camión introduciendo su pedido en otro."

    def comparte_destino(camion_1: logistica.Camion, camion_2: logistica.Camion):
        "Devuelve el número de rutas compartidas"
        return sum(destino in camion_2.ruta for destino in camion_1.ruta)

    comparador = partial(comparte_destino, camion)
    for camion_candidato in sorted(lista_camiones, key=comparador, reverse=True):
        if camion is camion_candidato:
            continue
        if unir_camiones(camion, camion_candidato):
            return True
    return False


def optimizar_camiones(camiones_por_rutas: dict[str, list[logistica.Camion]]) -> list[logistica.Camion]:
    "Optimiza los camiones uniendo las rutas."
    lista_plana = [camion for camion in itertools.chain(*camiones_por_rutas.values())]
    while True:
        lista_plana.sort(key=lambda camion: camion.peso)
        for index, camion in enumerate(lista_plana):
            if reducir_camion(camion, lista_plana):
                del lista_plana[index]
                break
        else:
            break
    return lista_plana


def gestor_pedidos(lista_pedidos: list[logistica.Pedido]):
    "Gestiona una lista de pedidos y devuelve los camiones necesarios."
    rutas_pedidos: Mapping[str, list[logistica.Pedido]] = defaultdict(list) 
    for pedido in lista_pedidos:
        rutas_pedidos[pedido.destino].append(pedido) 

    camiones = {ruta: asignar_camiones(pedidos) for ruta, pedidos in rutas_pedidos.items()}
    return optimizar_camiones(camiones)
