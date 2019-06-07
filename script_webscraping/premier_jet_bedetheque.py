import requests
import csv
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import urllib.request
from my_url_bedetheque import my_html
from my_url_bedetheque import my_url
from html_serie_a import html_serie_a
from url_list import my_url_list
from my_list_of_list import mylofl
import time as t
from random import randint


def getAlbumMain(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        soup = BeautifulSoup(html.read(), 'html.parser')
    except AttributeError as e:
        print(e)
        return None
    return soup

def getAlbumTitle(soup):
    try:
        for a in soup.findAll("a", {"class": "titre"}):
            print(a['title'])
    except:
        print('Pas de <a>')

def getIllustrator(soup):
    try:
        for illustrator in soup.findAll("span", itemprop="illustrator"):
            print(illustrator.text)
    except:
        print('Pas de dessinateur')

def getAuthor(soup):
    try:
        for author in soup.findAll("span", itemprop="author"):
            print(author.text)
    except:
        print('Pas de scénariste')

def getLinkSerie(url):
    session = requests.Session()
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,application/xml;'
    'q=0.9,image/webp,*/*;q=0.8'}
    req = session.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    list_url_serie_a = []
    try:
        for link in soup.find("ul", {"class": "nav-liste"}).findAll("li"):
            # print(link.find("a")['href'])
            list_url_serie_a.append(link.find("a")['href'])
    except:
        print('Pas de link serie a')
    return list_url_serie_a

def getSoup(url):
    session = requests.Session()
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,application/xml;'
    'q=0.9,image/webp,*/*;q=0.8'}
    try:
        req = session.get(url, headers=headers)
    except HTTPError as e:
        print(e)
        return None
    try:
        soup = BeautifulSoup(req.text, 'html.parser')
    except AttributeError as e:
        print(e)
        return None
    return soup

def makeCsvLinkSerie(info_list, csv_name):
    with open(csv_name+'.csv', 'a') as csvFile:
        writer = csv.writer(csvFile, delimiter = ';')
        writer.writerow(info_list)
    csvFile.close()


def getInfoSerie(url, csv_name):
    list_serie = getLinkSerie(url)
    # List dans laquelle on va mettre chaque élément que l'on souhaite conserver dans le csv
    row = []

    for serie in list_serie:
        soup = getSoup(serie)
        t.sleep(randint(3,7))
        # print(soup)
        for div in soup.findAll("div", {"class":"album-main"}):
            try:
                print('Couverture url: ' + soup.find('img', itemprop='image')['src'])
                # Les lignes suivantes servent à sauvegarder les miniatures des couvertures de chaque album
                # img_url = soup.find('img', itemprop='image')['src']
                # img_name_array = img_url.split('/')
                # urllib.request.urlretrieve(img_url,'couvertures/'+img_name_array[-1])
                row.append(soup.find('img', itemprop='image')['src'])
            except:
                print('Pas d\'image de couverture')
                row.append('Pas d\'image de couverture')
            try:
                print('Résumé: ' + soup.find("meta", property="og:description")['content'])
                row.append(soup.find("meta", property="og:description")['content'])
            except:
                print('Pas de résumé')
                row.append('Pas de résumé')
            try:
                print('Genre: ' + soup.find("span", {"class": "style-serie"}).text)
                row.append(soup.find("span", {"class": "style-serie"}).text)
            except:
                print('Pas de genre')
                row.append('Pas de genre')
            try:
                print('Langue: ' + soup.find('img', {'class':'flag'})['src'])
                row.append(soup.find('img', {'class':'flag'})['src'])
            except:
                print('Pas de langue')
                row.append('Pas de langue')
            try:
                print('Titre: ' + div.find("a", {"class": "titre"})['title'])
                row.append(div.find("a", {"class": "titre"})['title'])
            except:
                print('Pas de titre')
                row.append('Pas de titre')
            try:
                print('Scénariste: ' + div.find("ul", {"class": "infos"}).find("span", itemprop="author").text)
                row.append(div.find("ul", {"class": "infos"}).find("span", itemprop="author").text)
            except:
                print('Pas de scénariste')
                row.append('Pas de scénariste')
            try:
                print('Dessin: ' + div.find("ul", {"class": "infos"}).find("span", itemprop="illustrator").text)
                row.append(div.find("ul", {"class": "infos"}).find("span", itemprop="illustrator").text)
            except:
                print('Pas de dessinateur')
                row.append('Pas de dessinateur')
            try:
                print('Date de publication: ' + div.find("ul", {"class": "infos"}).find('meta').attrs['content'])
                row.append(div.find("ul", {"class": "infos"}).find('meta').attrs['content'])
            except:
                print('Pas de date de publication')
                row.append('Pas de date de publication')
            try:
                print('Editeur: ' + div.find("ul", {"class": "infos"}).find("span", itemprop="publisher").text)
                row.append(div.find("ul", {"class": "infos"}).find("span", itemprop="publisher").text)
            except:
                print('pas d\'éditeur')
                row.append('Pas d\'éditeur')
            try:
                print('Isbn: ' + div.find("ul", {"class": "infos"}).find("span", itemprop="isbn").text)
                row.append(div.find("ul", {"class": "infos"}).find("span", itemprop="isbn").text)
            except:
                print('Pas d\'ISBN')
                row.append('Pas d\'ISBN')

            makeCsvLinkSerie(row, csv_name)
            row = []

            print('_______________________________________')
        print('----------------AUTRE SERIE----------------')




# soup = getAlbumMain(my_url)
# soup = BeautifulSoup(my_html, 'html.parser')

france = 'https://www.bdgest.com/skin/flags/France.png'

serie_a = 'https://www.bedetheque.com/bandes_dessinees_A.html'
serie_l = 'https://www.bedetheque.com/bandes_dessinees_L.html'

getInfoSerie(serie_a, 'serie_a')

# getInfoSerie()
# list_of_links = getLinkSerie(serie_l)
# makeCsvLinkSerie(mylofl)
# print(list_of_links)
# print(soup)
# img_url = soup.find('img', itemprop='image')['src']
# img_name_array = img_url.split('/')
# print(img_name_array[-1])
# urllib.request.urlretrieve(img_url,'couvertures/'+img_name_array[-1])
# getInfoSerie(soup)
# print(soup.find('div', {"class":"album-main"}).find("ul", {"class": "infos"}).find("span", itemprop="illustrator").text)

# print(list_serie_a)
# print(soup.find("div", {"class":"album-main"}).find("ul", {"class": "infos"}).find('meta').attrs['content'])

