from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'username',
            'email',
            'birthday',
            'genre',
            'phone_number',
        ]


class CreateUserSerializer(UserSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + [
            'password',
            'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        del validated_data['confirm_password']
        return super().create(validated_data)

    def validate(self, attrs):
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError('Passwords do not match')

        attrs['password'] = make_password(password)
        return attrs
