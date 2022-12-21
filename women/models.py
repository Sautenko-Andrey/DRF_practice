from django.contrib.auth.models import User
from django.db import models

class Women(models.Model):
    '''Моедль статьи с заголовком, контентом, временем создания,
    временем изменения(возможным), функцией опубликовано/неопубликовано
    и ссылкой на категории (ссылкой на модель Category)'''
    title=models.CharField(max_length=255)
    content=models.TextField(blank=True)
    time_create=models.DateTimeField(auto_now_add=True)
    time_update=models.DateTimeField(auto_now=True)
    is_published=models.BooleanField(default=True)
    cat=models.ForeignKey('Category',on_delete=models.PROTECT,null=True)
    user=models.ForeignKey(User, verbose_name='Пользователь',on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    '''Модель определяет что это за категория знаменитых женщин:
    актриса, певица или спортсменка'''
    name=models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class VolleyballTeams(models.Model):
    team_name=models.CharField(max_length=25)
    players=models.CharField(max_length=50)
    rank=models.CharField(max_length=3)
    city=models.CharField(max_length=25)
    cat_players=models.ForeignKey('PlayersCategory',on_delete=models.PROTECT,null=True)

    def __str__(self):
        return self.team_name

class PlayersCategory(models.Model):
    name=models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


