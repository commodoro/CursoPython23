"""
Añade los métodos OPTIONS a los recursos creados.
"""

import functools
from . import bottle

options = functools.partial(bottle.route, method="OPTIONS")
rules: list[str] = [route.rule for route in bottle.app[0].routes]


@options(rules)
def resource_options(*args, **kwargs):
    "Añade las funciones disponibles para ese recurso."
    methods = [route.method for route in bottle.request.app.routes if route.rule == bottle.request.route.rule]  # type: ignore
    bottle.response.add_header("Allow", ",".join(set(methods)))
