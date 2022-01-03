
from django.core import exceptions
from re import T
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from modules.Certificates.selfSigned import makeCertAuthority
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

from datetime import datetime, timedelta
import json
import copy

from modules.paymentCodes.parse import (
    Parse
)

from modules.exchangeRates.parse import (
    MyParser
)

from sbesbank.helpMethods.dbAccess.dbAccess import (
    ModelsExistsFields,
    ModelExists,
    GetNextId,
    CreateModel
)

from modules.Certificates.Cypher import *


#region UserViews
@api_view(['POST'])
def LogInUser(request):
    
    requestStr = json.loads(request.body.decode('utf-8'))
    decrypted = DecryptTextRSA(
        requestStr['data'],
        LoadKey(GetCertificateFilePath(False))     
    )
    print(decrypted)

    body = json.loads(decrypted)

    userPublicPath = GetCertificateFilePath(
        True, body['username']
    )

    if(ModelsExistsFields(
        IUser,
        body,
        ['username', 'password'],
        True
    )):
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



        return JsonResponse(
            ser.data,
            status=200
        )

    else:
        return JsonResponse(
            "User with given credentials doesn't exist.",
            status=404,
            safe=False
        )

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

    # body['userType']='client'
    # userType should be sent from frontend!

    
    pemPath, keyPath = NewUserCert(
            os.path.join(
                os.getcwd(),
                'modules',
                'Certificates'
            ),
            body['username']
    )


    user = CreateModel(IUser, body)
       
    certificate = CreateModel(Certificate, {
        'id' : GetNextId(Certificate),
        'authorityName' : getCertAuthorityName(),
        'pemPath' : getPathForDB(pemPath),
        'keyPath' : getPathForDB(keyPath),
        'certificateName' : body['username'],
        'userId' : user
    })

    if (body['userType'].lower() == 'client'):
        client = CreateModel(Client, {
            'id' : GetNextId(Client),
            'userId' : user
        })

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

        cardProcessor = CreditCardProcessor.VISA
        cardType = CardType.DEBIT
        cardNumber = BankNumbers.GenerateCardNumber(cardProcessor)
        td = timedelta(days= 365*4)
        validUntil = (datetime.now()+ td).strftime("%Y-%m-%d")
        
        card = CreateModel(Card,{
            'id': GetNextId(Card),
            'cardHolder': body['fullName'],
            'cardNumber': cardNumber,
            'cvc': BankNumbers.GenerateCVC(cardNumber, accountNumber),
            'pin': BankNumbers.GeneratePIN(cardNumber, accountNumber),
            'cardProcessor':cardProcessor.__str__(),
            'cardType' :cardType.__str__(),
            'validUntil': validUntil,
            'accountFK' : account
        })
        
        return JsonResponse(ClientSerializer(client).data)
    else:
        return JsonResponse(
            IUserSerializer(user).data
        )


#endregion

#region AdminViews
# NOTE: for this methods perform credentials check

@api_view(['GET'])
def GetAllAccountsInBank(request):
    return JsonResponse(
        AccountSerializer(
            Account.objects.all(),
            many=True
        ).data,
        safe=False
    )

@api_view(['POST'])
def BlockAccount(request):
    '''
        Admin method
    '''
    block_data = JSONParser().parse(request) 
    check = block_data['check']
    accountNum = block_data['accNum']

    if(ModelsExistsFields(
            Account,
            {'accountNumber':accountNum},
            ['accountNumber'],
            True
        )):

        account = Account.objects.get(accountNumber = accountNum)
        if check==True:
            account.blocked = True
        else:
            account.blocked = False
        account.save()

        return  JsonResponse({
                "Blocked":account.blocked
            })
    else:
        return JsonResponse(
            "Account with given number was not found.",
            status=404,
            safe=False
        )

#endregion

#region AccountViews

@api_view(['GET'])
def AccInfo(request):
    accId = request.GET.get("id")
    obj1 = list(Account.objects.filter(
        clientId=accId
    ))
    serializer1 =  AccountSerializer(obj1, many=True)
    return JsonResponse(
            serializer1.data, safe=False
    )

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
    print(transactions)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def CreateAccount(request):
    '''
        Create new account for existing client
    '''
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

#endregion

#region CardViews

@api_view(['GET'])
def AccCards(request):
    accountID = request.GET.get('accountId')
    
    return JsonResponse(
        CardSerializer(
            Card.objects.filter(accountFK=accountID),
            many=True
        ).data,
        safe=False
    )

