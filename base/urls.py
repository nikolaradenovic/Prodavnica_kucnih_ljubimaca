from django.urls import path
from . import views
from .views import AdListCreateView, AdRetrieveUpdateDestroyView, UserListCreateView, UserRetrieveUpdateDestroyView, UserLoginView, UsersAds, UserLogout, AdListView, logintestview, AdFilter
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
    #view za test logina
    path('logintest/', logintestview, name='logintest'),
    #filter oglasa
    path('ad_filter/', AdFilter.as_view(), name='ad-filter'),    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)