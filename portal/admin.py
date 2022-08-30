from django.contrib import admin
from .models import HotelAdmin, Room, Food
# from rest_framework import routers, serializers, viewsets
# # Register your models here.

# admin.site.register(HotelAdmin)
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

@admin.register(HotelAdmin)
class HotelModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'location', 'images', 'ratings', 'city', 'description', 'password', 'admin']
    
@admin.register(Room)
class RoomModelAdmin(admin.ModelAdmin):
    list_display =  ['id', 'hotel', 'room','room_type', 'beds', 'room_description', 'is_available', 'room_price', 'room_images', 'admin']
    


@admin.register(Food)
class FoodModelAdmin(admin.ModelAdmin):
    list_display =  ['id', 'food_name', 'food_price','food_type', 'hotel_no', 'food_image', 'admin']