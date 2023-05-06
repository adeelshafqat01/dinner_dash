from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(blank=False)
    last_name = models.CharField(max_length=32,
                                 validators=[MinLengthValidator(2)])
