from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name = 'pr1'
urlpatterns = [

    url(r'^$', views.login, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^input/$', views.upload, name='input'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'model/$', views.model, name='model')
]
urlpatterns += staticfiles_urlpatterns()
