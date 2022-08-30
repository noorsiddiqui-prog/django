
from django.db import models
# from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.


class HotelAdmin(models.Model):
 
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    ratings = models.PositiveIntegerField(default=2)
    city = models.CharField(max_length=100, default="")
    images = models.ImageField(blank=True, upload_to='HotelImages' )
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    # password2 = models.CharField(max_length=50)
    # available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    # def nameFile(instance, filename):
    #     return '/'.join(['HotelImages', str(instance.name), filename])
    
    def __str__(self):
        return self.name


class Room(models.Model):
    
    hotel = models.ForeignKey(HotelAdmin, on_delete=models.CASCADE)
    room = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=100)
    beds = models.PositiveIntegerField(default=2)
    room_description = models.TextField(max_length=255)
    is_available = models.BooleanField(default=True)
    room_price = models.IntegerField()
    room_images = models.ImageField(blank=True, upload_to='RoomImages' )
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Room No: "+str(self.id)
    
    
    
class Food(models.Model):
    food_name=models.CharField(max_length=255, unique=True)
    food_price = models.IntegerField()
    food_type = models.CharField(max_length=255)
    hotel_no = models.ForeignKey(HotelAdmin, on_delete=models.CASCADE)
    food_image=models.ImageField(blank=True, upload_to='FoodImages' )
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Food name: "+str(self.food_name)
    
    


    