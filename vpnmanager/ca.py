from pathlib import Path

class CA:
    def __init__(self, ca_data_path: str, open_ssl_config_path: str):
        self.ca_dir: Path = Path(ca_data_path).resolve()
        self.ssl_cfg: Path = Path(open_ssl_config_path).resolve()

    def make_ca(self):
        #self._prep_data_dir()
        self._prep_ca_cert_key()

    def _prep_data_dir(self):
        self.ca_dir.mkdir(0o755)
        index_file = self.ca_dir.joinpath("index.txt").touch(0o644)
        with self.ca_dir.joinpath("serial").open("wt") as fp:
            fp.write("01\n")

    def _prep_ca_cert_key(self):
        cmd = [
            "openssl", "req",
            "-new", "-newkey", "rsa:4096", 
            "-days", "3650", "nodes", "-x509",
            "-extensions", "easyrsa_ca",
            "-keyout", str(self.ca_dir.joinpath("ca.key")),
            "-out", str(self.ca_dir.joinpath("ca.crt")),
            "-config", str(self.ssl_cfg),
            "-subj", "/C=KG/ST=NA/L=BISHKEK/O=OpenVPN-TEST/emailAddress=me@myhost.mydomain" #!TODO убрать 
        ]

    def issue_cert(self):
        pass

    def revoke_cert(self):
        pass

if __name__ == '__main__':

    ca = CA("/tmp/ca_data", "./openssl.cnf")
    ca.make_ca()
