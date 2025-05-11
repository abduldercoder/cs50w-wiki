# This file contains all the logic that responds to user actions.
# Each function below is a Django "view" that handles a specific URL request.

from django.shortcuts import render, redirect 
import markdown2
from django.http import HttpResponse
import random  # built-in Python module for randomness

from . import util


# HOME PAGE / INDEX
def index(request):
    """
    Show the homepage with a list of all encyclopedia entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# ENTRY PAGE /wiki/<title>
def entry(request, title):
    """
    Show a specific encyclopedia entry.
    If it doesn't exist, show an error page.
    """
    content = util.get_entry(title)

    if content is None:
        # If the entry was not found, show custom error page
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found."
        })

    else:
        # Convert Markdown content to HTML before displaying
        html = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })


# SEARCH PAGE
def search(request):
    """
    Handle search queries from the sidebar.
    If there's an exact match, redirect to that entry.
    If partial matches exist, show a list of suggestions.
    """
    query = request.GET.get("q", "")  # Get the search query from the URL
    entries = util.list_entries()

    # Exact match? → Redirect to that page
    if query.lower() in [entry.lower() for entry in entries]:
        return redirect("entry", title=query)

    # Partial match? → Show search results
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": matching_entries
    })


def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if util.get_entry(title):
            # If entry already exists, show error
            return render(request, "encyclopedia/error.html", {
                "message": "This entry already exists."
            })
        else:
            # Save the entry and redirect to it
            util.save_entry(title, content)
            return redirect("entry", title=title)

    # If request is GET, show empty form
    return render(request, "encyclopedia/new_page.html")


def edit(request, title):
    if request.method == "POST":
        # Get updated content from form
        content = request.POST.get("content")

        # Save the new content for the given title
        util.save_entry(title, content)

        # Redirect user back to the entry page
        return redirect("entry", title=title)

    # If GET request, get existing content to pre-fill the form
    content = util.get_entry(title)

    # If entry doesn't exist, show error page
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page doesn't exist and can't be edited."
        })

    # Render the edit form with existing content pre-filled
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })




def random_page(request):
    entries = util.list_entries()  # Get list of all entry titles
    chosen = random.choice(entries)  # Pick one randomly
    return redirect("entry", title=chosen)  # Redirect to that entry page


