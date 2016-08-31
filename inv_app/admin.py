from django.contrib import admin
from inv_app.models import *


from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery


admin.site.register(Inv_User)

class GalleryExtendedInline(admin.StackedInline):
    model = GalleryExtended
    can_delete = False

class GalleryAdmin(GalleryAdminDefault):

    inlines = (GalleryExtendedInline,)

admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)
