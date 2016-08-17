from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Inv_User(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=30, null=True, blank=False)
    last_name = models.CharField(max_length=30, null=True, blank=False)

    def __unicode__(self):
        return self.user.username
    def __str__(self):
        return self.user.username
