from rest_framework import status
from rest_framework.exceptions import APIException


class AuthException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "auth fail"

    def __init__(self, error_code=None, detail=None, desire_status_code=status_code):
        self.detail = {
            'desire_status_code': desire_status_code,
            'error_code': error_code,
            'detail': detail
        }


class LoginException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "登录失败"