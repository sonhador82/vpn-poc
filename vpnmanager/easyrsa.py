import os
import pathlib
import sys
import logging
import subprocess

#!TODO решить проблему с запросом пароля (возможно накидать свой easyrsa)

class EasyRSA:
    def __init__(self, file_path: str, ca_pass: str):
        self.easy_rsa_path = str(pathlib.Path(file_path).resolve())
        self.easy_rsa_dir = str(pathlib.Path(file_path).parent.resolve())
        self.pki_path = str(pathlib.Path(file_path).parent.joinpath('pki').resolve())
        self.ca_pass = ca_pass

    def make_client_cert(self, name: str):
        cmd = [
            'bash', '-c',
            f'{self.easy_rsa_path} build-client-full {name} nopass'
            ]

        logging.debug(f'cmd: {cmd}')
        try:
            result = subprocess.run(cmd, cwd=self.easy_rsa_dir, check=True)
        except Exception as e:
            logging.error(f'Cant create client certificate')
            sys.exit(1)


if __name__ == '__main__':
    er = EasyRSA('/home/sonhador/projects/vpn-poc/ca/easyrsa', 'secret')
    er.make_client_cert('dummy3')

