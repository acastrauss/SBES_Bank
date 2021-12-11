from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sbesbank.models import *
from sbesbank.serializers import *
# Create your views here.

from modules.exchangeRates import (
    parse
)
import copy

from sbesbank.models import Currency

@api_view(['GET'])
def TrAcTransfer(request, id):
    obj = TrAcTransferInfo.objects.get(id=id)
    serializer = TrAcTransferInfoSerializer(obj) 

    parser = parse.MyParser()
    parser.Parse()
    
    dataDict = copy.deepcopy(parser.dataDict)
    # del dataDict['DKK']
    # del dataDict['JPY']
    # del dataDict['NOK']
    # del dataDict['SEK']

    ids = ExchangeRate.objects.values('id')

    maxId = 1

    if len(ids) > 0:
        maxId = ids.order_by('-id').first()

    print(maxId)

    for key in dataDict:
        
        try:
            c = str(copy.deepcopy(key))
            rate = float(copy.deepcopy(dataDict[key]))
            curr = Currency[c]

            ExchangeRate.objects.create(
                id=maxId,
                currency=Currency[c],
                rateInDinar=rate
            )

            maxId += 1

        except KeyError:
            continue

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
def CertData(requset, userId):
    obj = Certificate.objects.get(userId = userId)
    serializer = CertificateSerializer(obj)

    return JsonResponse(serializer.data)


