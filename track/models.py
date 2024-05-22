from django.db import models


class Track(models.Model):
    file = models.FileField(upload_to="tracks/")
    artist = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
