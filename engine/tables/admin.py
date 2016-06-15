from django.contrib import admin

from . import models

admin.site.register(models.Page, admin.ModelAdmin)
admin.site.register(models.Publication, admin.ModelAdmin)
