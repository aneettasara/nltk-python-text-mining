
from django.shortcuts import render
import random
import operator
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage
import nltk
import os
import operator
from nltk.corpus import stopwords
import re
from preprocess import *
from nltk.tokenize import word_tokenize
stop=set(stopwords.words('english'))
# Create your views here.
dire = "googleapp/files"
def home(requests):
    return render(requests,"index.html",{})

def login(request):
    print "ok"
    try:
        if request.POST.get("user")=="admin" and request.POST.get("password")=="admin":
                 return render(request,'admin.html',{})
    except Exception,e:
        print e
        return render(request, 'index.html', {})
def logout(request):
    return render(request,"index.html",{})
def upload(request):
     f=request.FILES["upl"]
     fs=FileSystemStorage("googleapp/files")
     fs.save(f.name,f)
     return render(request,"admin.html",{})
def search(request):
    data= request.POST.get("search")
    request.session["sess"]=data
    fil = os.listdir(dire)
    full = []
    print fil
    x=""
    preprocess(data)
    for i in fil:
        textcontent = open(dire + "/" + str(i), "rb")
        x=textcontent.read()
        dat =x.split(".")
        for i in dat:
            if len(i) < 3:
                dat.remove(i)
        fi = []
        for w in dat:
            if w not in stop:
                fi.append(w)
        ordata = str(fi)
        full.append(ordata)
        textcontent.close()
    cou = []
    di = {}

    for i, j in zip(full, fil):
        di[j] = i.count(data)
    print di
    sorted_x = sorted(di, key=di.get, reverse=True)
    print sorted_x
    name = []
    content = []
    for i in sorted_x:
        if di[i] != 0:
            name.append(i)
            f = open(dire + "/" + i, "r").read(500)
            f.replace("\n"," ")
            f.replace("\r"," ")
            f.replace("\t", " ")
            f.replace("\a", " ")
            stri = unicode(f, errors='replace')
            content.append(stri)
    print name
    if len(content)!=0:
        data=zip(name,content)
        text1=content[0].split(" ")
        fdist=nltk.FreqDist(text1)
        ls=fdist.most_common()
        print ls
        ori=[]
        for i,j in ls:
            if i.isalpha()==True:
                if len(i)>5:
                   ori.append(i.capitalize())
            if len(ori)>5:
                break
        return render(request,'index.html',{"data":data,"sugge":ori,"query":request.session["sess"],"st":1})
    else:
        return render(request,'index.html',{"status":"No result found"})
def viewdata(request):
    print request.GET.get("pk")
    f=open(dire + "/" + request.GET.get("pk"), "r").read()
    a=[m.start() for m in re.finditer(request.session["sess"], f)]
    print a
    x=f.replace(str(request.session["sess"]),"<mark><b>"+str(request.session["sess"])+"</b></mark>")
    print x
    return HttpResponse(x)
def suggestions(request):
    print request.GET.get("pk"),"suggestions"
    data=request.GET.get("pk")
    request.session["sess"]=data
    fil = os.listdir(dire)
    full = []
    print fil
    x=""
    preprocess(data)
    for i in fil:
        textcontent = open(dire + "/" + str(i), "rb")
        x=textcontent.read()
        dat =x.split(".")
        for i in dat:
            if len(i) < 3:
                dat.remove(i)
        fi = []
        for w in dat:
            if w not in stop:
                fi.append(w)
        ordata = str(fi)
        full.append(ordata)
        textcontent.close()
    cou = []
    di = {}

    for i, j in zip(full, fil):
        di[j] = i.count(data)
    print di
    sorted_x = sorted(di, key=di.get, reverse=True)
    print sorted_x
    name = []
    content = []
    for i in sorted_x:
        if di[i] != 0:
            name.append(i)
            f = open(dire + "/" + i, "r").read(500)
            f.replace("\n"," ")
            f.replace("\r"," ")
            f.replace("\t", " ")
            f.replace("\a", " ")
            stri = unicode(f, errors='replace')
            content.append(stri)
    print name
    if len(content)!=0:
        data=zip(name,content)
        text1=content[0].split(" ")
        fdist=nltk.FreqDist(text1)
        ls=fdist.most_common()
        print ls
        ori=[]
        for i,j in ls:
            if i.isalpha()==True:
                if len(i)>5:
                   ori.append(i.capitalize())
            if len(ori)>5:
                break
        return render(request,'index.html',{"data":data,"sugge":ori,"query":request.session["sess"],"st":1})
    else:
        return render(request,'index.html',{"status":"No result found"})
