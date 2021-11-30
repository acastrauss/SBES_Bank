#######################################################
# 
# Certificate.py
# Python implementation of the Class Certificate
# Generated by Enterprise Architect
# Created on:      29-Nov-2021 6:55:28 PM
# Original author: acast
# 
#######################################################


class Certificate():
    def __init__(
        self,
        certificateName: str,
        authorityName: str,
        cerPath: str,
        pfxPath: str,
        pvkPath: str
        ) -> None:
        
        self.certificateName = certificateName
        self.authorityName = authorityName
        self.cerPath = cerPath
        self.pfxPath = pfxPath
        self.pvkPath = pvkPath

    def ValidateCertificate(self)->bool:
        pass