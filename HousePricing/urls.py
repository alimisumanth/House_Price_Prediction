from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name = 'HousePricing'
urlpatterns = [

    url('login/', views.loginpage, name='login'),
    url(r'^$', views.home, name='home'),
    url(r'^input/$', views.upload, name='input'),
    url(r'^logout/$', views.logoutpage, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'model/$', views.model, name='model'),
    url(r'stats/$', views.eda, name='stats'),
    url(r'charts/$', views.charts, name='charts'),
    url(r'download/$', views.download, name='download'),
    url(r'features/$',views.download_featureinfo,name='features')
]
urlpatterns += staticfiles_urlpatterns()
