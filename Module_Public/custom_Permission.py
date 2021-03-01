from functools import wraps

from django.forms.utils import pretty_name
from rest_framework.decorators import MethodMapper
from rest_framework.permissions import BasePermission

from Module_Public.custom_exception import PermissionFailed


class SecondaryPermission(BasePermission):

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


class MainPermission(SecondaryPermission):

    def has_permission(self, request, view):
        base_action = ["list", "retrieve", "create", "update", "partial_update", "destroy"]
        is_check = super(MainPermission, self).has_permission(request, view)
        action = view.action

        if action not in base_action:
            # 动作类型不是基础action / 子路由
            if is_check:
                # 拥有主路由权限
                request.main_permission = True

            return True
        else:
            return is_check


def action(methods=None, detail=None, url_path=None, url_name=None, permission=None, inherit=True, **wra_kwargs):
    methods = ['get'] if (methods is None) else methods
    methods = [method.lower() for method in methods]
    assert detail is not None, (
        "@action() missing required argument: 'detail'"
    )
    if 'name' in wra_kwargs and 'suffix' in wra_kwargs:
        raise TypeError("`name` and `suffix` are mutually exclusive arguments.")

    def wrapper(func):
        func.mapping = MethodMapper(func, methods)
        func.detail = detail
        func.url_path = url_path if url_path else func.__name__
        func.url_name = url_name if url_name else func.__name__.replace('_', '-')
        func.kwargs = wra_kwargs
        if 'name' not in wra_kwargs and 'suffix' not in wra_kwargs:
            func.kwargs['name'] = pretty_name(func.__name__)
        func.kwargs['description'] = func.__doc__ or None

        @wraps(func)
        def decorated(*args, **kwargs):
            view, request = args
            main_permission = getattr(request, "main_permission", None)
            print(main_permission)
            if permission:
                check = permission().has_permission(view=view, request=request)

                if inherit and main_permission:
                    return func(*args, **kwargs)
                elif check:
                    return func(*args, **kwargs)
                else:
                    raise PermissionFailed
            elif (main_permission is True) or (main_permission is None):
                return func(*args, **kwargs)
            else:
                raise PermissionFailed

        return decorated

    return wrapper
