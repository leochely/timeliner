from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Evenement, Personnage

# Register your models here.
admin.site.register(Evenement)
admin.site.register(Personnage)
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_url = "/timeline"
