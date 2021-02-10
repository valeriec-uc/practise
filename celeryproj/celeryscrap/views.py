from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from celeryscrap.models import Author
from celeryscrap.models import Quotes
from celeryscrap.models import Tag
from celeryscrap.models import Link
import requests
from bs4 import BeautifulSoup
import re


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


# def index(request):
#     vgm_url = 'http://toscrape.com/'
#     html_text = requests.get(vgm_url).text
#     soup = BeautifulSoup(html_text, 'html.parser')
#     links = re.findall("href=[\"\'](.*?)[\"\']", html_text)
#     author_url = links[5];
#     html_text = requests.get(author_url).text
#     soup = BeautifulSoup(html_text, 'html.parser')
#     authornames = [e.text for e in soup.find_all("small", {"class": "author"})]
#     link = soup.small.string
#     linkauthor = re.findall("href=[\"\'](.*?)[\"\']", html_text)
#     authordis = "http://quotes.toscrape.com" + linkauthor[4];
#     html_text = requests.get(authordis).text
#     soup = BeautifulSoup(html_text, 'lxml')
#     dateofbirth = soup.find("span", class_="author-born-date").string
#     authdesc = soup.find("div", class_="author-description").string
#
#     # insert in Author table
#     for authorname in authornames:
#         author = Author(author_text=authorname, DateOfBirth=dateofbirth, author_desc=authdesc)
#         author.save()
#
#         #Quotes table
#         vgm_url = 'http://quotes.toscrape.com/'
#         html_text = requests.get(vgm_url).text
#         soup = BeautifulSoup(html_text, 'html.parser')
#         quotenames = [e.text for e in soup.find_all("span", {"class": "text"})]
#
#         # tag table
#         tagnames = [e.text for e in soup.find_all("a", {"class": "tag"})]
#         for tagname in tagnames:
#             try:
#                 tag = Tag.objects.get(tag_name=tagname)
#             except Tag.DoesNotExist:
#                 tag = Tag(tag_name=tagname)
#                 tag.save()
#
#         for quotename in quotenames:
#             quotes = Quotes(author_id=author.id, quotes_text=quotename,tag_id=tag.id)
#             quotes.save()
#             break;
