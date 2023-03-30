from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# from .managers import CustomUserManager 
import re
from django.utils import timezone
# from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
# import validators
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
from rest_framework import permissions
# from django.contrib.postgres.fields import ArrayField

class AccountManager(BaseUserManager):

    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        print("H")
        return user

    def create_superuser(self, email, password,**extra_fields):
        user = self.create_user(
            password=password,
            email=self.normalize_email(email)
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
class UserAccount(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email",validators = [EmailValidator()], max_length=60, unique=True,null=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    pass1 = models.CharField(('password'), max_length=128)
    pass2 = models.CharField(('password'), max_length=128)
    usermoney=models.IntegerField(default=1000000)
    # meta = ArrayField(base_field=models.CharField(max_length=200, null=True), default=list, blank=True)
    # cart=[]
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        if "." in perm: perm=perm.split(".")[1]
        if self.is_admin:
            return True
        if self.is_staff and perm in self.get_all_permissions():
            return True
        return False
    
    # # return all the user permission
    def get_all_permissions(self, obj=None):
        
        all_perm=[]
        if self.group is None:
            return all_perm
        for perm in self.group.permissions.all():
            all_perm.append(perm.codename)
        return all_perm
        

    def has_module_perms(self, app_label):
        return True
    
class Stocks(AbstractBaseUser):
    stock_name=models.CharField(max_length=100)
    stock_originalprice=models.IntegerField()
    stock_user=models.CharField(max_length=100)
    