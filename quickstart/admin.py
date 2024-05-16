from django.contrib import admin
from .models import *

admin.site.register(Zone)
admin.site.register(Equipement)
admin.site.register(Etage)
admin.site.register(ExcelData)
admin.site.register(Batiment)
admin.site.register(PeriodeActivite)
admin.site.register(Alerte)
admin.site.register(ProfileUser)
admin.site.register(Rapport)

from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']


