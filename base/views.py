from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from .models import Ad, User, PetTypes, Cities
from .serializers import AdSerializer, UserSerializer
from django.shortcuts import get_object_or_404

#basic Home Page view

def home(request):
    content = "<html><h1>Pocetna</h1></html>"
    return HttpResponse(content)

#CRUD oglasa
class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

class AdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

#CRUD korisnika
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#CRUD za filter oglasa po pet_type
def ads_by_pet_type(request, pet_type):
    pet_type_obj = get_object_or_404(PetTypes, pet_type_name=pet_type)
    ads_with_matching_pet_type = Ad.objects.filter(pet_type=pet_type_obj).select_related('user') #select related sluzi da selektuje objekte povezane na Ad preko user FK
    ad_list = []
    for ad in ads_with_matching_pet_type:
        #user = ad.user.username
        ad_list.append({ #srediti ovaj serializer!!!!!!!! da radi sa user i city
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
         })

    return JsonResponse({'ads': ad_list})