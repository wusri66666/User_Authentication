from rest_framework import serializers
from app.models import User
from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from app import models
import re
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class UserCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create(
            phone=validated_data.get('phone'),
            username=validated_data.get('username')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model = User
        fields = ["phone", "password", "username"]


class LoginSerializer(ModelSerializer):
    username = CharField(write_only=True)
    password = CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ('username', 'password')

    def validate(self, attrs):
        user = self._many_method_login(**attrs)

        # 通过user对象生成payload载荷
        payload = jwt_payload_handler(user)
        # 通过payload签发token
        token = jwt_encode_handler(payload)

        # 将user和token存放在序列化对象中,方便返回到前端去
        self.user = user
        self.token = token

        return attrs

    # 多方式登录 （用户名、邮箱、手机号三种方式登录）
    def _many_method_login(self, **attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        # 利用正则匹配判断用户输入的信息
        # 1.判断邮箱登录
        if re.match(r'.*@.*', username):
            user = models.User.objects.filter(email=username).first()  # type: models.User
        # 2.判断手机号登录
        elif re.match(r'^1[3-9][0-9]{9}$', username):
            user = models.User.objects.filter(phone=username).first()
        # 3.用户名登录
        else:
            user = models.User.objects.filter(username=username).first()

        if not user:
            raise ValidationError({'username': '账号有误'})

        if not user.check_password(password):
            raise ValidationError({'password': '密码错误'})

        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
