from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


# -----PAGINATION-----
class LargeResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# -----PERMISSIONS-----
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


# -----throttle-----
class CustomUserRateThrottle(UserRateThrottle):
    rate = "30/min"


class CustomAnonRateThrottle(AnonRateThrottle):
    rate = "20/min"
