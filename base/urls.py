from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #login
    path('login/', UserLoginView.as_view(), name='login'),
    #logout
    path('logout/', UserLogout.as_view(), name='logout'),
    #izlistavanje svih oglasa
    path('ads/', AdListView.as_view(), name='get-ad-list'), 
    #kreiranje novog oglasa
    path('ads/create_new_ad/', AdListCreateView.as_view(), name='ad-list-create'), 
    #CRUD odredjenog oglasa
    path('ads/<int:pk>/', AdRetrieveUpdateDestroyView.as_view(), name='ad-retrieve-update-destroy'),
    #url svi korisnici
    path('users/', UserListCreateView.as_view(), name='user-list-create'), 
    #url neki korisnik
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    #oglasi nekog korisnika
    path('users/<int:user_id>/user_ads/', UsersAds.as_view(), name='current-user-ads'),
    #filter oglasa
    path('ad_filter/', AdFilter.as_view(), name='ad-filter'),  
    #fetch svih gradova
    path('cities/', FetchCities.as_view(), name='fetch-all-cities'),
    #fetch svih pet_typova
    path('pet_types/', FetchPetTypes.as_view(), name='fetch-all-pet_types'),
    #fetch svih pet_breedova za neki pet_type
    path('pet_breeds/<str:pet_type>/', FetchPetBreeds.as_view(), name='fetch-all-pet_breeds'),
    #view za dodavanje novih tipova ljubimaca. prima json sa pet_type i optional pet_type_image
    path('add_pet_type/', AddPetType.as_view(), name='add-pet_type'),
    #view za dodavanje novih gradova. prima json sa city_name
    path('add_city/', AddCity.as_view(), name='add-city'),
    #view za dodavanje novih rasa. prima json sa pet_breed i pet_type za koji se ovaj pet breed vezuje
    path('add_pet_breed/', AddPetBreed.as_view(), name='add-pet_breed'),
  
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)