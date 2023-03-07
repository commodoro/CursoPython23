from typing import Any, Iterator
import uuid


class Pallet:
    "Representa un pallet de mercancía"

    def __init__(self, carga: str, peso: float):
        self.carga = carga
        self.peso = peso
        self._uuid = uuid.uuid4()

    @property
    def uuid(self) -> str:
        "Identificador único."
        return str(self._uuid)

    def __eq__(self, otro: Any) -> bool:
        if isinstance(otro, Pallet):
            return self.uuid == otro.uuid
        return otro == self.uuid


class Pedido:
    "Representa un pedido por parte de un cliente de pallets con mercancía"

    def __init__(self, cliente: str, destino: str):
        self.cliente = cliente
        self.destino = destino
        self.pallets : list[Pallet] = []
        self._uuid = uuid.uuid4()

    @property
    def uuid(self) -> str:
        "Identificador único."
        return str(self._uuid)

    @property
    def cantidad_pallets(self) -> int:
        "La cantidad de pallets en el pedido."
        return len(self.pallets)

    @property
    def peso_total(self) -> float:
        "Peso total de los pallets asociados al pedido."
        return sum(pallet.peso for pallet in self.pallets)

    def __repr__(self) -> str:
        return f"> Pedido {self.uuid} - {self.cliente} - {self.destino} - Pallets: {self.cantidad_pallets} >"

    def agregar_pallet(self, pallet: Pallet) -> None:
        "Añade un pallet al pedido."
        assert isinstance(pallet, Pallet), "Solo se pueden añadir pallets a un Pedido."
        self.pallets.append(pallet)

    def eliminar_pallet(self, uuid: str) -> bool:
        "Elimina un pallet según su uuid."
        if uuid in self.pallets:  # type: ignore
            self.pallets.remove(uuid)
            return True
        return False

    @classmethod
    def from_dict(cls, datos_dict: dict[str, Any]) -> "Pedido":
        "Crea un pedido a partir de un diccionario."
        cliente = datos_dict["cliente"]
        destino = datos_dict["destino"]
        pedido = cls(cliente, destino)
        for pallet in datos_dict["pallets"]:
            carga = pallet["carga"]
            peso = pallet["peso"]
            pedido.agregar_pallet(Pallet(carga, peso))
        return pedido


class Camion:
    "Abstrae una unida de transporte a la que asociar pedidos."

    PESO_MAXIMO : int = 24000

    def __init__(self):
        self._pedidos : list[Pedido] = []

    def __repr__(self):
        return f"> Camión - Ruta: {self.ruta} - Pedidos: {len(self._pedidos)} - Peso: {self.peso}"

    @property
    def ruta(self) -> list[str]:
        "Devuelve la ruta de los pedidos."
        ruta : list[str] = []
        for pedido in self._pedidos:
            if pedido.destino not in ruta:
                ruta.append(pedido.destino)
        return ruta

    @property
    def peso(self) -> float:
        "Peso del camión."
        return sum(pedido.peso_total for pedido in self._pedidos)

    @property
    def pedidos(self) -> Iterator[Pedido]:
        "Devuelve el iterador para la lista de pedidos."
        return iter(self._pedidos)

    def agregar_pedido(self, pedido: Pedido) -> bool:
        "Agrega un pedido al camión."
        if pedido.peso_total + self.peso > self.PESO_MAXIMO:
            return False
        self._pedidos.append(pedido)
        return True