@api_view(['POST'])
def createCardPOST(request):
    '''
        Create new card for existing client
    '''
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
 
#endregion

#region TransactionViews

#r
def TemplatePaymentCode(code:int, description:str)->PaymentCode:

    paymentCodeFK = CreateModel(PaymentCode,{
            'code':code,
            'description':description
        })

    return paymentCodeFK

#r
def TemplateTrMyAccountInfo(balanceBefore:float, balanceAfter:float, 
        accountNumber:str, billingAddress:str, fullName:str
        )->TrMyAccountInfo:

    myAccountInfo = CreateModel(TrMyAccountInfo,{
                'id':GetNextId(TrMyAccountInfo),
                'balanceBefore':balanceBefore,
                'balanceAfter':balanceAfter,
                'accountNumber':accountNumber,
                'billingAddress':billingAddress,
                'fullName':fullName
            })

    return myAccountInfo

#r
def TemplateTrAccountTransferInfo(accountNumber:str, billingAddress:str,
        fullName:str)->TrMyAccountInfo:

    trTransferAccInfo = CreateModel(TrAcTransferInfo,{
            'id':GetNextId(TrAcTransferInfo),
            'accountNumber':accountNumber,
            'billingAddress':billingAddress,
            'fullName':fullName
        })

    return trTransferAccInfo    

#r
def TemplateTransaction(amount:float, modelCode:int, 
        paymentCodeFK:PaymentCode, paymentPurpose:str, 
        preciseTime:datetime, provision:float,
        referenceNumber:int, transactionType:str, 
        currency:Currency, trMyAccInfo:TrMyAccountInfo,
        trTransferAccInfo:TrAcTransferInfo
        )->Transaction:

    transaction = CreateModel(Transaction,{
            'id': GetNextId(Transaction),
            'amount':amount,
            'modelCode':modelCode,
            'paymentCodeFK':paymentCodeFK,
            'paymentPurpose': paymentPurpose,
            'preciseTime': preciseTime,
            'provision': provision,
            'referenceNumber': referenceNumber,
            'transactionType':transactionType,
            'currency': currency,
            'myAccInfoFK': trMyAccInfo,
            'transferAccInfoFK': trTransferAccInfo
        }
        )
    return transaction

@api_view(['GET'])
def TrAcTransfer(request):
    id = request.GET.get("id")
    
    if(ModelsExistsFields(
        TrAcTransferInfo,
        {'id':id},
        ['id'],
        True
    )):
        obj=TrAcTransferInfo.objects.get(id=id)
        serializer=TrAcTransferInfoSerializer(obj) 

        return JsonResponse(
            serializer.data,
            status=200
        )

    else:
        return JsonResponse(
            "Requested account information was not found.",
            status=404,
            safe=False
        )


@api_view(['GET'])
def TrMyAcc(request):
    id = request.GET.get("id")

    if(
        ModelsExistsFields(
            TrMyAccountInfo,
            {'id':id},
            ['id'],
            True
        )
    ):
        obj = TrMyAccountInfo.objects.get(id=id)
        serializer = TrMyAccountInfoSerializer(obj) 
        
        return JsonResponse(serializer.data)

    else:
        return JsonResponse(
            "Requested account information was not found.",
            status=404,
            safe=False
        )

