import os
import configparser


class BankConfigParser():
    def __init__(self) -> None:
        configFile = os.path.join(
            os.getcwd(), 'Shared', 'bankConfig.ini'
        )

        if os.path.isfile(configFile):
            config = configparser.ConfigParser()
            config.read(configFile)
            try:
                # bank bussines info
                confDict = config['BankInfo']
                self.AccountMaintanceCost = float(confDict[str('AccountMaintanceCost').lower()])
                self.ProvisionPercentage = float(confDict[str('ProvisionPercentage').lower()])
                self.CardValidityYears = int(confDict[str('CardValidityYears').lower()])

                # bank cards info
                confDict = config['CardInfo']
                self.AmericanExpressStartDigit = int(confDict[str('AmericanExpressStartDigit').lower()])
                self.VisaStartDigit = int(confDict[str('VisaStartDigit').lower()])
                self.MasterCardStartDigit = int(confDict[str('MasterCardStartDigit').lower()])
                self.BankCardDigits = int(confDict[str('BankCardDigits').lower()])

                # bank account info
                confDict = config['AccountInfo']
                self.BankIdentifier = int(confDict[str('BankIdentifier').lower()])
                self.BankAccountDigitsCount = int(confDict[str('BankAccountDigitsCount').lower()])

            except Exception:
                print(
                    f'Not all keys found in bank config file: {configFile}'
                    )
        else:
            raise Exception(
                f'Bank config file not found at path {configFile}'
                )