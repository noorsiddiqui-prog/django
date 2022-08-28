from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user:
            return request.user == obj.user
            # return obj.owner == request.user
        return False
    
# class CustomerIsOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if obj.customer:
#             return request.user == obj.customer
#             # return obj.owner == request.user
#         return False  