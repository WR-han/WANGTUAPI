import inspect

from django.apps import AppConfig
from django.utils.module_loading import import_string

from Module_Auth import permissions


class AppRbacConfig(AppConfig):
    name = 'APP_RBAC'

    def ready(self):
        Permissions = import_string("AppRBAC.models.Permissions")
        clsmembers = inspect.getmembers(permissions, inspect.isclass)
        print(clsmembers)
        classes = [(c[0], c[1].__doc__.strip()) for c in clsmembers if
                   c[0] not in ('MainPermission', 'SecondaryPermission')]
        prefixes = [('GET', '获取'), ('PUT', '修改'), ('POST', '创建'), ('DELETE', '删除')]
        for prefix in prefixes:
            for Permission in classes:
                Permissions.objects.get_or_create(name=f"{prefix[1]}{Permission[1]}",
                                                  codeName=f"{prefix[0]}_{Permission[0]}")
