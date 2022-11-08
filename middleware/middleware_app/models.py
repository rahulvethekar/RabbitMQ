from django.db import models

# Create your models here.
class MaxCount(models.Model):
    url = models.CharField(max_length=200,unique=True)
    count = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.url}:- {self.count}"