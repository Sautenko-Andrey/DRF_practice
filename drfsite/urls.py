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
from django.urls import path

from women.views import WomenAPIView, CategoryAPIView, TeamsAPIList, CategoryTeamsAPIList, TeamsAPIUpdate, \
    TeamsAPIDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/womenlist/',WomenAPIView.as_view()),
    path('api/v1/womenlist/<int:pk>/',WomenAPIView.as_view()), #дополнительно передаем ключ pk(идентификатор записи, которую собираемся поменять)
    path('api/v1/categorylist/',CategoryAPIView.as_view()),
    path('api/v1/teamslist/',TeamsAPIList.as_view()),
    path('api/v1/teamslist/<int:pk>/',TeamsAPIUpdate.as_view()),
    path('api/v1/teamsdetail/<int:pk>/', TeamsAPIDetailView.as_view()),
    path('api/v1/teamscategorylist/',CategoryTeamsAPIList.as_view()),

]
