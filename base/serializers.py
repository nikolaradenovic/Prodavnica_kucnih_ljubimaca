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
    pet_breed_name = serializers.CharField(source='pet_type.pet_breed.pet_breed_name')
    class Meta:
        model = Ad
        fields = ('ad_title', 'description', 'pet_date_of_birth', 'phone_number', 'price', 'address', 'user', 'city', 'pet_type','pet_breed_name', 'image', 'created')

#serializer za fetchovanje oglasa
class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    city = serializers.StringRelatedField() 
    pet_breed_name = serializers.SerializerMethodField()
    def get_pet_breed_name(self, obj):
        if obj.pet_type:
            pet_breeds = PetBreeds.objects.filter(pet_type=obj.pet_type)
            if pet_breeds.exists():
                return pet_breeds[0].pet_breed_name
        return None

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
                  'pet_breed_name')

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