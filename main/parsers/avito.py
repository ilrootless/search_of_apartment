import requests
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0', 'accept': '*/*'}
HOST = 'https://www.avito.ru'

# Получение html нужной страницы
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


# Получение колличества страниц
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-1WyVp')
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1

# Получение даннх об объявлениях из заданной страницы
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    
    ads = []
    for item in items:
        ad_address = item.find('span', class_='item-address__string')
        if ad_address:
            ad_address = ad_address.get_text(strip=True)
        else:
            ad_address = 'Адрес уточняйте'
        ad_image = item.find('img', class_='large-picture-img')
        if ad_image:
            ad_image = ad_image.get('src')
        else:
            ad_image = 'Изображение отсутсвует'
        ads.append({
            'title': item.find('h3', class_='snippet-title').get_text(strip=True),
            'link': HOST + item.find('a', class_='snippet-link').get('href'),
            'image': ad_image,
            'price': item.find('span', class_='snippet-price').get_text(strip=True),
            'address': ad_address,
            #'address': item.find('span', class_='item-address__string').get_text(strip=True),
            'date': item.find('div', class_='snippet-date-info').get('data-tooltip'),
        })
    return ads

# Получение словаря параметров и собственно парсинг
def parsing_avito(post):
    urls = []
    params = {}
    ads = []

# Вид сделки

    # Если выбрана аренда, добавляем url аренды
    if 'rental' in post['type_of_transaction']:
        urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934')
    # Если выбрана покупка, добавляем url покупки
    if 'purchase' in post['type_of_transaction']:
        urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')

# Новизна квартиры

    # Если выбраны и вторичка и новостройка одновременно, то, если в urls пусто, то добавляем url просто покупок
    if 'new_building' in post['novelty'] and 'secondary' in post['novelty']:
        if not urls:
            urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
    # Если выбрана только новостройка или только вторичка, добавляем соответствующий url
    else:
        if 'new_building' in post['novelty'] and not 'rental' in post['type_of_transaction']:
            urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg?cd=1&rn=25928')
            # Если выбрана и новостройка и покупка (общий список и новостроек и вторичек), то удаляем url просто покупок 
            if 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' in urls:
                urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'secondary' in post['novelty'] and not 'rental' in post['type_of_transaction']:
            urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?cd=1')
            # Если выбрана и вторичка и покупка (общий список и новостроек и вторичек), то удаляем url просто покупок 
            if 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' in urls:
                urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')

# Колличество комнат
    
    # Если выбраны все значения одновременно: 
    #   если в urls пусто:
    #       добавляем просто продажи
    if 0 in post['number_of_rooms'] and 1 in post['number_of_rooms'] and 2 in post['number_of_rooms'] and 3 in post['number_of_rooms'] and 4 in post['number_of_rooms'] and 5 in post['number_of_rooms'] and 6 in post['number_of_rooms']:
        if not urls:
            urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
    # Иначе 
    #   если выбрана только студия/1/2/...:
    #       если выбрана аренда:
    #           url студии/... в аренду.
    #           если в urls есть url просто аренды
    #               url просто аренды - удалить
    #       если продажа:
    #           url студии... в продажу
    #           если в urls есть url просто аренды
    #               url просто покупки - удалить
    #       иначе:
    #           url покупки студии/1/...
    else:
        if 0 in post['number_of_rooms']: 
            if 'rental' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/studii-ASgBAQICAUSSA8gQAUDMCBSMWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934')
            if 'purchase' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/studii-ASgBAQICAUSSA8YQAUDKCBT~WA?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
            else:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/studii-ASgBAQICAUSSA8YQAUDKCBT~WA?cd=1')
        if 1 in post['number_of_rooms']: 
            if 'rental' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/1-komnatnye-ASgBAQICAUSSA8gQAUDMCBSOWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934')
            if 'purchase' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/1-komnatnye-ASgBAQICAUSSA8YQAUDKCBSAWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
            else:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/1-komnatnye-ASgBAQICAUSSA8YQAUDKCBSAWQ?cd=1')
        if 2 in post['number_of_rooms']:
            if 'rental' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/2-komnatnye-ASgBAQICAUSSA8gQAUDMCBSQWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934')
            if 'purchase' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/2-komnatnye-ASgBAQICAUSSA8YQAUDKCBSCWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
            else:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/2-komnatnye-ASgBAQICAUSSA8YQAUDKCBSCWQ?cd=1')
        if 3 in post['number_of_rooms']:
            if 'rental' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/3-komnatnye-ASgBAQICAUSSA8gQAUDMCBSSWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934')
            if 'purchase' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/3-komnatnye-ASgBAQICAUSSA8YQAUDKCBSEWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
            else:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/3-komnatnye-ASgBAQICAUSSA8YQAUDKCBSEWQ?cd=1')
        if 4 in post['number_of_rooms']:
            if 'rental' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/4-komnatnye-ASgBAQICAUSSA8gQAUDMCBSUWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934')
            if 'purchase' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/4-komnatnye-ASgBAQICAUSSA8YQAUDKCBSGWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
            else:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/4-komnatnye-ASgBAQICAUSSA8YQAUDKCBSGWQ?cd=1')
        if 5 in post['number_of_rooms']:
            if 'rental' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/5-komnatnye-ASgBAQICAUSSA8gQAUDMCBSWWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934')
            if 'purchase' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/5-komnatnye-ASgBAQICAUSSA8YQAUDKCBSIWQ?cd=1')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
            else:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam/5-komnatnye-ASgBAQICAUSSA8YQAUDKCBSIWQ?cd=1')
        if 6 in post['number_of_rooms']:
            if 'rental' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/sdam-ASgBAgICAUSSA8gQ?cd=1&f=ASgBAQICAUSSA8gQAUDMCFSYWaKsAaCsAZ6sAZysAQ')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&rn=25934')
            if 'purchase' in post['type_of_transaction']:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&f=ASgBAQICAUSSA8YQAUDKCFSKWZqsAZisAZasAZSsAQ')
                if 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1' in urls:
                    urls.remove('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
            else:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1&f=ASgBAQICAUSSA8YQAUDKCFSKWZqsAZisAZasAZSsAQ')
    
# Прайсы    

    # Если введена цена от:
    #   присвоить значение соответствующему параметру
    #   если urls пустой:
    #       добавить url просто продажи
    # Если введена цена до:
    #   присвоить значение соответствующему параметру
    #   если urls пустой:
    #       добавить url просто продажи
    if post['price_from']:
        params['pmin'] = post['price_from']
        if not urls:
            urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
    if post['price_up_to']:
        params['pmax'] = post['price_up_to']
        if not urls:
            urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')

# Районы

    # Если выбраны все значения одновременно: 
    #   если в urls пусто:
    #       добавляем просто продажи
    if 'Admiralteyskiy' in post['district'] and 'Vasileostrovskiy' in post['district'] and 'Vyborgskiy' in post['district'] and 'Kalininskiy' in post['district'] and 'Kirovsky' in post['district'] and 'Kolpinsky' in post['district'] and 'Krasnogvardeisky' in post['district'] and 'Krasnoselsky' in post['district'] and 'Kronshtadtskiy' in post['district'] and 'Kurortnyy' in post['district'] and 'Moskovskiy' in post['district'] and 'Nevsky' in post['district'] and 'Petrogradsky' in post['district'] and 'Petrodvortsovyy' in post['district'] and 'Primorskiy' in post['district'] and 'Pushkinskiy' in post['district'] and 'Frunzenskiy' in post['district'] and 'Tsentralnyy' in post['district']:
        if not urls:
            urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
    # Иначе 
    #   если выбран только один из параметров:
    #       добавить соответстующие параметры
    #       если в urls пусто:
    #           добавить url просто продажи
    else:
        metro = ''
        if 'Admiralteyskiy' in post['district']:
            metro += '-155-199-201-202-205-1015-1016-2132'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Vasileostrovskiy' in post['district']:
            metro += '-194-209'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Vyborgskiy' in post['district']:
            metro += '-173-183-197-207-211-213'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Kalininskiy' in post['district']:
            metro += '-153-166-189-192'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Kirovsky' in post['district']:
            metro += '-154-167-172-179-198'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Kolpinsky' in post['district']:
            metro += '-200'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Krasnogvardeisky' in post['district']:
            metro += '-171-181'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Krasnoselsky' in post['district']:
            metro += '-198'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Kronshtadtskiy' in post['district']:
            metro += '-2216'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Kurortnyy' in post['district']:
            metro += '-168'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Moskovskiy' in post['district']:
            metro += '-161-163-177-178-184-212'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Nevsky' in post['district']:
            metro += '-162-175-182-195-196-200-208'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Petrogradsky' in post['district']:
            metro += '-158-164-169-185-203'
            if not urls:
                urls += ['https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1',]
        if 'Petrodvortsovyy' in post['district']:
            metro += '-198'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Primorskiy' in post['district']:
            metro += '-156-168-186-204'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Pushkinskiy' in post['district']:
            metro += '-170'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Frunzenskiy' in post['district']:
            metro += '-170-1017-2137-2138'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        if 'Tsentralnyy' in post['district']:
            metro += '-160-165-174-176-180-187-191-210'
            if not urls:
                urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')
        params['metro'] = metro

# Если не выбран ни один из параметров, добавить url просто продаж
    if not urls:
        urls.append('https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1')

    for url in urls:
        html = get_html(url, params=params)
        pages_count = get_pages_count(html.text)
        for page in range(1, 2):#pages_count + 1):
            # получаем html каждой страницы
            html = get_html(url, params=params)
            # и вытаскиваем из нее объявления
            ads.extend(get_content(html.text))
    return ads
