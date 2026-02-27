from rest_framework.permissions import BasePermission

class IsRegistration(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == "registration"


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == "admin"


class IsJudge(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == "judge"


class IsCertification(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == "certification"
