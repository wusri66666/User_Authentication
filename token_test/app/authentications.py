from rest_framework.authentication import BaseAuthentication
from rest_framework_expiring_authtoken.models import ExpiringToken as Token

from app.exceptions import AuthException


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            obj = Token.objects.filter(key=token).first()
            if not obj:
                raise AuthException(detail="用户认证失败", desire_status_code=401)
            if not obj.user.is_active or not obj.user.status:
                raise AuthException(detail='用户账号被禁用或被删除', desire_status_code=401)
            if obj.expired():
                raise AuthException(detail='token已过期', desire_status_code=401)
            return (obj.user, obj)
        else:
            raise AuthException(detail='未提供认证信息', desire_status_code=401)
