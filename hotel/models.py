
from tkinter import CASCADE
from django.db import models
from portal.models import Room, HotelAdmin
# from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

User = get_user_model()
# from django.contrib.auth import get_user_model

# Create your models here.



# class MyUserManager(BaseUserManager):
#     def create_user(self, email, date_of_birth, password=None):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#             date_of_birth=date_of_birth,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, date_of_birth, password=None):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             date_of_birth=date_of_birth,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class MyUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     date_of_birth = models.DateField()
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = MyUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['date_of_birth']

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin
    
    
    
    # User = get_user_model()










class Customer(models.Model):
    
    # cus_id = models.IntegerField(primary_key=True)
    cus_name=models.CharField(max_length=255)
    cus_cnic=models.IntegerField(unique=True)
    cus_username=models.CharField(max_length=255, unique=True)
    cus_email=models.EmailField(max_length=255, unique=True)
    cus_password = models.CharField(max_length=50)
    room= models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Customer id: "+str(self.id)
    
    
    
class Bookings(models.Model):
    room_no = models.ForeignKey(Room, on_delete=models.CASCADE)
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    booked_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    #customer id, room id, amount
    
    def __str__(self):
        return "Booking ID: "+str(self.id)
    @property
    def is_past_due(self):
        return date.today()>self.end_date
    
    

    
class Payments(models.Model):
    bookings_no=models.ForeignKey(Bookings, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    payment_amount = models.IntegerField()
    payment_type = models.CharField(max_length=255)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Payment id: "+str(self.id)
    

    
    