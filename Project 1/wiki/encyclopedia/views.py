from django.shortcuts import render, redirect
from django.http import HttpResponse
from markdown import markdown
from django import forms
from . import util
from django.contrib import messages
from random import randint

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        content = "## Page does not exist"
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "content": content, 'title': title
        })

def search(request):
    query = request.GET['q']
    entries = util.list_entries()
    entrieslower = [entry.lower() for entry in entries]
    if query.lower() in entrieslower:
        return redirect("entry", title=query)
    else:
        return render(request, "encyclopedia/search.html", {
            "query": query, "entries": util.search(query)
        })

def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        description = request.POST.get("description").strip()
        entries = util.list_entries()
        entrieslower = [entry.lower() for entry in entries]
        if title.lower() in entrieslower:
            messages.error(request, 'This page already exists.')
            return render(request, "encyclopedia/newpage.html")
        util.save_entry(title=title, content=description)
    return render(request, "encyclopedia/newpage.html")

def editpage(request, title):
    description = util.get_entry(title.strip())
    if description == None:
        return render(request, "encyclopedia/editpage.html", {
            "error": "Page does not exist"})
    if request.method == "POST":
        description = request.POST.get("description").strip()
        util.save_entry(title=title, content=description)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/editpage.html", {
        "title": title,
        "description": description
    })

def randompage(request):
    entries = util.list_entries()
    randomtitle = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=randomtitle)