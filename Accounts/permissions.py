from rest_framework import permissions


class IsPostOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == 'POST':
            return True

        # Otherwise, only allow authenticated requests

        return request.user and request.user.is_authenticated


class IsAdminOrGetCreate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        elif request.method == 'GET':
            return True
        return request.user.account_type == 3


class RenterPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.account_type == 1 or request.user.account_type == 3


class AgentPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.account_type == 2 or request.user.account_type == 3
