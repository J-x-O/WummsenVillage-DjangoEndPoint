from rest_framework.permissions import BasePermission
from rest_framework.request import Request

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request: Request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser
