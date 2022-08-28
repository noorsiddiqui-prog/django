from rest_framework.response import Response
from django.http import Http404
from hotel.models import HotelAdmin, Bookings, Room, Customer, Payments
from hotel.serializers import BookingsSerializer, CustomerSerializer,  PaymentSerializer,  UserSerializer, UserRegisterSerializer
from rest_framework.views import APIView
from rest_framework import status, viewsets
# from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from hotel.permissions import IsOwner


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer
    # permission_classes = [IsAuthenticated ,]

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }
            return Response({'msg': ' Successfully',
                             'status': 'success', 'candidate': response_data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)


class LogOutAPIView(APIView):
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')

            # print(token)
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status=status.HTTP_200_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BookingsView(APIView):

    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, format=None):
        serializer = BookingsSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Room is booked Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            try:
                candidates = Bookings.objects.get(pk=id)
                self.check_object_permissions(self.request, candidates)
                serializer = BookingsSerializer(candidates)
                return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
                # return candidates
            except Bookings.DoesNotExist:
                raise Http404

        candidates = Bookings.objects.filter(customer=request.user)
        serializer = BookingsSerializer(candidates, many=True)
        return Response({'status': 'success', 'candidate': serializer.data},
                        status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            obj = Bookings.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Bookings.DoesNotExist:
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
        candidates = Bookings.objects.get(pk=pk)
        # candidates = self.get_object(pk=pk)
        self.check_object_permissions(self.request, candidates)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerView(APIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, format=None):
        serializer = CustomerSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Room is booked Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            try:
                candidates = Customer.objects.get(pk=id)
                self.check_object_permissions(self.request, candidates)
                serializer = CustomerSerializer(candidates)
                return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
                # return candidates
            except Bookings.DoesNotExist:
                raise Http404

        candidates = Customer.objects.filter(customer=request.user)
        serializer = CustomerSerializer(candidates, many=True)
        return Response({'status': 'success', 'candidate': serializer.data},
                        status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            obj = Customer.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Bookings.DoesNotExist:
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
        candidates = Customer.objects.get(pk=pk)
        # candidates = self.get_object(pk=pk)
        self.check_object_permissions(self.request, candidates)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentView(APIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, format=None):
        serializer = PaymentSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Room is booked Successfully',
                             'status': 'success', 'candidate': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            try:
                candidates = Payments.objects.get(pk=id)
                self.check_object_permissions(self.request, candidates)
                serializer = PaymentSerializer(candidates)
                return Response({'status': 'success', 'candidate': serializer.data},
                                status=status.HTTP_200_OK)
                # return candidates
            except Bookings.DoesNotExist:
                raise Http404

        candidates = Payments.objects.filter(customer=request.user)
        serializer = PaymentSerializer(candidates, many=True)
        return Response({'status': 'success', 'candidate': serializer.data},
                        status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            obj = Payments.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Bookings.DoesNotExist:
            raise Http404

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

    def delete(self, request, pk, format=None):
        candidates = Payments.objects.get(pk=pk)
        # candidates = self.get_object(pk=pk)
        self.check_object_permissions(self.request, candidates)
        candidates.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get(self, request, pk=None, format=None):

    #     if pk is not None:
    #         try:
    #             candidates = Bookings.objects.get(pk=pk)
    #             self.check_object_permissions(self.request, candidates)
    #             serializer = BookingsSerializer(candidates )
    #             return Response({'status': 'success', 'candidate': serializer.data},
    #                                 status=status.HTTP_200_OK)
    #             # return candidates
    #         except Bookings.DoesNotExist:
    #             raise Http404

    #     candidates=Bookings.objects.filter(customer = request.user)
    #     serializer=BookingsSerializer(candidates, many=True)
    #     return Response({'status': 'success', 'candidate':serializer.data},
    #                             status=status.HTTP_200_OK)

    # def put(self, request, pk, format=None):
    #     id=pk
    #     candidates = Bookings.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = BookingsSerializer(candidates, data=request.data, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, pk, format=None):
    #     id=pk
    #     candidates = Bookings.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = BookingsSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     id=pk
    #     candidates = Bookings.objects.get(pk=id)
    #     candidates.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# def get(self, request, pk=None, format=None):
    #     id=pk
    #     if id is not None:
    #         try:
    #             candidates = Customer.objects.get(id=pk)
    #             self.check_object_permissions(self.request, candidates)
    #             serializer = CustomerSerializer(candidates )
    #             return Response({'status': 'success', 'candidate': serializer.data},
    #                                 status=status.HTTP_200_OK)
    #             # return candidates
    #         except Customer.DoesNotExist:
    #             raise Http404

    #     candidates=Customer.objects.filter(customer = request.user)
    #     serializer=CustomerSerializer(candidates, many=True)
    #     return Response({'status': 'success', 'candidate':serializer.data},
    #                             status=status.HTTP_200_OK)


#    def patch(self, request, pk, format=None):

#         # candidates = Customer.objects.get(pk=pk)
#         candidates = Customer.objects.get(pk=pk)
#         self.check_object_permissions(self.request, candidates)
#         # snippet = self.get_object(pk)
#         serializer = CustomerSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
#         if serializer.is_valid():
#             serializer.save()
#             # return Response(serializer.data)
#             return Response({'msg' :'Complete Data Updated'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk, format=None):
    #     id=pk
    #     candidates = Payments.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = PaymentSerializer(candidates, data=request.data, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     id=pk
    #     candidates = Customer.objects.get(pk=id)
    #     candidates.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

        # def put(self, request, pk, format=None):
    #     id=pk
    #     candidates = Customer.objects.get(pk=id)
    #     self.check_object_permissions(self.request, candidates)

    #     # snippet = self.get_object(pk)
    #     serializer = CustomerSerializer(candidates, data=request.data, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     candidates=Customer.objects.filter(customer = request.user)
    #     serializer=CustomerSerializer(candidates, many=True)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, pk=None, format=None):

    #         candidates = Customer.objects.get(id=id)
    #         serializer = CustomerSerializer(candidates , many=True)
    #         serializer_data = serializer.data
    #         return Response({'status': 'success', 'candidate':serializer_data},
    #                             status=status.HTTP_200_OK)

    # def get_object(self,pk):
    #     try:
    #         obj = Customer.objects.get(id=id)
    #         self.check_object_permissions(self.request, obj)
    #         return obj
    #     except Bookings.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk=None, format=None):
    #     id=pk
    #     if id is not None:
    #         try:
    #             candidates = Payments.objects.get(id=pk)
    #             self.check_object_permissions(self.request, candidates)
    #             serializer = PaymentSerializer(candidates )
    #             return Response({'status': 'success', 'candidate': serializer.data},
    #                                 status=status.HTTP_200_OK)
    #             # return candidates
    #         except Customer.DoesNotExist:
    #             raise Http404

    #     candidates=Payments.objects.filter(customer = request.user)
    #     serializer=PaymentSerializer(candidates, many=True)
    #     return Response({'status': 'success', 'candidate':serializer.data},
    #                             status=status.HTTP_200_OK)

    # def get(self, request, pk, format=None):

    #     candidates = Payments.objects.get(id=id)
    #     serializer = PaymentSerializer(candidates , many=True)
    #     serializer_data = serializer.data
    #     return Response({'status': 'success', 'candidate':serializer_data},
    #                         status=status.HTTP_200_OK)

        # id= pk
        # serializer = self.serializer_class(self.get_object(pk=id))
        # serialized_data = serializer.data

        # candidates=Payments.objects.filter(customer = request.user)
        # serializer=PaymentSerializer(candidates, many=True)
        # return Response({'status': 'success', 'candidate':serializer.data},
        #                         status=status.HTTP_200_OK)

        # candidates = Payments.objects.get(id=id)
        # serializer = PaymentSerializer(candidates , many=True)
        # serializer_data = serializer.data
        # return Response({'status': 'success', 'candidate':serialized_data},
        #                     status=status.HTTP_200_OK)

    # if pk is not None:
    #         try:
    #             candidates = Bookings.objects.get(pk=pk)
    #             self.check_object_permissions(self.request, candidates)
    #             serializer = BookingsSerializer(candidates )
    #             return Response({'status': 'success', 'candidate': serializer.data},
    #                                 status=status.HTTP_200_OK)
    #             # return candidates
    #         except Bookings.DoesNotExist:
    #             raise Http404

    #     candidates=Bookings.objects.filter(customer = request.user)
    #     serializer=BookingsSerializer(candidates, many=True)
    #     return Response({'status': 'success', 'candidate':serializer.data},
    #                             status=status.HTTP_200_OK)

    # def patch(self, request, pk, format=None):
    #     id=pk
    #     candidates = Payments.objects.get(pk=id)
    #     # snippet = self.get_object(pk)
    #     serializer = PaymentSerializer(candidates, data=request.data, partial=True, context = {'request' : request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # return Response(serializer.data)
    #         return Response({'msg' :'Complete Data Updated'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     id=pk
    #     candidates = Payments.objects.get(pk=id)
    #     candidates.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
