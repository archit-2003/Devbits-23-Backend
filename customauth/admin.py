from django.contrib import admin

# Register your models here.
from customauth.models import UserAccount,Stock
admin.site.register(UserAccount)
admin.site.register(Stock)
