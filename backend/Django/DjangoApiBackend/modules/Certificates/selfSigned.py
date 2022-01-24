import OpenSSL.crypto
from os.path import join
import random


def makeCertAuthority():
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    CN = "certAuthority"
    pubkey = "%s.pem" % CN #replace %s with CN
    privkey = "%s.key" % CN # replcate %s with CN

    pubkey = join(".", pubkey)
    privkey = join(".", privkey)

    ca = OpenSSL.crypto.X509()
    ca.set_version(3)
    ca.set_serial_number(1)
    ca.get_subject().CN = "certAuthority"
    ca.gmtime_adj_notBefore(0)
    ca.gmtime_adj_notAfter(360 * 24 * 60 * 60)
    ca.set_issuer(ca.get_subject())
    ca.set_pubkey(key)
    ca.add_extensions([
    OpenSSL.crypto.X509Extension(b'basicConstraints', True,
                                b'CA:TRUE, pathlen:0' , ),
    OpenSSL.crypto.X509Extension(b'keyUsage', True,
                                b'keyCertSign, cRLSign'),
    OpenSSL.crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash',
                                subject=ca),
    ])
    ca.sign(key, "sha1")
    pub=OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, ca)
    priv=OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
    open(pubkey,"wt").write(pub.decode("utf-8"))
    open(privkey, "wt").write(priv.decode("utf-8") )

    return (pub,priv)


def getCertAuthorityName():
    CN = "certAuthority"
    return CN
   