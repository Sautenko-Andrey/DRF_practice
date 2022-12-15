from rest_framework import serializers
from .models import Women


class WomenSerializer(serializers.ModelSerializer):
    '''Мы наследуемся от сериализатора ModelSerializer,
    потому что он работает с моделями, потому что мы будем брать
    из таблицы БД определенные записи, представлять их в
    JSON-формате и отправлять в ответ на запрос пользователя'''
    class Meta:
        '''Объяснения будут чуть позже'''
        model=Women                 #указываем нужную модель
        fields=('title','cat_id')   #поля, которые мы будем использовать для сериализации, т.е. те, которые будут отправляться обратно пользователю

