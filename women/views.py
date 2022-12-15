from django.forms import model_to_dict
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Women, Category
from .serializers import WomenSerializer, CategorySerializer


class WomenAPIView(APIView):
    '''APIView - базовый класс представлений.
    Здесь приведен пример как на базовом уровне происходит обработка запросов
    в представлении DRF. Класс APIView как раз и выполняет эту работу:
    он связывает пришедший запрос с соответствующим методом (get,put,delete и т.д),
    а метод прописывается уже самостоятельно вручную.'''
    def get(self, request):
        '''Метод, отвечающий за обработку API-запросов,
        т.е. когда на вход серверу будут поступать get-запросы,
        то автоматически будет вызываться этот метод.
        Аргумент request содержит все параметры входящего get-запроса.
        Класс Response - возвращает клиенту, который сделал get-запрос,
        JSON-строку. JSON-строка будет формироваться следующим образом:
        мы на уровне python-программы прописываем словарь и этот словарь
        автоматически будет преобразован в JSON-строку.
        Т.е. класс Response() преобразовывает словарь в соответствующую JSON-строку.
        По данному get-запросу мы будем отправлять список всех записей из БД Women'''

        #для начала получим список всех записей Women из БД:
        pages_list=Women.objects.all()
        #вернем список всех записей из таблицы Women и т.к. здесь будет использоваться список записей,
        # а не одна какая-то запись,то дополнительно указываем many=True,чтобы он вернул список записей
        #data - это словарь преобразованных данных из таблицы Women
        #объект Response уже в свою очередь все преобразовывает в байтовую JSON-строку
        #здесь выполняется все действия из ф-ии encode, которую мы прописывали в ручную в serializers
        return Response({'posts': WomenSerializer(pages_list, many=True).data})

    def post(self, request):
        '''Метод, отвечающий за post-запросы.
        Т.е. он позволяет нам добавлять новые записи в БД.'''

        #прежде чем добавлять новую запись в БД мы сделаем проверку:
        #сначала мы создадим сериализатор на основе тех данных, которые поступили с post-запросом:
        serializer=WomenSerializer(data=request.data)

        #далее с помощью метода is_valid мы проверяем корректность принятых данных:
        serializer.is_valid(raise_exception=True)

        #определим перменную new_post, которая будет ссылаться на новую добавленную запись в табл.Women
        new_post=Women.objects.create(
            #title будет брать из коллекции request data значение title,
            #т.е. уогда мы будем отправялть post-апрос на сервер, то будем передвать ключ 'title'
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )
        #в качестве ответа клиенту мы будем отправлять обратно значение,данное этой новой добавленной записи,
        #т.е. мы будем знать что именно мы добавили в БД. Ключ будет 'post', а значение - сериализатор WomenSerializer,
        #many указывать не нужно,т.к. один объект берем,а не список
        return Response({'post':WomenSerializer(new_post).data})

class CategoryAPIView(APIView):
    def get(self,request):
        all_categories=Category.objects.all()
        return Response({'categories':CategorySerializer(all_categories, many=True).data})

    def post(self, request):
        new_category=Category.objects.create(
            name=request.data['name']
        )
        return Response({'category':CategorySerializer(new_category).data})

# class WomenAPIView(generics.ListAPIView):
#     '''1) Определим атрибут queryset, который из таблицы Women
#     будет брать все записи.
#     2) Параметром serializer_class мы укажем класс сериализатора WomenSerializer,
#      который мы определим в файле serializers.py.'''
#
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

