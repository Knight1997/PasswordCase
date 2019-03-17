#username: mayadmin
#password: adminpassword

from django.contrib import admin
from .models import Case, Profile, Passwords, Otp_database

# Register your models here.
admin.site.register(Case)
admin.site.register(Passwords)
admin.site.register(Profile)
admin.site.register(Otp_database)
