from django.conf.urls import url
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^home$', views.start, name='home'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name="logout"),

    # navbar
    url(r'^about_us$', views.about_us, name="about_us"),
    url(r'^contact_us$', views.contact_us, name="contact_us"),

    # common
    url(r'^profile$', views.profile, name="profile"),
    url(r'^update$', views.update, name="update"),
    url(r'^update_password$', views.update_password, name='update_password'),

    # student
    url(r'^assignments_stu', views.assignments_stu, name='assignments_stu'),
    url(r'^assignment_submit$', views.assignment_submit, name='assignment_submit'),

    # faculty
    url(r'^assignments', views.assignments, name='assignments'),
    url(r'^grades', views.grades, name='grades'),
    url(r'^student_grade', views.student_grade, name='student_grade'),

    # miscellaneous
    url(r'^favicon.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'), permanent=False), name="favicon"),
    url(r'.*', views.error, name='error'),
]
