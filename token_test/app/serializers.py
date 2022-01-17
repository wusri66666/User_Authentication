from rest_framework import serializers
from rest_framework.authtoken.models import Token

from app.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create(
            phone=validated_data.get('phone'),
            username=validated_data.get('username')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        token = Token.objects.create(user=user)
        user.token = token.key
        return user

    class Meta:
        model = User
        fields = ["phone", "password", "username"]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
