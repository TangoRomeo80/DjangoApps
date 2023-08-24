from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

# Custom class for creating a user


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'username', 'password',
                  'first_name', 'last_name']
