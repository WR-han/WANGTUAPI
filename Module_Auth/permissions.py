from rest_framework.permissions import BasePermission


class BasisPermission(BasePermission):

    def has_permission(self, request, view):
        user_permissions = request.user.get_permissions
        if "AdminPermission" in user_permissions:
            return True
        
        method = request.method
        if request.method == "PATCH":
            method = "PUT"
        need_permission = f"{method}_{type(self).__name__}"

        if need_permission in user_permissions:
            return True
        else:
            return False


class UserPermission(BasisPermission):
    """
    学生信息权限
    """
    pass
