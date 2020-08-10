from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Evenement, Personnage, Categorie

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Evenement)
admin.site.register(Personnage)
admin.site.register(Categorie)

admin.site.site_url = "/timeline"
