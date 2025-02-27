from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken

from util.models import Timestamps

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise TypeError('Users should have a username')
        if not email:
            raise TypeError('Users should have an email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, username, email, password=None):
        if not password:
            raise TypeError("Password cannot be none")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

    #     return user

    def create_staff(self, username, email, password=None):
        if not password:
            raise TypeError("Password cannot be none")

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.save()

        return user


class User(Timestamps,AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True, db_index=True)
    email = models.EmailField(max_length=200, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user has specific permissions ??
        """
        return True

    def has_module_perm(self, app_label):
        """
        Does the user has permissions to view the app 'app_label'
        """

        return True

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }



class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='user_profile'
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class StaffProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='staff_profile'
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)
