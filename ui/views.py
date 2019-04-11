from django.shortcuts import render
from django.http import HttpResponse
import os.path
from corpus_access import corpusAccess
from models import booleanmodel, vsmodel
from django.template import Context, loader
from nltk.corpus import words
from optional import spellCorrection
from bigram import bigrammodel
import json
from dictionaryBuilding import dictionaryBuilding
cspath=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\ComputerScience(CSI)uOttawa.json"
reuterpath=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\reuters_parsed.json"
reuterdicpath=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\dictionaryBuilding\\reutersdic.json"
csdicpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\dictionaryBuilding\\csdic.json"

with open(reuterdicpath, 'r') as f:
    reuterdic=json.load(f)

with open(csdicpath, 'r') as f:
    csdic=json.load(f)


def index(request):
    template= loader.get_template('index.html')
    return HttpResponse(template.render())

def result(request):
    template = loader.get_template('result.html')
    reslist=[]
    query=request.GET.get('query', '')
    if request.GET['model']=='Boolean':
        reslist=boolean(query, request.GET['collection'])
    else:
        reslist=vsm(query, request.GET['collection'])
    return HttpResponse(template.render({'query':request.GET['query'], 'reslist':''.join(reslist)}))

def query_complete(request):
    reuters_bi_path=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\bigram\\reutersbigram.json"
    with open(reuters_bi_path,"r") as f:
        bigramsCollection = json.load(f)
    bigramModel = bigrammodel.bigrammodel(bigramsCollection)
    query=request.GET['word']
    reslist=bigramModel.getRecommandations(query.split(' ')[-2], 5)
    res=''
    for elem in reslist:
        res+='<p class=\'suggest\'>'+query+'<b>'+elem+'</b>'+'</p>'
    return HttpResponse(res)

def detail(request):
    template=loader.get_template('detail.html')
    resultset=[]
    if request.GET['collection']=='Reuters_2157':
        resultset=corpusAccess.getDocDetail(reuterpath, request.GET['docid'])
    else:
        resultset = corpusAccess.getDocDetail(cspath, request.GET['docid'])
    return  HttpResponse(template.render({'title':resultset[0], 'description':resultset[1]}))

def boolean(query, collection):
    reslist=[]
    index = booleanmodel.BooleanModel()
    path=''
    doclist =[]
    if collection=='UO_Courses':
        doclist=index.search(query, csdic)
        path=cspath
    else:
        doclist = index.search(query, reuterdic)
        path=reuterpath

    for elem in corpusAccess.getDocContent(path, doclist):
        reslist.append("<div><h6><a href=\"/result/detail?collection="+collection+"&docid="+elem[0]+"\">")
        reslist.append(elem[1])
        reslist.append("</a></h6><div><p>")
        reslist.append(elem[2])
        reslist.append('</p></div></div>')
    return reslist


def vsm(query, collection):
    reslist = []
    resultset=[]
    doclist=[]
    index=vsmodel.VSModel()
    if collection=='UO_Courses':
        doclist = index.search(query, csdic)
        path=cspath
        resultset=corpusAccess.getDocContent(path, [i[0] for i in doclist])
    else:
        doclist = index.search(query, reuterdic)
        path = reuterpath
        resultset = corpusAccess.getDocContent(path, [i[0] for i in doclist])

    if not resultset:
        tokenized = list(filter(None, query.lower().split(' ')))
        if collection=='UO_Courses':
            spellindex= index.buildIndex(csdic)
        else:
            spellindex = index.buildIndex(reuterdic)
        flag=False
        for i in range(len(tokenized)):
            if tokenized[i] not in words.words():
                flag=True
                tokenized[i]=spellCorrection.edits(tokenized[i], spellindex)[0]
        if flag:
            reslist.append('<div>No result was returned, did you mean:<a href=\"/result/?collection=UO_Courses&model=VSM&query='+'+'.join(tokenized)+'\">')
            for i in range(len(tokenized)):
                reslist.append(" "+spellCorrection.edits(tokenized[i], spellindex)[0])
            reslist.append('</a></div>')
    else:
        for i in range(len(resultset)):

            reslist.append("<div><h6 style=\"display:inline\"><a href=\"/result/detail?collection="+collection+"&docid="+resultset[i][0]+"\">")
            reslist.append(resultset[i][1])
            reslist.append("</a></h6><span style=\"float:right\"><b>Score: </b>")
            reslist.append(str(doclist[i][1]))
            reslist.append("</span><div><p>")
            reslist.append(resultset[i][2])
            reslist.append('</p></div></div>')

    return reslist