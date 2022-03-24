from .client import Client


class ClientConfig:
    """ Класс коннект клиента / файл конфигурации openvpn """
    def __init__(self):
        self.start_time: None
        self.end_time: None
        self.client: Client
