from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=True, null=True)
    year = models.IntegerField()
    description = models.CharField(max_length=400)
    image_url = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    movie_id = models.IntegerField()
    owner = models.ForeignKey(User, default=None, blank=True, on_delete=models.SET_NULL, null=True)
    due_date = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="default_profile.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
