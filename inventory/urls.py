from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from inv_app import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('inv_app.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
