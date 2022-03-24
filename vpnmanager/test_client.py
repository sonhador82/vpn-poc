import os

from .client import Client, ClientCollection


def test_users():
    users_file = '/tmp/users.db'
    users = [
        Client(123, 'user-1'),
        Client(456, 'user-2')
    ]
    col = ClientCollection(users_file)
    for u in users:
        col.add(u)
    col.save_users()
    del col

    col2 = ClientCollection(users_file)
    assert users == col2.users

    os.unlink(users_file)


def test_user():
    user1 = Client(123, 'user-1')
    user2 = Client(123, 'user-1')
    assert user1 == user2
