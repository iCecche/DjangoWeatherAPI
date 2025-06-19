from rest_framework.permissions import BasePermission

class IsPremiumOrLimitedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.can_request_forecast()
