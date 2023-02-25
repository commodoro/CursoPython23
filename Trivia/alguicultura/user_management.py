"Contenedores para la base de datos y los usuarios."


from dataclasses import dataclass
import pickle


@dataclass
class User:
    "Define un usuario."
    username: str
    password: str


class UsersDB:
    "Define una base de datos de usuarios sencilla (sobre csv)"

    def __init__(self, database_file: str):
        self.db_file = database_file
        self.db = {}

    def __enter__(self) -> "UsersDB":
        self.load()
        return self

    def __exit__(self, *herr):
        self.commit()

    def load(self) -> None:
        "Carga la base datos en la clase."
        try:
            with open(self.db_file, "rb") as db:
                self.db = pickle.load(db)
        except FileNotFoundError:
            pass

    def commit(self) -> None:
        "Descarga la base de datos en la clase."
        with open(self.db_file, "wb") as db:
            pickle.dump(self.db, db)

    def register_user(self, user: User, *, update=False) -> bool:
        "Registra un usuario en la base de datos."
        if user.username in self.db and not update:
            return False
        self.db[user.username] = user
        return True

    def check_user(self, user: User) -> bool:
        "Comprueba si un usuario en la base de datos coincide la contraseña."
        return user in self.db.values()

    def delete_user(self, user: User) -> bool:
        "Borra un usuario."
        if not self.check_user(user):
            return False
        del self.db[user.username]
        return True

    def get_users(self) -> list[str]:
        "Devuelve una lista de todos los usuarios registrados."
        return list(self.db.keys())

    def __call__(self, username: str, password: str) -> bool:
        "Check if a user is in the db."
        with self as db:
            return db.check_user(User(username, password))
