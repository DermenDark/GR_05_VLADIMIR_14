from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r'^all_teg$', views.spec_lab, name='spec_lab'),
    re_path(r'^js_task$', views.spec_lab_js, name='spec_lab_js'),
]