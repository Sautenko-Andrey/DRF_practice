"""drfsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

from women.views import *
#создание объекта-роутера:
router=routers.DefaultRouter()
#далее в этом объекте нужно зарегестрировать класс ViewSet
router.register(r'players_category', PlayersCategoryViewSet, basename='players_category') #добавил basename,т.к. мы закоментили queryset  в вьюсете,если queryset есть, то basename прописывать не нужно
# print(router.urls)

# !!! в качестве примера будет показано, как писать свои собственные роутеры (требуется редко,но знать нужно о таком)
class MyCustomRouter(routers.SimpleRouter):
    '''Данный класс был взят из оф.документации и немного кастомизирован.
    Мы наследуемся от класса SimpleRouter, как наиболее простого класса роутеров.
    А затем внутри нашего класса определяем специальный атрибут routes - т.е.
    это список наших маршрутов. каждый элемент этого списка представляется объектом класса Route.
    Каждый класс определяет один отдельный маршрут, и в каждрм классе прописываются парметры:
    1)url - это шаблон маршрута;
    2)mapping - связывает тип запроса с соответствующим методом вьюсета;
    3)name - определяет название маршрута;
    4)detail - определяет: это будет список или отдельная запись;
    5)initkwargs - это доп.аргументы , которые передаются конкретному определению при срабатывании маршрута
    В результате в данном кастомизированном роутере определено 2 маршрута
    '''

    routes=[
        #первый маршрут читает список статей
        routers.Route(
            url=r'^{prefix}$',
            mapping={'get':'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix':'List'}
        ),
        # второй маршрут читает конкретную статью по ее идентификатору
        routers.Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        )
    ]

#далее в router=routers.DefaultRouter() вместо DefaultRouter мы прописываем MyCustomRouter без routers.
#router=MyCustomRouter()
#router.register(r'players_category', PlayersCategoryViewSet, basename='players_category')



urlpatterns = [
    path('admin/', admin.site.urls),

    #пропишем маршрут, чтобы мы могли использовать авторизацию на основе сессий и кук.
    #этот маршрут мы придумываем сами, к примеру он будет api/v1/drf-auth/
    path('api/v1/drf-auth/',include('rest_framework.urls')), #теперь подключена авторизация на основе сессий

    #path('api/v1/womenlist/',WomenAPIView.as_view()),
    #path('api/v1/womenlist/<int:pk>/',WomenAPIView.as_view()), #дополнительно передаем ключ pk(идентификатор записи, которую собираемся поменять)
    path('api/v1/women/',WomenAPIList.as_view()),
    path('api/v1/women/<int:pk>/',WomenAPIUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>/',WomenAPIDestroy.as_view()),

    path('api/v1/categorylist/',CategoryAPIView.as_view()),

    path('api/v1/teamslist/',TeamsAPIList.as_view()),
    path('api/v1/teamslist/<int:pk>/',TeamsAPIUpdate.as_view()),
    path('api/v1/teamsdetail/<int:pk>/', TeamsAPIDetailView.as_view()),

    #path('api/v1/teamscategorylist/',PlayersCategoryViewSet.as_view({'get':'list'})), #для получения списка записей из БД
    #path('api/v1/teamscategorylist/<int:pk>/',PlayersCategoryViewSet.as_view({'put':'update'})), #для изменения записи в БД
    #вместо этих двух маршрутов мы пропишем весь набор маршрутов, которые были автоматически сгенерированн роутером
    path('api/v1/',include(router.urls)), #маршрут будет включать префикс http://127.0.0.1:8000/api/v1/players_category/ - отвечает за чтение и добавление новой записи в БД
    #а если добавляем ключ в конце - http://127.0.0.1:8000/api/v1/players_category/2/ - мы можем прочитать ,изменить запись или удалить запись

    #подключение библиотеки djoser к нашему проекту.авторизация через простые токены
    path('api/v1/auth/',include('djoser.urls')), #строка отвечающая за регистрацию,изменение,удаление пользователя
    re_path(r'^auth/',include('djoser.urls.authtoken')), #строка, отвечающая за авторизацию по токенам

    #маршруты для авторизации через JWT-токенов
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #для авторизации через JWT-токен
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #для обновления JWT-токена, когда его срок действия истек
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
