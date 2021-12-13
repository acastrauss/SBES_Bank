
from django.forms.widgets import ClearableFileInput
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from Shared.Enums.CardType import CardType
from sbesbank.models import *
from sbesbank.serializers import *
from rest_framework import status
from Shared.BankNumbers import *

from datetime import datetime
# Create your views here.
from rest_framework.parsers import JSONParser 
import json
from modules.exchangeRates import (
    parse
)
import copy

from sbesbank.models import Currency

@api_view(['GET'])
def TrAcTransfer(request, id):
    obj = TrAcTransferInfo.objects.get(id=id)
    serializer = TrAcTransferInfoSerializer(obj) 

    # parser = parse.MyParser()
    # parser.Parse()
    
    # dataDict = copy.deepcopy(parser.dataDict)
    # # del dataDict['DKK']
    # # del dataDict['JPY']
    # # del dataDict['NOK']
    # # del dataDict['SEK']

    # ids = ExchangeRate.objects.values('id')

    # maxId = 1

    # if len(ids) > 0:
    #     maxId = ids.order_by('-id').first()

    # print(maxId)

    # for key in dataDict:
        
    #     try:
    #         c = str(copy.deepcopy(key))
    #         rate = float(copy.deepcopy(dataDict[key]))
    #         curr = Currency[c]

    #         ExchangeRate.objects.create(
    #             id=maxId,
    #             currency=Currency[c],
    #             rateInDinar=rate
    #         )

    #         maxId += 1

    #     except KeyError:
    #         continue

    return JsonResponse(serializer.data)

@api_view(['GET'])
def TrMyAcc(request, id):
    obj = TrMyAccountInfo.objects.get(id=id)
    serializer = TrMyAccountInfoSerializer(obj) 

    return JsonResponse(serializer.data)

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

    return JsonResponse({"IUser": serializer1.data,
    "Certificate": serializer2.data})


@api_view(['GET'])
def AccInfo(request, id):
    obj1 = Account.objects.get(id=id) 
    obj2 = list(Card.objects.filter(accountFK=id))
    serializer1 =  AccountSerializer(obj1)
    serializer2 = CardSerializer(obj2,many = True)

    return JsonResponse({"Account": serializer1.data,
    "Cards": serializer2.data})

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
    return JsonResponse(iuser_serializer.errors, status
        = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createClient(request):
    client_data = JSONParser().parse(request)
    userr = IUser.objects.get(id = client_data['userId'])
    client = Client()
    client.userId = userr
    client.save()
    idd = Client.objects.get(userId=client.userId)
    povratna = idd.id
    serialized_data = ClientSerializer(client)
    return JsonResponse(serialized_data.data)



@api_view(['POST'])
def createAccount(request):
    account_data = JSONParser().parse(request)
    account_serializer = AccountSerializer(data = account_data)
    if account_serializer.is_valid():
        account_serializer.save()
        return JsonResponse(account_serializer.data)
    return JsonResponse(account_serializer.errors, status
        = status.HTTP_400_BAD_REQUEST)


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
        card = createCard(userr.fullName,CardType.DEBIT,account.accountNumber)
        card.accountFK = account
        idss = Card.objects.values('id')
        card.id = idss.order_by('-id').first()['id'] + 1
        card.save()
        return JsonResponse(iuser_serializer.data)
    else:
        return JsonResponse(iuser_serializer.errors, status
        = status.HTTP_400_BAD_REQUEST)

def createAccount():
    account = Account()
    account.accountBalance = 0.0
    account.accountNumber = BankNumbers.GenerateAccountNumber()
    account.blocked = False
    account.currency = Currency.RSD
    account.dateCreated = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    return account

def createCard(cardHolder,cardType,accountNumber):
    card = Card()
    card.cardHolder= cardHolder
    card.cardNumber = BankNumbers.GenerateCardNumber(cardProcessor= CreditCardProcessor.CreditCardProcessor.MASTER_CARD)
    card.cardProcessor = CreditCardProcessor.CreditCardProcessor.MASTER_CARD
    card.pin = BankNumbers.GeneratePIN(card.cardNumber,accountNumber)    
    card.validUntil =  (datetime.now()).strftime("%Y-%m-%d")
    card.cardType = cardType
    return card