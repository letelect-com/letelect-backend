from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from management.manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    '''custom user model'''
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, default='unknown user')
    is_active = models.BooleanField(default=True)
    is_voter = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_fullname(self):
        '''return the full name of the user'''
        return self.fullname if self.fullname else self.email

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.get_fullname()

    class Meta:
        db_table = 'user'
