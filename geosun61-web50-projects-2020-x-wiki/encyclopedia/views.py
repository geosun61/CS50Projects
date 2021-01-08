from django import  forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
from . import util
from markdown2 import Markdown
import random,os,re

entries = util.list_entries()
markdowner = Markdown()

#form for create new page
class CreateForm(forms.Form):
    title = forms.CharField(label="Enter Title...")
    textD = forms.CharField(widget=forms.Textarea,label="Add Description...")

def index(request):
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def wiki(request,title):

    md = util.get_entry(title)

    if md is None:
        return render(request, "encyclopedia/error.html",{
            "title": title, "error": "Entry does not exist"
        })

    html = markdowner.convert(md)

    return render(request,"encyclopedia/wikipage.html",{
        "contents": html, "title": title
    })

def random1(request):
    dir = "./entries"                           #pick from this directory entries
    filename = random.choices(os.listdir(dir))  #random choice from list of filenames
    splitFname = filename[0].split(".md")       #remove .md file extension to filename
    path= "/wiki/" + splitFname[0]               #save to path name for wiki url page

    return HttpResponseRedirect(path)           #redirct to random path

def create(request):
    entries = util.list_entries()
    print(entries)

    if request.method == "POST":
        form = CreateForm(request.POST)# create createform
        if form.is_valid():#if form is vaild collect form data on submit
            title = form.cleaned_data["title"] # get title form data
            textD = form.cleaned_data["textD"] # get Description form data

            print(f"{title}, {textD}")

            if title in entries: # if title already exists in entries then return error
                return render(request,"encyclopedia/error.html",{
                    "title": title, "error": "Entry already exists"
                })
            else:#else save entry and redirect to new wikipage
                util.save_entry(title,textD)
                path = f"/wiki/{title}"
                return HttpResponseRedirect(path)

        else:
            # create form
            return render(request,"encyclopedia/create.html",{
                "form": form
            })
    # create form
    return render(request,"encyclopedia/create.html",{
        "form": CreateForm()
    })

def edit(request,title):
    if request.method == "POST": #if request POST get post data from textarea form named textedit and save entry then redirect
        textE = request.POST["textedit"]
        util.save_entry(title,textE)
        path = f"/wiki/{title}"
        return HttpResponseRedirect(path)
    else:
        editText = util.get_entry(title)
        editSplit = editText.split("\r")#remove \r return character whitespace problem for textarea
        #print(editSplit)
        return render(request,"encyclopedia/edit.html",{
            "content": "".join(editSplit), "title": title
        })

def search(request):

    query= str(request.GET.get('q'))# get query string
    entries= [item for item in util.list_entries()] # get all entries
    results= [entry for entry in entries if query in entry] # get all results that match entries
    #strres= "".join(results[0])


    if query in results:
        return HttpResponseRedirect(f"/wiki/{query}")# redirect if one Entry

    elif query not in results:
        return render(request,"encyclopedia/search.html",{
            "query": query, "results": results
        })
    else:
        return render(request,"encyclopedia/search.html",{
            "query": "query does not exist"
        })
