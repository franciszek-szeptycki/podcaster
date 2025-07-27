from django.db import models

class Podcast(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title



class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, related_name='episodes', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='episodes/')
    is_listened = models.BooleanField(default=False)
