from django.http import Http404
from django.shortcuts import render
from markdown2 import Markdown

from . import util

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def wiki_page(request, name):
    # return HttpResponse(f"{name}")  # Testing
    entry_page = util.get_entry(name)
    if entry_page:
        return render(request, "encyclopedia/wiki_page.html",{
            "title": name,
            "page_text": markdowner.convert(entry_page)
        })
    raise Http404


def custom_404(request):
    return render(request, "encyclopedia/404.html")
