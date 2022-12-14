from rest_framework import generics
from django.shortcuts import render
from .models import Women, Category
from .serializers import WomenSerializer, CategorySerializer


class WomenAPIView(generics.ListAPIView):
    '''1) Определим атрибут queryset, который из таблицы Women
    будет брать все записи.
    2) Параметром serializer_class мы укажем класс сериализатора WomenSerializer,
     который мы определим в файле serializers.py.'''

    queryset = Women.objects.all()
    serializer_class = WomenSerializer

class CategoryAPIView(generics.ListAPIView):
    '''Для тренировки!!!'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
