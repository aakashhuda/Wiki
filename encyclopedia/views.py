from django.shortcuts import render
from markdown2 import Markdown
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django import forms
import re
import random

from . import util

#Django form for new blog entry.
class NewEntryForm(forms.Form):
    title = forms.CharField(required=True, label="Enter title ",max_length=20,min_length=1,widget=forms.TextInput(attrs={"placeholder":"Title","class":"form-control w-50 font-italic"}))
    blog = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Type markdown content here...","class":"form-control w-75"}))

#Index page where all the entries are presented
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#Retrieve a particular file & converts markdown content to html
def get(request,title):
    m = Markdown()
    f= util.get_entry(title)
    if not f:
        return render(request, "encyclopedia/error.html",{
            "heading":"Error",
            "message":f"requested \"{title}\" page was not found"
        })
    content = m.convert(f)
    return render(request, "encyclopedia/blog.html", {
        "content":content,
        "title":title
    })
#Search for a particular file. This search function is case not sensitive.
def search(request):
    if request.method == 'POST':
        s_result = []
        q = request.POST["q"]
        q_lower = q.lower()
        entries = util.list_entries()
        pattern = re.compile(q_lower)
        for entry in entries:
            if q.lower()==entry.lower():
                return HttpResponseRedirect(reverse('encyclopedia:get',kwargs={"title":entry}))
            else:
                match = pattern.search(entry.lower())
                if match is None:
                    continue
                else:
                    s_result.append(entry)
                    match = ''
        return render(request, "encyclopedia/search.html", {
            "s_result":s_result,
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "heading":"Error",
            "message": "Invalid form submission."
        })
# Presents a new empty form for a new entry.
def new_page(request):
    return render(request, "encyclopedia/new_page.html",{
        "form": NewEntryForm()
    })
# Adds an entry if it doesn't exist.
def add_entry(request):
    if request.method =="POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            blog = form.cleaned_data["blog"]
            entries = util.list_entries()
            for entry in entries:
                if title.lower()==entry.lower():
                    return render(request, "encyclopedia/error.html", {
                        "heading": "ERROR",
                        "message": "This title already exists!"
                    })
                else:
                    continue
            util.save_entry(title,blog)
            return HttpResponseRedirect(reverse('encyclopedia:index'))
        else:
            return render(request, "encyclopedia/new_page.html",{
                "form": form,
            })
    else:
        return render(request, "encyclopedia/error.html", {
            "heading":"Error",
            "message": "Invalid form submission!"
        })
# Opens a random existing entry
def rand_func(request):
    entries = util.list_entries()
    rand_value = random.randint(0,len(entries)-1)
    title = entries[rand_value]
    return HttpResponseRedirect(reverse('encyclopedia:get', kwargs={"title":title}))
# Allows a user to edit an existing entry.
def edit(request,title):
    post = util.get_entry(title)
    if post:
        return render(request, "encyclopedia/edit_page.html", {
            "post":post,
            "title":title,
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "heading": "Error",
            "message": "Invalid post edit request!"
        })
# This function saves a post after editting
def save_post(request):
    if request.method == "POST":
        content = request.POST["edit_post"]
        title = request.POST["title"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('encyclopedia:get', kwargs={"title":title}))
    else:
        return render(request, "encyclopedia/error.html", {
            "heading":"Error",
            "message": "Invalid post saving request!"
        })