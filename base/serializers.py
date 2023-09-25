from rest_framework import serializers
from .models import Ad, PetTypes
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

#serializer za user crud
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name') 
#serializer
class UserLoginSerializer(serializers.Serializer):  
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
#serializer za user login response
#class UserLoginResponseSerializer(serializers.Serializer):
#    id = serializers.IntegerField()
#    username = serializers.CharField()
#    first_name = serializers.CharField()
#    last_name = serializers.CharField()
#    email = serializers.EmailField()

class AdSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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
                #'image': get_image_url(ad)
            })
        return (ad_list)