from django.db import models

# Create your models here.
class Article(models.Model):
    name = models.CharField("Nombre" , default="Sin nombre", null= False, max_length=200)
    content = models.TextField("Contenido", default="", blank=True)

    def __str__(self):
        return self.name
