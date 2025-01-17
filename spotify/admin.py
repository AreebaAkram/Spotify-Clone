from django.contrib import admin
from .import models
# Register your models here.
admin.site.register(models.userProfile)
admin.site.register(models.song)
admin.site.register(models.Comment)
admin.site.register(models.Like)