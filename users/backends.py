from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


User = get_user_model()


# _______________________ Customized django authentication backend ________________
class EmailOrPhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phoneNumber=None, password=None, **kwargs):
        if '@' in str(phoneNumber):
            try:
                user = User.objects.get(email=phoneNumber)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(phoneNumber=phoneNumber)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# _______________________ Customized rest_framework_simplejwt authentication backend ________________
class EmailOrPhoneNumberJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            user = User.objects.get(id=user_id)
            return user
        except (ObjectDoesNotExist, KeyError):
            return None

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        if user is None:
            return None
        return (user, validated_token)

    def authenticate_credentials(self, request_data):
        try:
            username = request_data.get('phoneNumber')
            if not username:
                raise AuthenticationFailed('No username provided')
            password = request_data.get('password')
            if not password:
                raise AuthenticationFailed('No password provided')
            user = User.objects.filter(
                Q(email=username) | Q(phoneNumber=username)
            ).first()
            if user is None:
                raise AuthenticationFailed(
                    'No active account found with the given credentials')
            if not user.check_password(password):
                raise AuthenticationFailed('Invalid password')
            if not user.is_active:
                raise AuthenticationFailed('User is inactive')
            return user
        except AuthenticationFailed:
            raise
        except Exception:
            raise AuthenticationFailed(
                'No active account found with the given credentials')
