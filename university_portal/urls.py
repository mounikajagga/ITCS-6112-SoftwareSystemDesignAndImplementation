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

    # common
    url(r'^profile', views.profile, name="profile"),
    url(r'^update_password$', views.password, name="update"),

    # student
    url(r'^assignments_stu', views.assignments_stu, name='assignments_stu'),

    # faculty
    url(r'^assignments', views.assignments, name='assignments'),
    url(r'^grades', views.grades, name='grades'),

    url(r'.*', views.error, name='error')

]
