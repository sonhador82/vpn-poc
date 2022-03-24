import pathlib
import pickle


class Client:
    def __init__(self, user_id: int, first_name: str):
        self.tg_user_id = user_id
        self.first_name = first_name

    def __eq__(self, other):
        if self.tg_user_id == other.tg_user_id:
            return True

    def __repr__(self):
        return f'<Client: {self.first_name}, id: {self.tg_user_id}>'


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
