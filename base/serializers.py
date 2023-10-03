from rest_framework import serializers
from .models import Ad, PetTypes, Cities, PetBreeds
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

#serializer za user crud
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name') 
        
#serializer za user create
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','password', 'first_name', 'last_name') 
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super(UserCreateSerializer, self).create(validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):  
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

#serializer za kreiranje oglasa  
class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('ad_title', 'description', 'pet_date_of_birth', 'phone_number', 'price', 'address', 'user', 'city', 'pet_type','pet_breed', 'image', 'created')
    def validate_pet_breed(self, value): #da li unijeti pet breed odgovara unijetom pet typeu
        pet_type = self.initial_data.get('pet_type')
        if pet_type and value:
            if pet_type == self.pet_breed.pet_type:
                raise serializers.ValidationError("Selected pet breed does not belong to the selected pet type.")
        return value
#serializer za fetchovanje oglasa
class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    city = serializers.StringRelatedField() 
    pet_type = serializers.StringRelatedField()
    class Meta:
        model = Ad
        fields = ('id', 
                  'ad_title', 
                  'description', 
                  'created', 
                  'pet_date_of_birth', 
                  'phone_number', 
                  'price', 
                  'address', 
                  'user',
                  'city',
                  'pet_type',
                  'image',
                  'pet_breed')

#serializer za fetch svih gradova   
class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ('id', 'city_name')
        
#serializer za fetch svih pet_typeova          
class PetTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetTypes
        fields = ('id', 'pet_type_name')

#serializer za fetch svih pet_breedova u zavisnosti od pet_typea. prima pk pet_typea        
class PetBreedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetBreeds
        fields = ('id', 'pet_breed_name', 'pet_type')