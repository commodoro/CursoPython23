"""
Recursos auxiliares.
"""

import functools
import json
from typing import Any, Callable, ParamSpec, TypeVar
from .bottle import hook, abort, request, error, HTTPError, response

P = ParamSpec("P")
R = TypeVar("R")


@hook("before_request")
def check_headers() -> None:
    "Comprueba si la petición contiene los headers adecuados."
    for header in ["User-Agent", "Accept", "Content-Length"]:
        if header not in request.headers:  # type: ignore
            abort(400, "Few headers")


@error(400)
@error(401)
@error(404)
@error(405)
@error(500)
def master_error(error: HTTPError) -> str:
    "Devuelve los errores en formato json."
    response.set_header("content-type", "application/json")
    return json.dumps({"code": error.status_code, "message": error.body})


def rest(resource: Callable[P, R]) -> Callable[P, R]:
    """Decorador que comprueba si el recurso recibe una petición con el contenido en formato application/json
    y añade JSON al response."""

    @functools.wraps(resource)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if request.method == "POST" and request.get_header("content-type") != "application/json":
            abort(400, "This method only accept content in json format.")
        response.add_header("Content-Type", "application/json; charset=UTF-8")
        return resource(*args, **kwargs)

    return wrapper


def req_json() -> dict[Any, Any]:
    "Devuelve el json del request sin que me dé follón."
    return dict(request.json)  # type: ignore

