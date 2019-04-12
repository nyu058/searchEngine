import json


def getDocContent(path, doclist, topic='all'):
    print(topic)
    with open(path,'r') as f:
        collection=json.load(f)
    result=[]
    if doclist:
        if topic=='all':
            for docid in doclist:
                for doc in collection['documents']:
                    if doc['docID']==docid:
                        result.append((docid, docid+' '+doc['title'],doc['description'].split('.')[0]))
        else:
            for docid in doclist:
                for doc in collection['documents']:
                    if (doc['docID']==docid) and (topic in doc['topics']):
                        print(topic)
                        result.append((docid, docid+' '+doc['title'],doc['description'].split('.')[0]))
    return result


def getDocDetail(path, docid):
    with open(path, 'r') as f:
        collection = json.load(f)
    for doc in collection['documents']:
        if doc['docID']==docid:
            return docid+' '+doc['title'], doc['description']
