from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.fields import FloatField

from enum import Enum
from datetime import (
    date,
    datetime
)

class Currency(Enum):
    USD = "USA Dollar"
    EUR = "Euro"
    CHF = "Swiss franc"
    GBP = "British pound"
    RUB = "Russian rouble"
    CNY = "Chinese Yuan Renminbi"
    CAD = "Canadian dollar"
    AUD = "Australian dollar"
    RSD = "Serbian dinar"

# Create your models here.


class PaymentCode(models.Model):
    """
        Represents payment code with description
        (
            source:
            https://nbs.rs/sr/drugi-nivo-navigacije/servisi/sistem-veb-servisa-NBS/
        )
    """
    
    code = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        max_length=3,
        primary_key=True
    )

    description = models.CharField(
        blank=False,
        null=False,
        max_length=100
    )


class ExchangeRate(models.Model):
    """
        Exchange rates
        (
            source:
            https://nbs.rs/sr/drugi-nivo-navigacije/servisi/sistem-veb-servisa-NBS/
        )
    """
    
    currency = models.CharField(
        choices=[
            (tag, tag.value) for tag in Currency
        ],
        blank=False,
        null=False,
        primary_key=True
    )

    rateInDinar = models.FloatField(
        blank=False,
        null=False
    )


class TrAcTransferInfo(models.Model):
    """
        This is NOT the account from current client, that is:\n
        If client is sending money, this is TARGET account\n
        If client is receiving money, this is SOURCE account
    """

    accountNumber = models.CharField(
        blank=False,
        null=False,
        max_length=20
    )

    billingAddress = models.CharField(
        blank=False,
        null=False,
        max_length=50
    )

    fullName = models.CharField(
        blank=False,
        null=False,
        max_length=50
    )


class TrMyAccountInfo(models.Model):
    """
        This is the account from current client, that is:\n
        If client is sending money, this is SOURCE account\n
        If client is receiving money, this is TARGET account
    """

    balanceBefore = models.FloatField(
        blank=False,
        null=False
    )

    balanceAfter = models.FloatField(
        blank=False,
        null=False
    )

    accountNumber = models.CharField(
        blank=False,
        null=False,
        max_length=20
    )

    billingAddress = models.CharField(
        blank=False,
        null=False,
        max_length=50
    )

    fullName = models.CharField(
        blank=False,
        null=False,
        max_length=50
    )


class Account(models.Model):
    accountBalance = models.FloatField()

    accountNumber = models.CharField(
        max_length=20
    )

    blocked = models.BooleanField(
        default=False
    )

    currency = models.CharField(
        choices=[
            (tag, tag.value) for tag in Currency
        ]
    )

    dateCreated = models.DateTimeField(
        default=datetime.today()
    )


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

    """
        Hash value has 64 length
    """
    cvc = models.CharField(
        max_length=64
    )

    """
        Hash value has 64 length
    """
    pin = models.CharField(
        max_length=64
    )

    CARD_PROCESSOR = (
        ('VISA'),
        ('MASTER_CARD'),
        ('AMERICAN_EXPRESS')
    )

    cardProcessor = models.CharField(
        choices=CARD_PROCESSOR
    )

    validUntil = models.DateField()

    accountFK = models.ForeignKey(
        Account,
        on_delete=models.PROTECT
    )


class Transaction(models.Model):
    amount = models.FloatField(
        
    )

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
        ('INFLOW'),
        ('OUTFLOW')
    )

    transactionType = models.CharField(
        choices=TRANSACTION_TYPE
    )

    currency = models.CharField(
        choices=[
            (tag, tag.value) for tag in Currency
        ]
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

