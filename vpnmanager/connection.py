import datetime


class Connection:
    def __init__(self, _id, expire: datetime.datetime):
        self.id = _id
        self.expire = expire

    def __repr__(self):
        return f'<Cert uuid={self.id}, expire={self.expire}'
