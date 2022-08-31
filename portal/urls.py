from django.contrib import admin
from django.urls import path, include
from portal import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from portal.views  import UserViewSet
from rest_framework import routers

from portal.views import portalRegisterAPIView, PortalLogOutAPIView
# router = routers.DefaultRouter()
# router.register('users', UserViewSet )




urlpatterns = [
    
    # path('', include(router.urls)),
    # path('manager/', include('portal.urls')),
    path('room/', views.RoomView.as_view(), name='room'),
    path('room/<int:pk>/', views.RoomView.as_view(), name='room'),
    path('room/list/', views.RoomList.as_view(), name='room-list-view'),

    
    path('roomtypes/', views.RoomTypesView.as_view(), name='roomtypes'),
    path('roomtypes/<int:pk>/', views.RoomTypesView.as_view(), name='roomtypes'),

    path('roomtypes/list/', views.RoomTypesList.as_view(), name='roomtypes-list-view'),

    
  
    
    path('food/', views.FoodView.as_view(), name='food'),
    path('food/<int:pk>/', views.FoodView.as_view(), name='food-list'),
    path('food/list/', views.FoodList.as_view(), name='food-list-view'),

    
    path('hotelprofile/', views.HotelAdminView.as_view(), name='hotelprofile'),
    path('hotelprofile/<int:pk>/', views.HotelAdminView.as_view(), name='list'),
    path('hotelprofilelogin' , TokenObtainPairView.as_view(), name='login'),
    path('hotelprofile/refresh-token' , TokenRefreshView.as_view(), name='refrehtoken'),
    path('hotelprofile/list/', views.HotelAdminList.as_view(), name='hotel-list-view'),


    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout', PortalLogOutAPIView.as_view(), name='logout_view'),
    
    path('api/register/', portalRegisterAPIView.as_view()),
    
    path('auth/', obtain_auth_token),
] 