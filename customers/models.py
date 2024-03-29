from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='customers', default='no_picture.jpg')

    def __str__(self):
        return self.name