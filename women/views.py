from django.forms import model_to_dict
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Women, Category, VolleyballTeams, PlayersCategory
from .serializers import WomenSerializer, CategorySerializer, TeamsSerializer, PlayersCategorySerializer


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
        #метод save() автоматически вызовет метод create()в сериализаторе и добавит новую запись в БД
        serializer.save()

        #в качестве ответа клиенту мы будем отправлять обратно значение,данное этой новой добавленной записи,
        #т.е. мы будем знать что именно мы добавили в БД. Ключ будет 'post', а значение - сериализатор WomenSerializer
        return Response({'post':serializer.data})

    def put(self,request,*args,**kwargs):
        '''С помощью коллекции kwargs мы можем определить значение pk -
        идентификатор записи, которую нужно поменять. Как это делается? Мы обращаемся
        к словарю kwargs, берем у него ключ pk(если он там присутствует), а если не
        присутствует, то мы возвртим значение None.
        Далее сделаем проверку, что если этот ключ pk не присутствует в этой коллекции kwargs
        (т.е. этот ключ не указан в url-запросе), то мы возвратим ответ клиенту: "Method PUT is not allowed",
        т.к. мы не будем знать, что надо поменять.
        Далее мы попробуем взять указанную запись из модели Women по ключу pk,
        но если мы по каким-то причинам не можем взять выбранную запись,то мы возвратим ответ
        клиенту, что объект не найден - "Object doesn't exist".
        А если все прошло успешно, т.е. мы получили и ключ и запись по этому ключу,
        то соответственно создаем объект-сериализатор с помощью класса WomenSerializer,
        в качестве аргументов мы ему передадим request.data - потому что это как раз те данные,
        которые мы хотим изменить, и объект instance - это объект, конкретно который мы будем менять,
        т.е. ту запись ,которую мы собираемся поменять. Затем в этом объекте serializer мы должны проверить
        принятые данные с помощью is_valid и сохраняем его c помощью save(), причем метод save() автоматически вызовет
        метод update() из сериализатора (потому что когда мы создаем объект-сериализатор, мы указываем 2 параметра:
        (data и instance), поэтому вызывается метод update ,а не get(указывается для этого только data))
        А в самом конце, после того, как мы изменим запись, мы отправим клиенту запрос в виде
        JSON-строки : {"post":serializer.data}, где serializer.data - данные, которые были изменены.'''

        pk=kwargs.get('pk',None)
        if not pk:
            return Response({'Error':'Method PUT is not allowed'})
        try:
            instance=Women.objects.get(pk=pk)
        except:
            return Response({'Error':"Object doesn't exist"})

        serializer=WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post':serializer.data})

    def delete(self,request,*args,**kwargs):
        '''Метод для удаления записей из таблицы БД'''
        # определяем ключ записи, по которму будем удалять запись
        pk=kwargs.get('pk',None)
        if not pk:
            Response({'Error':'Method delete is not allowed'})
        try:
            instance=Women.objects.get(pk=pk).delete()
        except:
            return Response({'Error': "Object doesn't exist"})

        return Response({'post':'delete post'+str(pk)})

class CategoryAPIView(APIView):
    def get(self,request):
        all_categories=Category.objects.all()
        return Response({'categories':CategorySerializer(all_categories, many=True).data})

    def post(self, request):
        #проверка:
        serializer=CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #если все нормально, создаем post-запрос:

        return Response({'category':serializer.data})

    def put(self,request,*args,**kwargs):
        pk=kwargs.get('pk',None)
        if not pk:
            return Response({'Error':'Method PUT is not allowed'})
        try:
            instance=Category.objects.get(pk=pk)
        except:
            return Response({'Error':"Object doesn't exist"})

        serializer=CategorySerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'category': serializer.data})

    def delete(self,request,*args,**kwargs):
        pk=kwargs.get('pk',None)
        if not pk:
            return Response({'Error':'Method delete is not allowed'})
        try:
            instance=Category.objects.get(pk=pk).delete()
        except:
            return Response({'Error': "Object doesn't exist"})

        return Response({'category':'delete category'+str(pk)})


class TeamsAPIList(generics.ListCreateAPIView):
    '''ListCreateAPIView -  с помощью этого класса можно читать данные из БД по get-запросу,
    а так же добавлять новые по post-запросу. Внутри нашего класса мы должны определить 2 атрибута:
    queryset - будет ссылаться на список записей, возвращаемых клиенту,
    serializer_class - сериализатор, который мы будем применять.
    '''
    queryset = VolleyballTeams.objects.all()
    serializer_class = TeamsSerializer

class TeamsAPIUpdate(generics.UpdateAPIView):
    '''UpdateAPIView - класс для изменения данных в БД.
    Внутри определяются два атрибута:
    queryset - будет получать набор всех данных из таблицы VolleyballTeams.
    serializer_class - указываем класс сериализатора. Используется абсолютно
    тотже класс сериализатора, потому что мы по-прежнему работаем с моделью VolleyballTeams.
    Здесь будет отправляться клиенту только одна измененная запись из таблицы, а не вся таблица,
    потому что в Django queryset = VolleyballTeams.objects.all() - это ленивый запрос, и мы просто
    связываем queryset  с нужной нам табл. БД. А далее базовый класс UpdateAPIView уже сам
    обработает атрибут queryset и возвратит клиенту только одну измененную запись.
    '''

    queryset = VolleyballTeams.objects.all()
    serializer_class = TeamsSerializer

class TeamsAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''базовый класс RetrieveUpdateDestroyAPIView позволяет читать, изменять и добавлять
    записи в БД, а так же удалять.
    Прописываем 2 атрибута:
    queryset и serializer_class. Сериализатор будет абсолютно тот же самый,
    т.к. мы работаем с той же моделью из БД.'''

    queryset = VolleyballTeams.objects.all()
    serializer_class = TeamsSerializer



class CategoryTeamsAPIList(generics.ListCreateAPIView):
    queryset = PlayersCategory.objects.all()
    serializer_class = PlayersCategorySerializer


# class WomenAPIView(generics.ListAPIView):
#     '''1) Определим атрибут queryset, который из таблицы Women
#     будет брать все записи.
#     2) Параметром serializer_class мы укажем класс сериализатора WomenSerializer,
#      который мы определим в файле serializers.py.'''
#
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

