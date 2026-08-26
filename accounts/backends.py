from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class MemberIDBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # The login form passes the field as 'username', but we treat it as member_id
        member_id = username
        try:
            user = User.objects.get(member_id=member_id)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None
