from django.db import models

# Create your models here.
class skuId(models.Model):
    searchID = models.CharField(max_length=15)
    date = models.TextField()
