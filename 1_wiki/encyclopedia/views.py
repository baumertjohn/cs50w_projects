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
        page_content = request.POST.get("content")
        if util.get_entry(page_title):  # Check for existing page
            return render(
                request,
                "encyclopedia/new_page.html",
                {
                    "error": True,
                    "page_title": f'"{page_title}" exists, change name.',
                    "page_content": page_content,
                },
            )
        else:
            formatted_content = f"# {page_title}\n\n{page_content}"
            util.save_entry(page_title, formatted_content)
            return redirect("wiki_page", name=page_title)
    return render(
        request,
        "encyclopedia/new_page.html",
        {"error": False, "page_title": "Page Title", "page_content": ""},
    )


def edit_page(request):
    if request.POST:
        page_title = request.POST.get("title")
        page_content = request.POST.get("content")
        formatted_content = f"# {page_title}\n\n{page_content}"
        util.save_entry(page_title, formatted_content)
        return redirect("wiki_page", name=page_title)
    page_title = request.GET.get("title")
    page_text = util.get_entry(page_title).splitlines()
    title = page_text[0][1:]
    content = "\n".join(page_text[2:])
    return render(
        request,
        "encyclopedia/edit_page.html",
        {"title": title, "content": content},
    )


def custom_404(request):
    return render(request, "encyclopedia/404.html")
