from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username:
            username = username.strip().lower()

        try:
            try:
                user = UserModel._default_manager.filter(username__iexact=username).get()
            except UserModel.DoesNotExist:
                user = UserModel._default_manager.filter(email__iexact=username).get()
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
