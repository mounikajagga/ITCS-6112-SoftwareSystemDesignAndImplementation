from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.hi, name='hi1'),
    url(r'^path', views.login, name='login'),
    url(r'^grades', views.grades, name='grades'),
]
