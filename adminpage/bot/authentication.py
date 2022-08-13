import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header

from accounts.models import User as _User_type

User: _User_type = get_user_model()


class TelegramAuthentication(authentication.BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Telegram 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = "Bearer"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        return self.authenticate_credentials(token)

    @staticmethod
    def authenticate_credentials(token):
        try:
            decoded = jwt.decode(token, settings.TELEGRAM_BOT_TOKEN, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')

        try:
            user = User.objects.get(telegram_id=decoded['tg_user']['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return user, token

    def authenticate_header(self, request):
        return self.keyword
