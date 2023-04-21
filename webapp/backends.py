from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# noinspection PyMethodMayBeStatic
class EmailBackend(BaseBackend):
    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(email=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    def authenticate(self, request, email=None, password=None):
        if email is None or password is None:
            return
        try:
            # print(f"{email}-{password}")
            user = UserModel.objects.get_by_email(email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
