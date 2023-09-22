from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from .models import Ad, User, PetTypes, Cities
from .serializers import AdSerializer, UserSerializer
from django.shortcuts import get_object_or_404

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

#crud za filter oglasa po pet_type
def ads_by_pet_type(request, pet_type):
    pet_type_obj = get_object_or_404(PetTypes, pet_type_name=pet_type)
    ads_with_matching_pet_type = Ad.objects.filter(pet_type=pet_type_obj)
    ad_list = []
    for ad in ads_with_matching_pet_type:
        ad_list.append({
            'ad_title': ad.ad_title,
            'description': ad.description,
            'created': ad.created,
            'phone_number':ad.phone_number,
            'price': ad.price,
            'address': ad.address,
            'user': ad.user,
            'city': ad.city.__str__
         })

    return JsonResponse({'ads': ad_list})