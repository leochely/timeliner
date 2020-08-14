from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Evenement, Personnage, Categorie

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)

class EvenementAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']
    list_filter = ['personnages']
    ordering = ['date']

admin.site.register(Evenement, EvenementAdmin)
admin.site.register(Personnage)
admin.site.register(Categorie)

admin.site.site_url = "/timeline"
