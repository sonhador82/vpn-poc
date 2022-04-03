import logging

log = logging.getLogger()

from client import Client


#!TODO писать абстракнтную имплементацю с заделом на ipsec/l2tp

class OpenVpnService:
    pass

    def issue_access_for(self, client: Client, days: int):
        log.debug(f"выписать доступ: {client.tg_user_id} на {days} день/дней")
        self._gen_cert()

    def get_config_for(self, client: Client) -> str:
        return "some config"

    def _gen_cert(self):
        log.debug("генерирую сертификат")
        #!todo написать обертку для easyrsa? или что-то такое.


def get_vpn_service():
    return OpenVpnService()
