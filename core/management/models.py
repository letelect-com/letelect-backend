import uuid
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from management.manager import AccountManager
import time


class User(AbstractBaseUser, PermissionsMixin):
    '''custom user model'''

    def generate_voter_id():
        '''generate voter id for each user'''
        return str(time.time()).split(".")[1]

    def generate_default_email():
        '''generate default email for each user'''
        return str(time.time()).split(".")[1] + "@gmail.com"

    email = models.EmailField(
        max_length=255, default=generate_default_email, unique=True)
    voter_id = models.CharField(max_length=10, default=generate_voter_id, unique=True, blank=True)  # noqa
    fullname = models.CharField(max_length=255, default='unknown user')
    votes_cast = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_voter = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_fullname(self):
        '''return the full name of the user'''
        return self.fullname if self.fullname else self.voter_id

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.get_fullname()

    class Meta:
        db_table = 'user'


class Contact(models.Model):
    '''contact model - for contact us form'''
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'contact'


class Pricing(models.Model):
    '''pricing model - for pricing page'''
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    description = models.TextField()  # description of the plan - separated by |
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pricing'


class Election(models.Model):
    '''election model - for creating elections'''
    election_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa
    name = models.CharField(max_length=500)
    description = models.TextField()
    voters = models.ManyToManyField('User', related_name='voters', blank=True)  # noqa
    candidates = models.ManyToManyField('Candidate', related_name='candidates', blank=True)  # noqa
    type_of_election = models.CharField(max_length=55)
    admin = models.ForeignKey('User', on_delete=models.CASCADE, related_name='elections')  # noqa
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'election'


class Position(models.Model):
    '''position model - for creating positions'''
    sn = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    description = models.TextField()
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')  # noqa
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'position'


class Candidate(models.Model):
    '''Model to create and manage cnadidates'''
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)  # noqa
    house = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    picture = models.ImageField(upload_to='pictures', null=True, blank=True)
    ballot_number = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'candidate'


class Vote(models.Model):
    '''vote model - for creating votes'''
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='votes')  # noqa
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')  # noqa
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')  # noqa
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.voter.get_fullname()

    class Meta:
        db_table = 'vote'
