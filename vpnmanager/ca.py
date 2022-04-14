import sys
import logging as log
from pathlib import Path
from subprocess import run, CalledProcessError

# openssl.cnf должен генерироваться, в ca не указать.

class CA:
    def __init__(self, ca_data_path: str, open_ssl_config_path: str):
        self.ca_dir: Path = Path(ca_data_path).resolve()
        self.ssl_cfg: Path = Path(open_ssl_config_path).resolve()

    def make_ca(self):
        self._prep_data_dir()
        self._prep_ca_cert_key()
        self._prep_srv_cert_key()

    def _prep_data_dir(self):
        self.ca_dir.mkdir(0o755)
        index_file = self.ca_dir.joinpath("index.txt").touch(0o644)
        with self.ca_dir.joinpath("serial").open("wt") as fp:
            fp.write("01\n")

    def _prep_ca_cert_key(self):
        cmd = [
            "openssl", "req",
            "-new", "-newkey", "rsa:4096", 
            "-days", "3650", "-nodes", "-x509",
            "-extensions", "easyrsa_ca",
            "-keyout", str(self.ca_dir.joinpath("ca.key")),
            "-out", str(self.ca_dir.joinpath("ca.crt")),
            "-config", str(self.ssl_cfg),
            "-subj", "/C=KG/ST=NA/L=BISHKEK/O=OpenVPN-TEST/emailAddress=me@myhost.mydomain" #!TODO убрать 
        ]
        try:
            run(cmd, check=True, capture_output=True)
        except CalledProcessError as e:
            log.error(e.stderr)
            sys.exit(1)

    def _prep_srv_cert_key(self):
        cmd_req = [
            "openssl", "req",
            "-config", str(self.ssl_cfg),
            "-new", "-nodes",
            "-extensions", "server",
            "-keyout", str(self.ca_dir.joinpath("server.key")),
            "-out", str(self.ca_dir.joinpath("server.csr")),
            "-subj", "/C=KG/ST=NA/O=OpenVPN-TEST/CN=Test-Server/emailAddress=me@myhost.mydomain",
        ]
        cmd_sign = [
            "openssl", "ca",
            "-config", str(self.ssl_cfg),
            "-batch",
            "-extensions", "server",
            "-keyfile", str(self.ca_dir.joinpath("ca.key")),
            "-cert", str(self.ca_dir.joinpath("ca.crt")),
            "-out", str(self.ca_dir.joinpath("server.crt")),
            "-in", str(self.ca_dir.joinpath("server.csr"))
        ]
        try:
            req_result = run(cmd_req, check=True, capture_output=True)
            sing_result = run(cmd_sign, check=True, capture_output=True)
        except CalledProcessError as e:
            log.error(e.stdout)
            log.error(e.stderr)
            sys.exit(1)

    def make_cert(self, client_name: str):
        cmd_req = [
            "openssl", "req",
            "-new", "-nodes",
            "-config", str(self.ssl_cfg),
            "-keyout", str(self.ca_dir.joinpath(f"{client_name}.key")),
            "-out", str(self.ca_dir.joinpath(f"{client_name}.csr")),
            "-subj", f'/C=KG/ST=NA/O=OpenVPN-TEST/CN={client_name}/emailAddress=me@myhost.mydomain',
        ]
        cmd_sign = [
            "openssl", "ca",
            "-config", str(self.ssl_cfg),
            "-batch",
            "-out", str(self.ca_dir.joinpath(f'{client_name}.crt')),
            '-in', str(self.ca_dir.joinpath(f'{client_name}.csr'))
        ]
        try:
            req_result = run(cmd_req, check=True, capture_output=True)
            sing_result = run(cmd_sign, check=True, capture_output=True)
        except CalledProcessError as e:
            log.error(e.stdout)
            log.error(e.stderr)
            sys.exit(1)


if __name__ == '__main__':

    ca = CA("/tmp/ca_data", "./openssl.cnf")
    ca.make_cert("user-1")


