from rest_framework import serializers 
from sbesbank.models import *

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
            'rateInDinar'
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
        max_length=20
    )

    billingAddress = serializers.CharField(
        max_length=50
    )

    fullName = serializers.CharField(
        max_length=50
    )


class TrMyAccountInfoSerializer(serializers.serializerserializer):
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
            'balaceAfter',
            'accountNumber',
            'billingAddress',
            'fullName'
        ]

    balanceBefore = serializers.FloatField()

    balanceAfter = serializers.FloatField()

    accountNumber = serializers.CharField(
        max_length=20
    )

    billingAddress = serializers.CharField(
        max_length=50
    )

    fullName = serializers.CharField(
        max_length=50
    )


class CardSerializer(serializers.ModelSerializer):
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
            'validUntil'
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

    cardProcessor = serializers.CharField(
        max_length = 30,
        choices=CARD_PROCESSOR
    )

    validUntil = serializers.DateField()


class TransactionSerializer(serializers.ModelSerializer):
    trAcTransferInfo = TrAcTransferInfoSerializer()
    trMyAccountInfo = TrMyAccountInfoSerializer()
    paymentCode = PaymentCodeSerializer()
    class Meta:
        model = Transaction
        fields = [
            'id',
            'amount',
            'modelCode',
            'paymentPurpose',
            'preciseTime',
            'provision',
            'referenceNumber',
            'transactionType',
            'currency',

        ]

    amount = serializers.FloatField()

    modelCode = serializers.IntegerField(
        blank=True,
        null=True,
        default=None,
        max_length=2
    )

    paymentPurpose = serializers.CharField(
        blank=True,
        null=True,
        default=None,
        max_length=70
    )

    preciseTime = serializers.DateTimeField(
        default=datetime.today()
    )

    provision = serializers.FloatField(
        null=True     
    )

    referenceNumber = serializers.CharField(
        blank=True,
        null=True,
        max_length=50,
        default=None
    )

    TRANSACTION_TYPE = (
        ('INFLOW','INFLOW'),
        ('OUTFLOW','INFLOW')
    )

    transactionType = serializers.CharField(
        max_length = 30,
        choices=TRANSACTION_TYPE
    )

    currency = serializers.CharField(
        max_length = 20,
        choices=[
            (tag, tag.value) for tag in Currency
        ]
    )


class AccountSerializer(serializers.ModelSerializer):
    currency = EnumChoiceField(
        enum_class=Currency
    )
    
    querysetCards = Card().objects.all()
    accounts = CardSerializer(
        querysetCards, many=True
    )

    querysetTransactions = Transaction().objects.all()
    transactions = TransactionSerializer(
        querysetTransactions, many=True
    )

    class Meta:
        model = Account
        fields = [
            'accountBalance',
            'accountNumber',
            'blocked',
            'currency',
            'dateCreated'
        ]


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'authorityName',
            'cerPath',
            'pfxPath',
            'pvkPath',
            'certificateName'
        ]


class IUserSerializer(serializers.ModelSerializer):
    
    certificate = CertificateSerializer()

    class Meta:
        model = IUser
        fields = [
            'id',
            'fullName',
            'password',
            'username',
            'billingAddress',
            'gender',
            'jmbg',
            'birthDate',
            'userType'
        ]
    
    def create(self, validated_data):
        """
        Create and return a new User instance
        """
        return models.objects.create(**validated_data)
    

class ClientSerializer(serializers.ModelSerializer):
    queryset = Account().objects.all()
    accounts = AccountSerializer(
        queryset, many=True
    )

    class Meta:
        model = Client

        fields = [
            'user'
        ]

        depth = 1

