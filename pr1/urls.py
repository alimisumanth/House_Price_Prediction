from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name = 'pr1'
urlpatterns = [

    url(r'^$', views.login, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
]
urlpatterns += staticfiles_urlpatterns()
