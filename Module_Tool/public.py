from functools import wraps

from rest_framework import pagination
from rest_framework.response import Response

from Module_Public.custom_exception import PermissionFailed


class CustomPagination(pagination.LimitOffsetPagination):
    """
    自定义分页返回结构
    """

    def get_paginated_response(self, serializer):
        try:
            field_header = serializer.field_header
        except Exception as e:
            field_header = [f"{e}"]
        return Response({
            "code": 200,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.count,
            "data": serializer.data,
            "field_header": field_header
        })

#
# def action_permission(permission, inherit=True):
#     """
#     子路由二级权限装饰器
#     :param permission: 二级权限类
#     :param inherit: 一级权限通过后是否允许跳过二级权限检测 默认True
#     :return:
#     """
#
#     def wrapper(func):
#         @wraps(func)
#         def decorated(*args, **kwargs):
#             view, request = args
#             main_permission = getattr(request, "main_permission", "")
#             check = permission().has_permission(view=view, request=request)
#
#             if inherit and main_permission:
#                 # 允许继承以及权限 且 拥有一级权限
#                 return func(*args, **kwargs)
#             elif check:
#                 # 不能继承一级权限 或者 一级权限验证未通过 判断是否有当前的二级权限
#                 return func(*args, **kwargs)
#             else:
#                 raise PermissionFailed
#
#         return decorated
#
#     return wrapper
