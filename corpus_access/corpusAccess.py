import json

def getDocContent(path, doclist):
    with open(path,'r') as f:
        collection=json.load(f)
    result=[]

    for docid in doclist:
        for doc in collection['documents']:
            if doc['docID']==docid:
                result.append((docid+' '+doc['title'],doc['description']))
    return result
