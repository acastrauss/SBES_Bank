from django.db.models import fields
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


class CardSerializer(serializers.ModelSerializer):
    pass


class TransactionSerializer(serializers.ModelSerializer):
    pass


class AccountSerializer(serializers.ModelSerializer):
    currency = EnumChoiceField(
        enum_class=Currency
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