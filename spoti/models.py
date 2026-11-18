from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200,unique=True)
    email = models.CharField(max_length=200,unique=True)
    photo_profi = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.username

class Musice(models.Model):
    name_music = models.CharField(max_length=200)
    musice = models.FileField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_music

class Genere(models.Model):
    name_g = models.CharField(max_length=180)

    def __str__(self):
        return self.name_g


class Alsbome(models.Model):
    name_als = models.CharField(max_length=200)
    create_at = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name_als

class Like(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)