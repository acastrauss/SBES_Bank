from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from OpenSSL import crypto
import modules.Certificates.selfSigned as selfSigned
import os

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

def EncryptText(text:str, key:RSA.RsaKey)->str:
    return PKCS1_OAEP.new(key).encrypt(text.encode('utf-8'))

def DecryptServerCAPublicKey(text:str, key:RSA.RsaKey)->str:
    return PKCS1_OAEP.new(key).decrypt(text.encode('utf-8'))