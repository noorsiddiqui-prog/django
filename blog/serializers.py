
from rest_framework import serializers
from blog.models import Blog, Comments
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
User = get_user_model()

class BlogUserRegisterSerializer(serializers.ModelSerializer):
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
    class Meta:
        model=User
        fields = ['id', 'username', 'email', 'password' ]
        # extra_kwargs = {
        #     'password' : {'write_only' :  True , 
        #     'required' : True}
        #     }
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
        
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields =  ['id', 'blog_title', 'blog_content', 'blog_image', 'blog_date']
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields =  ['id', 'comment_content', 'blog_no']