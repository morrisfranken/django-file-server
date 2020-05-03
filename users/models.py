from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager

# Create your models here.
# extend models with __repr__ function
def repr_(self):
    variables = [attr for attr in dir(self) if
                 attr not in ["objects", "pk"] and not attr.startswith("_") and not callable(getattr(self, attr))]
    variables = [v for v in variables if not v.endswith("_id") or v[:-3] not in variables]
    lines = ["{:<16} = {}".format(v, str(getattr(self, v))) for v in variables]
    return "\n".join(lines)


models.Model.__repr__ = repr_


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, db_index=True, unique=True)
    username = models.CharField(max_length=50, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def json(self):
        return {"email": str(self.email),
                "created_at": str(self.created_at),
                "is_admin": self.is_admin,
                }
