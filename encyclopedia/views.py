from django.shortcuts import render
from markdown2 import Markdown
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
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
def search(request):
    if request.method == 'POST':
        s_result = []
        m = Markdown()
        q = request.POST["q"]
        entries = util.list_entries()
        pattern = re.compile(q)
        for entry in entries:
            if q.lower()==entry.lower():
                f = util.get_entry(entry)
                content = m.convert(f)
                return render(request, "encyclopedia/blog.html", {
                    "content":content,
                    "title":entry,
                })
            else:
                match = pattern.search(entry)
                if match is None:
                    continue
                else:
                    s_result.append(entry)
                    match = ''
        return render(request, "encyclopedia/search.html", {
            "s_result":s_result,
        })