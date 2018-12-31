from django.urls import path
from . import views

app_name = "search_course"
urlpatterns = [
    path("index", views.search_static, name="search_static"),
    path("search_teacher", views.search_teacher, name="search_teacher"),
    path("search_classroom", views.search_classroom, name="search_classroom"),
    path("search_data", views.search_data, name="search_data"),
]