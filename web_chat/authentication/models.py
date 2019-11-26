from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email =  models.EmailField(max_length=50)

    def __str__(self):
        return self.email
