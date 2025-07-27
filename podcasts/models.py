from django.db import models
from django.contrib.auth.models import User

class Podcast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='podcasts', null=True, blank=True)
    title = models.CharField(max_length=200)


class Episode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='episodes', null=True, blank=True)
    podcast = models.ForeignKey(Podcast, related_name='episodes', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='episodes/')
    is_listened = models.BooleanField(default=False)
