# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User,Image,Patient

# Register your models here.

admin.site.register(User)
admin.site.register(Image)
admin.site.register(Patient)