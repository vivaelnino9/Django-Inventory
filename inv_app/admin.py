from django.contrib import admin
from inv_app.models import *
from photologue.forms import UploadZipForm
from photologue.admin import PhotoAdmin as PhotoAdminDefault
from photologue.models import *
from django.contrib.admin import helpers
from django.shortcuts import render
from django import forms

admin.site.register(Inv_User)
admin.site.unregister(Watermark)
admin.site.unregister(PhotoEffect)
admin.site.unregister(Gallery)



class PhotoAdmin(PhotoAdminDefault):
    def upload_zip(self,request):
        context = {
            'title': ('Upload a zip archive of photos'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        # Handle form request
        if request.method == 'POST':
            form = UploadPhotoZipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('..')
            else:
                form = UploadPhotoZipForm()
            context['form'] = form
            context['adminform'] = helpers.AdminForm(form,
                                                     list([(None, {'fields': form.base_fields})]),
                                                     {})
            return render(request,'upload_zip.html',context)






admin.site.unregister(Photo)
admin.site.register(Photo, PhotoAdmin)
