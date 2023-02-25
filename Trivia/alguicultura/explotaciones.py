"Crea y gestiona las explotaciones de cada alumno."

import json
import os
import time
from .bottle import BaseRequest
from .user_management import User


class UserPlant:
    "Crea un entorno asociado a un alumno donde se ejecuta la explotación."

    FOLDER = "./explotaciones"
    TEMPLATE = os.path.join(FOLDER, "alguicultura.json")

    def __init__(self, user: User):
        self.user = user
        self.file = os.path.join(self.FOLDER, user.username + ".json")
        self.data = {}
        if not os.path.exists(self.file):
            self._build_from_template(self.file)

    @staticmethod
    def _build_from_template(new_file: str) -> None:
        "Construye un archivo descriptor de explotación."
        assert os.path.exists(UserPlant.FOLDER), "La carpeta no existe."
        assert os.path.exists(UserPlant.TEMPLATE), "La plantilla no existe."
        with open(UserPlant.TEMPLATE, "r") as template, open(new_file, "w") as destiny:
            destiny.write(template.read())

    def __enter__(self) -> "UserPlant":
        with open(self.file, "r") as plant_file:
            self.data = json.load(plant_file)
        return self

    def __exit__(self, *err) -> None:
        self.data["last_sys_check"] = round(time.time())
        self.data["checked_by"] = self.user.username
        with open(self.file, "w") as plant_file:
            json.dump(self.data, plant_file, indent=4)

    @classmethod
    def from_auth(cls, request: BaseRequest) -> "UserPlant":
        "Instancia la clase desde la el campo 'auth' de la petición."
        assert isinstance(request.auth[0], str) and isinstance(request.auth[1], str), 'Error con la autenticación' # type: ignore
        user = User(request.auth[0], request.auth[1])  # type: ignore
        return cls(user)