from urllib import request
import bs4


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


def main():
    url = "https://catalogue.uottawa.ca/en/courses/"
    print(geturlList(url))

if __name__ == "__main__":
    main()
