import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def write_to_csv(data):
    with open('data.csv','a') as file:
        write = csv.writer(file)
        write.writerow([data['img'],data['model'], data['disk'],data['price']])

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    cars = soup.find('div',class_ = 'search-results-table').find_all('div', class_ = 'list-item list-label')
    for car in cars:
        model = car.find('div',class_= 'block title').text.strip()
        disk1 = car.find('div',class_='block info-wrapper item-info-wrapper').find('p', class_ = 'year-miles').text.strip()
        disk2 = car.find('div',class_='block info-wrapper item-info-wrapper').find('p', class_ = 'body-type').text.strip()
        disk3 = car.find('div',class_='block info-wrapper item-info-wrapper').find('p', class_ = 'volume').text.strip()
        disk = disk1 + disk2 + disk3
        price = car.find('div',class_ = 'block price').find('strong').text.strip()
        try:
            img = car.find('div',class_='thumb-item-carousel').find('img').get('data-src').strip() + ' '
        except:
            img = 'NO IMAGE'
        data = {'model':model,'disk':disk, 'price':price,'img':img}
        write_to_csv(data)

with open('data.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['                   image','                                                                    model','    discription','                                     price'])

def get_last_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    page_list = soup.find('nav').find('ul', class_ = 'pagination').find_all('li')
    last_page  = page_list[6].text
    print(int(last_page))
    return int(last_page)

def main():
    url = 'https://www.mashina.kg/search/bmw/'
    html = get_html(url)
    num = int(get_last_pages(html))
    i = 1
    while i <= num:
        print(i)
        url = f'https://www.mashina.kg/search/bmw/?page={i}'
        html = get_html(url)
        num = int(get_last_pages(html))
        i+=1
        if not BeautifulSoup(html, 'lxml').find('div', class_='list-item list-label'):
            break
        get_data(html)

main()