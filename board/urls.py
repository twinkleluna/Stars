from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path("login", views.ctf_login, name="login"),
    path("logout", views.ctf_logout, name="logout"),
    path("checkimg", views.ctf_checkimg, name="checkimg"),
    path("register", views.ctf_register, name="register"),
]