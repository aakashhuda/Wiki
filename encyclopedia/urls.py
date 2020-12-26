from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get, name = "get"),
    path("search", views.search, name = "search"),
    path("create_page", views.new_page, name = "new_page"),
    path("add_entry", views.add_entry, name = "add_entry"),
]
