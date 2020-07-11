from django.db import models
from django.conf import settings

from eat.models import Recipe

class Comment(models.Model):
    recipe_name = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    comment = models.CharField(max_length="300", blank=True, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
