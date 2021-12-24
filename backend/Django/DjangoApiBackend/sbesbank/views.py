from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser 

from sbesbank.models import *
from sbesbank.serializers import *
from modules.Shared.BankNumbers import *
from modules.Shared.Enums.CardType import CardType
from datetime import datetime, timedelta
import json
import copy

from django.db import models

from modules.paymentCodes.parse import (
    Parse
)

from modules.exchangeRates.parse import (
    MyParser
)


def ModelsExistsFields(
    model:models.Model,
    dataDict:dict,
    keys:list[str],
    all:bool
) -> list[str]:
    """
        Return list of fields that already exist in DB
    """
    fieldsExists:list[str] = []

    for key in dataDict:
        if str(key) in keys:
            dictCopy = {}
            dictCopy[copy.deepcopy(key)] = copy.deepcopy(dataDict[key]) 
            
            if model.objects.filter(**dictCopy).exists():
                fieldsExists.append(str(key))

    if all:
        return [] if len(fieldsExists) != len(keys) else fieldsExists
    else:
        fieldsExists



def ModelExists(
    model:models.Model,
    dataDict:dict,
    keys:list[str])->bool:
    """
        Model is Django model\n
        Data Dict are key-value pairs with 
        key as column name and value as column value\n
        Keys are column names that need to be checked
    """
    dictCopy = {}

    for key in dataDict:
        if str(key) in keys:
            dictCopy[copy.deepcopy(key)] = copy.deepcopy(dataDict[key]) 

    return model.objects.filter(**dictCopy).exists()


def GetNextId(model:models.Model):
    if(len(model.objects.all()) > 0):
        return model.objects.all().order_by('-id')[0].id + 1
    else:
        return 1

def CreateModel(model:models.Model, dataDict:dict) -> models.Model: 
    m = model(**dataDict)
    m.save()
    return m



@api_view(['GET'])
def InitCurrencies(request):

    # Enter payment codes
    # paymentCodes = Parse()

    # for k in paymentCodes.keys():
    #     PaymentCode.objects.create(
    #         code=k,
    #         description=paymentCodes[k]
    #     )

    # Enter exchange rates
    dateModified = date.today()
    rates = ExchangeRate.objects.all()    
    updated = False

    if(len(rates) > 0):
        updated = rates[0].dateModified >= dateModified

    if(not updated):
        exchangeRateParser = MyParser()
        exchangeRateParser.Parse()
        
        for k in exchangeRateParser.dataDict:
            if(ModelsExistsFields(
                ExchangeRate, 
                {'currency': Currency[k]},
                ['currency'], True
            )):
                er = ExchangeRate.objects.get(
                    currency=Currency[k]
                )
                er.dateModified = dateModified
                er.rateInDinar=exchangeRateParser.dataDict[k]
                er.save()

            else:
                ExchangeRate.objects.create(
                    currency=Currency[k],
                    dateModified=dateModified,
                    rateInDinar=exchangeRateParser.dataDict[k]
                )
  
    return JsonResponse(
        1,
        status=200,
        safe=False
    )

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


<<<<<<< HEAD

=======
>>>>>>> 49a168748992e232e74ba5fbba7fb22372b30339
@api_view(['POST'])
def LogInUser(request):
    bodyUnicode = request.body.decode('utf-8')
    body = json.loads(bodyUnicode)

    user = IUser.objects.get(
        username=body['username'],
        password=body['password']
    )

    client = Client.objects.get(
        userId=user
    )

    ser = ClientSerializer(client)

    return JsonResponse(ser.data)



@api_view(['POST'])
def RegisterUser(request):
    body = json.loads(
        request.body.decode('utf-8')
    )

    userFound = ModelsExistsFields(
        IUser, body, ["username", "jmbg", "userType"], True
    )
    
    if(len(userFound) != 0):
        retStr = "User with "
        for f in userFound:
            retStr += f"{f}={body[f]}, "
        
        retStr += " already exists."

        return JsonResponse(retStr, status=409, safe=False)

    
    body['id'] = GetNextId(IUser)
    user = CreateModel(IUser, body)

    if (body['userType'] == 'client'):
        client = CreateModel(Client, {
            'id' : GetNextId(Client),
            'userId' : user
        })

        return JsonResponse(
            ClientSerializer(client).data
        )
    else:
        return JsonResponse(
            IUserSerializer(user).data
        )


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



@api_view(['GET'])
def ChangeAccount(request, id, currency):
    curr = Currency(getCurrency(currency))
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
    iuser_serializer = IUserSerializer(data=iuser_data)
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
    userr = IUser.objects.get(id=client_data['userId'])
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
                currency = Currency(getCurrency(transaction_data['currency'])),
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
