# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Credential, Company, CTG

# Register your models here.
admin.site.register(Credential)
admin.site.register(Company)
admin.site.register(CTG)