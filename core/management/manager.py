from django.contrib.auth.models import BaseUserManager
import time


class AccountManager(BaseUserManager):
    '''manages User account creation'''
    def generate_default_email():
        '''generate default email for each user'''
        return str(time.time()).split(".")[1] + "@gmail.com"

    def create_user(self, email, password, fullname='unknown user', **kwargs):
        '''Create a new user - client or applicant'''
        user = self.model(email=email, password=password,
                          fullname=fullname, **kwargs)
        user.set_password(password)
        user.is_staff = True
        user.is_voter = False
        user.is_superuser = False
        user.save()
        return user

    def create_voter(self, email, password, fullname='unknown user', **kwargs):
        '''Create a new user - voter'''
        user = self.model(email=email, password=password,
                          fullname=fullname, **kwargs)
        user.set_password(password)
        user.is_voter = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email, password, fullname='unknown user', **kwargs):
        user = self.create_user(
            email,  password, fullname='unknown user', **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
