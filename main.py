import requests
import csv
import sys
import time
from datetime import datetime

from urllib.parse import urlparse
from bs4 import BeautifulSoup
# import telebot





domain = input(str('Введите адрес сайта в формате site.com :'))
site = 'https://' + domain



links = set() # тут будем хранить все уникальные внутренние ссылки сайта



def get_links(url):
    """Получает списко всех внутренних страниц сайта и собирает в множество links"""
    list_links = [] # список url, от которого будем запускаться рекурсивно
    page = requests.get(url)
    print(f"Парсится: {url}")
    soup = BeautifulSoup(page.text, "html.parser")
    for link in soup.find_all('a'):
        link = link.get('href')
        if link: # проверяем, что вернулось не None, иначе вылетим с ошибкой
            if link.startswith('/'): # если ссылка относительная, делаем ее абсолютной
                link = site + link
            if link not in links and urlparse(link).netloc == domain and not link[-4:] == ('.jpg'):
                # если ссылки еще нет в множестве и она принадлежит нашему домену
                links.add(link)
                list_links.append(link)
    for link in list_links: # запускаемся заново от всех собранных ссылок
        get_links(link)


def get_data(links):
    """Получает информацию о нужных тегах"""
    data = []
    for link in links:
        print(f"Получаем информацию о тегах страницы: {link}")
        page = requests.get(link)
        page.encoding = 'utf8' # чтоб нормально кириллицу отображало
        soup = BeautifulSoup(page.text, "html.parser")
        if soup.title:
            title = soup.title.contents[0]
        if soup.h1:
            h1 = soup.h1.contents[0]
        data.append({'url': link,
                     'title': title,
                     'h1': h1})
    return data


def write_csv(data):
    with open(domain + '.' + 'csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('URL', 'TITLE', 'H1'))
        for i in data:
            writer.writerow((i['url'], i['title'], i['h1']))

# def save_for_bot():
#     global read
#     read = open("linksdata.csv")  # читаем файл с данными
#     return read  # Возвращает файл с данными

def main():
    print("Запущен")
    start = datetime.now()
    get_links(site)
    get_data(links)
    write_csv(get_data(links))
    stop = datetime.now()
    total = stop - start
    print(f"Обработано {len(links)} страниц")
    print(f"Затрачено времени {total}")
    print("CSV файл выгружен в директорию с программой")
    # return(save_for_bot())

if __name__ == '__main__':
    main()



# def bot():
#     bot = telebot.TeleBot('1059669648:AAE0hWqchemB2sXqBesPJJ9BtqMqDeAIQ64')  # Подключаемся к боту
#
#
#     @bot.message_handler(commands=["File"])  # Создаем команду
#     def sendMessage(message):  # Создаем функцию команды
#         bot.send_document(message.chat.id, main())  # отправляем файл
#         read.close()  # убираем файл из памяти
#         # os.remove("linksdata.csv")  # удаляем файл с хостинга после отправки
#     bot.polling()  # Прослушивание бота
#
#
# bot() # Вызываем функцию
