from rest_framework import serializers
from .models import Ad 
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email') 

class AdSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Ad
        fields = ('id', 
                  'ad_title', 
                  'description', 
                  'created', 
                  'age', 
                  'phone_number', 
                  'price', 
                  'address', 
                  'user',
                  'city',
                  'pet_type',)
