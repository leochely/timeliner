from django.db import models

# Create your models here.
class Evenement(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.CharField(max_length=100)
    personnages = models.ManyToManyField("Personnage")
    categorie = models.ManyToManyField("Categorie", blank=True)

    def __str__(self):
        return self.name

class Personnage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Categorie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
