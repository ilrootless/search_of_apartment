import requests
from bs4 import BeautifulSoup

URL = 'https://spb.cian.ru/cat.php'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0', 'accept': '*/*'}

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

# Получение объявлений из заданной страницы
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='_93444fe79c--card--_yguQ')
    
    ads = []
    for item in items:
        if item.find('div', class_='c6e8ba5398--single_title--22TGT'):
            title = item.find('div', class_='c6e8ba5398--single_title--22TGT').get_text(strip=True)
        elif item.find('div', class_='c6e8ba5398--title--2CW78'):
            title = item.find('div', class_='c6e8ba5398--title--2CW78').get_text(strip=True)
        elif item.find('div', class_='c6e8ba5398--title--39crr'):
            title = item.find('div', class_='c6e8ba5398--title--39crr').get_text(strip=True)
        else:
            title = 'Без названия'
        
        if item.find('div', class_='c6e8ba5398--header--1dF9r'):
            price = item.find('div', class_='c6e8ba5398--header--1dF9r').get_text(strip=True)
        elif item.find('div', class_='c6e8ba5398--header--1df-X'): 
            price = item.find('div', class_='c6e8ba5398--header--1df-X').get_text(strip=True)
        else:
            price = 'Цену уточняйте'

        ad_image = item.find('img', class_='c6e8ba5398--image--3ua1b')
        if ad_image:
            ad_image = ad_image.get('src')
        else:
            ad_image = 'Изображение отсутсвует'
        ads.append({
            'title': title, 
            'link': item.find('a', class_='c6e8ba5398--header--1fV2A').get('href'),
            'image': ad_image,
            'price': price,
            'address': item.find('div', class_='c6e8ba5398--address-links--1tfGW').contents[0].get('content'),
            'date': item.find('div', class_='c6e8ba5398--absolute--9uFLj').get_text(strip=True),
        })
    return ads

# Получение словаря параметров
def parsing_cian(post):
    params = {
            'currency': 2,
            'engine_version': 2,
            'offer_type': 'flat',
            'region': 2,
    }
    ads = []

# Вид сделки

    # Если выбрана аренда, добавляем параметр аренды
    if 'rental' in post['type_of_transaction']:
        params['deal_type'] = 'rent'
    # Если выбрана покупка, добавляем параметр покупки
    if 'purchase' in post['type_of_transaction']:
        params['deal_type'] = 'sale'

# Новизна квартиры

    # Если выбрана только новостройка или только вторичка, добавляем соответствующий параметр 
    if 'new_building' in post['novelty']:
        if 'rent' not in params['deal_type']:
            params['object_type[0]'] = 2
    if 'secondary' in post['novelty']:
        if 'rent' not in params['deal_type']:
            params['object_type[0]'] = 1

# Колличество комнат
    
    #   если выбрана только студия/1/2/...:
    #       добавить параметр студии...
    #       если параметр вида сделки пуст:
    #           поместить туда просто покупки
    if 0 in post['number_of_rooms']: 
        params['room9'] = 1
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 1 in post['number_of_rooms']: 
        params['room1'] = 1
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 2 in post['number_of_rooms']: 
        params['room2'] = 1
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 3 in post['number_of_rooms']: 
        params['room3'] = 1
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 4 in post['number_of_rooms']: 
        params['room4'] = 1
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 5 in post['number_of_rooms']: 
        params['room5'] = 1
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 6 in post['number_of_rooms']: 
        params['room6'] = 1
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    
# Прайсы    

    # Если введена цена от:
    #   присвоить значение соответствующему параметру
    #   если параметр вида сделки пуст:
    #       поместить туда просто покупки
    # Если введена цена до:
    #   присвоить значение соответствующему параметру
    #   если параметр вида сделки пуст:
    #       поместить туда просто покупки
    if post['price_from']:
        params['minprice'] = post['price_from']
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if post['price_up_to']:
        params['maxprice'] = post['price_up_to']
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'

# Районы

    #   если выбран один из параметров:
    #       добавить соответствующий параметр
    #       если в "виде сделки" пусто:
    #           добавить просто продажи
    if 'Admiralteyskiy' in post['district']:
        params['district[0]'] = 150
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Vasileostrovskiy' in post['district']:
        params['district[1]'] = 149
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Vyborgskiy' in post['district']:
        params['district[2]'] = 148
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Kalininskiy' in post['district']:
        params['district[3]'] = 147
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Kirovsky' in post['district']:
        params['district[4]'] = 146
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Kolpinsky' in post['district']:
        params['district[5]'] = 145
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Krasnogvardeisky' in post['district']:
        params['district[6]'] = 144
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Krasnoselsky' in post['district']:
        params['district[7]'] = 143
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Kronshtadtskiy' in post['district']:
        params['district[8]'] = 142
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Kurortnyy' in post['district']:
        params['district[9]'] = 141
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Moskovskiy' in post['district']:
        params['district[10]'] = 140
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Nevsky' in post['district']:
        params['district[11]'] = 139
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Petrogradsky' in post['district']:
        params['district[12]'] = 138
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Petrodvortsovyy' in post['district']:
        params['district[13]'] = 137
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Primorskiy' in post['district']:
        params['district[14]'] = 136
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Pushkinskiy' in post['district']:
        params['district[15]'] = 135
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Frunzenskiy' in post['district']:
        params['district[16]'] = 134
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    if 'Tsentralnyy' in post['district']:
        params['district[17]'] = 133
        if not 'deal_type' in params:
            params['deal_type'] = 'sale'
    
    for page in range(1, 2):#pages_count + 1):
        # получаем html каждой страницы
        html = get_html(URL, params=params)
        # и вытаскиваем из нее объявления
        ads.extend(get_content(html.text))
    return ads
