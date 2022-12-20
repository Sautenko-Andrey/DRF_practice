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
from django.urls import path, include

from rest_framework import routers

from women.views import WomenAPIView, CategoryAPIView, TeamsAPIList, TeamsAPIUpdate,TeamsAPIDetailView, PlayersCategoryViewSet

#создание объекта-роутера:
router=routers.SimpleRouter()
#далее в этом объекте нужно зарегестрировать класс ViewSet
router.register(r'players_category', PlayersCategoryViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/womenlist/',WomenAPIView.as_view()),
    path('api/v1/womenlist/<int:pk>/',WomenAPIView.as_view()), #дополнительно передаем ключ pk(идентификатор записи, которую собираемся поменять)
    path('api/v1/categorylist/',CategoryAPIView.as_view()),
    path('api/v1/teamslist/',TeamsAPIList.as_view()),
    path('api/v1/teamslist/<int:pk>/',TeamsAPIUpdate.as_view()),
    path('api/v1/teamsdetail/<int:pk>/', TeamsAPIDetailView.as_view()),
    #path('api/v1/teamscategorylist/',PlayersCategoryViewSet.as_view({'get':'list'})), #для получения списка записей из БД
    #path('api/v1/teamscategorylist/<int:pk>/',PlayersCategoryViewSet.as_view({'put':'update'})), #для изменения записи в БД
    #вместо этих двух маршрутов мы пропишем весь набор маршрутов, которые были автоматически сгенерированн роутером
    path('api/v1/',include(router.urls)) #маршрут будет включать префикс http://127.0.0.1:8000/api/v1/players_category/ - отвечает за чтение и добавление новой записи в БД
    #а если добавляем ключ в конце - http://127.0.0.1:8000/api/v1/players_category/2/ - мы можем прочитать ,изменить запись или удалить запись



]
