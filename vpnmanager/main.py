import logging
from uuid import uuid4
from datetime import datetime

from client import ClientCollection, Client
from vpnservice import get_vpn_service
from ca import CA
from connection import Connection


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    telegram_id = 365848986
    first_name = 'Sonhador'
    days = 1

    clients = ClientCollection('users.db')
    try:
        client: Client = clients.get_user((telegram_id))
        if client.conn.expire > datetime.utcnow():
            print("refresh cert")
            cert_id = str(uuid4())
            expire_date = datetime.utcnow()  # !TODO + 1Day
            ca = CA("/tmp/ca_data", "./openssl.cnf")
            ca.make_cert(cert_id)
            client.set_conn(Connection(cert_id, expire_date))
            clients.save_users()

    except KeyError:
        ca = CA("/tmp/ca_data", "./openssl.cnf")
        cert_id = str(uuid4())
        ca.make_cert(cert_id)
        expire_date = datetime.utcnow() # !TODO + 1Day
        client = Client(telegram_id, first_name, Connection(cert_id, expire_date))
        clients.add(client)
        clients.save_users()

    print(client)

    #
    # vpn_service = get_vpn_service()
    # vpn_service.issue_access_for(client, days)
    # client_cfg = vpn_service.get_config_for(client)
    # print(f"config for {client.first_name}: {client_cfg}")
    #
