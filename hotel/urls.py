# """Project URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/4.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path, include
from hotel import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from hotel.views  import UserViewSet
from rest_framework import routers

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from hotel.views import RegisterAPIView, LogOutAPIView
# router = routers.DefaultRouter()
# router.register('users', UserViewSet )




urlpatterns = [

#     path('', include(router.urls)),
    path('customer/', views.CustomerView.as_view(), name='customer'),
    path('customer/<int:pk>/', views.CustomerView.as_view(), name='customer-list'),
    
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout', LogOutAPIView.as_view(), name='logout_view'),
    
    path('api/register/', RegisterAPIView.as_view()),
    
    path('bookings/', views.BookingsView.as_view(), name='bookings'),
    path('bookings/<int:pk>/', views.BookingsView.as_view(), name='bookings-list'),
    path('bookings/list/', views.BookingsList.as_view(), name='bookings-list-view'),


    
    path('payments/', views.PaymentView.as_view(), name='payments'),
    path('payments/<int:pk>/', views.PaymentView.as_view(), name='payments-list'),
    

    
    
#     path('auth/', obtain_auth_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


