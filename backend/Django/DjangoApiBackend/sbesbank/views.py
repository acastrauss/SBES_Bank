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