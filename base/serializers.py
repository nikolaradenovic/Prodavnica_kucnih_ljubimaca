from rest_framework import serializers
from .models import Ad, PetTypes
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
        fields = ('ad_title', 'description', 'pet_date_of_birth', 'phone_number', 'price', 'address', 'user', 'city', 'pet_type', 'image', 'created')

#serializer za fetchovanje oglasa
class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    city = serializers.StringRelatedField() 
    pet_type = serializers.StringRelatedField()
    #image_url = serializers.SerializerMethodField() # ----------------
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
                  'image')
    # metoda za serializovanje filtera po pet_type    
        # ----------------------------------------------
    def get_image_url(self, ad):
        if ad.image:
            return self.context['request'].build_absolute_uri(ad.image.url)
        else:
            return None
        # -----------------------------------------------
    def ads_by_pet_type_serializer(ads_with_matching_pet_type, ad_list):
        for ad in ads_with_matching_pet_type:
            ad_list.append({ 
                'ad_title': ad.ad_title,
                'description': ad.description,
                'created': ad.created,
                'last_updated': ad.last_updated,
                
                'pet_date_of_birth' : ad.pet_date_of_birth,
                'phone_number':ad.phone_number,
                'price': ad.price,
                'address': ad.address,
                'user': ad.user.username, 
                'city': ad.city.city_name,
                #'image': ad.image.url or ''
            })
        return (ad_list)