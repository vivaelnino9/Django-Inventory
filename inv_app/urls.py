from django.conf.urls import include, url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/(?P<inv_user_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^products/$', views.products, name='products'),
]
