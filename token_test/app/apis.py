from django.contrib.auth.hashers import check_password
from rest_framework import generics
from rest_framework_expiring_authtoken.models import ExpiringToken as Token
from rest_framework.response import Response
from rest_framework.views import APIView

from app.exceptions import LoginException
from app.models import User
from app.serializers import UserCreateSerializer, UserListSerializer


class UserCreateAPI(generics.CreateAPIView):
    authentication_classes = []
    serializer_class = UserCreateSerializer


class UserLoginAPI(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            data = UserListSerializer(user).data
            token, _ = Token.objects.get_or_create(user=user)
            if token.expired():
                token.delete()
                token = Token.objects.create(user=user)
            user.token = token.key
            if user and user.status:
                data['token'] = token.key
                return Response({"code": 0, "msg": "登录成功", "data": data})
            else:
                raise LoginException
        else:
            raise LoginException


class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
