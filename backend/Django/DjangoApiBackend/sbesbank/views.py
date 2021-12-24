
from typing import KeysView
from django.forms.widgets import ClearableFileInput
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import translation
from rest_framework.decorators import api_view
from Shared.Enums.CardType import CardType
# from Shared.Enums.CreditCardProcessor import CreditCardProcessor
from sbesbank.models import *
from sbesbank.serializers import *
from rest_framework import status
import json

# from Shared.BankNumbers import (
#     BankNumbers
# )
#from Shared.BankNumbers import *
from sbesbank.models import *
from datetime import datetime
from rest_framework.parsers import JSONParser

# Create your views here.


@api_view(['GET'])
def TrAcTransfer(request, id):
    obj=TrAcTransferInfo.objects.get(id=id)
    serializer=TrAcTransferInfoSerializer(obj) 

    return JsonResponse(serializer.data)


@api_view(['GET'])
def TrMyAcc(request):
    id = request.GET.get("id")
    obj = TrMyAccountInfo.objects.get(id=id)
    serializer = TrMyAccountInfoSerializer(obj) 
    
    return JsonResponse(serializer.data)



@api_view(['POST'])
def LogInUser(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    user = IUser.objects.get(
        username=body['username'],
        password=body['password']
    )

    print(user)

    client = Client.objects.get(
        userId=user
    )

    ser = ClientSerializer(client)

    return JsonResponse(ser.data)








@api_view(['GET'])
def Transact(request, id):
    obj = Transaction.objects.get(id=id)
    serializer = TransactionSerializer(obj) 

    return JsonResponse(serializer.data)


@api_view(['GET'])
def getClient(request, id):
    obj = Client.objects.get(id=id)
    serializer = ClientSerializer(obj) 

    return JsonResponse(serializer.data)


@api_view(['GET'])
def IUserData(request, id):
    obj1 = IUser.objects.get(id=id) 
    obj2 = Certificate.objects.get(userId=id)
    serializer1 =  IUserSerializer(obj1)
    serializer2 = CertificateSerializer(obj2)

    return JsonResponse(
        {
            "IUser": serializer1.data,
            "Certificate": serializer2.data
        }
    )


@api_view(['GET'])
def AccInfo(request):
    accId = request.GET.get("id")
    obj1 = list(Account.objects.filter(
        clientId=accId
    ))

    print(obj1)
    # obj1 = Account.objects.get(clientId_id=accId) 
    # obj2 = list(Card.objects.filter(accountFK=id))
    serializer1 =  AccountSerializer(obj1, many=True)
    # serializer2 = CardSerializer(obj2,many = True)
    return JsonResponse(
            serializer1.data, safe=False
            # "Cards": serializer2.data
    )


@api_view(['GET'])
def CertData(request, userId):
    obj = Certificate.objects.get(userId = userId)
    serializer = CertificateSerializer(obj)

    return JsonResponse(serializer.data)


@api_view(['GET'])
def AccTransactions(request, id):
    obj =list(TrMyAccountInfo.objects.filter(accountNumber = id))
    transactions = list()
    for x in obj:
        transactions+=Transaction.objects.filter(myAccInfoFK = x.id)
    serializer = TransactionSerializer(transactions,many = True) 

    return JsonResponse(serializer.data)


@api_view(['POST'])
def createUser(request):
    iuser_data = JSONParser().parse(request)
    iuser_serializer = IUserSerializer(data = iuser_data)
    if iuser_serializer.is_valid():
        iuser_serializer.save()
        return JsonResponse(iuser_serializer.data)
    return JsonResponse(
        iuser_serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def createClient(request):
    client_data = JSONParser().parse(request)
    userr = IUser.objects.get(id = client_data['userId'])
    client = Client()
    client.userId = userr
    client.save()
    idd = Client.objects.get(userId=client.userId)
    # povratna = idd.id
    serialized_data = ClientSerializer(client)
    return JsonResponse(serialized_data.data)


@api_view(['POST'])
def createAccount(request):
    account_data = JSONParser().parse(request)
    account_serializer = AccountSerializer(data = account_data)
    if account_serializer.is_valid():
        account_serializer.save()
        return JsonResponse(account_serializer.data)
    else:
        return JsonResponse(
            account_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createNewClientAccount(request):
    iuser_data = JSONParser().parse(request)
    iuser_serializer = IUserSerializer(data = iuser_data)
    if iuser_serializer.is_valid():
        iuser_serializer.save()
        userr = IUser.objects.get(id = iuser_data['id'])
        client = Client()
        client.userId = userr
        client.save()
        account = Account()
        account = createAccount()
        client1 = Client.objects.get(userId =iuser_data['id'])
        ids = Account.objects.values('id')
        account.id = ids.order_by('-id').first()['id'] + 1 
        account.clientId = client1
        account.save()
        # card = createCard(userr.fullName,CardType.DEBIT,account.accountNumber)
        # card.accountFK = account
        # idss = Card.objects.values('id')
        # card.id = idss.order_by('-id').first()['id'] + 1
        # card.save()
        return JsonResponse(iuser_serializer.data)
    else:
        return JsonResponse(
            iuser_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# @api_view(['POST'])
# def createAccount():
#     account = Account()
#     account.accountBalance = 0.0
#     account.accountNumber = BankNumbers.GenerateAccountNumber()
#     account.blocked = False
#     account.currency = Currency.RSD
#     account.dateCreated = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
#     return account


# @api_view(['POST'])
# def createCard(cardHolder,cardType,accountNumber):
#     card = Card()
#     card.cardHolder= cardHolder
#     card.cardNumber = BankNumbers.GenerateCardNumber(cardProcessor= CreditCardProcessor.CreditCardProcessor.MASTER_CARD)
#     card.cardProcessor = CreditCardProcessor.CreditCardProcessor.MASTER_CARD
#     card.pin = BankNumbers.GeneratePIN(card.cardNumber,accountNumber)
#     card.validUntil =  (datetime.now()).strftime("%Y-%m-%d")
#     card.cardType = cardType
#     return card
#       return JsonResponse(iuser_serializer.errors, status
#        = status.HTTP_400_BAD_REQUEST)
#

@api_view(['POST'])
def AddTransaction(request):
    transaction_data = JSONParser().parse(request) 
    myacc = transaction_data['myAccInfoFK']
    tracc = transaction_data['transferAccInfoFK']
    paymentCod= transaction_data['paymentCodeFK']
    pym = PaymentCode.objects.get(code = paymentCod['code'])
    myacc_serializer = TrMyAccountInfoSerializer(data = myacc)
    tracc_serializer = TrAcTransferInfoSerializer(data = tracc)
    
    if myacc_serializer.is_valid():
        myacc_serializer.save()
        if tracc_serializer.is_valid():
            tracc_serializer.save()
            # transact.paymentCodeFK = pym
            # transact.paymentPurpose = transaction_data['paymentPurpose']
            # transact.amount = transaction_data['amount']
            # transact.modelCode = transaction_data['modelCode']
            # transact.paymentPurpose = transaction_data['paymentPurpose']
            # transact.provision = transaction_data['provision']
            # transact.preciseTime = transaction_data['preciseTime']
                
            idtrac = TrAcTransferInfo.objects.values('id')
            idmyac = TrMyAccountInfo.objects.values('id')
            idtr = Transaction.objects.values('id')

           # transaction_serializer.paymentCodeFK = PaymentCodeSerializer(data = pym)
            transferAccInfoFK = TrAcTransferInfo.objects.get(id= idtrac.order_by('-id').first()['id'])
            myAccInfoFK = TrMyAccountInfo.objects.get(id = idmyac.order_by('-id').first()['id'])
            #transaction_serializer.id = 
            idtrr = idtr.order_by('-id').first()['id'] + 1
            typetr = 0
            if transaction_data['transactionType']=='INFLOW':
                typetr = 0
            else:
                typetr = 1
            currencyId = 0
            if transaction_data['currency']=='USD':
                currencyId = 1
            elif transaction_data['currency']=='EUR':
                currencyId = 2
            elif transaction_data['currency']=='CHF':
                currencyId = 3
            elif transaction_data['currency']=='GBP':
                currencyId = 4
            elif transaction_data['currency']=='RUB':
                currencyId = 5
            elif transaction_data['currency']=='CNY':
                currencyId = 6
            elif transaction_data['currency']=='CAD':
                currencyId = 7
            elif transaction_data['currency']=='AUD':
                currencyId = 8
            elif transaction_data['currency']=='RSD':
                currencyId = 9

            transaction = Transaction.objects.create(
                id = idtrr,
                amount =transaction_data['amount'],
                modelCode = transaction_data['modelCode'],
                paymentCodeFK = pym,
                paymentPurpose = transaction_data['paymentPurpose'],
                preciseTime = transaction_data['preciseTime'], 
                provision = transaction_data['provision'],
                referenceNumber = transaction_data['referenceNumber'],
                transactionType = Transaction.TRANSACTION_TYPE[typetr][1],
                currency = Currency(currencyId),
                myAccInfoFK = myAccInfoFK,
                transferAccInfoFK = transferAccInfoFK
            )
            
            transaction.save()
            return JsonResponse(transaction_data)
        else:
            return JsonResponse(tracc_serializer.errors, status
        = status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(myacc_serializer.errors, status
    = status.HTTP_400_BAD_REQUEST)
    
