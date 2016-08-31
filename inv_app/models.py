from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from photologue.models import Gallery

class Inv_User(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=30, null=True, blank=False)
    last_name = models.CharField(max_length=30, null=True, blank=False)

    def __unicode__(self):
        return self.user.username
    def __str__(self):
        return self.user.username

CATEGORIES = (
        ('rings','rings'),
        ('necklaces','necklaces'),
        ('bracelets','bracelets')
)

class GalleryExtended(models.Model):
    # Link back to Photologue's Gallery model.
    gallery = models.OneToOneField(Gallery, related_name='extended')
    collection = models.CharField(
        unique=True,
        max_length=250,
        verbose_name='collection'
    )
    category = models.CharField(
        unique=True,
        max_length=250,
        choices=CATEGORIES,
        verbose_name='category'
    )


    # Boilerplate code to make a prettier display in the admin interface.
    class Meta:
        verbose_name = 'Extra fields'
        verbose_name_plural = 'Extra fields'

    def __str__(self):
        return self.gallery.title
