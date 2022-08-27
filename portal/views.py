from rest_framework.response import Response
from portal.models import HotelAdmin, Room, Food
from portal.serializers import HotelAdminSerializer, RoomSerializer, FoodSerializer, UserPortalRegisterSerializer
from rest_framework.views import APIView
from rest_framework import status, viewsets
# from django.contrib.auth.models import User


from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken



class portalRegisterAPIView(APIView):
    serializer_class = UserPortalRegisterSerializer
    # permission_classes = [IsAuthenticated ,]
    
    def post(self, request, format=None):
        serializer = UserPortalRegisterSerializer(data=request.data)
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

class PortalLogOutAPIView(APIView):
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            
            # print(token)
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status=status.HTTP_200_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
        


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class HotelAdminView(APIView):
    
    serializer_class = HotelAdminSerializer
    permission_classes = [IsAuthenticated ,]
    
    def post(self, request, format=None):
        serializer = HotelAdminSerializer(data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Hotel Profile created  Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def get(self, request, pk=None, format=None):
        id=pk
        if id is not None:
            candidates = HotelAdmin.objects.get(id=id)
            serializer = HotelAdminSerializer(candidates)
            return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
        candidates=HotelAdmin.objects.all()
        serializer=HotelAdminSerializer(candidates, many=True)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        id=pk
        candidates = HotelAdmin.objects.get(pk=id)
        # snippet = self.get_object(pk)
        serializer = HotelAdminSerializer(candidates, data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        id=pk
        candidates = HotelAdmin.objects.get(pk=id)
        # snippet = self.get_object(pk)
        serializer = HotelAdminSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        id=pk
        candidates = HotelAdmin.objects.get(pk=id)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
     

        
class RoomView(APIView):
    permission_classes = [IsAuthenticated ,]

    def post(self, request, format=None):
        serializer = RoomSerializer(data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Room is booked Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def get(self, request, pk=None, format=None):
        id=pk
        if id is not None:
            candidates = Room.objects.get(id=id)
            serializer = RoomSerializer(candidates)
            return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
        candidates=Room.objects.all()
        serializer=RoomSerializer(candidates, many=True)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        id=pk
        candidates = Room.objects.get(pk=id)
        # snippet = self.get_object(pk)
        serializer = RoomSerializer(candidates, data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        id=pk
        candidates = Room.objects.get(pk=id)
        # snippet = self.get_object(pk)
        serializer = RoomSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        id=pk
        candidates = Room.objects.get(pk=id)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
    
class FoodView(APIView):
    permission_classes = [IsAuthenticated ,]

     
    def post(self, request, format=None):
        serializer = FoodSerializer(data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Room is booked Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def get(self, request, pk=None, format=None):
        id=pk
        if id is not None:
            candidates = Food.objects.get(id=id)
            serializer = FoodSerializer(candidates)
            return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
        candidates=Food.objects.all()
        serializer=FoodSerializer(candidates, many=True)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        id=pk
        candidates = Food.objects.get(pk=id)
        # snippet = self.get_object(pk)
        serializer = FoodSerializer(candidates, data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        id=pk
        candidates = Food.objects.get(pk=id)
        # snippet = self.get_object(pk)
        serializer = FoodSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data)
            return Response({'msg' :'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        id=pk
        candidates = Food.objects.get(pk=id)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   
   
