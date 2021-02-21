from rest_framework import serializers

from APP_RBAC.models import User


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
