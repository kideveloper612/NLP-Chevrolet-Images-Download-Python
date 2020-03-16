import os
import csv
import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import json
from random import randrange


def write_direct_csv(self, lines, filename):
    with open('extra/%s' % filename, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)
    csv_file.close()


def write_csv(self, lines, filename):
    if not os.path.isdir('extra'):
        os.mkdir('extra')
    if not os.path.isfile('extra/%s' % filename):
        self.write_direct_csv(lines=self.csv_header, filename=filename)
    self.write_direct_csv(lines=lines, filename=filename)


def read_csv(path):
    with open(file=path, encoding='utf-8') as csv_reader:
        return list(csv.reader(csv_reader))


def download(url, name):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, '2/' + name)
    except Exception as e:
        print(e)


def scrape_carconnection():
    url = 'https://www.thecarconnection.com/cars/chevrolet_bolt'
    url_soup = BeautifulSoup(requests.request('GET', url=url).content, 'html5lib')
    vehicles = url_soup.select('.divmodels .menu-column', limit=4)
    for vehicle in vehicles:
        links = vehicle.find_all('a')
        for loop in links:
            link = 'https://www.thecarconnection.com' + loop['href']
            link_soup = BeautifulSoup(requests.request('GET', url=link).content, 'html5lib')
            if link_soup.find('a', text=re.compile('2020')):
                new_link = 'https://www.thecarconnection.com' + link_soup.find('a', text=re.compile('2020'))['href']
            model = loop.text.replace(' ', '-').strip()
            if 'chevrolet' in new_link:
                print(new_link)
                new_link_soup = BeautifulSoup(requests.request('GET', url=new_link).content, 'html5lib')
                if new_link_soup.find('div', {'class': 'gallery'}):
                    data_prop = new_link_soup.find('div', {'class': 'gallery'})['data-model']
                    props = json.loads(data_prop)
                    for prop in props:
                        if not prop['isInt']:
                            image_url = prop['images']['huge']['url']
                            name = image_url.split('/')[-1]
                            if '2020' in name:
                                print(image_url, 'chevrolet_2020_' + model.lower() + '_' + str(randrange(100000, 1000000)))
                                download(url=image_url, name=model.lower() + '_' + str(randrange(100000, 1000000)))


def usnews():
    url = 'https://cars.usnews.com/ajax/finder/models/Chevrolet/'
    headers = {
        'user-agent': 'Mozila/5.0'
    }
    res = requests.get(url=url, headers=headers).json()
    for r in res:
        vehicle_link = 'https://cars.usnews.com' + r['url']
        vehicle_soup = BeautifulSoup(requests.request('GET', url=vehicle_link, headers=headers).content, 'html5lib')
        if vehicle_soup.find('h1', {'class': 'hero-title__header--overview'}):
            head = vehicle_soup.find('h1', {'class': 'hero-title__header--overview'}).text.split(' ')[0]
            if int(head) == 2020:
                photo_link = 'https://cars.usnews.com' + vehicle_soup.find('a', {'class': 'vwo-profile-nav-photos'})['href']
                photo_soup = BeautifulSoup(requests.request('GET', url=photo_link, headers=headers).content, 'html5lib')
                slides = photo_soup.find_all('img', {'class': 'slider--nav-box__img'})
                print(photo_link)
                for slide in slides:
                    if slide.has_attr('data-lazy'):
                        image_url = slide['data-lazy']
                        if '2020' in image_url:
                            print(image_url)


def google_chvrolet():
    count = 0
    for t, tt, ttt in os.walk('2'):
        print(len(ttt))

    exit()
    for d, o, f in os.walk('HTML'):
        for file in f:
            fi = open(file='HTML/' + file, encoding='utf-8')
            soup = BeautifulSoup(fi.read(), 'html5lib')
            images = soup.find_all('img', {'class': 'rg_i Q4LuWd tx8vtf'})
            for image in images:
                if image.has_attr('src'):
                    image_url = image['src']
                elif image.has_attr('data-src'):
                    image_url = image['data-src']
                if 'http' in image_url:
                    title = image.find_next(attrs={'class': 'WGvvNb'})
                    if title and '2020' in title.text:
                        name = 'chevrolet_2020_%s' % file.split('.')[0] + '_' + str(randrange(100000, 1000000)) + '.jpg'
                        download(url=image_url, name=name)
                        count += 1
                        print(count)
                        print(file, name, image_url)


if __name__=='__main__':
    print('+++++++++++++++++++START+++++++++++++++++++++++++')
    google_chvrolet()
    print('++++++++++++++++++++++End++++++++++++++++++++++++++')