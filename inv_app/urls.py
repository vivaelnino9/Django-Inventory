from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from photologue.views import PhotoListView

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/(?P<inv_user_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^products/$', PhotoListView.as_view(template_name='products.html'), name='products'),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
]
