from django.contrib import admin
from inv_app.models import *
from django import forms
from django.conf.urls import url
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib import messages


admin.site.register(Inv_User)


class GalleryAdminForm(forms.ModelForm):
    model = Gallery


class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'date_added', 'photo_count', 'collection','category'
    )
    list_filter = ['date_added',]
    date_hierarchy = 'date_added'
    form = GalleryAdminForm

    def add_photos(modeladmin, request, queryset):
        photos = Photo.objects.filter(gallery__in=queryset)
        current_gallery = Gallery.objects.get_current()
        current_gallery.photo_set.add(*photos)
        msg = ungettext(
            "The gallery has been successfully added to %(gallery)s",
            "The galleries have been successfully added to %(gallery)s",
            len(queryset)
        ) % {'gallery': current_gallery.name}
        messages.success(request, msg)
    add_photos.short_description = \
        _("Add all photos of selected galleries to the current gallery")

    def remove_photos(modeladmin, request, queryset):
        photos = Photo.objects.filter(gallery__in=queryset)
        current_gallery = Gallery.objects.get_current()
        current_gallery.photo_set.remove(*photos)
        msg = ungettext(
            "The gallery has been successfully removed from %(gallery)s",
            "The galleries have been successfully removed from %(gallery)s",
            len(queryset)
        ) % {'gallery': current_gallery.name}
        messages.success(request, msg)
    remove_photos.short_description = \
        _("Remove all photos of selected galleries to the current gallery")

    # def upload_zip(self,request):
    #     # Handle form request
    #     if request.method == 'POST':
    #         form = UploadZipForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save(request=request)
    #             return HttpResponseRedirect('..')
    #     else:
    #         form = UploadZipForm()
    #     context['form'] = form
    #     context['adminform'] = helpers.AdminForm(form,
    #                                              list([(None, {'fields': form.base_fields})]),
    #                                              {})
    #     return render(request, 'upload_zip.html')


admin.site.register(Gallery,GalleryAdmin)

class PhotoAdminForm(forms.ModelForm):
    model = Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added','view_count','admin_thumbnail')
    list_filter = ['date_added',]
    search_fields = ['title', 'caption']
    list_per_page = 10
    form = PhotoAdminForm


admin.site.register(Photo,PhotoAdmin)
