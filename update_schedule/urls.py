from django.urls import path
from . import views

app_name = "update_schedule"
urlpatterns = [
    path("add_course", views.add_course, name="add_course"),
    path("sub_course",views.sub_course,name="sub_course"),
    path("update_schedule",views.update_schedule,name="update_schedule")
]