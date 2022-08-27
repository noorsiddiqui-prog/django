
from rest_framework import serializers
from portal.models import HotelAdmin,  Room, Food
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
User = get_user_model()

class UserPortalRegisterSerializer(serializers.ModelSerializer):
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



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields = ['id', 'username', 'email', 'password' ]
#         # extra_kwargs = {
#         #     'password' : {'write_only' :  True , 
#         #     'required' : True}
#         #     }
        
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         Token.objects.create(user=user)
#         return user


class HotelAdminSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type' : 'password'}, write_only = True)
    # bookings_no = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = HotelAdmin
        fields =  ['id', 'name', 'email', 'location', 'images', 'ratings', 'city', 'description', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only' : True, 'required' : True},
            'password2' : {'write_only' : True, 'required' : True}
        }
        
        def validate(self, args):
            email = args.get('email', None)
            username = args.get('username', None)
            
            if HotelAdmin.objects.filter(email=email).exists():
                raise serializers.ValidationError({'email' : 'email already exists'})
            
            if HotelAdmin.objects.filter(username=username).exists():
                raise serializers.ValidationError({'username' : 'username already exists'})
            
            return super.validate(args)
        
        def create(self, validated_data):
            return HotelAdmin
        

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields =  ['id', 'hotel', 'room','room_type', 'beds', 'room_description', 'is_available', 'price', 'room_images']
        
        
       
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields =  ['id', 'food_name', 'food_price', 'food_type', 'hotel_no', 'food_image']
        
       
