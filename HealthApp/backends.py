# backends.py
from django.contrib.auth.backends import BaseBackend
from .models import RegisterDB

class RegisterDBBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = RegisterDB.objects.get(Username=username)
            if user.Password1 == password:  # Consider hashing passwords
                return user
        except RegisterDB.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return RegisterDB.objects.get(pk=user_id)
        except RegisterDB.DoesNotExist:
            return None
