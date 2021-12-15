from django.forms.widgets import ClearableFileInput
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import translation
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser 

from sbesbank.models import *
from sbesbank.serializers import *
from modules.Shared.BankNumbers import *
from modules.Shared.Enums.CardType import CardType

from datetime import datetime

from typing import KeysView
import json
import copy


@api_view(['GET'])
def TrAcTransfer(request, id):
    obj=TrAcTransferInfo.objects.get(id=id)
    serializer=TrAcTransferInfoSerializer(obj) 

    return JsonResponse(serializer.data)


@api_view(['GET'])
def TrMyAcc(request, id):
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
def AccInfo(request, id):
    obj1 = Account.objects.get(id=id) 
    obj2 = list(Card.objects.filter(accountFK=id))
    serializer1 =  AccountSerializer(obj1)
    serializer2 = CardSerializer(obj2,many = True)

    return JsonResponse(
        {
            "Account": serializer1.data,
            "Cards": serializer2.data
            }
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



@api_view(['GET'])
def ChangeAccount(request, id, currency):
    typetr = 0
    currencyId = 0
    if currency=='USD':
        currencyId = 1
    elif currency=='EUR':
        currencyId = 2
    elif currency=='CHF':
        currencyId = 3
    elif currency=='GBP':
        currencyId = 4
    elif currency=='RUB':
        currencyId = 5
    elif currency=='CNY':
        currencyId = 6
    elif currency=='CAD':
        currencyId = 7
    elif currency=='AUD':
        currencyId = 8
    elif currency=='RSD':
        currencyId = 9
    curr = Currency(currencyId)
    account =Account.objects.get(clientId = id, currency = curr)
    cards = list(Card.objects.filter(accountFK = account.id))
    serializer_acc = AccountSerializer(account)
    serializer_cards = CardSerializer(cards,many = True)

    return JsonResponse(
        {
            "Account": serializer_acc.data,
            "Cards": serializer_cards.data
        }
    )

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
def createAccountPOST(request, clientId,currency):
    account = Account()
    account = createAccount()
    account.clientId = Client.objects.get(id = clientId)
    account.currency = Currency(getCurrency(currency))
    account.save()
    account_serialized = AccountSerializer(account)
    return JsonResponse(account_serialized.data)


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
        account.clientId = client1
        account.save()
        card = createCard(userr.fullName,CardType.DEBIT,account.accountNumber)
        card.accountFK = account
        card.save()
        return JsonResponse(iuser_serializer.data)
    else:
        return JsonResponse(iuser_serializer.errors, status
        = status.HTTP_400_BAD_REQUEST)

def createAccount():
    account = Account()
    ids = Account.objects.values('id')
    try:
        account.id = ids.order_by('-id').first()['id'] + 1 
    except:
        account.id = 1
    account.accountBalance = 0.0
    account.accountNumber = BankNumbers.GenerateAccountNumber()
    account.blocked = False
    account.currency = Currency.RSD
    account.dateCreated = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    return account

def createCard(cardHolder,cardType,accountNumber):
    card = Card()
    idss = Card.objects.values('id')
    try:
        card.id = idss.order_by('-id').first()['id'] + 1    
    except:
        card.id = 1
    card.cardHolder= cardHolder
    card.cardNumber = BankNumbers.GenerateCardNumber(cardProcessor= CreditCardProcessor.CreditCardProcessor.MASTER_CARD)
    card.cardProcessor = CreditCardProcessor.CreditCardProcessor.MASTER_CARD
    card.pin = BankNumbers.GeneratePIN(card.cardNumber,accountNumber)    
    card.validUntil =  (datetime.now()).strftime("%Y-%m-%d")
    card.cardType = cardType
    return card

def getCurrency(currency):
    currencyId = 0
    if currency=='USD':
        currencyId = 1
    elif currency=='EUR':
        currencyId = 2
    elif currency=='CHF':
        currencyId = 3
    elif currency=='GBP':
        currencyId = 4
    elif currency=='RUB':
        currencyId = 5
    elif currency=='CNY':
        currencyId = 6
    elif currency=='CAD':
        currencyId = 7
    elif currency=='AUD':
        currencyId = 8
    elif currency=='RSD':
        currencyId = 9       
    return currencyId

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

            #transaction_serializer.paymentCodeFK = PaymentCodeSerializer(data = pym)
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
    

