from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.wiki_page, name="wiki_page"),
    path("search/", views.search_results, name="search_results"),
]
