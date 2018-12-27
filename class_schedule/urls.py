from django.urls import path
from . import views

app_name = "class_schedule"
urlpatterns = [
    path("show_schedule", views.class_schedule, name="show_schedule"),
    path("get_schedule",views.get_schedule,name="get_schedule"),
    path("get_scheduleOther",views.get_scheduleOther,name="get_scheduleOther")
]