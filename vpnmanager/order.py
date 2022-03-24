import enum

from .user import User


class Order:
    def __init__(self, user: User, created_ts, status,):