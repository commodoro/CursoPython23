"""
Recursos principales de la aplicación.
"""

import json
import time
from typing import Any, Iterable, Mapping, Sequence

from .bottle import abort, request, route, auth_basic
from .api_aux import rest, req_json, rest
from .user_management import UsersDB
from .explotaciones import UserPlant


@route("/explotacion")
@auth_basic(UsersDB("./usuarios/usuarios.db"))
@rest
def explotacion() -> str:
    "Devuelve info de la explotación entera."
    with UserPlant.from_auth(request) as plant:
        return json.dumps(plant.data)


@route("/explotacion/piscinas")
@auth_basic(UsersDB("./usuarios/usuarios.db"))
@rest
def piscinas() -> str:
    "Devuelve info de las piscinas."
    with UserPlant.from_auth(request) as plant:
        return json.dumps(plant.data["pools"])


def check_index(pools: Sequence, index: int):
    "Comprueba que el índice de la piscina está en el rango adecuado."
    if index >= len(pools):
        abort(400, f"Not found pool #{index}")
    if index < 0:
        abort(400, "Pool index starts at 0")


@route("/explotacion/piscinas/<index:int>")
@auth_basic(UsersDB("./usuarios/usuarios.db"))
@rest
def piscina(index: int) -> str:
    "Devuelve info de una piscina concreta."
    with UserPlant.from_auth(request) as plant:
        check_index(plant.data["pools"], index)
        return json.dumps(plant.data["pools"][index])


@route("/explotacion/piscinas/<index:int>/sensores")
@auth_basic(UsersDB("./usuarios/usuarios.db"))
@rest
def sensores(index: int) -> str:
    "Devuelve información sobre los sensores de una piscina determinada."
    with UserPlant.from_auth(request) as plant:
        check_index(plant.data["pools"], index)
        return json.dumps(plant.data["pools"][index]["sensors"])


def check_sensor(sensores: Iterable[str], sensor: str):
    "Comprueba que el sensor exista en la lista."
    if sensor not in sensores:
        abort(400, f"Sensor '{sensor}' does not exist")


@route("/explotacion/piscinas/<index:int>/sensores/<sensor>")
@auth_basic(UsersDB("./usuarios/usuarios.db"))
@rest
def sensor(index: int, sensor: str):
    "Devuelve información sobre un sensor en concreto."
    with UserPlant.from_auth(request) as plant:
        check_index(plant.data["pools"], index)
        check_sensor(plant.data["pools"][index]["sensors"], sensor)
        return json.dumps(plant.data["pools"][index]["sensors"][sensor])


def check_set_points_keys(set_points: Iterable[str], variable: str | Iterable[str]):
    "Comprueba si las variables de los setpoints son correctas."
    if isinstance(variable, str):
        return variable in set_points
    return all(var in set_points for var in variable)


def check_set_points_values(set_points: Mapping[str, Any], variable: str | Iterable[str]):
    "Comprueba si los valores de los setpoints son correctos."
    if isinstance(variable, str):
        return isinstance(set_points[variable], (int, float))
    return all(isinstance(set_points[var], (int, float)) for var in variable)


@route("/explotacion/piscinas/<index:int>/set_points", method=["POST", "GET"])
@auth_basic(UsersDB("./usuarios/usuarios.db"))
@rest
def set_points(index: int):
    "Maneja en conjunto los setpoints."
    with UserPlant.from_auth(request) as plant:
        check_index(plant.data["pools"], index)
        if request.method == "GET":
            return json.dumps(plant.data["pools"][index]["set_points"])
        data = req_json()
        if not check_set_points_keys(plant.data["pools"][index]["set_points"], data):
            abort(400, "At least one variable does not exist.")
        if not check_set_points_values(plant.data["pools"][index]["set_points"], data):
            abort(400, "The values to set must be numbers.")
        plant.data["pools"][index]["set_points"].update(data)
        return {"status": "ok"}


@route("/explotacion/piscinas/<index:int>/feed", method=["POST"])
@auth_basic(UsersDB("./usuarios/usuarios.db"))
def feed(index: int):
    "Maneja en conjunto los setpoints."
    with UserPlant.from_auth(request) as plant:
        check_index(plant.data["pools"], index)
        plant.data["pools"][index]["last_feeding"] = round(time.time())
        return 0
