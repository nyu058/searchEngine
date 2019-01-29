from urllib import request
import bs4
import os.path

def geturlList(url):
    connection = request.urlopen(url)
    html = connection.read()
    connection.close()
    lst = bs4.BeautifulSoup(html, "html.parser").find('div', {"class": "az_sitemap"})
    lst.find("div", {"class": "azMenu"}).extract()
    result=[]
    for elem in lst.find_all('a', href=True):
        result.append("https://catalogue.uottawa.ca"+elem['href'])
    return result


def download(lst):
    for elem in lst:
        connection = request.urlopen(elem)
        html = connection.read()
        soup = bs4.BeautifulSoup(html, "html.parser")
        title= soup.title.text.replace(' ','').replace('<','')
        file = open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"\\UOcourses\\"+title+".html", "w")
        file.write(str(soup).encode('gbk', errors='ignore').decode('utf-8', errors='ignore'))
        file.close()


def main():
    url = "https://catalogue.uottawa.ca/en/courses/"
    download(geturlList(url))


if __name__ == "__main__":
    main()
