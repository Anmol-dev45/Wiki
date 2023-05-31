from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def converter(title):
    markdowner = Markdown()
    content = util.get_entry(title)
    if content is None:
        return None
    else:
        return markdowner.convert(content)
    

def content(request, title,):
    content = converter(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "content": "This entry doesn't exist!"
        })
    else:
        return render(request, "encyclopedia/content.html", {
            "title": title,
            "content":content
        })
    

def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        entries = util.list_entries()
        reccomandation =[]
        if converter(title) is None:
            for entry in entries:
                if title.lower() in entry.lower():
                    reccomandation.append(entry)
            return render(request, "encyclopedia/reccomandation.html" , {
                "reccomandation":reccomandation
            })
        else:
            return HttpResponseRedirect(reverse('content', kwargs={'title': title}))
        
       

def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new_entry_form.html", {
        
        })
    else:
        title = request.POST["title"]
        md_content = request.POST["md_content"]
        if converter(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "content": "This entry already exist!"
            })
        else:
            util.save_entry(title, md_content)
            return HttpResponseRedirect(reverse('content', kwargs={'title': title}))
        
def edit(request):
    if request.method == 'POST':
        title = request.POST["title"]
        md_content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "md_content":md_content,
            "title": title
        })
    

def save(request):
    if request.method == 'POST':
        title = request.POST["title"]
        md_content = request.POST["md_content"]
        util.save_entry(title, md_content)
        return HttpResponseRedirect(reverse('content', kwargs={'title': title}))
          
def ran(request):
    entries = util.list_entries()
    title = random.choice(entries)

    return HttpResponseRedirect(reverse('content', kwargs={'title': title}))

