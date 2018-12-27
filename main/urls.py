from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('',views.ctf_main,name='main'),
    path("main_la", views.ctf_main, name="main_la"),
]