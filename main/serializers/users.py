from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from ..models import User


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


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'current_password',
            'confirm_password',
            'new_password',
        ]

    def validate_current_password(self, value):
        user = self.context.get('user')

        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect')

        return value

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']
        user = self.context.get('user')

        if new_password != confirm_password:
            raise serializers.ValidationError('Passwords do not match')

        if user.check_password(new_password):
            raise serializers.ValidationError('New password cannot be equal to current')

        return attrs
