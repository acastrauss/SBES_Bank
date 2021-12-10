from rest_framework import serializers 
from sbesbank.models import models

class ModelsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    fullName = serializers.CharField(max_length = 50, unique=False)
    password = serializers.CharField(max_length = 100)
    username = serializers.CharField(max_length = 40, unique = True)
    billingAddress = serializers.CharField(max_length = 50 )
    genders = (('female','female'), ('male','male'))
    gender = serializers.CharField(choices = genders, max_length = 20)
    jmbg = serializers.BigIntegerField(unique = True)
    birthDate  = serializers.DateField()
    userTypes = (('admin','admin'),('client','client'))
    userType = serializers.CharField(choices = userTypes, max_length = 40)

    def create(self, validated_data):
        """
        Create and return a new User instance
        """
        return models.objects.create(**validated_data)
    
