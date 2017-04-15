from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^home', views.start, name='home'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name="logout"),

    # navbar
    url(r'^about_us', views.about_us, name="about_us"),
    url(r'^contact_us', views.contact_us, name="contact_us"),

    # student forms
    url(r'^assignments', views.assignments, name='assignments'),
]