from django.db import models
import datetime


# Create your models here.

class Thread(models.Model):
    Author = models.TextField()
    Content = models.TextField()
    ContentEncode = models.TextField()
    ImageUpload = models.TextField()
    TimeStr = models.TextField()
    Timestamp = models.IntegerField()

    def __str__(self):
        return self.Author + ': ' + self.TimeStr + ' ' + self.ImageUpload + ' ' + self.Content

        # def __str__(self):
        #     return self.Author + ': ' + datetime.datetime.fromtimestamp(int(self.Timestamp)).strftime(
        #         '%Y-%m-%d %H:%M:%S') + ' ' + self.ImageUpload + ' ' + self.Content


class VisitInfo(models.Model):
    TimeStr = models.TextField()
    Url = models.TextField()
    Addr = models.TextField()
    UserAgent = models.TextField()
    Location = models.TextField()

    def __str__(self):
        return self.TimeStr + ' ' + self.Addr + ' ' + self.Location + ' ' + self.Url + ' ' + self.UserAgent
