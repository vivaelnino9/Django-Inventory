from django.conf.urls import include, url
from django.contrib import admin
from inv_app import views

urlpatterns = [
    url(r'^', include('inv_app.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
