#######################################################
# 
# BankNumbers.py
# Python implementation of the Class BankNumbers
# Generated by Enterprise Architect
# Created on:      29-Nov-2021 6:55:28 PM
# Original author: acast
# 
#######################################################
from BankConfig import (
    BankConfigParser
)
import random
import copy
from Enums.CreditCardProcessor import (
    CreditCardProcessor
)


class BankNumbers():
    def GenerateAccountNumber()-> str:
        digits = []
        conf = BankConfigParser()
        
        # first 3 digits is bank identifier
        digits.extend(
            BankNumbers.GetDigitsFromInt(
                conf.BankIdentifier
            )
        )

        digits.extend(
            BankNumbers.GetDigitsFromInt(
                random.randint(
                    pow(10, conf.BankAccountDigitsCount - 1), 
                    pow(10, conf.BankAccountDigitsCount) - 1 
                )
            )
        )
        num = 0

        for i in range(1, len(digits) + 1):
            # + 2 so check sum will be zero before set
            num += pow(10, i + 2) * digits[-i]

        checkDigits = BankNumbers.GetDigitsFromInt(num % 97)
        if(len(checkDigits) == 1):
            # if module is one digit number
            checkDigits.insert(0, 0)
        elif (len(checkDigits) == 0):
            checkDigits = [0, 0]

        digits = BankNumbers.GetDigitsFromInt(num)
        digits[-1] = checkDigits[1]
        digits[-2] = checkDigits[0]
        
        retStr = ''

        for i in range(len(digits)):
            retStr += f'{digits[i]}'
            if i == 2 or i == len(digits) - 3:
                retStr += '-'

        return retStr

    @staticmethod 
    def GetDigitsFromInt(a:int)->list[int]:
        temp = copy.deepcopy(a)
        digits = []
        while temp != 0:
            digits.insert(0, temp % 10)
            temp //= 10

        return digits

    @staticmethod
    def LuhnAlgorithm(digits:list[int]):
        """
            Algorithm for calculating check digit (last) on credit card:
            1. Starting form right multiple every second digit by 2 (including 0 index)
            2. Sum digits of each value at position
            3. Sum all the values
            4. Check digit is SUM % 10
            https://en.wikipedia.org/wiki/Luhn_algorithm
        """
        digitsCopy = copy.deepcopy(digits)

        # 1.
        for i in range(len(digitsCopy)):
            # right most digit will have index 14
            if i % 2 == 0:
                digitsCopy[-i] *= 2

        # 2. 
        for i in range(len(digitsCopy)):
            temp = copy.deepcopy(digitsCopy[i])
            digitsCopy[i] = sum(
                BankNumbers.GetDigitsFromInt(temp)
            )
        # 3. 
        digitsSum = sum(digitsCopy)

        # 4.
        digits.append(digitsSum % 10)

    @staticmethod
    def SetFirst6Digits(
        cardProcessor: CreditCardProcessor.CreditCardProcessor,
        digits:list[int]):
        
        """
            First digits represents credit cards processor (
                e.g. Visa, MasterCard, etc.
            )
            Next 5 digits represent bank number
        """
        config = BankConfigParser()
        
        if cardProcessor == CreditCardProcessor.CreditCardProcessor.AMERICAN_EXPRESS:
            digits.append(config.AmericanExpressStartDigit)
        elif cardProcessor == CreditCardProcessor.CreditCardProcessor.MASTER_CARD:
            digits.append(config.MasterCardStartDigit)
        else:
            digits.append(config.VisaStartDigit)
        
        digits.extend(BankNumbers.GetDigitsFromInt(
            config.BankCardDigits
        ))

    @staticmethod
    def AccountDigits(digits:list[int]):
        # check in db for uniqueness
        # six digit number
        
        digits.extend(
            BankNumbers.GetDigitsFromInt(
                random.randint(
                    pow(10, 8),
                    pow(10, 9) - 1
                )
            )
        )

    @staticmethod
    def GenerateCardNumber(cardProcessor: CreditCardProcessor.CreditCardProcessor)-> str:
        digits = []
        BankNumbers.SetFirst6Digits(cardProcessor, digits)
        BankNumbers.AccountDigits(digits)
        BankNumbers.LuhnAlgorithm(digits)
        retStr = ''
        for i in range(len(digits)):
            retStr += f'{digits[i]}'
            if i % 4 == 3:
                retStr += ' '

        return retStr

    def GenerateCVC(
        cardNumber: str, accountNumber: str
    )-> str:
        cn = int(cardNumber.replace(' ', '', -1)) 
        an = int(accountNumber.replace('-', '', -1))
        randLower = pow(10, 6)
        randHigher = pow(10, 7) - 1
        randHash = hash(random.randint(
            randLower, randHigher
        ))

        cvc = str(
            (cn + an + randHash) % 1000
        ).zfill(3)

        return cvc

    def GeneratePIN(
        cardNumber: str, accountNumber: str
    )-> str:
        cn = int(cardNumber.replace(' ', '', -1)) 
        an = int(accountNumber.replace('-', '', -1))
        randLower = pow(10, 6)
        randHigher = pow(10, 7) - 1
        randHash = hash(random.randint(
            randLower, randHigher
        ))

        pin = str(
            (cn + an + randHash) % 10000
        ).zfill(4)

        return pin

    def GenerateTransactionID()-> int:
        # extract next number from db
        pass
