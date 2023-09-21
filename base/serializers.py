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
                  'user',)
        
    #def create(self, validated_data):
        #user_data = validated_data.pop('user')
        #user_instance, created = User.objects.get_or_create(**user_data)
        #ad = Ad.objects.create(user=user_instance, **validated_data)
        #return ad