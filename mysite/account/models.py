from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Profile(models.Model):
    id = models.AutoField(primary_key=True)

class Case(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    phone_regex = RegexValidator(regex=r'^\+?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16, blank=False)
    place = models.OneToOneField(Profile, on_delete=models.CASCADE)

class Passwords(models.Model):
    website = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    encrypted_password = models.CharField(max_length=100)
    belongs_to = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Otp_database(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    otp_id = models.CharField(max_length=10)
    otp_text = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
