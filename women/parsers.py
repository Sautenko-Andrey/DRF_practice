import requests
from bs4 import BeautifulSoup as BS

# получаем содержимое странички с обзорами игр на Stop Game:
my_request=requests.get("https://chudo-market.ua/tizhnevij-top")

#результат прогоняем через BeautifulSoup:
html=BS(my_request.content, 'html.parser')

#зываем метод select, указывая нужный нам селектор тегов:
for el in html.select(".main__inner > .promo__body"):
    title=el.select('.promo__body > .promo__item')
    print(title[0].text)

