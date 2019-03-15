import re
import os.path
import json

def parser(indir, outdir):
    print('parsing...')
    dirlist = os.listdir(indir)
    id = 0
    docs=[]
    progress = 0
    size = 100 / len(dirlist)
    for elem in dirlist:
        if elem.endswith('.sgm'):
            with open(indir + elem,'r') as f:
                content=f.read()
            jsonobj = {}
            jsonobj['documents'] = parse(content)
            id += 1
            if id==1:
                break
            # file = open(outdir + 'reuters_parsed' + '.json', 'w')
            # file.write(json.dumps(jsonobj))

            # progress += size
            # sys.stdout.write("\r" + str(round(progress, 1)) + '%')
            # sys.stdout.flush()

def parse(content):
    jsonarr=[]
    docid=0
    titlere='<TITLE>(.*)</TITLE>'
    title=re.findall(titlere, content)
    bodyre = '<BODY>(.*?)</BODY>'
    body = re.findall(bodyre, content, re.DOTALL)
    topicsre = '<TOPICS>(.*)</TOPICS>'
    topics = re.findall(topicsre, content)
    jsonobj={}
    #for i in range(len(title)):

    print(title)
    print(len(title))
    print(topics)
    print(len(topics))
    print(body)
    print(len(body))

if __name__ == '__main__':
    indir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\reuters\\"
    outdir =os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\"
    parser(indir,outdir)

