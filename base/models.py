from django.db import models
from django.contrib.auth.models import User 

class PetBreeds(models.Model):
    pet_breed_name =  models.CharField(max_length=20, null=False)
    
    def __str__(self):
        return self.pet_breed_name

class PetTypes(models.Model):
    pet_type_name =  models.CharField(max_length=20, null=False)
    pet_breed = models.ForeignKey(PetBreeds, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.pet_type_name

class Cities(models.Model):
    city_name = models.CharField(max_length=30, null=False)
    
    def __str__(self):
        return self.city_name

class Ad(models.Model): #oglas
    ad_title = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=200, null=True, blank=True) #null = True znaci da nije obavezno polje
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    pet_date_of_birth = models.DateField(null=True) #null True jer nije htjelo da radi. Ispraviti!!!
    phone_number = models.CharField(max_length=15, null=False)
    price = models.IntegerField(null=False)
    address = models.CharField(max_length=50, null=False)
    #image = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0, null=False) #fk od Users
    pet_type = models.ForeignKey(PetTypes, on_delete=models.SET_NULL,null=True) #fk od PetTypes
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True) #fk on Cities
    #null = true sam stavio jer zelim da pri brisanju grada/tipa upisem null. Ovo nije cest use case
    
    def __str__(self):
        return self.ad_title
    