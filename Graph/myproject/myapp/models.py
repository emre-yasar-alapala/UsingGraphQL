from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.name