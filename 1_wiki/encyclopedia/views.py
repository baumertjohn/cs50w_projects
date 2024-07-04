from django.http import Http404
from django.shortcuts import render, redirect
from markdown2 import Markdown

from . import util

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def wiki_page(request, name):
    entry_page = util.get_entry(name)
    if entry_page:
        return render(
            request,
            "encyclopedia/wiki_page.html",
            {"title": name, "page_text": markdowner.convert(entry_page)},
        )
    raise Http404


def search_results(request):
    query = request.GET.get("q")
    if not query:  # Default if 'blank' query.
        return redirect("index")
    entry_list = util.list_entries()
    if query in entry_list:  # Exact match, maybe make case insensitive?
        return redirect("wiki_page", name=query)
    query_list = [s for s in entry_list if query.lower() in s.lower()]
    return render(
        request,
        "encyclopedia/search_results.html",
        {"query": query, "entries": query_list},
    )


def new_page(request):
    if request.POST:
        page_title = request.POST.get("title")
        page_text = request.POST.get("text")
        print(page_title, page_text)
    return render(request, "encyclopedia/new_page.html")


def custom_404(request):
    return render(request, "encyclopedia/404.html")
