from django.urls import path
from . import views

app_name = "information"
urlpatterns = [
    path("information", views.information, name="information"),
    path("submitphoto", views.submitphoto, name="submitphoto"),
    path("logout", views.ctf_logout, name="logout"),
]