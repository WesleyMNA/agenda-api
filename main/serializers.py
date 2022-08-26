from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'username',
            'password',
            'confirm_password',
            'email',
            'birthday',
            'genre',
            'phone_number',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
