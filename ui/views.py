from django.shortcuts import render
from django.http import HttpResponse
import os.path
from corpus_access import corpusAccess
from indexing import booleanIndexer
from django.template import Context, loader

def index(request):
    template= loader.get_template('index.html')
    return HttpResponse(template.render())

def result(request):
    template = loader.get_template('result.html')
    reslist=[]
    index = booleanIndexer.BooleanIndexer()
    sw, stem, normal = False, False, False
    if request.GET.get('stopwords', 'false')=='true':
        sw=True
    if request.GET.get('stemming', 'false')=='true':
        stem=True
    if request.GET.get('normalize', 'false')=='true':
        normal=True
    doclist=index.search(request.GET['query'], [sw, stem, normal])
    for elem in corpusAccess.getDocContent(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json", doclist):
        reslist.append("<div><h6><a href=\"#\">")
        reslist.append(elem[0])
        reslist.append("</a></h6><div><p>")
        reslist.append(elem[1])
        reslist.append('</p></div></div>')

    return HttpResponse(template.render({'query':request.GET['query'], 'reslist':''.join(reslist)}))