from rest_framework import serializers
from .models import Ad, PetTypes, Cities, PetBreeds
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

#serializer za user crud
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 
                  'username', 
                  'email', 
                  'first_name', 
                  'last_name') 
        
#serializer za user create
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 
                  'username', 
                  'email',
                  'password', 
                  'first_name', 
                  'last_name') 
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super(UserCreateSerializer, self).create(validated_data)
        return user

#serializer za login. ima samo username i password
class UserLoginSerializer(serializers.Serializer):  
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

#serializer za kreiranje oglasa  
class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('user', #user salje frontend da bismo znali koji user kreira oglas
                  'ad_title', 
                  'description', 
                  'pet_date_of_birth', 
                  'phone_number', 
                  'price', 
                  'address', 
                  'city', 
                  'pet_type',
                  'pet_breed', 
                  'image', 
                  'created') 

#serializer za fetchovanje oglasa
class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    city = serializers.StringRelatedField() 
    pet_type = serializers.StringRelatedField()
    pet_breed = serializers.StringRelatedField()
    class Meta:
        model = Ad
        fields = ('user',
                  'id', 
                  'ad_title', 
                  'description', 
                  'pet_date_of_birth',
                  'phone_number',
                  'price',               
                  'address', 
                  'city',
                  'pet_type',
                  'pet_breed',
                  'image',                
                  'created')

#serializer za fetch svih gradova   
class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = ('id', 'city_name')
        
#serializer za fetch svih pet_typeova          
class PetTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetTypes
        fields = ('id', 'pet_type_name', 'pet_type_image')

#serializer za fetch svih pet_breedova u zavisnosti od pet_typea. prima pk pet_typea        
class PetBreedsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetBreeds
        fields = ('id', 'pet_breed_name', 'pet_type')