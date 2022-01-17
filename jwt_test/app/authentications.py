from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings as jwt_settings
from app.exceptions import AuthException
from app.models import User

jwt_decode_handler = jwt_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = jwt_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class UserAuthentication(JSONWebTokenAuthentication):
    def authenticate(self, request):
        token = self.get_jwt_value(request)
        if token:
            try:
                payload = jwt_decode_handler(token)
                username = jwt_get_username_from_payload(payload)
                user = User.objects.get_by_natural_key(username)
                return user, token
            except Exception as e:
                raise exceptions.AuthenticationFailed("用户认证失败")
        else:
            raise AuthException(detail='未提供认证信息', desire_status_code=401)
