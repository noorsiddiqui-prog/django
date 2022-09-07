from rest_framework.response import Response
from blog.models import  Blog, Comments
from blog.serializers import BlogSerializer, CommentSerializer, BlogUserRegisterSerializer
from rest_framework.views import APIView
from rest_framework import status, viewsets
# from django.contrib.auth.models import User
from django.http import Http404
from blog.permissions import IsOwner
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend



from rest_framework import status, viewsets, generics

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth import get_user_model
User = get_user_model()


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = BlogUserRegisterSerializer

     
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
        
        
        







    
class BlogList(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blog_date']



class BlogView(APIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated , IsOwner]
    
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', 'blog_title']
    # filter_backends = [SearchFilter]
    filter_fields = ('category',)
    search_fields = ('blog_title')
    # ordering_fields=()
    
    
    def post(self, request, format=None):
        serializer = BlogSerializer(data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Room is booked Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)





    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            try:
                candidates = Blog.objects.get(pk=id)
                self.check_object_permissions(self.request, candidates)
                serializer = BlogSerializer(candidates)
                return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
                # return candidates
            except Blog.DoesNotExist:
                raise Http404

        candidates = Blog.objects.filter(user=request.user)
        serializer = BlogSerializer(candidates, many=True)
        return Response({'status': 'success', 'candidate': serializer.data},
                        status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            obj = Blog.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Blog.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        candidates = self.get_object(pk)
        # snippet = self.get_object(pk)
        serializer = self.serializer_class(
            candidates, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            # return Response(serializer.data)
            return Response({'msg': 'Complete Data Updated'}, serialized_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):

        candidates = self.get_object(pk)
        # snippet = self.get_object(pk)
        serializer = self.serializer_class(
            candidates, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            # return Response(serializer.data)
            return Response({'msg': 'Complete Data Updated'}, serialized_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        candidates = Blog.objects.get(pk=pk)
        # candidates = self.get_object(pk=pk)
        self.check_object_permissions(self.request, candidates)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)













    # def get(self, request, pk=None, format=None):
    #     id=pk
    #     if id is not None:
    #         candidates = Blog.objects.get(id=id)
    #         serializer = BlogSerializer(candidates)
    #         return Response({'status': 'success', 'candidate': serializer.data},
    #                             status=status.HTTP_200_OK)
    #     candidates=Blog.objects.all()
    #     serializer=BlogSerializer(candidates, many=True)
    #     return Response(serializer.data)
        
    # def put(self, request, pk, format=None):
    #     id=pk
    #     candidates = Blog.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = BlogSerializer(candidates, data=request.data, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def patch(self, request, pk, format=None):
    #     id=pk
    #     candidates = Blog.objects.get(pk=id)
    #     serializer = BlogSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
            
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self, request, pk, format=None):
    #     id=pk
    #     candidates = Blog.objects.get(pk=id)
    #     candidates.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    

class CommentView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated , IsOwner]
     
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Room is booked Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)



    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            try:
                candidates = Comments.objects.get(pk=id)
                self.check_object_permissions(self.request, candidates)
                serializer = CommentSerializer(candidates)
                return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
                # return candidates
            except Comments.DoesNotExist:
                raise Http404

        candidates = Comments.objects.filter(user=request.user)
        serializer = CommentSerializer(candidates, many=True)
        return Response({'status': 'success', 'candidate': serializer.data},
                        status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            obj = Comments.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Comments.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        candidates = self.get_object(pk)
        # snippet = self.get_object(pk)
        serializer = self.serializer_class(
            candidates, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            # return Response(serializer.data)
            return Response({'msg': 'Complete Data Updated'}, serialized_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):

        candidates = self.get_object(pk)
        # snippet = self.get_object(pk)
        serializer = self.serializer_class(
            candidates, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            # return Response(serializer.data)
            return Response({'msg': 'Complete Data Updated'}, serialized_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        candidates = Comments.objects.get(pk=pk)
        # candidates = self.get_object(pk=pk)
        self.check_object_permissions(self.request, candidates)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
    







    # def get(self, request, pk=None, format=None):
    #     id=pk
    #     if id is not None:
    #         candidates = Comments.objects.get(id=id)
    #         serializer = CommentSerializer(candidates)
    #         return Response({'status': 'success', 'candidate': serializer.data},
    #                             status=status.HTTP_200_OK)
    #     candidates=Comments.objects.all()
    #     serializer=CommentSerializer(candidates, many=True)
    #     return Response(serializer.data)
        
    # def put(self, request, pk, format=None):
    #     id=pk
    #     candidates = Comments.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = CommentSerializer(candidates, data=request.data, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def patch(self, request, pk, format=None):
    #     id=pk
    #     candidates = Comments.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = CommentSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self, request, pk, format=None):
    #     id=pk
    #     candidates = Comments.objects.get(pk=id)
    #     candidates.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
# class BlogList(generics.ListAPIView):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['blog_date']