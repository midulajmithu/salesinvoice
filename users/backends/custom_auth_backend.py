from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user_model = get_user_model()  # This fetches the correct custom user model
            user = user_model.objects.get(username=username)  # Query user by username
            if user.check_password(password):  # Check the password
                return user
        except user_model.DoesNotExist:
            return None  # If user is not found, return None

    def get_user(self, user_id):
        try:
            user_model = get_user_model()  # This fetches the correct custom user model
            return user_model.objects.get(id=user_id)
        except user_model.DoesNotExist:
            return None
