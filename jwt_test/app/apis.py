from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from app.models import User
from app.serializers import UserCreateSerializer, UserListSerializer, LoginSerializer


class UserCreateAPI(generics.CreateAPIView):
    authentication_classes = []
    serializer_class = UserCreateSerializer


class UserLoginAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # 将数据传到序列化组件进行校验
        user_ser = LoginSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)

        return Response({
            'username': user_ser.user.username,
            'token': user_ser.token
        })


class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
