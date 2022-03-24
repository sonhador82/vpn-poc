import logging

from client import ClientCollection, Client
from vpnservice import get_vpn_service




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    telegram_id = 365848986
    first_name = 'Sonhador'
    days = 1

    ccol = ClientCollection('users.db')
    #!TODO создавать если нет.
    client = ccol.get_user(telegram_id)

    vpn_service = get_vpn_service()
    vpn_service.issue_access_for(client, days)

