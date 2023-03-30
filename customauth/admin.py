from django.contrib import admin

# Register your models here.
from customauth.models import UserAccount
admin.site.register(UserAccount)