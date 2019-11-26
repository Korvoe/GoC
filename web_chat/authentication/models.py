from django.db import models
from django.contrib.auth.models import AbstractUser
from fernet_fields import EncryptedCharField, EncryptedEmailField

class CustomUser(AbstractUser):
    pass
    first_name = EncryptedCharField(('first name'), max_length=30, blank=True)
    last_name = EncryptedCharField(('last name'), max_length=30, blank=True)
    email =  EncryptedEmailField()

    def __str__(self):
        return self.email
