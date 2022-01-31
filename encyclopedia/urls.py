from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<page>", views.wiki, name="entry_wiki"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit/<page>", views.edit, name="edit"),
    path("random", views.random_entry, name="random"),
]
