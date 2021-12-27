import re
from django.core import exceptions
from django.http import JsonResponse
from django.http.response import Http404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from modules.Certificates.newCertMaker import NewUserCert
from modules.Certificates.selfSigned import getCertAuthorityName
import os
from sbesbank.models import *
from sbesbank.serializers import *
from modules.Shared.Enums.CreditCardProcessor import CreditCardProcessor
from modules.Shared.Enums.CardType import CardType
from modules.Shared.BankNumbers import (
    BankNumbers
)

from datetime import datetime,timedelta
import json
import copy

# # from django.db import models

from modules.paymentCodes.parse import (
    Parse
)

from modules.exchangeRates.parse import (
    MyParser
)


def ModelsExistsFields(
    model:models.Model,
    dataDict:dict,
    keys,
    all:bool
):
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
    keys)->bool:
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

    #Enter payment codes
    paymentCodes = Parse()

    for k in paymentCodes.keys():
        PaymentCode.objects.create(
            code=k,
            description=paymentCodes[k]
        )

    #Enter exchange rates
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

@api_view(['POST'])
def BlockAccount(request):
    block_data = JSONParser().parse(request) 
    check = block_data['check']
    accountNum = block_data['accNum']
    account = Account.objects.get(accountNumber = accountNum)
    if check==True:
        account.blocked = True
    else:
        account.blocked = False
    account.save()
    return  JsonResponse({"Blocked":account.blocked})
    
@api_view(['GET'])
def AccCards(request):
    accountID = request.GET.get('accountId')
    print(accountID)
    cards = list(Card.objects.filter(accountFK=accountID))
    print(cards)
    
    cardS =  CardSerializer2(cards, many=True)
    
    return JsonResponse(
            cardS.data, safe=False
    )

@api_view(['GET'])
def GetAllAccountsInBank(request):
    accounts = Account.objects.all()
    account_serialized = AccountSerializer(accounts,many = True)
    return JsonResponse(account_serialized.data, safe = False)


