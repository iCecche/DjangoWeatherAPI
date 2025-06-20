from rest_framework.permissions import BasePermission

from CustomUser.models import CustomUser
from api.models import APICallRecord


class IsPremiumOrLimitedUser(BasePermission):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(id=request.user.id)
        print(user)
        record, _ = APICallRecord.objects.get_or_create(username = request.user.username)
        return record.can_request_forecast()
