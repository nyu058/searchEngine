import json


def getDocContent(path, doclist):
    with open(path,'r') as f:
        collection=json.load(f)
    result=[]
    if doclist:
        for docid in doclist:
            for doc in collection['documents']:
                if doc['docID']==docid:
                    result.append((docid, docid+' '+doc['title'],doc['description'].split('.')[0]))
    return result


def getDocDetail(path, docid):
    with open(path, 'r') as f:
        collection = json.load(f)
    for doc in collection['documents']:
        if doc['docID']==docid:
            return docid+' '+doc['title'], doc['description'], doc['courseComponent'], doc['Prerequisite']
