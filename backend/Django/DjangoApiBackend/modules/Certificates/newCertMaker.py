from OpenSSL import crypto
import os
import random

from modules.Certificates import selfSigned

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def NewUserCert(path,username):
    CN = selfSigned.getCertAuthorityName()
    
    with open(os.path.join(path, CN + ".pem"), "r") as f:
        cert_buf = f.read()
    with open(os.path.join(path, CN + ".key"), "r") as f:
        key_buf  = f.read()
    
    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_buf)
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_buf)
    
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    cert.get_subject().CN = username
    cert.set_serial_number(1)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(360 * 24 * 60 * 60)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(ca_key, "sha1")

    path = os.path.join(
        path, "UserCertificates"
    )

    pub=crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    cert_path = os.path.join(path, username + '.pem')
    with open(cert_path, "wt") as fcer: 
        fcer.write(pub.decode("utf-8"))
    priv=crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
    key_path = os.path.join(path, username + '.key')
    with open(key_path, "wt") as fkey: 
        fkey.write(priv.decode("utf-8"))

    return (cert_path, key_path)