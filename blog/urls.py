"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from blog.views  import UserViewSet
# from rest_framework import routers

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from blog.views import BlogRegisterAPIView, BlogLogOutAPIView

# router = routers.DefaultRouter()
# router.register('users', UserViewSet )




urlpatterns = [
    
    # path('', include(router.urls)),

    
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog/<int:pk>/', views.BlogView.as_view(), name='blog-list'),
    path('blog/list/', views.BlogList.as_view(), name='blog-list-view'),
    
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment-list'),
    
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout', BlogLogOutAPIView.as_view(), name='logout_view'),
    
    path('api/register/', BlogRegisterAPIView.as_view()),
    
    
    path('auth/', obtain_auth_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)