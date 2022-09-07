from rest_framework.response import Response
from portal.models import HotelAdmin, Room, Food, RoomTypes
from portal.serializers import HotelAdminSerializer, RoomSerializer, FoodSerializer, UserPortalRegisterSerializer, RoomTypesSerializer
from rest_framework.views import APIView
from rest_framework import status, viewsets
# from django.contrib.auth.models import User
from django.http import Http404
from portal.permissions import IsOwner
# from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics

import django_filters
from django_filters import rest_framework as filters
from django_filters import FilterSet, RangeFilter
from django.contrib.auth import get_user_model
User = get_user_model()




# from rest_framework import generics
# from rest_framework.generics import(ListCreateAPIView , RetrieveUpdateDestroyAPIView)



class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPortalRegisterSerializer

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
        
        








class HotelAdminList(generics.ListAPIView):
    queryset = HotelAdmin.objects.all()
    serializer_class = HotelAdminSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ratings', 'city']




    
class HotelAdminView(APIView):
    
    serializer_class = HotelAdminSerializer
    permission_classes = [IsAuthenticated ,IsOwner]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'city']
    # queryset = HotelAdmin.objects.all
    # filter_backends = [SearchFilter]
    # search_fields = ['city']
    
    
    
    def post(self, request, format=None):
        serializer = HotelAdminSerializer(data=request.data, context = {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Hotel Profile created  Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)
    
    def get(self, request, pk=None, format=None):
        
        id = pk
        if id is not None:
            try:
                candidates = HotelAdmin.objects.get(pk=id)
                self.check_object_permissions(self.request, candidates)
                serializer = HotelAdminSerializer(candidates)
                return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
                # return candidates
            except HotelAdmin.DoesNotExist:
                raise Http404

        candidates = HotelAdmin.objects.filter(admin=request.user)
        serializer = HotelAdminSerializer(candidates, many=True)
        return Response({'status': 'success', 'candidate': serializer.data},
                        status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            obj = HotelAdmin.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except HotelAdmin.DoesNotExist:
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
        candidates = HotelAdmin.objects.get(pk=pk)
        # candidates = self.get_object(pk=pk)
        self.check_object_permissions(self.request, candidates)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
    
    
    
    
    
    
    
    

    # def get(self, request, pk=None, format=None):
    #     id=pk
    #     if id is not None:
    #         candidates = HotelAdmin.objects.get(id=id)
    #         serializer = HotelAdminSerializer(candidates)
    #         return Response({'status': 'success', 'candidate': serializer.data},
    #                             status=status.HTTP_200_OK)
    #     candidates=HotelAdmin.objects.all()
    #     serializer=HotelAdminSerializer(candidates, many=True)
    #     return Response(serializer.data)
        
    # def put(self, request, pk, format=None):
    #     id=pk
    #     candidates = HotelAdmin.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = HotelAdminSerializer(candidates, data=request.data, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def patch(self, request, pk, format=None):
    #     id=pk
    #     candidates = HotelAdmin.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = HotelAdminSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self, request, pk, format=None):
    #     id=pk
    #     candidates = HotelAdmin.objects.get(pk=id)
    #     candidates.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)




# class FoodPriceFilter(filters.FilterSet):
#     food_price = filters.RangeFilter()

#     class Meta:
#         model = Food
#         fields = ['food_price']
# # qs = Food.objects.all().order_by('food_price')
# # f = FoodPriceFilter( queryset=qs)





# class FoodList(generics.ListAPIView):
#     queryset = Food.objects.all()
#     serializer_class = FoodSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['food_name', 'food_type', 'food_price']
#     filterset_class = FoodPriceFilter


    
    
    
    
    
class RoomPriceFilter(filters.FilterSet):
    room_price = filters.RangeFilter()
    
    class Meta:
        model = Room
        fields = ['room_price']

class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room', 'room_type', 'room_price', 'is_available']    
    filterset_class = RoomPriceFilter

    
    
    

        
class RoomView(APIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated , IsOwner]

    def post(self, request, format=None):
        serializer = RoomSerializer(data=request.data, context = {'request' : request})
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
                candidates = Room.objects.get(pk=id)
                self.check_object_permissions(self.request, candidates)
                serializer = RoomSerializer(candidates)
                return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
                # return candidates
            except Room.DoesNotExist:
                raise Http404

        candidates = Room.objects.filter(admin=request.user)
        serializer = RoomSerializer(candidates, many=True)
        return Response({'status': 'success', 'candidate': serializer.data},
                        status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            obj = Room.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Room.DoesNotExist:
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
        candidates = Room.objects.get(pk=pk)
        # candidates = self.get_object(pk=pk)
        self.check_object_permissions(self.request, candidates)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#==============RoomTypes==================


# class RoomTypesPriceFilter(filters.FilterSet):
#     room_price = filters.RangeFilter()
    
#     class Meta:
#         model = RoomTypes
#         fields = ['room_price']

class RoomTypesList(generics.ListAPIView):
    queryset = RoomTypes.objects.all()
    serializer_class = RoomTypesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [ 'room_type']    

    
    
    

        
class RoomTypesView(APIView):
    serializer_class = RoomTypesSerializer
    permission_classes = [IsAuthenticated , IsOwner]

    def post(self, request, format=None):
        serializer = RoomTypesSerializer(data=request.data, context = {'request' : request})
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
                candidates = RoomTypes.objects.get(pk=id)
                self.check_object_permissions(self.request, candidates)
                serializer = RoomTypesSerializer(candidates)
                return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
                # return candidates
            except RoomTypes.DoesNotExist:
                raise Http404

        candidates = RoomTypes.objects.filter(admin=request.user)
        serializer = RoomTypesSerializer(candidates, many=True)
        return Response({'status': 'success', 'candidate': serializer.data},
                        status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            obj = RoomTypes.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except RoomTypes.DoesNotExist:
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
        candidates = RoomTypes.objects.get(pk=pk)
        # candidates = self.get_object(pk=pk)
        self.check_object_permissions(self.request, candidates)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







    # def get(self, request, pk=None, format=None):
    #     id=pk
    #     if id is not None:
    #         candidates = Room.objects.get(id=id)
    #         serializer = RoomSerializer(candidates)
    #         return Response({'status': 'success', 'candidate': serializer.data},
    #                             status=status.HTTP_200_OK)
    #     candidates=Room.objects.all()
    #     serializer=RoomSerializer(candidates, many=True)
    #     return Response(serializer.data)
        
    # def put(self, request, pk, format=None):
    #     id=pk
    #     candidates = Room.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = RoomSerializer(candidates, data=request.data, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def patch(self, request, pk, format=None):
    #     id=pk
    #     candidates = Room.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = RoomSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self, request, pk, format=None):
    #     id=pk
    #     candidates = Room.objects.get(pk=id)
    #     candidates.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
            







# class FoodPriceFilter(filters.FilterSet):
#     food_price = filters.RangeFilter()

#     class Meta:
#         model = Food
#         fields = ['food_price']
# qs = Food.objects.all().order_by('food_price')
# f = FoodPriceFilter( queryset=qs)





class FoodList(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['food_name', 'food_type', 'food_price']
    # filterset_class = FoodPriceFilter







class FoodView(APIView):
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated , IsOwner]

     
    def post(self, request, format=None):
        serializer = FoodSerializer(data=request.data, context = {'request' : request})
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
                candidates = Food.objects.get(pk=id)
                self.check_object_permissions(self.request, candidates)
                serializer = FoodSerializer(candidates)
                return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
                # return candidates
            except Food.DoesNotExist:
                raise Http404

        candidates = Food.objects.filter(admin=request.user)
        serializer = FoodSerializer(candidates, many=True)
        return Response({'status': 'success', 'candidate': serializer.data},
                        status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            obj = Food.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Food.DoesNotExist:
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
        candidates = Food.objects.get(pk=pk)
        # candidates = self.get_object(pk=pk)
        self.check_object_permissions(self.request, candidates)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)











    # def get(self, request, pk=None, format=None):
    #     id=pk
    #     if id is not None:
    #         candidates = Food.objects.get(id=id)
    #         serializer = FoodSerializer(candidates)
    #         return Response({'status': 'success', 'candidate': serializer.data},
    #                             status=status.HTTP_200_OK)
    #     candidates=Food.objects.all()
    #     serializer=FoodSerializer(candidates, many=True)
    #     return Response(serializer.data)
        
    # def put(self, request, pk, format=None):
    #     id=pk
    #     candidates = Food.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = FoodSerializer(candidates, data=request.data, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def patch(self, request, pk, format=None):
    #     id=pk
    #     candidates = Food.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = FoodSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self, request, pk, format=None):
    #     id=pk
    #     candidates = Food.objects.get(pk=id)
    #     candidates.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
   
   
        


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class HotelAdminView(ListCreateAPIView):
#     serializer_class = HotelAdminSerializer
#     permission_classes = [IsAuthenticated ,IsOwner]
#     lookup_fields = ('id')

    
#     def get_queryset(self):
#         queryset = HotelAdmin.objects.filter(admin=self.request.user)
#         return queryset
    
# class HotelAdminView(RetrieveUpdateDestroyAPIView):
#     serializer_class = HotelAdminSerializer
#     permission_classes = [IsAuthenticated ,IsOwner]
#     lookup_fields = ('id')

    
#     def get_queryset(self):
#         queryset = HotelAdmin.objects.filter(admin=self.request.user)
#         return queryset   
    
    