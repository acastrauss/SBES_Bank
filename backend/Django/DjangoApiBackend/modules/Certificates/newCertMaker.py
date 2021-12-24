import OpenSSL
from os.path import join
import random
import selfSigned

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def NewUserCert(username):
    CN = selfSigned.getCertAuthorityName()

    with open(CN + ".pem", "r") as f:
        cert_buf = f.read()
    with open(CN + ".key", "r") as f:
        key_buf  = f.read()
    ca_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_buf)
    ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key_buf)

    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    cert = OpenSSL.crypto.X509()
    cert.get_subject().CN = username
    cert.set_serial_number(1)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(360 * 24 * 60 * 60)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(ca_key, "sha1")

    pub=OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    open(username +'.pem', "wt").write(pub.decode("utf-8"))
    priv=OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
    open(username +'.key', "wt").write(priv.decode("utf-8") )

    return (pub,priv)