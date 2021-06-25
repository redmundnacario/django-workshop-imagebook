from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=64, unique=True)

#     def __str__(self):
#         return f"{self.id} : {self.name}"


class Post(models.Model):
    active = models.BooleanField(default=True)
    content = models.TextField()
    picture_url = models.CharField(max_length=200, null=True)
    author = models.ForeignKey( User,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name="posts")

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)



