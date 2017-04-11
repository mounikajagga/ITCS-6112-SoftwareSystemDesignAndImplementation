from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name="logout"),
    # forms
    url(r'^assignments', views.assignments, name='assignments'),
]