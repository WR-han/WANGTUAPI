from django.apps import AppConfig


class AppRbacConfig(AppConfig):
    name = 'APP_RBAC'

    def ready(self):
        print(123)
