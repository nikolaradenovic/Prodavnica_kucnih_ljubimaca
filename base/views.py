from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from .models import Ad, User, PetTypes, Cities
from .serializers import AdSerializer, UserSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login

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
    #def get_current_user_ads(self,  pk = None):
        #current_user_ads = Ad.objects.filter(user=self.request.user) #vraca sve Ad-ove ovog Usera
        #return Response({'current_user_ads': AdSerializer(current_user_ads)})
    #overrideovana get metoda koja vraca usera i sve njegove adove

class UsersAds(APIView):
    def get(self, request, pk):  
        current_user_ads = Ad.objects.filter(user=self.request.user) #vraca sve Ad-ove ovog Usera
        serialized_data = AdSerializer(current_user_ads)
        return Response({'current_user_ads': serialized_data})
#login view

class UserLoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username = username, password = password)# ako se korisnik autentifikuje sa ovim kredencijalima, taj User objekat ce biti stavljen u user promjenljivu. u suprotnom, user=None
            if user: #true ako je autentifikovan    
                refresh = RefreshToken.for_user(user)            
                login(request, user)
                return Response({'message': 'Login Successful!', 
                                 'user_id': user.id,
                                 'username': username,
                                 'email': user.email,
                                 'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'access_token': str(refresh.access_token),
                                 'refresh_token': str(refresh)
                                 }, status = status.HTTP_200_OK)
            else:
                return Response({'message': 'Username or password incorrect'}
                                ,status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#{
#"username": "nikolaradenovic",
#"password": "svjezeljeto"
#}

#CRUD za filter oglasa po pet_type
def ads_by_pet_type(request, pet_type, city = None):
    pet_type_obj = get_object_or_404(PetTypes, pet_type_name=pet_type) #fetch sve PetTypes objekte koji se poklapaju sa pet_types ulaznim arg
    ads_with_matching_pet_type = Ad.objects.filter(pet_type=pet_type_obj).select_related('user') #fetch Ad objekte odredjenog pet_type
    ad_list = [] #^^^select related sluzi da selektuje objekte povezane na Ad preko user FK
    if city:
        city_type_obj = get_object_or_404(Cities, city_name=city) 
        ads_with_matching_pet_type = ads_with_matching_pet_type.filter(city = city_type_obj)
    return JsonResponse({'ads': AdSerializer.ads_by_pet_type_serializer(ads_with_matching_pet_type, ad_list)})
