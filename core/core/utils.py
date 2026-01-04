from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission

#-----PAGINATION-----
class LargeResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100



#-----PERMISSIONS-----
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
    
