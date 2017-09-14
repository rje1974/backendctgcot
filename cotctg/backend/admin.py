# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Entidad, Credencial, CTG
from .models import Especie, Cosecha, Localidad, Establecimiento,\
    Provincia
from backend.models import Operacion, COT, Provincia_ARBA

# Register your models here.
admin.site.register(Credencial)
admin.site.register(Entidad)
admin.site.register(CTG)
admin.site.register(COT)
admin.site.register(Especie)
admin.site.register(Cosecha)
admin.site.register(Establecimiento)
admin.site.register(Provincia)
admin.site.register(Provincia_ARBA)
admin.site.register(Localidad)
admin.site.register(Operacion)