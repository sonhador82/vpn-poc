import pathlib
import pickle

from connection import Connection


class Client:
    def __init__(self, user_id: int, first_name: str, conn: Connection):
        self.tg_user_id = user_id
        self._first_name = first_name
        self.conn = conn

    def set_conn(self, conn: Connection):
        self.conn = conn

    def encode(self) -> bytes:
        return pickle.dumps(self)

    @property
    def first_name(self):
        return self._first_name

    @staticmethod
    def decode(data: bytes):
        return pickle.loads(data)

    def __eq__(self, other):
        if self.tg_user_id == other.tg_user_id:
            return True

    def __repr__(self):
        return f'<Client: {self.first_name}, id: {self.tg_user_id}, conn: {self.conn}>'



class ClientCollection:
    def __init__(self, filepath: str):
        self.path = str(pathlib.Path(filepath).resolve())
        self._users = self._load_users()

    @property
    def users(self):
        return self._users

    def get_user(self, tg_id: int):
        for u in self.users:
            if u.tg_user_id == tg_id:
                return u
        raise KeyError

    def add(self, user: Client):
        self.users.append(user)

    def save_users(self):
        with open(self.path, 'wb') as fp:
            pickle.dump(self.users, fp)

    def _load_users(self) -> []:
        try:
            with open(self.path, 'rb') as fp:
                return pickle.load(fp)
        except FileNotFoundError:
            return []
