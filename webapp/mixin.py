class AuthMixin(object):
    @property
    def is_admin(self):
        if self.is_staff or self.is_superuser:
            return True
        else:
            return False

    @property
    def is_normal_user(self):
        return True if not self.is_admin else False