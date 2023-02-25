from .bottle import Bottle


with Bottle() as app:
    from .bottle import *

    assert app is default_app, "La aplicación no ha sido cargada por defecto en el operador de contexto."

    from . import api_resources
    from . import api_users
    from . import api_options

    run()
