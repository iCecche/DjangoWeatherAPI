from rest_framework.permissions import BasePermission
from api.models import APICallRecord


class IsPremiumOrLimitedUser(BasePermission):
    def has_permission(self, request, view):
        record, _ = APICallRecord.objects.get_or_create(user_id = request.user.id)
        return record.can_request_forecast()

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
