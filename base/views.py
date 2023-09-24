from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, serializers
from .models import Ad, User, PetTypes, Cities
from .serializers import AdSerializer, UserSerializer
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
import json

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
    
#login view
class UserLoginView(LoginView):
    def form_invalid(self, form):
        return JsonResponse({'error': 'Invalid username or password'}, status=401)

    def form_valid(self, form):
        self.request.session['user_logged_in'] = True 
        return JsonResponse({'message': 'Login successful'})

#CRUD za filter oglasa po pet_type
def ads_by_pet_type(request, pet_type, city = None):
    pet_type_obj = get_object_or_404(PetTypes, pet_type_name=pet_type) #fetch sve PetTypes objekte koji se poklapaju sa pet_types ulaznim arg
    ads_with_matching_pet_type = Ad.objects.filter(pet_type=pet_type_obj).select_related('user') #fetch Ad objekte odredjenog pet_type
    ad_list = [] #^^^select related sluzi da selektuje objekte povezane na Ad preko user FK
    if city:
        city_type_obj = get_object_or_404(Cities, city_name=city) 
        ads_with_matching_pet_type = ads_with_matching_pet_type.filter(city = city_type_obj)
    return JsonResponse({'ads': AdSerializer.ads_by_pet_type_serializer(ads_with_matching_pet_type, ad_list)})
