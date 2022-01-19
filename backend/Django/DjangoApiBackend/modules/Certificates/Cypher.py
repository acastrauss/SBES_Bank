from typing import ByteString

from OpenSSL import crypto
import modules.Certificates.selfSigned as selfSigned
import os


   
import base64

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5 as sign

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
    userPublicKey = LoadKey(
        GetCertificateFilePath(True, username)
    )

    if(userPublicKey is None): # user doesn't exists
        return False
    else:
        signValidator = sign.new(userPublicKey)
        try:
            signValidator.verify(SHA256.new(data=message), signature.encode('utf-8'))
            return True
        except ValueError:
            return False

        # hashedMsg = SHA256.new(data=message).hexdigest().decode('utf-8')

        # decrypted = DecryptTextRSA(
        #     signature, userPublicKey
        # )

        # return hashedMsg == decrypted