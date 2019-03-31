import re
import os.path
import json
import bs4
import sys

def parser(indir, outdir):
    print('parsing...')
    dirlist = os.listdir(indir)
    id = 0
    docs=[]
    progress = 0
    size = 100 / len(dirlist)
    jsonobj = {}

    for elem in dirlist:
        if elem.endswith('.sgm'):
            with open(indir + elem,'r', encoding='utf-8', errors='ignore') as f:
                content=f.read()
            filedoc, endid=parse(content, id)
            docs.extend(filedoc)
            id= endid
            progress += size
            sys.stdout.write("\r" + str(round(progress, 1)) + '%')
            sys.stdout.flush()

    jsonobj['documents']=docs
    file = open(outdir + 'reuters_parsed' + '.json', 'w')
    file.write(json.dumps(jsonobj), )
    file.close()

def parse(content, id):
    jsonarr=[]

    reuters='<REUTERS(.*?)</REUTERS>'
    titlere='<TITLE>(.*)</TITLE>'
    bodyre = '<BODY>(.*?)</BODY>'
    topicsre = '<TOPICS>(.*)</TOPICS>'
    topicsubre='<D>(.*?)</D>'
    endingre='( Reuter &#3;| REUTER &#3;| reuter &#3;| Reuters &#3;| reuters &#3;| REUTER &#3;|&#.{1,3};| &#3;)'
    ret=re.findall(reuters, content, re.DOTALL)
    for elem in ret:
        title=re.findall(titlere, elem)

        if title:
            jsonobj={}
            jsonobj['docID']=id
            jsonobj['title']= title[0].replace('&lt;','<').replace('&amp;','&')
            jsonobj['topics']=re.findall(topicsubre,re.findall(topicsre, elem)[0], re.DOTALL)
            desc=re.findall(bodyre, elem, re.DOTALL)[0].replace('\n', ' ').replace('&lt;','<').replace('&amp;','&')
            jsonobj['description']= re.sub(endingre,'',desc)
            id+=1
            jsonarr.append(jsonobj)

    return jsonarr, id

if __name__ == '__main__':
    indir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\reuters\\"
    outdir =os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\"
    parser(indir,outdir)

