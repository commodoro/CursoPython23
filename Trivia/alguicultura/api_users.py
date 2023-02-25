"""
Recursos relacionados con los usuarios.
"""

from .bottle import abort, request, route
from .api_aux import rest, req_json
from .user_management import User, UsersDB


@route("/echo", method="POST")
@rest
def echo_test():
    "Echo tests"
    print("Echo from:", request.auth)
    return req_json()


@route("/users/register", method="POST")
@rest
def register_user():
    "Registra un usuario en el sistema."
    reqdata = req_json()
    try:
        assert "username" in reqdata, "No se encuentra el campo 'username'."
        assert "password" in reqdata, "No se encuentra el campo 'password'."
    except AssertionError as err:
        abort(400, str(err))
    user = User(username=reqdata["username"], password=reqdata["password"])
    with UsersDB("./usuarios/usuarios.db") as db:
        registered = db.register_user(user)
    return {"status": "ok"} if registered else {"status": "fail", "message": "User already registered."}


@route("/users/delete", method="POST")
@rest
def delete_user():
    "Elimina un usuario del sistema."
    reqdata = req_json()
    try:
        assert "username" in reqdata, "No se encuentra el campo 'username'."
        assert "password" in reqdata, "No se encuentra el campo 'password'."
    except AssertionError as err:
        abort(400, str(err))
    user = User(username=reqdata["username"], password=reqdata["password"])
    with UsersDB("./usuarios/usuarios.db") as db:
        registered = db.delete_user(user)
    return {"status": "ok"} if registered else {"status": "fail", "message": "User does not exist."}


@route("/users/list")
@rest
def list_users():
    "Devuelve una lista de usuarios registrados."
    with UsersDB("./usuarios/usuarios.db") as db:
        registered = db.get_users()
    return {"users": registered}
