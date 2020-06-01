"""
This module provides a custom DRF Permission class for supporting the course certificates
to Admin users and users whom they belongs to.
"""

from rest_framework.permissions import BasePermission


class IsAdminOrSelfUser(BasePermission):
    """
    Method that will ensure whether the requesting user is staff or
    the user whom the certificate belongs to
    """
    def has_permission(self, request, view):
        requested_profile_username = view.kwargs.get('username')
        return request.user.is_staff or request.user.username == requested_profile_username
