from django.forms.fields import TypedChoiceField
from rest_framework import serializers
from sbesbank.models import *
from django.db.models import *
class PaymentCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCode
        fields = [
            'code',
            'description'
        ]

class ExchangeRateSerializer(serializers.ModelSerializer):
    currency = EnumChoiceField(
        enum_class=Currency
    )
    
    class Meta:
        model = ExchangeRate
        fields = [
            'currency',
            'rateInDinar',
            'dateModified'
        ]
        

class TrAcTransferInfoSerializer(serializers.ModelSerializer):
    """
        This is NOT the account from current client, that is:\n
        If client is sending money, this is TARGET account\n
        If client is receiving money, this is SOURCE account
    """
    class Meta:
        model = TrAcTransferInfo
        fields = [
            'id',
            'accountNumber', 
            'billingAddress', 
            'fullName'
            ]

    accountNumber = serializers.CharField(
        max_length=25
    )

    billingAddress = serializers.CharField(
        max_length=50
    )

    fullName = serializers.CharField(
        max_length=50
    )


class TrMyAccountInfoSerializer(serializers.ModelSerializer):
    """
        This is the account from current client, that is:\n
        If client is sending money, this is SOURCE account\n
        If client is receiving money, this is TARGET account
    """
    
    class Meta:
        model = TrMyAccountInfo
        fields = [
            'id',
            'balanceBefore',
            'balanceAfter',
            'accountNumber',
            'billingAddress',
            'fullName'
        ]

    balanceBefore = serializers.FloatField()

    balanceAfter = serializers.FloatField()

    accountNumber = serializers.CharField(
        max_length=25
    )

    billingAddress = serializers.CharField(
        max_length=50
    )

    fullName = serializers.CharField(
        max_length=50
    )


class TransactionSerializer(serializers.ModelSerializer):
    transferAccInfoFK = TrAcTransferInfoSerializer()
    myAccInfoFK = TrMyAccountInfoSerializer()
    paymentCodeFK = PaymentCodeSerializer()
    class Meta:
        model = Transaction
        fields = [
            'id',
            'amount',
            'modelCode',
            'paymentCodeFK',
            'paymentPurpose',
            'preciseTime',
            'provision',
            'referenceNumber',
            'transactionType',
            'currency',
            'myAccInfoFK',
            'transferAccInfoFK'
        ]

    amount = serializers.FloatField()

    modelCode = serializers.IntegerField(
        default=None
    )

    paymentPurpose = serializers.CharField(
        default=None,
    )

    preciseTime = serializers.DateTimeField(
        default=datetime.today()
    )

    provision = serializers.FloatField()

    referenceNumber = serializers.CharField(
        max_length=50,
    )

    TRANSACTION_TYPE = (
        ('INFLOW','INFLOW'),
        ('OUTFLOW','INFLOW')
    )

    transactionType = TypedChoiceField(
        choices=TRANSACTION_TYPE
    )

    currency = EnumChoiceField(
        enum_class=Currency
    )
    
class CardSerializer2(serializers.ModelSerializer):
    """
        Card model\n
        CVC and PIN are save as Hash (SHA256) values
    """
    class Meta:
        model = Card
        fields = [
            'id',
            'cardHolder',
            'cardNumber',
            'cvc',
            'pin',
            'cardProcessor',
            'cardType',
            'validUntil'
        ]

class IUserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = IUser
        fields = [
            'id',
            'fullName',
            'password',
            'username',
            'email',
            'billingAddress',
            'gender',
            'jmbg',
            'birthDate',
            'userType',
        ]
    
    def create(self, validated_data):
        """
        Create and return a new User instance
        """
        return IUser.objects.create(**validated_data)
    

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client

        fields = [
            'id',
            'userId'
        ]

        depth = 1
    
    
    def create(self, validated_data):
        """
        Create and return a new User instance
        """
        validated_data.userId= validated_data.userId['id']
        return Client.objects.create(**validated_data)
        

class AccountSerializer(serializers.ModelSerializer):
   
    clientId = ClientSerializer()

    class Meta:
        model = Account
        fields = [
            'id',
            'accountBalance',
            'accountNumber',
            'blocked',
            'currency',
            'dateCreated',
            'clientId'
        ]


class CardSerializer2(serializers.ModelSerializer):
    """
        Card model\n
        CVC and PIN are save as Hash (SHA256) values
    """
    class Meta:
        model = Card
        fields = [
            'id',
            'cardHolder',
            'cardNumber',
            'cvc',
            'pin',
            'cardProcessor',
            'cardType',
            'validUntil'
        ]


class CardSerializer(serializers.ModelSerializer):
    """
        Card model\n
        CVC and PIN are save as Hash (SHA256) values
    """
    
    accountFK = AccountSerializer()
    class Meta:
        model = Card
        fields = [
            'id',
            'cardHolder',
            'cardNumber',
            'cvc',
            'pin',
            'cardProcessor',
            'cardType',
            'validUntil',
            'accountFK'
        ]

    cardHolder = serializers.CharField(
        max_length=100
    )

    cardNumber = serializers.CharField(
        max_length=20
    )

    """
        Hash value has 64 length
    """
    cvc = serializers.CharField(
        max_length=64
    )

    """
        Hash value has 64 length
    """
    pin = serializers.CharField(
        max_length=64
    )

    CARD_PROCESSOR = [
        ('VISA','VISA'),
        ('MASTER_CARD','MASTER_CARD'),
        ('AMERICAN_EXPRESS','AMERICAN_EXPRESS')
    ]
    
    cardProcessor = TypedChoiceField(
        choices=CARD_PROCESSOR
    )

    CARD_TYPE = [
        ('DINA', 'DINA'),
        ('CREDIT', 'CREDIT')
    ]

    cardType = TypedChoiceField(
        choices=CARD_TYPE
    )

    validUntil = serializers.DateField()


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'userId',
            'authorityName',
            'pemPath',
            'keyPath',
            'certificateName'
        ]



