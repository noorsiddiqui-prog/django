from rest_framework.response import Response
from blog.models import  Blog, Comments
from blog.serializers import BlogSerializer, CommentSerializer, BlogUserRegisterSerializer
from rest_framework.views import APIView
from rest_framework import status, viewsets
# from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken




# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
     
class BlogRegisterAPIView(APIView):
    serializer_class = BlogUserRegisterSerializer
    # permission_classes = [IsAuthenticated ,]
    
    def post(self, request, format=None):
        serializer = BlogUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()        
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user' : serializer.data 
            }            
            return Response({'msg' : ' Successfully',
                             'status': 'success', 'candidate': response_data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

class BlogLogOutAPIView(APIView):
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            
            # print(token)
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status=status.HTTP_200_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        


    
class BlogView(APIView):
    permission_classes = [IsAuthenticated ,]
    def post(self, request, format=None):
        serializer = BlogSerializer(data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Room is booked Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def get(self, request, pk=None, format=None):
        id=pk
        if id is not None:
            candidates = Blog.objects.get(id=id)
            serializer = BlogSerializer(candidates)
            return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
        candidates=Blog.objects.all()
        serializer=BlogSerializer(candidates, many=True)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        id=pk
        candidates = Blog.objects.get(pk=id)
        # snippet = self.get_object(pk)
        serializer = BlogSerializer(candidates, data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        id=pk
        candidates = Blog.objects.get(pk=id)
        serializer = BlogSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        id=pk
        candidates = Blog.objects.get(pk=id)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CommentView(APIView):
    permission_classes = [IsAuthenticated ,]
     
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Room is booked Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def get(self, request, pk=None, format=None):
        id=pk
        if id is not None:
            candidates = Comments.objects.get(id=id)
            serializer = CommentSerializer(candidates)
            return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
        candidates=Comments.objects.all()
        serializer=CommentSerializer(candidates, many=True)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        id=pk
        candidates = Comments.objects.get(pk=id)
        # snippet = self.get_object(pk)
        serializer = CommentSerializer(candidates, data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        id=pk
        candidates = Comments.objects.get(pk=id)
        # snippet = self.get_object(pk)
        serializer = CommentSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        id=pk
        candidates = Comments.objects.get(pk=id)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)