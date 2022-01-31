# Importing the necerrary packages

from django.shortcuts import render, redirect
from . import util
from django.urls import reverse
import re
import random
from markdown2 import Markdown


# Constructing the logic for the main page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Constructing the logic for each wiki entry web page
# Markdown is converted to HTML too
def wiki(request, page):
    entry = util.get_entry(page)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "page": page
        })
    else:
        wikiaddress = Markdown().convert(entry)
        return render(request, "encyclopedia/wiki.html", {
                "page": page,
                "wikiaddress": wikiaddress
            })


# Search engine for the wiki entries
# Substrings also provide relevant results
# If the key words/letters match, the engine provides direct
# access to the wiki page otherwise error message appears
def search(request):
    entries = util.list_entries()
    substring = []

    if request.method == "GET":
        entry = util.get_entry(request.GET["q"])
        if entry:
            return redirect("entry_wiki", request.GET["q"])
        else:
            for entry in entries:
                if re.search(request.GET["q"], entry, re.IGNORECASE):
                    substring.append(entry)
            if not substring:
                return render(request, "encyclopedia/error.html", {
                    "page": request.GET["q"]
                })
            else:
                return render(request, "encyclopedia/index.html", {
                    "entries": substring
                })


# Adding new wiki pages funcion. The function saves the new entries,
# but cannot save the pages that already exist
def new(request):
    if request.method == "POST":
        if util.get_entry(request.POST.get("new_page")):
            return render(request, "encyclopedia/error_new.html", {
                "new_page": request.POST.get("new_page")
            })
        else:
            util.save_entry(request.POST.get("new_page"),
                            request.POST.get("new_wiki"))
            return redirect("entry_wiki", request.POST.get("new_page"))
    return render(request, 'encyclopedia/new.html')


# The function enabling to edit the saved pages
def edit(request, page):
    if not request.method == "POST":
        update = {
            "page": page,
            "edited": util.get_entry(page)
        }
        return render(request, "encyclopedia/edit.html", update)
    else:
        util.save_entry(page, request.POST.get("edited"))
        return redirect("entry_wiki", page)


# Displaying the pages randomly
def random_entry(request):
    entries = util.list_entries()
    return redirect("entry_wiki", random.choice(entries))
