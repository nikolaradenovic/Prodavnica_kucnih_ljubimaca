from django.urls import path
from . import views
from .views import AdListCreateView, AdRetrieveUpdateDestroyView, UserListCreateView, UserRetrieveUpdateDestroyView, ads_by_pet_type, UserLoginView, UsersAds, UserLogout, AdListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #home
    path('', views.home, name='home'),
    #login
    path('login/', UserLoginView.as_view(), name='login'),
    #logout
    path('logout/', UserLogout.as_view(), name='logout'),
    #izlistavanje svih oglasa
    path('ads/', AdListView.as_view(), name='get-ad-list'), 
    #kreiranje novog oglasa
    path('ads/create_new_ad', AdListCreateView.as_view(), name='ad-list-create'), 
    #CRUD odredjenog oglasa
    path('ads/<int:pk>/', AdRetrieveUpdateDestroyView.as_view(), name='ad-retrieve-update-destroy'),
    #url korisnici
    path('users/', UserListCreateView.as_view(), name='user-list-create'), 
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    #oglasi trenutnog korisnika
    path('users/<int:user_id>/user_ads/', UsersAds.as_view(), name='current-user-ads'),
    #url za filter oglasa po pet_type
    path('pet_type_filter/<str:pet_type>', ads_by_pet_type, name='ads-by-pet-type'),
    #url za filter po gradovima oglasa vec filtriranih po pet_type. mapiran na isti view
    path('pet_type_filter/<str:pet_type>/<str:city>/', ads_by_pet_type, name='ads-by-pet-type-and-city'),
    #napraviti filter za pet breed kao prethodni za city !!!!!!!!!!!!!!!!!
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)