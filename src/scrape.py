
from bs4 import BeautifulSoup
import urllib.request
import requests
import re


def main():
    url = "https://www.news24.com"
    req = requests.get(url)
    soppie = BeautifulSoup(req.text, "html.parser")

    content = soppie.find_all("a", attrs={'data-track' : re.compile('mostread')})

    req_2 = requests.get(content[0]['href'])
    soppie_2 = BeautifulSoup(req_2.text, "html.parser")

    headings = soppie_2.find_all("h1")
    article = soppie_2.find("article", attrs={'id': re.compile('article-body')})
    article = article.find_all("p")

    title = headings[1].text

    print('Title:\n', title, '\n')
    print('Article:\n')
    for p in article:
        print(p.text)

    


if __name__ == "__main__":
    main()