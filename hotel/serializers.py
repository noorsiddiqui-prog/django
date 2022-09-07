
from rest_framework import serializers
from hotel.models import Bookings, Payments, Customer, Payments
from rest_framework.validators import UniqueValidator
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only = True)
    password2 = serializers.CharField(required=True, write_only = True)

    class Meta:
        model = User
        fields= [
             'username',
             'email',
             'password',
             'password2',
        ]
        extra_kwargs = {
            'password': {'write_only' : True},
            'password2': {'write_only' : True}
            
        }

    def create(self, validated_data):
        username= validated_data.get('username')
        email= validated_data.get('email')
        password= validated_data.get('password')
        password2= validated_data.get('password2')
        
        
        if password == password2:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({
                'error' : 'Both passwords do not match'
            })
        
        # return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    pass
    # class Meta:
    #     model=User
    #     fields = ['id', 'username', 'email', 'password' ]
    #     # extra_kwargs = {
    #     #     'password' : {'write_only' :  True , 
    #     #     'required' : True}
    #     #     }
        
    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     Token.objects.create(user=user)
    #     return user

        
class BookingsSerializer(serializers.ModelSerializer):
    #using the customer field here to be choose default customer/user while booking
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # room_no = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Bookings
        fields =  ['id', 'customer', 'start_date', 'end_date', 'booked_on', 'room_type', 'city']
             
class CustomerSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault(),)
    class Meta:
        model = Customer
        fields =  ['id', 'room', 'cus_name', 'cus_cnic', 'cus_username', 'cus_email', 'cus_password', 'customer']
        
        
class PaymentSerializer(serializers.ModelSerializer):
    
    bookings_no = Bookings.objects.all()
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Payments
        fields =  ['id', 'bookings_no', 'payment_date', 'payment_amount', 'payment_type', 'customer']
        