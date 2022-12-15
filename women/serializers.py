import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Women

#ПОКАЗАН ВЕСЬ ПРОЦЕСС КОДИРОВАНИЯ И ДЕКОДИРОВАНИЯ ДАННЫХ, КОТОРЫЕ ПРЕДСТАВЛЯЮТСЯ В ВИДЕ JSON-ФОРМАТА
# class WomenModel:
#     '''Класс, объекты которого будем сериализовать,
#     т.е. преобразовывать в JSON-строку. Этот класс будем имитировать моедли фреймворка Django.
#     '''
#
#     def __init__(self,title,content):
#         #оздаем локальные атрибуты класса
#         self.title=title
#         self.content=content

class WomenSerializer(serializers.Serializer):
    '''Данный класс будет наследоваться от базового класса Serializer,
    и в нем надо вручную прописать весь функционал по преобразованию
    объектов класса WomenModel в JSON-формат.
     !!!!ВАЖНО!!!
     В сериализаторе мы прописываем атрибуты абсолютно с теми же самыми именами,
     что и локальные свойства, которые присутствуют в объектах класса WomenModel'''

    #определим все атрибуты класса Women:
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True) #только для чтения
    time_update = serializers.DateTimeField(read_only=True) #только для чтения
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()

class CategorySerializer(serializers.Serializer):
    name=serializers.CharField(max_length=50)


# def encode():
#     '''Мы будем выполнять кодирование (преобразование) объектов класса WomenModel
#     в JSON-формат.'''
#
#     #создадим объект класса WomenModel:
#     model=WomenModel('Sandra Bullock','Content: about Sandra Bullock')
#
#     #далее мы пропустим этот объект через сериализатор WomenSerializer, на вход подаввя объект model:
#     result=WomenSerializer(model)
#     #выведем в консоль то,что у нас получилосьи посмотрим на тип
#     #data-это как раз сериализованные данные
#     print(result.data, type(result.data), sep='\n')
#
#     #result представляет объект сериализации, а не JSON-строку.
#     #чтобы мы result могли представить в виде JSON-строки,
#     # нужно выполнить следующее:
#     json=JSONRenderer().render(result.data)
#
#     #выведем то, что у нас получится
#     print(json)
#
# def decode():
#     '''Обратное преобразование из JSON-строки в объект класса WomenModel.
#     '''
#     #Мы будем имитировать потсупление запроса от клиента
#     #и как будто читаем JSON-строку, которая пришла от клиента
#     stream=io.BytesIO(b'{"title":"Sandra Bullock","content":"Content: about Sandra Bullock"}')
#
#     #далее для формирования словаря мы воспользуемся JSON-парсером:
#     data=JSONParser().parse(stream)
#
#     #далее с помощью сериализатора WomenSerializer преобразовываем набор данных data
#     # для того чтобы получить объект сериализации.Чтобы он декодировал данные,нужно
#     # изпользовать именованный параметр data
#     serializer=WomenSerializer(data=data)
#
#     #далее мы должныпроверить корректность принятых данных:
#     serializer.is_valid()
#     #после того, как is_valid отработает, в сериализаторе появится коллекция validated_data,
#     #которая и есть результат декодирования JSON-строки
#     print(serializer.validated_data)




# class WomenSerializer(serializers.ModelSerializer):
#     '''Мы наследуемся от сериализатора ModelSerializer,
#     потому что он работает с моделями, т.к. мы будем брать
#     из таблицы БД определенные записи, представлять их в
#     JSON-формате и отправлять в ответ на запрос пользователя'''
#     class Meta:
#         '''Объяснения будут чуть позже'''
#         model=Women                 #указываем нужную модель
#         fields=('title','cat_id')   #поля, которые мы будем использовать для сериализации, т.е. те, которые будут отправляться обратно пользователю

