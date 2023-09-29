from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from .models import Ad, User, PetTypes, Cities, PetBreeds
from .serializers import AdSerializer, AdCreateSerializer, UserSerializer, UserLoginSerializer, UserCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.decorators import login_required

#basic Home Page view
def home(request):
    content = "<html><h1>Pocetna</h1></html>"
    return HttpResponse(content)

#kreiranje oglasa
class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    #ovaj view ce da sluzi samo da kreira novi ad i zbog toga je get metod disabled
    def get(self, request, *args, **kwargs):
        return Response({})

#izlistavanje svih oglasa
class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    #permission_classes =[IsAuthenticated]
    #authentication_classes = (JWTAuthentication)

#CRUD odredjenog oglasa
class AdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =[IsAuthenticated]
    authentication_classes = (JWTAuthentication,)
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

#CRUD korisnika
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
        
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#view za Ad-ove nekog korisnika
class UsersAds(APIView):
    def get(self, request, user_id):  
        user = get_object_or_404(User, id=user_id)
        current_user_ads = Ad.objects.filter(user=user) #vraca sve Ad-ove ovog Usera
        serialized_data = AdSerializer(current_user_ads, many=True)
        return Response({'current_user_ads': serialized_data.data})

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

class UserLogout(APIView):
    def post(self, request):
        logout(request)

        return Response({'message': 'You have been logged out'})

#filter oglasa po pet_type
#ovaj view mozda predefinisati u get metodu APIview klase, a filtere po
#gradu, rasi itd. pretvoriti u metode te klase?
@permission_classes([IsAuthenticated])
def ads_by_pet_type(request, pet_type, city = None, breed = None):
    pet_type_obj = get_object_or_404(PetTypes, pet_type_name=pet_type) #fetch sve PetTypes objekte koji se poklapaju sa pet_types ulaznim arg
    ads_with_matching_pet_type = Ad.objects.filter(pet_type=pet_type_obj).select_related('user') #fetch Ad objekte odredjenog pet_type
    ad_list = [] #^^^select related sluzi da selektuje objekte povezane na Ad preko user FK
    if city and breed == None:
        city_type_obj = get_object_or_404(Cities, city_name=city) 
        ads_with_matching_pet_type = ads_with_matching_pet_type.filter(city = city_type_obj)
    if breed and city == None:
        breed_type_obj = get_object_or_404(PetBreeds, breed_name=breed) 
        ads_with_matching_pet_type = ads_with_matching_pet_type.filter(breed = breed_type_obj)
    return JsonResponse({'ads': AdSerializer.ads_by_pet_type_serializer(ads_with_matching_pet_type, ad_list)})

#view za testiranje logina (bice)
@login_required
def logintestview(request):
    content = "<html><h1>Youre logged in!</h1></html>"
    return HttpResponse(content)