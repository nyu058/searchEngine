from django.shortcuts import render
from django.http import HttpResponse
import os.path
from corpus_access import corpusAccess
from indexing import booleanIndexer, vsIndexer
from django.template import Context, loader

def index(request):
    template= loader.get_template('index.html')
    return HttpResponse(template.render())

def result(request):
    template = loader.get_template('result.html')
    reslist=[]
    sw, stem, normal = False, False, False
    if request.GET.get('stopwords', 'false') == 'true':
        sw = True
    if request.GET.get('stemming', 'false') == 'true':
        stem = True
    if request.GET.get('normalize', 'false') == 'true':
        normal = True
    query=request.GET['query']
    if request.GET['model']=='Boolean':
        reslist=boolean(query, sw, stem, normal)
    else:
        reslist=vsm(query, sw, stem, normal)
    return HttpResponse(template.render({'query':request.GET['query'], 'reslist':''.join(reslist)}))


def boolean(query, sw, stem, normal):
    reslist=[]
    index = booleanIndexer.BooleanIndexer()

    doclist = index.search(query, [sw, stem, normal])
    for elem in corpusAccess.getDocContent(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json",
            doclist):
        reslist.append("<div><h6><a href=\"#\">")
        reslist.append(elem[0])
        reslist.append("</a></h6><div><p>")
        reslist.append(elem[1])
        reslist.append('</p></div></div>')
    return reslist


def vsm(query, sw, stem, normal):
    reslist = []
    index=vsIndexer.VSIndexer()
    doclist = index.search(query, [sw, stem, normal])
    resultset=corpusAccess.getDocContent(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json",
        [i[0] for i in doclist])
    for i in range(len(resultset)):

        reslist.append("<div><h6 style=\"display:inline\"><a href=\"#\">")
        reslist.append(resultset[i][0])
        reslist.append("</a></h6><span style=\"float:right\"><b>Score: </b>")
        reslist.append(str(doclist[i][1]))
        reslist.append("</span><div><p>")
        reslist.append(resultset[i][1])
        reslist.append('</p></div></div>')
    return reslist