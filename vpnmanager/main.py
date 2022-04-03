import logging

from client import ClientCollection, Client
from vpnservice import get_vpn_service




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    telegram_id = 365848986
    first_name = 'Sonhador'
    days = 1

    clients = ClientCollection('users.db')

    #!TODO создавать если нет.
    client: Client
    try:
        client = clients.get_user(telegram_id)
    except KeyError:
        client = Client(telegram_id, first_name)
        clients.add(client)
        clients.save_users()

    vpn_service = get_vpn_service()
    vpn_service.issue_access_for(client, days)
    client_cfg = vpn_service.get_config_for(client)
    print(f"config for {client.first_name}: {client_cfg}")

