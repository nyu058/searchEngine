from urllib import request
import bs4
import os.path
import sys
import json


def get_url_list(url):
    connection = request.urlopen(url)
    html = connection.read()
    connection.close()
    lst = bs4.BeautifulSoup(html, "html.parser").find('div', {"class": "az_sitemap"})
    lst.find("div", {"class": "azMenu"}).extract()
    result = []
    for elem in lst.find_all('a', href=True):
        result.append("https://catalogue.uottawa.ca" + elem['href'])
    return result


def download(lst, location):
    print('Downloading documents...')
    size = 100 / len(lst)
    progress = 0
    for elem in lst:
        connection = request.urlopen(elem)
        html = connection.read()
        soup = bs4.BeautifulSoup(html, "html.parser")
        title = soup.title.text.replace(' ', '').replace('<', '')
        soup = soup.find('div', {'class': 'sc_sccoursedescs'})
        file = open(location + title + ".html", "w")
        file.write(str(soup).encode('gbk', errors='ignore').decode('utf-8', errors='ignore'))
        file.close()
        progress += size
        sys.stdout.write("\r" + str(round(progress, 1)) + '%')
        sys.stdout.flush()
    print()
    print('Download complete')


def parser(htmldir, parsedir):
    print('parsing...')
    dirlist = os.listdir(htmldir)
    id = 0
    progress = 0
    size = 100 / len(dirlist)
    for elem in dirlist:
        if elem.endswith('.html'):
            soup = bs4.BeautifulSoup(open(htmldir + elem), 'html.parser')
            jsonobj = {}
            title = os.path.splitext(elem)[0]
            jsonobj['docID'] = id
            jsonobj['title'] = title
            jsonobj['description'] = rename(title)
            jsonobj['entries'] = parse(soup)
            id += 1
            file = open(parsedir + title + '.json', 'w')
            file.write(json.dumps(jsonobj))
            file.close()
            progress += size
            sys.stdout.write("\r" + str(round(progress, 1)) + '%')
            sys.stdout.flush()
    print()
    print('parsing complete')


def parse(soup):
    jsonarr = []
    courseblock = soup.find_all('div', {'class': 'courseblock'})

    for elem in courseblock:
        title = elem.find('p', {'class': 'courseblocktitle'}).strong.text
        desc = elem.find('p', {'class': 'courseblockdesc'})
        if desc is not None:
            desc = desc.text.replace("\n", '')
        comp = elem.find('p', {'class': 'courseblockextra'})
        if comp is not None:
            comp = comp.contents[-1]
        prereq = elem.find('p', {'class': 'courseblockextra highlight noindent'})
        if prereq is not None:
            prereq = prereq.text
        jsonobj = {'courseTitle': title, 'courseDescription': desc, 'courseComponent': comp, 'Prerequisite': prereq}
        jsonarr.append(jsonobj)
    return jsonarr


def rename(name):
    result = ''
    name = name[0].lower() + name[1:]
    for i in range(len(name) - 1):
        if name[i] == '(':
            break
        else:
            if name[i + 1].isupper():
                result += name[i] + ' '
            else:
                result += name[i].lower()
    return result + ' courses'


def main():
    url = "https://catalogue.uottawa.ca/en/courses/"
    htmldir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\UOcourses\\"
    parsedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\parsed\\"
    download(get_url_list(url), htmldir)
    parser(htmldir, parsedir)


if __name__ == "__main__":
    main()
