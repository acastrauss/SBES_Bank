from django.db import models
from django.db.models.fields import DateField
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import FloatField
from enumchoicefield import ChoiceEnum, EnumChoiceField

from enum import Enum
from datetime import (
    date,
    datetime
)


class IUser(models.Model):
    fullName = models.CharField(max_length = 50, unique=False)
    password = models.CharField(max_length = 64)
    """
        Hash value has 64 length
    """
    
    username = models.CharField(max_length = 40, unique = True)
    billingAddress = models.CharField(max_length = 50 )
    genders = (('female','female'), ('male','male'))
    gender = models.CharField(choices = genders, max_length = 20)
    jmbg = models.BigIntegerField(unique = True)
    birthDate  = models.DateField()
    userTypes = (('admin','admin'),('client','client'))
    userType = models.CharField(choices = userTypes, max_length = 40)

    class Meta:
        db_table = "iuser"

class Client(models.Model):
    userId = models.ForeignKey(IUser, on_delete = models.CASCADE, unique = True)
    class Meta:
        db_table = "client"

class Certificate(models.Model):
    """
        User certificates to cipher paths!
    """
    userId = models.ForeignKey(IUser, on_delete = models.CASCADE, unique = True)
    authorityName = models.CharField(max_length = 50)
    cerPath = models.CharField(max_length = 200, unique = True)
    pfxPath = models.CharField(max_length = 200, unique = True)
    pvkPath = models.CharField(max_length = 200, unique = True)
    certificateName = models.CharField(max_length = 100, unique = True)
    class Meta:
        db_table = "certificate"


class Currency(ChoiceEnum):
    USD = "USA Dollar"
    EUR = "Euro"
    CHF = "Swiss franc"
    GBP = "British pound"
    RUB = "Russian rouble"
    CNY = "Chinese Yuan Renminbi"
    CAD = "Canadian dollar"
    AUD = "Australian dollar"
    RSD = "Serbian dinar"



class PaymentCode(models.Model):
    """
        Represents payment code with description
        (
            source:
            https://nbs.rs/sr/drugi-nivo-navigacije/servisi/sistem-veb-servisa-NBS/
        )
    """
    
    code = models.PositiveSmallIntegerField(
        max_length=3,
        primary_key=True
    )

    description = models.CharField(
        max_length=100
    )
    class Meta:
        db_table = "paymentcode"


class ExchangeRate(models.Model):
    """
        Exchange rates
        (
            source:
            https://nbs.rs/sr/drugi-nivo-navigacije/servisi/sistem-veb-servisa-NBS/
        )
    """
  
    currency = EnumChoiceField(
        enum_class=Currency
    )
    
    rateInDinar = models.FloatField()
    class Meta:
        db_table = "exchangerate"


class TrAcTransferInfo(models.Model):
    """
        This is NOT the account from current client, that is:\n
        If client is sending money, this is TARGET account\n
        If client is receiving money, this is SOURCE account
    """

    accountNumber = models.CharField(
        max_length=20
    )

    billingAddress = models.CharField(
        max_length=50
    )

    fullName = models.CharField(
        max_length=50
    )
    class Meta:
        db_table = "tractransferinfo"


class TrMyAccountInfo(models.Model):
    """
        This is the account from current client, that is:\n
        If client is sending money, this is SOURCE account\n
        If client is receiving money, this is TARGET account
    """

    balanceBefore = models.FloatField()

    balanceAfter = models.FloatField()

    accountNumber = models.CharField(
        max_length=20
    )

    billingAddress = models.CharField(
        max_length=50
    )

    fullName = models.CharField(
        max_length=50
    )
    class Meta:
        db_table = "trmyaccountinfo"


class Account(models.Model):
    clientId = models.ForeignKey(Client, on_delete = PROTECT, unique = True)
    accountBalance = models.FloatField()

    accountNumber = models.CharField(
        max_length=20
    )

    blocked = models.BooleanField(
        default=False
    )

    currency = EnumChoiceField(
        enum_class=Currency
    )

    dateCreated = models.DateTimeField(
        default=datetime.today()
    )
    class Meta:
        db_table = "account"


class Card(models.Model):
    """
        Card model\n
        CVC and PIN are save as Hash (SHA256) values
    """
    
    cardHolder = models.CharField(
        max_length=100
    )

    cardNumber = models.CharField(
        max_length=20
    )

    cvc = models.CharField(
        max_length=64
    )
    """
        Hash value has 64 length
    """
    
    pin = models.CharField(
        max_length=64
    )
    """
        Hash value has 64 length
    """
    
    CARD_PROCESSOR = [
        ('VISA','VISA'),
        ('MASTER_CARD','MASTER_CARD'),
        ('AMERICAN_EXPRESS','AMERICAN_EXPRESS')
    ]

    cardProcessor = models.CharField(
        max_length = 30,
        choices=CARD_PROCESSOR
    )

    validUntil = models.DateField()

    accountFK = models.ForeignKey(
        Account,
        on_delete=models.PROTECT
    )
    class Meta:
        db_table = "card"


class Transaction(models.Model):
    amount = models.FloatField()

    modelCode = models.IntegerField(
        blank=True,
        null=True,
        default=None,
        max_length=2
    )

    paymentPurpose = models.CharField(
        blank=True,
        null=True,
        default=None,
        max_length=70
    )

    preciseTime = models.DateTimeField(
        default=datetime.today()
    )

    provision = models.FloatField(
        null=True     
    )

    referenceNumber = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        default=None
    )

    TRANSACTION_TYPE = (
        ('INFLOW','INFLOW'),
        ('OUTFLOW','INFLOW')
    )

    transactionType = models.CharField(
        max_length = 30,
        choices=TRANSACTION_TYPE
    )

    currency = EnumChoiceField(
        enum_class=Currency
    )
    
    paymentCodeFK = models.ForeignKey(
        PaymentCode,
        on_delete=models.PROTECT,
    )

    myAccInfoFK = models.ForeignKey(
        TrMyAccountInfo,
        on_delete=models.PROTECT,
    )

    transferAccInfoFK = models.ForeignKey(
        TrAcTransferInfo,
        on_delete=models.PROTECT,
    )
    class Meta:
        db_table = "transaction"

