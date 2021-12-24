import OpenSSL.crypto as crypto
# from Shared.BankConfig import (
#     BankConfigParser
# )

bankName = "sbesbank"
yearsValid = 1

class Certificates():
    
    caName = bankName + "CA"
        
    def CreateBankCA():
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        ca = crypto.X509()
        ca.set_version(0)
        ca.set_serial_number(1)
        ca.get_subject().CN = Certificates.caName
        ca.gmtime_adj_notBefore(0)
        ca.gmtime_adj_notAfter(yearsValid * 365 * 24 * 3600)
        ca.set_issuer(ca.get_subject())
        ca.set_pubkey(key)
        ca.add_extensions([
        crypto.X509Extension(str.encode("basicConstraints"), True,
                                    str.encode("CA:TRUE, pathlen:0")),
        crypto.X509Extension(str.encode("keyUsage"), True,
                                    str.encode("keyCertSign, cRLSign")),
        crypto.X509Extension(str.encode("subjectKeyIdentifier"), False,
                                    str.encode("hash"),
                                    subject=ca),
        ])
        ca.sign(key, "sha256")
        
        with open('sbesCA.pem', 'wb') as f:
            f.write(ca.to_cryptography().tbs_certificate_bytes)

    def CertificateUsingCA():
        ca_cert = crypto.load_certificate(
            crypto.FILETYPE_PEM,
            open("sbesCA.pem", 'rb').read()
        )
        ca_key = crypto.load_privatekey(
            crypto.FILETYPE_PEM,
            open("sbesCA.pem", 'rb').read()
        )

        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()
        cert.get_subject().CN = "client1"
        cert.set_serial_number(1)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(yearsValid * 365 * 24 * 3600)
        cert.set_issuer(ca_cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(ca_key, "sha256")

Certificates.CreateBankCA()
Certificates.CertificateUsingCA()
