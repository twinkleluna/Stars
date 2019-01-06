from django.urls import path
from . import views

app_name = "create_course"
urlpatterns = [
    path("", views.show, name="create_course"),
    path("add_course", views.add_course, name="add_course"),
    path("delete_course", views.delete_course, name="delete_course"),
    path("update_course", views.update_course, name="update_course"),
]