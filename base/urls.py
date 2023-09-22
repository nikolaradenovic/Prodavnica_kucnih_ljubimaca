from django.urls import path
from . import views
from .views import AdListCreateView, AdRetrieveUpdateDestroyView, UserListCreateView, UserRetrieveUpdateDestroyView, ads_by_pet_type

urlpatterns = [
    #url oglasi
    path('ads/', AdListCreateView.as_view(), name='ad-list-create'), 
    path('ads/<int:pk>/', AdRetrieveUpdateDestroyView.as_view(), name='ad-retrieve-update-destroy'),
    #url korisnici
    path('users/', UserListCreateView.as_view(), name='user-list-create'), 
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    #url za filter oglasa po pet_type
    path('ads/<str:pet_type>', ads_by_pet_type, name='ads-by-pet-type')
]
