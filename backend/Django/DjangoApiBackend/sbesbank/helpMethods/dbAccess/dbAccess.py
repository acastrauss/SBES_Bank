
from sbesbank.models import *
import copy

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
