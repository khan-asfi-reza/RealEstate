from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.agent is not None:
            return obj.agent == request.user
        elif obj.agent is None:
            return obj.owner.user == request.user


"""
Image ---> Property ---> Agent and Owner
Obj  ----> Property ----> Agent and Owner
"""


class IsAgentOrIsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.property.agent is not None:
            return obj.property.agent == request.user
        elif obj.property.owner is None:
            return obj.property.owner.user == request.user
