from django.contrib import admin

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery
from inv_app.models import *

from django import forms


class GalleryAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = Gallery
        exclude = ['description']


class GalleryAdmin(GalleryAdminDefault):
    form = GalleryAdminForm

admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Inv_User)