@api_view(['POST'])
def CreatePayment(request):
    inflow_data = JSONParser().parse(request) 
    accountNum = inflow_data['accNum']
    amount = inflow_data['amount']
    thisAccount = Account.objects.get(accountNumber = accountNum)
    thisClient = Client.objects.get(id = thisAccount.clientId.id)
    thisUser = IUser.objects.get(id = thisClient.userId.id)
    try:
        paymentCodeFK = CreateModel(PaymentCode,{
            'code':263,
            'description':'Оstаli trаnsfеri '
        })
        myAccInfo = CreateModel(TrMyAccountInfo,{
            'id':GetNextId(TrMyAccountInfo),
            'balanceBefore':thisAccount.accountBalance,
            'balanceAfter':thisAccount.accountBalance+amount,
            'accountNumber':thisAccount.accountNumber,
            'billingAddress':thisUser.billingAddress,
            'fullName':thisUser.fullName
        })
        trTrAcInfo = CreateModel(TrAcTransferInfo,{
            'id':GetNextId(TrAcTransferInfo),
            'accountNumber':thisAccount.accountNumber,
            'billingAddress':thisUser.billingAddress,
            'fullName':thisUser.fullName
        })
        
        transaction = CreateModel(Transaction,{
            'id': GetNextId(Transaction),
            'amount':amount,
            'modelCode':0,
            'paymentCodeFK':paymentCodeFK,
            'paymentPurpose': 'Uplata novca sebi',
            'preciseTime':datetime.now(),
            'provision':0,
            'referenceNumber':0,
            'transactionType':'INFLOW',
            'currency':thisAccount.currency,
            'myAccInfoFK':myAccInfo,
            'transferAccInfoFK':trTrAcInfo
        }
        )
        
        thisAccount.accountBalance+= amount
        thisAccount.save()
        serializer = TransactionSerializer(transaction) 
        

        return JsonResponse(serializer.data)
    except:
        return JsonResponse({"Error message":"Invalid transaction data"},status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def DoTransaction(request):
    #proveri postojanje drugog racuna
    transaction_data = JSONParser().parse(request) 
    transferInfoFK = transaction_data['transferAccInfoFK']
    print(transferInfoFK['accountNumber'])
    paymentC = transaction_data['paymentCodeFK']
    #print(JSONParser().parse(paymentC))
    
    myAccData = transaction_data['myAccInfoFK']
  #  print(JSONParser().parse(myAccData))
    
    try:
        # obj = Account.objects.get(accountNumber=transferInfoFK['accountNumber'])
        # obj['accountBalance'] += transaction_data['amount']
        paymentCodeFK = CreateModel(PaymentCode,{
            'code':paymentC['code'],
            'description':paymentC['description']
        })
        myAccInfo = CreateModel(TrMyAccountInfo,{
            'id':GetNextId(TrMyAccountInfo),
            'balanceBefore':myAccData['balanceBefore'],
            'balanceAfter':myAccData['balanceAfter'],
            'accountNumber':myAccData['accountNumber'],
            'billingAddress':myAccData['billingAddress'],
            'fullName':myAccData['fullName']
        })
        trTrAcInfo = CreateModel(TrAcTransferInfo,{
            'id':GetNextId(TrAcTransferInfo),
            'accountNumber':transferInfoFK['accountNumber'],
            'billingAddress':transferInfoFK['billingAddress'],
            'fullName':transferInfoFK['fullName']
        })
        transaction = CreateModel(Transaction,{
            'id': GetNextId(Transaction),
            'amount':transaction_data['amount'],
            'modelCode':transaction_data['modelCode'],
            'paymentCodeFK':paymentCodeFK,
            'paymentPurpose': transaction_data['paymentPurpose'],
            'preciseTime':datetime.now(),
            'provision':transaction_data['provision'],
            'referenceNumber':transaction_data['referenceNumber'],
            'transactionType':transaction_data['transactionType'],
            'currency':Currency[transaction_data['currency']],
            'myAccInfoFK':myAccInfo,
            'transferAccInfoFK':trTrAcInfo
        }
        )
        account = Account.objects.get(accountNumber= myAccData['accountNumber'])
        account.accountBalance =  myAccData['balanceAfter'] 
        account.save()
        serializer = TransactionSerializer(transaction) 
        
        DoTransactionTransfer(transaction_data)
        return JsonResponse(serializer.data)
    except:
        return JsonResponse({"Error message":"Invalid transaction data"},status = status.HTTP_400_BAD_REQUEST)

def DoTransactionTransfer(tracData):
    transaction_data = tracData

    paymentC = transaction_data['paymentCodeFK']
    trAcTransf = transaction_data['myAccInfoFK']
    myAcInfo = transaction_data['transferAccInfoFK']
    
    # tracinfo iz requesta mi postaje myaccinfo
    #  s tim sto baalance before i after moram da podesim
    # fullname je isti 
    # billing adres isti
    #
    # myacinfo iz requesta postaje tracinfo 
    # imam sve podatke 
    # adresa acc num  i full name
    thisAcc = Account.objects.get(accountNumber= myAcInfo['accountNumber'])
    # accountTo.accountBalance += transaction_data['amount']

    try:
        paymentCodeFK = CreateModel(PaymentCode,{
            'code':paymentC['code'],
            'description':paymentC['description']
        })
        myAccInfo = CreateModel(TrMyAccountInfo,{
            'id':GetNextId(TrMyAccountInfo),
            'balanceBefore':thisAcc.accountBalance,
            'balanceAfter':thisAcc.accountBalance+transaction_data['amount'],
            'accountNumber':myAcInfo['accountNumber'],
            'billingAddress':myAcInfo['billingAddress'],
            'fullName':myAcInfo['fullName']
        })

        trTrAcInfo = CreateModel(TrAcTransferInfo,{
            'id':GetNextId(TrAcTransferInfo),
            'accountNumber':trAcTransf['accountNumber'],
            'billingAddress':trAcTransf['billingAddress'],
            'fullName':trAcTransf['fullName']
        })
        transaction = CreateModel(Transaction,{
            'id': GetNextId(Transaction),
            'amount':transaction_data['amount'],
            'modelCode':transaction_data['modelCode'],
            'paymentCodeFK':paymentCodeFK,
            'paymentPurpose': transaction_data['paymentPurpose'],
            'preciseTime':datetime.now(),
            'provision':transaction_data['provision'],
            'referenceNumber':transaction_data['referenceNumber'],
            'transactionType':'INFLOW',
            'currency':Currency[transaction_data['currency']],
            'myAccInfoFK':myAccInfo,
            'transferAccInfoFK':trTrAcInfo
        }
        )
       
        thisAcc.accountBalance = thisAcc.accountBalance+transaction_data['amount']
        thisAcc.save()
        serializer = TransactionSerializer(transaction) 

        return JsonResponse(serializer.data)
    except:
        return JsonResponse({"Error message":"Invalid transaction data"},status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def LogInUser(request):
    bodyUnicode = request.body.decode('utf-8')
    body = json.loads(bodyUnicode)

    user = IUser.objects.get(
        username=body['username'],
        password=body['password']
    )
    if user.userType==IUser.userTypes[1][1]:
        client = Client.objects.get(
        userId=user
        )
        ser = ClientSerializer(client)
    else:
        ser = IUserSerializer(user)

    return JsonResponse(ser.data)


def getPathForDB(path):
    pathForDB = path.split('DjangoApiBackend\\')[1]
    return pathForDB

def getAbsolutePath(dbPath):
    absPath = os.path.join(os.getcwd() ,dbPath)
    return absPath

@api_view(['POST'])
def RegisterUser(request):
    body = json.loads(
        request.body.decode('utf-8')
    )

    userFound = ModelsExistsFields(
        IUser, body, ["username", "jmbg", "userType","email"], True
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

        pemPath,keyPath = NewUserCert(os.path.join(os.getcwd(),'modules','Certificates'),body['username'])
       
        certificate = CreateModel(Certificate, {
            'id' : GetNextId(Certificate),
            'authorityName' : getCertAuthorityName(),
            'pemPath' : getPathForDB(pemPath),
            'keyPath' : getPathForDB(keyPath),
            'certificateName' : body['username'],
            'userId' : user
            }
        )
        accountNumber = BankNumbers.GenerateAccountNumber()
        account = CreateModel(Account,{
            'id': GetNextId(Account),
            'accountBalance': 0,
            'accountNumber' : accountNumber,
            'blocked': False,
            'currency' : Currency['RSD'],
            'dateCreated': datetime.now(),
            'clientId': client
        })
        cardNumber = BankNumbers.GenerateCardNumber(CreditCardProcessor.VISA)
        td = timedelta(days= 365*4)
        validUntil = (datetime.now()+ td).strftime("%Y-%m-%d")
        card = CreateModel(Card,{
            'id': GetNextId(Card),
            'cardHolder': body['fullName'],
            'cardNumber': cardNumber ,
            'cvc': BankNumbers.GenerateCVC(cardNumber, accountNumber),
            'pin': BankNumbers.GeneratePIN(cardNumber,accountNumber),
            'cardProcessor':'VISA',
            'cardType' :'DEBIT',
            'validUntil': validUntil,
            'accountFK' : account
        })
        
        return JsonResponse( ClientSerializer(client).data)
    else:
        return JsonResponse(
            IUserSerializer(user).data
        )


@api_view(['POST'])
def ExchangeMoney(request):
    exchange_data = JSONParser().parse(request)
    rikvest = request
    # accountFrom
    # accountTo
    # amount
    accountFrom = exchange_data['accountFrom']
    accountTo = exchange_data['accountTo']
    amount = exchange_data['amount']
 
    try:
        accountF = Account.objects.get(accountNumber= accountFrom)
        accountT = Account.objects.get(accountNumber= accountTo)
        
        clientEx = Client.objects.get(id = accountF.clientId.id)
        userEx = IUser.objects.get(id = clientEx.userId.id)

        paymentCodeFK = CreateModel(PaymentCode,{
            'code':986,
            'description':'Kupoprodaja deviza'
        })

        myAccInfo = CreateModel(TrMyAccountInfo,{
            'id':GetNextId(TrMyAccountInfo),
            'balanceBefore':accountF.accountBalance,
            'balanceAfter':accountF.accountBalance-amount,
            'accountNumber':accountFrom,
            'billingAddress':userEx.billingAddress,
            'fullName':userEx.fullName
        })
        trTrAcInfo = CreateModel(TrAcTransferInfo,{
            'id':GetNextId(TrAcTransferInfo),
            'accountNumber':accountTo,
            'billingAddress':userEx.billingAddress,
            'fullName':userEx.fullName
        })
        transaction = CreateModel(Transaction,{
            'id': GetNextId(Transaction),
            'amount':amount,
            'modelCode':0,
            'paymentCodeFK':paymentCodeFK,
            'paymentPurpose':'konverzija',
            'preciseTime':datetime.now(),
            'provision':0,
            'referenceNumber':0,
            'transactionType':'OUTFLOW',
            'currency':accountF.currency,
            'myAccInfoFK':myAccInfo,
            'transferAccInfoFK':trTrAcInfo
        }
        )
        accountF.accountBalance = accountF.accountBalance - amount
        accountF.save()
        DoExchangeTransfer(exchange_data)
        return JsonResponse(TransactionSerializer(transaction).data)
    except:
        return JsonResponse({"Error":"Error when exchange money"})

def DoExchangeTransfer(exchange_data):
   
    accountFrom = exchange_data['accountTo']
    accountTo = exchange_data['accountFrom']
    amount = exchange_data['amount']
    try:
        accountF = Account.objects.get(accountNumber = accountFrom)

        accountT = Account.objects.get(accountNumber = accountTo)
        clientEx = Client.objects.get(id = accountF.clientId.id)
        userEx = IUser.objects.get(id = clientEx.userId.id)
        paymentCodeFK = CreateModel(PaymentCode,{
            'code':986,
            'description':'Kupoprodaja deviza'
        })
        exchangedMoney = ExchangeAmount(accountT.currency, amount, accountF.currency)
        
       
        myAccInfo = CreateModel(TrMyAccountInfo,{
            'id':GetNextId(TrMyAccountInfo),
            'balanceBefore':accountF.accountBalance,
            'balanceAfter':accountF.accountBalance+exchangedMoney,
            'accountNumber':accountFrom,
            'billingAddress':userEx.billingAddress,
            'fullName':userEx.fullName
        })
        trTrAcInfo = CreateModel(TrAcTransferInfo,{
            'id':GetNextId(TrAcTransferInfo),
            'accountNumber':accountTo,
            'billingAddress':userEx.billingAddress,
            'fullName':userEx.fullName
        })
        transaction = CreateModel(Transaction,{
            'id': GetNextId(Transaction),
            'amount':exchangedMoney,
            'modelCode':0,
            'paymentCodeFK':paymentCodeFK,
            'paymentPurpose':'konverzija',
            'preciseTime':datetime.now(),
            'provision':0,
            'referenceNumber':0,
            'transactionType':'INFLOW',
            'currency':accountF.currency,
            'myAccInfoFK':myAccInfo,
            'transferAccInfoFK':trTrAcInfo
        }
        )
        accountF.accountBalance = accountF.accountBalance + exchangedMoney
        accountF.save()
        serializer = TransactionSerializer(transaction) 

        return JsonResponse(serializer.data)
    except:
        return JsonResponse({"Error message":"Invalid transaction data"},status = status.HTTP_400_BAD_REQUEST)

def ExchangeAmount(fromCurr, amount , toCurrency)->float:

    convertedValue = amount
    convertedInDinars = amount
    if str(fromCurr)!='RSD':
        try:
            currFrom = ExchangeRate.objects.get(currency = fromCurr)
            convertedInDinars = amount*currFrom.rateInDinar
        except:
            print("Error currency from")
    
    if str(toCurrency)!='RSD':
        try:
            currTo = ExchangeRate.objects.get(currency = toCurrency)
            convertedValue = convertedInDinars/currTo.rateInDinar
        except:
            print("Error currency to")
    else:
        convertedValue = convertedInDinars
    
    return convertedValue


#C:\Users\HP\Documents\GitHub\SBES_Bank\backend\Django\DjangoApiBackend\modules\Certificates\ddedrefe.key
@api_view(['GET'])
def Transact(request, id):
    obj = Transaction.objects.get(id=id)
    serializer = TransactionSerializer(obj) 

    return JsonResponse(serializer.data)


@api_view(['POST'])
def CheckCurrency(request):
    accNum = JSONParser().parse(request) 
    try:
        account = Account.objects.get(accountNumber = accNum['accountNumber'])
        serializedAcc = AccountSerializer(account)
        if account!=None:
            return JsonResponse({"Currency":serializedAcc.data['currency']})
        else:
            return JsonResponse({"Error":"Account with that accountNumber doesn't exist"})
    except:
        return JsonResponse({"Error":"Account with that accountNumber doesn't exist"})
    
@api_view(['GET'])
def GetPaymentCodes(request):
    payment_codes= PaymentCode.objects.all()
    payment_codes_serialize = PaymentCodeSerializer(payment_codes, many = True)
    return JsonResponse(payment_codes_serialize.data)
    

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

    print(request)
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
def TryTry(request):
    toCurrency = 'EUR'
    toInDinars = ExchangeRate.objects.get(currency =  Currency[toCurrency])
    ss = 100/toInDinars.rateInDinar
    return JsonResponse({"vrednosT":ss})

@api_view(['POST'])
def AccTransactions(request):
    
    body = JSONParser().parse(request)
    accNum = body['accountNumber']
    obj =list(TrMyAccountInfo.objects.filter(accountNumber = accNum))
    transactions = list()
    for x in obj:
        transactions+=Transaction.objects.filter(myAccInfoFK = x.id)

    for c in transactions:
        print(c)
    serializer = TransactionSerializer(transactions,many = True) 

    return JsonResponse(serializer.data)



@api_view(['GET'])
def ChangeAccount(request, id, currency):
    curr = Currency[currency]
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
def CreateAccount(request):
    account_data = JSONParser().parse(request)
    account_curr = account_data['currency']
    client_id = account_data['clientId']
    try:
        client = Client.objects.get(id = client_id)
        account = CreateModel(Account,{
            'id':GetNextId(Account),
            'accountNumber':BankNumbers.GenerateAccountNumber(),
            'accountBalance':0,
            'blocked':False,
            'currency':Currency[account_curr],
            'dateCreated':datetime.now(),
            'clientId':client
        })
        account.save()
        acc_serialized = AccountSerializer(account)
        return JsonResponse(acc_serialized.data)
    except:
        return JsonResponse({"Error":"Error when creating new Account"})




# @api_view(['POST'])
# def createAccountPOST(request):
#     req_data = JSONParser().parse(request)
#     currency = req_data['currency']
#     clientId = req_data['clientId']
#     account = CreateModel(Account,{
#         'id':GetNextId(Account),
#         'accountBalance':0,
#         'accountNumber': BankNumbers.GenerateAccountNumber(),
#         'blocked':False,
#         'currency':Currency[currency],
#         'dateCreated':datetime.now(),
#         'clientId':
#     }) 
#     account = createAccount()
#     account.clientId = Client.objects.get(id = clientId)
#     account.currency = Currency[currency]
#     account.save()
#     account_serialized = AccountSerializer(account)
#     return JsonResponse(account_serialized.data)


@api_view(['POST'])
def createCardPOST(request):
    body = JSONParser().parse(request)
    try:
        accountFK = Account.objects.get(accountNumber=body['accNum'])
    except:
        return JsonResponse({'Error':'Acc num not found'})
    cardNumber = BankNumbers.GenerateCardNumber(body['cardProcessor'])
    td = timedelta(days= 365*4)
    validUntil = (datetime.now()+ td).strftime("%Y-%m-%d")
    card = CreateModel(Card,{
    'id': GetNextId(Card),
    'cardHolder': body['cardHolder'],
    'cardNumber': cardNumber ,
    'cvc': BankNumbers.GenerateCVC(cardNumber, body['accNum']),
    'pin': BankNumbers.GeneratePIN(cardNumber,body['accNum']),
    'cardProcessor': body['cardProcessor'],
    'cardType' :body['cardType'],
    'validUntil': validUntil,
    'accountFK' : accountFK
        })
    return JsonResponse(CardSerializer(card).data)
    

# @api_view(['POST'])
# def createNewClientAccount(request):
#     iuser_data = JSONParser().parse(request)
#     iuser_serializer = IUserSerializer(data = iuser_data)
#     if iuser_serializer.is_valid():
#         iuser_serializer.save()
#         userr = IUser.objects.get(id = iuser_data['id'])
#         client = Client()
#         client.userId = userr
#         client.save()
#         account = Account()
#         account = createAccount()
#         client1 = Client.objects.get(userId =iuser_data['id'])
#         account.clientId = client1
#         account.save()
#         card = createCard(userr.fullName,CardType.DEBIT,account.accountNumber)
#         card.accountFK = account
#         card.save()
#         return JsonResponse(iuser_serializer.data)
#     else:
#         return JsonResponse(iuser_serializer.errors, status
#         = status.HTTP_400_BAD_REQUEST)

# def createAccount():
#     account = Account()
#     ids = Account.objects.values('id')
#     try:
#         account.id = ids.order_by('-id').first()['id'] + 1 
#     except:
#         account.id = 1
#     account.accountBalance = 0.0
#     account.accountNumber = BankNumbers.GenerateAccountNumber()
#     account.blocked = False
#     account.currency = Currency.RSD
#     account.dateCreated = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
#     return account

def createCard(cardHolder,cardType,accountNumber):
    card = Card()
    idss = Card.objects.values('id')
    try:
        card.id = idss.order_by('-id').first()['id'] + 1    
    except:
        card.id = 1
    card.cardHolder= cardHolder
    card.cardNumber = BankNumbers.GenerateCardNumber(cardProcessor=CreditCardProcessor.MASTER_CARD)
    card.cardProcessor = CreditCardProcessor.MASTER_CARD
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
                currency = Currency[transaction_data['currency']],
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
 