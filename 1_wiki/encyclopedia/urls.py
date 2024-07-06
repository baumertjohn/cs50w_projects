from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.wiki_page, name="wiki_page"),
    path("search/", views.search_results, name="search_results"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("random_page", views.random_page, name="random_page"),
]
