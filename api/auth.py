from rest_framework.permissions import BasePermission
from rest_framework.request import Request

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsModerator(BasePermission):
    def has_permission(self, request: Request, view):
        return request.user.is_moderator or request.user.is_admin


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, view):
        return request.user.is_admin


class IsReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request: Request, view):
        return request.method in SAFE_METHODS or request.user.is_admin


class IsReadOnlyOrModerator(BasePermission):
    def has_permission(self, request: Request, view):
        return request.method in SAFE_METHODS or request.user.is_moderator or request.user.is_admin
