from django.shortcuts import render
from django.http import HttpResponse
import os.path
from corpus_access import corpusAccess
from models import booleanmodel, vsmodel
from django.template import Context, loader
from nltk.corpus import words
from optional import spellCorrection
from dictionaryBuilding import dictionaryBuilding
reuterpath=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\reuters_parsed.json"
cspath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
print('building dictionary')
reuterdic = dictionaryBuilding.DictionaryBuilding(cspath, False, False, False).build()
csdic = dictionaryBuilding.DictionaryBuilding(cspath, False, False, False).build()
print('building dictionary complete')

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
    query=request.GET.get('query', '')
    if request.GET['model']=='Boolean':
        reslist=boolean(query, sw, stem, normal)
    else:
        reslist=vsm(query, sw, stem, normal)
    return HttpResponse(template.render({'query':request.GET['query'], 'reslist':''.join(reslist)}))

def detail(request):
    template=loader.get_template('detail.html')
    resultset=corpusAccess.getDocDetail( os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json", request.GET['docid'])
    return  HttpResponse(template.render({'title':resultset[0], 'description':resultset[1], 'comp':resultset[2], 'preq':resultset[3]}))

def boolean(query, sw, stem, normal, dic):
    reslist=[]
    index = booleanmodel.BooleanModel()

    doclist = index.search(query, [sw, stem, normal], dic)
    for elem in corpusAccess.getDocContent(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json",
            doclist):
        reslist.append("<div><h6><a href=\"/result/detail?docid="+elem[0]+"\">")
        reslist.append(elem[1])
        reslist.append("</a></h6><div><p>")
        reslist.append(elem[2])
        reslist.append('</p></div></div>')
    return reslist


def vsm(query, sw, stem, normal,dic):
    reslist = []
    index=vsmodel.VSModel()
    doclist = index.search(query, [sw, stem, normal], dic)
    path=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
    resultset=corpusAccess.getDocContent(path, [i[0] for i in doclist])
    if not resultset:
        tokenized = list(filter(None, query.lower().split(' ')))
        spellindex= index.buildIndex(dictionaryBuilding.DictionaryBuilding(path, sw, stem, normal).build())
        flag=False
        for i in range(len(tokenized)):
            if tokenized[i] not in words.words():
                flag=True
                tokenized[i]=spellCorrection.edits(tokenized[i], spellindex)[0]
        if flag:
            reslist.append('<di v>No result was returned, did you mean:<a href=\"/result/?collection=UO_Courses&model=VSM&query='+'+'.join(tokenized)+'\">')
            for i in range(len(tokenized)):
                reslist.append(" "+spellCorrection.edits(tokenized[i], spellindex)[0])
            reslist.append('</a></div>')
    else:
        for i in range(len(resultset)):

            reslist.append("<div><h6 style=\"display:inline\"><a href=\"/result/detail?docid="+resultset[i][0]+"\">")
            reslist.append(resultset[i][1])
            reslist.append("</a></h6><span style=\"float:right\"><b>Score: </b>")
            reslist.append(str(doclist[i][1]))
            reslist.append("</span><div><p>")
            reslist.append(resultset[i][2])
            reslist.append('</p></div></div>')
    return reslist