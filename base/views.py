from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import generics, serializers, status, permissions
from rest_framework.views import APIView
from .models import Ad, User, PetTypes, Cities, PetBreeds
from .serializers import * 
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, api_view
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

#basic Home Page view
def home(request):
    content = "<html><h1>Pocetna</h1></html>"
    return HttpResponse(content)

#kreiranje oglasa
class AdListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny] #<---obrisati kasnije
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    #ovaj view sluzi samo da kreira novi ad i zbog toga je get metod disabled
    def get(self, request, *args, **kwargs):
        return Response({})

#izlistavanje svih oglasa
class AdListView(generics.ListAPIView):
    permission_classes = [AllowAny] #obrisati ovu liniju !!!!!!!!!!!!
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

#CRUD odredjenog oglasa
class AdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self): #overridujem get_permissions metodu da get dozvoli svima, a update, create, delete dozvoli samo logovanim korisnicima
        if self.request.method in permissions.SAFE_METHODS: #safe methods su samo za view i one su allowany
            return [permissions.AllowAny()]
        else: #koje nisu safe (create, delete, update) dobijaju isauthenticated
            return [permissions.IsAuthenticated()]
    def get_object(self):
        obj = get_object_or_404(Ad, pk=self.kwargs.get('pk')) #ad koji hocemo da izmijenimo
        if self.request.user != obj.user: #ako user koji pravi zahtjev nije isti kao user koji je napravio ad blokiramo pristup
            pass #raise permissions.PermissionDenied("You do not have permission to perform this action.")
        return obj
    queryset = Ad.objects.all()
    serializer_class = AdSerializer 

#CRUD korisnika
class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
        
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self): 
        if self.request.method in permissions.SAFE_METHODS: 
            return [permissions.AllowAny()]
        else: 
            return [permissions.IsAuthenticated()]
        
    def get_object(self):
        obj = get_object_or_404(User, pk=self.kwargs.get('pk')) #user kojeg hocemo da izmijenimo
        if self.request.user != obj: #ako user koji je podnio zahtjev nije isti kao onaj koji hoce da promijeni odbijamo pristup
            pass#return PermissionDenied("You do not have permission to perform this action.")
        return obj
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

#view za listanje Ad-ove nekog korisnika
class UsersAds(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):  
        user = get_object_or_404(User, id=user_id)
        current_user_ads = Ad.objects.filter(user=user) #vraca sve Ad-ove ovog Usera
        serialized_data = AdSerializer(current_user_ads, many=True)
        return Response({'current_user_ads': serialized_data.data})

#login view
class UserLoginView(APIView):
    permission_classes = [AllowAny]
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
"""
{
"username": "nikolaradenovic",
"password": "svjezeljeto"
}
"""
#logout
class UserLogout(APIView):
    def post(self, request):
        logout(request)

        return Response({'message': 'You have been logged out'})

#filter za adove po pet_type, city i breed. prima json 
class AdFilter(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        json_data = request.data
        filter_results = Ad.objects.all()
        if 'pet_type' in json_data: #filter po tipu ljubimca
            pet_type = json_data['pet_type']
            pet_type_obj = get_object_or_404(PetTypes, pet_type_name=pet_type) #fetch sve PetTypes objekte koji se poklapaju sa pet_types ulaznim arg
            filter_results = filter_results.filter(pet_type=pet_type_obj).select_related('user') #fetch Ad objekte odredjenog pet_type
        if 'city' in json_data: #filter po gradu                       ^^^select related sluzi da selektuje objekte povezane na Ad preko user FK
            city = json_data['city']
            city_type_object = get_object_or_404(Cities, city_name=city)
            filter_results = filter_results.filter(city=city_type_object)
        if 'breed' in json_data: #filter po rasi
            breed = json_data['breed']
            breed_type_object = get_object_or_404(PetBreeds, breed_name=breed)
            filter_results = filter_results.filter(breed=breed_type_object)                       
        
        return JsonResponse({'filtered_ads': AdSerializer(filter_results, many=True).data})

#fetch svih gradova      
class FetchCities(APIView):
    permission_classes = [AllowAny]
    def get(self, request):     
        cities = Cities.objects.all()
        return Response({'cities': CitiesSerializer(cities, many=True).data})   
             
#fetch sve pet_types
class FetchPetTypes(APIView):
    permission_classes = [AllowAny]
    def get(self, request):     
        pet_types = PetTypes.objects.all()
        return Response({'pet_types': PetTypesSerializer(pet_types, many=True).data})

#fetch sve pet_breeds za neki pet_type
class FetchPetBreeds(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pet_type):
        pet_breeds = PetBreeds.objects.filter(pet_type__pet_type_name=pet_type)
        return Response({'pet_breeds': PetBreedsSerializer(pet_breeds, many=True).data})

#adminov view za dodavanje novih pet_typova 
class AddPetType(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        json_data = request.data
        if 'pet_type' in json_data: 
            pet_type_name = json_data['pet_type']
            try:
                pet_type = PetTypes.objects.get(pet_type_name=pet_type_name)
                return Response({'message': 'Pet type with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            except PetTypes.DoesNotExist:
                new_pet_type = PetTypes(pet_type_name=pet_type_name)
                new_pet_type.save()
                return Response({'message': 'Pet type added successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'No valid data provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
#adminov view za dodavanje novih citya 
class AddCity(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        json_data = request.data
        if 'city_name' in json_data:
            city_name = json_data['city_name']
            try:
                city = Cities.objects.get(city_name=city_name)
                return Response({'message': 'City with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            except Cities.DoesNotExist:
                new_city = Cities(city_name=city_name)
                new_city.save()
                return Response({'message': 'City added successfully.'}, status=status.HTTP_201_CREATED)
            
        return Response({'message': 'No valid data provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
#adminov view za dodavanje novih pet_breedova. Prima json sa pet_breed(string) i pet_type(string)           
class AddPetBreed(APIView):
    permission_classes = [AllowAny]
    def post(self, request):      
        json_data = request.data 
        if ('pet_breed' and 'pet_type') in json_data: #trebaju nam dva podatka is json
            pet_breed_name = json_data['pet_breed'] #smijestamo ih u promjenljive
            pet_type = json_data['pet_type']
            try:
                pet_type = PetTypes.objects.get(pet_type_name=pet_type) #gledamo da li u bazi postoji pettype sa imenom iz jsona
            except PetTypes.DoesNotExist: #ako ne postoji, vracamo odgovor
                return Response({'message': 'Pet breed with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                
            pet_type_id = pet_type.id #ako postoji, biljezimo njegov id
            try:
                pet_breed = PetBreeds.objects.get(pet_breed_name=pet_breed_name) #gledamo da li vec postoji pet breed sa imenom iz jsona
                return Response({'message': 'Pet breed with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST) #ako vec ima jedan takav, vracamo bad request
            except PetBreeds.DoesNotExist: #ako takav ne postoji kreiramo novi sa parametrima is jsona
                new_pet_breed = PetBreeds(pet_breed_name=pet_breed_name, pet_type_id = pet_type_id) #pet type id vezuje pet breed sa pet typom!!!!!
                new_pet_breed.save()
                return Response({'message': 'Pet breed added successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response({'message': 'No valid data provided.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logintestview(request):
    print(request.user)
    content = "<html><h1>Youre logged in!</h1></html>"
    return HttpResponse(content)