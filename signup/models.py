from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    email = models.EmailField("メールアドレス")
    icon = models.ImageField("アイコン", upload_to="Media", blank=True, null=False)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="follow_user")
