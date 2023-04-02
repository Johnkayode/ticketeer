from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from base.models import BaseModel
import uuid

from .manager import CustomUserManager

class User(AbstractUser, BaseModel):
    username = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    is_verified = models.BooleanField(_("verified"), default=False)
    code = models.CharField(default="", max_length=150)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def confirm_code(self, code: int) -> bool:
        return check_password(code, self.code)
