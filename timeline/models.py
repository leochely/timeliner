from django.db import models
from datetime import datetime

# Create your models here.
class Evenement(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    personnages = models.ManyToManyField("Personnage")
    categorie = models.ManyToManyField("Categorie", blank=True)
    flashback_date = models.DateField("Date de récit du flashback", blank=True, null=True)

    def __str__(self):
        return self.name

class Personnage(models.Model):
    name = models.CharField(max_length=100)
    date_naissance = models.DateField(default=datetime.now())

    def __str__(self):
        return self.name

class Categorie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
