from django.db import models

# Create your models here.
class Post(models.Model):
    objects = NotImplemented
    title = models.CharField(max_length=200)
    description = models.TextField()
