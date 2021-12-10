from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sbesbank.models import *
from sbesbank.serializers import *
# Create your views here.

@api_view(['GET'])
def TrAcTransfer(request, id):
    obj = TrAcTransferInfo.objects.get(id=id)
    serializer = TrAcTransferInfoSerializer(obj) 

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
def AccInfo(request, id):
    obj1 = Account.objects.get(id=id) 
    obj2 = list(Card.objects.filter(accountFK=id))
    serializer1 =  AccountSerializer(obj1)
    serializer2 = CardSerializer(obj2,many = True)
    return JsonResponse({"Account": serializer1.data,
    "Cards": serializer2.data})
