from django.http import HttpResponse

from celeryproj.celery import Celery
import os
import re
import requests
from celeryscrap.models import Author
from celeryscrap.models import Quotes
from celeryscrap.models import Tag
from celeryscrap.models import Link
from bs4 import BeautifulSoup

app = Celery('tasks', broker='amqp://guest:guest@localhost:5672/')

os.environ['DJANGO_SETTINGS_MODULE'] = "celeryproj.settings"


@app.task
def index(request):
    vgm_url = 'http://toscrape.com/'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    links = re.findall("href=[\"\'](.*?)[\"\']", html_text)
    author_url = links[5];
    html_text = requests.get(author_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    linkauthor = re.findall("href=[\"\'](.*?)[\"\']", html_text)
    authordis = "http://quotes.toscrape.com" + linkauthor[4];
    html_text = requests.get(authordis).text
    soup = BeautifulSoup(html_text, 'html.parser')
    dateofbirth = soup.find("span", class_="author-born-date").string
    authdesc = soup.find("div", class_="author-description").string
    return HttpResponse("COMPLETED")


def insertdb(request):
    index(request)
    response = requests.get('http://quotes.toscrape.com/')
    content = response.text
    mysoup = BeautifulSoup(content)
    for counttag in mysoup.find_all("div", class_="quote"):
        quotename = counttag.find("span", class_="text").string
        print(quotename)
        authorname = counttag.find("small", class_="author").string
        print(authorname)
        authorurl = counttag.find("a")

        # Insert data in author table
        author,created = Author.objects.get_or_create(author_text=authorname, DateOfBirth=dateofbirth, author_desc=authdesc)

        # insert data in quotes table
        quotes = Quotes(author_id=author.id, quotes_text=quotename)
        quotes.save()

        # Insert data in tag table
        tagnames =counttag.find_all("a", class_="tag")
        for tagname in tagnames:
            tag,created = Tag.objects.get_or_create(tag_name=tagname.string)

            # insert data in link table
            link = Link(quotes_id=quotes.id, tag_id=tag.id)
            link.save()

    return HttpResponse("completed")

