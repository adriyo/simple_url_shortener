from django.db import models
from django.contrib.auth.models import User


class UrlMapping(models.Model):
    short_url = models.CharField(max_length=10, unique=True)
    long_url = models.TextField(unique=True)
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    click_count = models.IntegerField()
