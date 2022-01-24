from typing import ByteString

from OpenSSL import crypto
import modules.Certificates.selfSigned as selfSigned
import os

from Crypto.Hash import SHA256
   
import base64
import rsa as rsakey
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import Crypto.Signature.pkcs1_15 as crypto_sign
import gmpy2
from gmpy2 import mpz, mpq, mpfr, mpc, powmod

def getPathForDB(path)->str:
    '''
        Splits path for certificate\n
        and returns relative path to server main dir
    '''
    pathForDB = path.split('DjangoApiBackend\\')[1]
    return pathForDB

def getAbsolutePath(dbPath)->str:
    '''
        Returns absoulte path
    '''
    absPath = os.path.join(os.getcwd(), dbPath)
    return absPath

def GetCertificateFilePath(public:bool, username:str=None)->str:
    '''
        If public, returns public key, else returns private\n
        If username is not None returns given key for user\n
        Else returns CA key
    '''

    listPath = [os.getcwd(), 'modules', 'Certificates']
    extension = '.pem' if public else '.key'

    cerPath:str = ""

    if username:        
        cerPath = os.path.join(
            listPath[0],
            listPath[1],
            listPath[2],
            'UserCertificates',
            username + extension
        )

        print(cerPath)

    else:
        CN = selfSigned.getCertAuthorityName()

        cerPath = os.path.join(
            listPath[0],
            listPath[1],
            listPath[2],
            CN + extension
        )
    
    return cerPath
    

def LoadCert(path:str)->crypto.X509:
    '''
        Path to certificate
        Public if cert
    '''
    caCert:crypto.X509 = None

    with open(path) as fCA:
        caCert = crypto.load_certificate(
            crypto.FILETYPE_PEM, fCA.read()
        )

    return caCert

def LoadKey(path:str)->RSA.RsaKey:
    '''
        Loads key (public or private)
    '''
    caKey:RSA.RsaKey = None

    with open(path) as fCA:
        caKey = RSA.import_key(fCA.read())

    return caKey

def EncryptTextRSA(text:str, key:RSA.RsaKey)->str:
    return PKCS1_v1_5.new(key).encrypt(text.encode('utf-8'))

def DecryptTextRSA(text:str, key:RSA.RsaKey)->str:
    """Decrypt's the given string input. The library works on bytes."""
    message_bytes = text.encode("utf-8")
    cipher = PKCS1_v1_5.new(key)
    decrypted_bytes = cipher.decrypt(base64.b64decode(message_bytes), "dummy text")
    # convert the bytes to string and return
    return decrypted_bytes.decode("utf-8")


def CheckUserSignature(username:str, message:str, signature:str)->bool:
    return True
    # try:
    #     userPublicKey = LoadKey(
    #         GetCertificateFilePath(True, username)
    #     )

    #     userPrivateKey = LoadKey(
    #         GetCertificateFilePath(False, username)
    #     )
    # except Exception:
    #     return False

    # # decpr = DecryptTextRSA(signature, userPublicKey)

    # if(userPublicKey is None): # user doesn't exists
    #     return False
    # else:
    #     s = SHA256.new()
    #     s.update(message.encode())
    #     c = int.from_bytes(signature.encode(), 'little')
    #     print(c)
    #     print(userPrivateKey.d)
    #     print(userPublicKey.n)
    #     ctx = gmpy2.get_context()

    #     gc = mpz(c)
    #     gd = mpz(userPrivateKey.d)
    #     temp = gc ** gd
    #     print(temp)
    #     # m = pow(c, userPrivateKey.d) % userPublicKey.n
    #     # tryHash = int.to_bytes(m).decode('utf-8')
    #     print("Hashed:" + s.digest())
    #     # print("Decrypted:" + int.to_bytes(m))
    #     return True
    #     # return int.to_bytes(m) == s.digest()
    #     # signValidator = crypto_sign.new(userPublicKey)
    #     # try:
    #     #     signValidator.verify(s.copy(), signature.encode())
    #     #     return True
    #     # except ValueError as e:
    #     #     return False