@api_view(['POST'])
def CreatePayment(request):
    '''
        When client pays money to himself/herself account
    '''
    inflow_data = JSONParser().parse(request) 
    accountNum = inflow_data['accNum']
    amount = inflow_data['amount']
    thisAccount = Account.objects.get(accountNumber = accountNum)

    try:
        
        paymentCodeFK = TemplatePaymentCode(
            263,
            'Ostali transferi '
        )

        balanceAfter = thisAccount.accountBalance + amount

        myAccInfo = TemplateTrMyAccountInfo(
            thisAccount.accountBalance,
            balanceAfter,
            thisAccount.accountNumber,
            thisAccount.clientId.userId.billingAddress,
            thisAccount.clientId.userId.fullName
        )

        trTrAcInfo = TemplateTrAccountTransferInfo(
            thisAccount.accountNumber,
            thisAccount.clientId.userId.billingAddress,
            thisAccount.clientId.userId.fullName
        )
        
        transaction = TemplateTransaction(
            amount,
            0,
            paymentCodeFK,
            'Payment to yourself',
            datetime.now(),
            0,
            0,
            'INFLOW',
            thisAccount.currency,
            myAccInfo,
            trTrAcInfo
        )
        
        thisAccount.accountBalance += amount
        thisAccount.save()
        serializer = TransactionSerializer(transaction) 
        
        return JsonResponse(serializer.data)
    except:
        return JsonResponse({"Error message":"Invalid transaction data"},status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def DoTransaction(request):
    '''
        When client sends money to other client
    '''

    transaction_data = JSONParser().parse(request) 
    
    #region check pin and cvc
    if(not ModelsExistsFields(
        Card,
        transaction_data,
        ['cardNumber', 'cvc', 'pin'],
        True
    )):
        return JsonResponse(
            "Invalid CVC/PIN for given card number.",
            status=400,
            safe=False
        )

    del transaction_data['cardNumber']
    del transaction_data['cvc']
    del transaction_data['pin']
    #endregion

    transferInfoFK = transaction_data['transferAccInfoFK']
    paymentC = transaction_data['paymentCodeFK']
    myAccData = transaction_data['myAccInfoFK']

    account = Account.objects.get(accountNumber= myAccData['accountNumber'])
    try:
        paymentCodeFK = TemplatePaymentCode(
            paymentC['code'],
            paymentC['description']
        )
    
        myAccInfo = TemplateTrMyAccountInfo(
            myAccData['balanceBefore'],
            myAccData['balanceAfter'],
            myAccData['accountNumber'],
            myAccData['billingAddress'],
            myAccData['fullName']
        )

        trTrAcInfo = TemplateTrAccountTransferInfo(
            transferInfoFK['accountNumber'],
            transferInfoFK['billingAddress'],
            transferInfoFK['fullName']
        )
        
        transaction = TemplateTransaction(
            transaction_data['amount'],
            transaction_data['modelCode'],
            paymentCodeFK,
            transaction_data['paymentPurpose'],
            datetime.now(),
            transaction_data['provision'],
            transaction_data['referenceNumber'],
            transaction_data['transactionType'],
            Currency[transaction_data['currency']],
            myAccInfo,
            trTrAcInfo
        )        
        
        account.accountBalance =  myAccData['balanceAfter'] 
        account.save()

        serializer = TransactionSerializer(transaction) 
        
        DoTransactionTransfer(transaction_data)
        return JsonResponse(serializer.data, status=200)
    except:
        return JsonResponse({"Error message":"Invalid transaction data"},status = status.HTTP_400_BAD_REQUEST)

def DoTransactionTransfer(tracData):
    transaction_data = tracData

    paymentC = transaction_data['paymentCodeFK']
    trAcTransf = transaction_data['myAccInfoFK']
    myAcInfo = transaction_data['transferAccInfoFK'] 
    thisAcc = Account.objects.get(accountNumber= myAcInfo['accountNumber'])
    
    try:
        paymentCodeFK = TemplatePaymentCode(
            paymentC['code'],
            paymentC['description']
        )
        
        balanceAfter = thisAcc.accountBalance + transaction_data['amount']

        myAccInfo = TemplateTrMyAccountInfo(
            thisAcc.accountBalance,
            balanceAfter,
            myAcInfo['accountNumber'],
            myAcInfo['billingAddress'],
            myAcInfo['fullName']
        )
        
        trTrAcInfo = TemplateTrAccountTransferInfo(
            trAcTransf['accountNumber'],
            trAcTransf['billingAddress'],
            trAcTransf['fullName']
        )
        
        transaction = TemplateTransaction(
            transaction_data['amount'],
            transaction_data['modelCode'],
            paymentCodeFK,
            transaction_data['paymentPurpose'],
            datetime.now(),
            transaction_data['provision'],
            transaction_data['referenceNumber'],
            'INFLOW',
            Currency[transaction_data['currency']],
            myAccInfo,
            trTrAcInfo
        )
       
        thisAcc.accountBalance = balanceAfter
        thisAcc.save()
        serializer = TransactionSerializer(transaction) 

        return JsonResponse(serializer.data)
    except:
        return JsonResponse({"Error message":"Invalid transaction data"},status = status.HTTP_400_BAD_REQUEST)

#r
@api_view(['POST'])
def ExchangeMoney(request):
    exchange_data = JSONParser().parse(request)
    accountFrom = exchange_data['accountFrom']
    accountTo = exchange_data['accountTo']
    amount = exchange_data['amount']
 
    try:
        accountF = Account.objects.get(accountNumber= accountFrom)
        
        paymentCodeFK = TemplatePaymentCode(
            986,
            'Kupoprodaja deviza'
        )
        
        balanceAfter = accountF.accountBalance - amount

        myAccInfo = TemplateTrMyAccountInfo(
            accountF.accountBalance,
            balanceAfter,
            accountFrom,
            accountF.clientId.userId.billingAddress,
            accountF.clientId.userId.fullName
        )

        trTrAcInfo = TemplateTrAccountTransferInfo(
            accountTo,
            accountF.clientId.userId.billingAddress,
            accountF.clientId.userId.fullName
        )

        transaction = TemplateTransaction(
            amount,
            0,
            paymentCodeFK,
            'konverzija',
            datetime.now(),
            0,
            0,
            'OUTFLOW',
            accountF.currency,
            myAccInfo,
            trTrAcInfo
        )

        accountF.accountBalance = balanceAfter
        accountF.save()

        DoExchangeTransfer(exchange_data)

        return JsonResponse(TransactionSerializer(transaction).data)
    except:
        return JsonResponse({"Error":"Error when exchange money"})


#r
def DoExchangeTransfer(exchange_data):
   
    accountFrom = exchange_data['accountTo']
    accountTo = exchange_data['accountFrom']
    amount = exchange_data['amount']
    try:
        accountF = Account.objects.get(accountNumber = accountFrom)
        accountT = Account.objects.get(accountNumber = accountTo)
         
        paymentCodeFK = TemplatePaymentCode(
            986,
            'Kupoprodaja deviza'
        )
        exchangedMoney = ExchangeAmount(accountT.currency, amount, accountF.currency)
        
        balanceAfter = accountF.accountBalance + exchangedMoney

        myAccInfo = TemplateTrMyAccountInfo(
            accountF.accountBalance,
            balanceAfter,
            accountFrom,
            accountF.clientId.userId.billingAddress,
            accountF.clientId.userId.fullName
        )
        trTrAcInfo = TemplateTrAccountTransferInfo(
            accountTo,
            accountF.clientId.userId.billingAddress,
            accountF.clientId.userId.fullName
        )
        transaction = TemplateTransaction(
            exchangedMoney,
            0,
            paymentCodeFK,
            'konverzija',
            datetime.now(),
            0,
            0,
            'INFLOW',
            accountF.currency,
            myAccInfo,
            trTrAcInfo
        )

        accountF.accountBalance = balanceAfter
        accountF.save()

        serializer = TransactionSerializer(transaction) 

        return JsonResponse(serializer.data)
    except:
        return JsonResponse({"Error message":"Invalid transaction data"},status = status.HTTP_400_BAD_REQUEST)

#r
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


@api_view(['POST'])
def CheckCurrency(request):
    '''
        Check existence of account and currency for transaction
    '''
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


#endregion

#region CurrencyViews

@api_view(['GET'])
def InitCurrencies(request):
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

#endregion

#region PaymentCodeViews
@api_view(['GET'])
def InitPaymentCodes(request):
    '''
        Initialization of payment codes
    '''
    if(len(PaymentCode.objects.all()) == 0):
        paymentCodes = Parse()

        for k in paymentCodes.keys():
            PaymentCode.objects.create(
                code=k,
                description=paymentCodes[k]
            )
        return JsonResponse(
            "OK",
            status=200,
            safe=False
        )
    else:
        return JsonResponse(
            "Payment codes already initialized.",
            status=409,
            safe=False
        )

@api_view(['GET'])
def GetPaymentCodes(request):
    return JsonResponse(
        PaymentCodeSerializer(
            PaymentCode.objects.all(), many=True
        ).data,
        status=200,
        safe=False
    )
    
#endregion

#region CertificateViews

@api_view(['GET'])
def GetServerPublicKey(request):
    try:
        publicKey = LoadKey(
            GetCertificateFilePath(True)
        )

        return JsonResponse(
            publicKey.export_key().decode('utf-8'),
            status=200,
            safe=False
        )
    except Exception:
        return JsonResponse(status=404, safe=False)

@api_view(['GET'])
def GetUserPublicKey(request):
    try:
        username = request.GET.get('username')
        publicKey = LoadKey(
            GetCertificateFilePath(True, username)
        )
        
        return JsonResponse(
            publicKey.export_key().decode('utf-8'),
            status=200,
            safe=False
        )

    except Exception as e:
        return JsonResponse(status=404, safe=False)

#endregion