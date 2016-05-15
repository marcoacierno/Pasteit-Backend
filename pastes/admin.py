from django.contrib import admin

from .models import Paste


@admin.register(Paste)
class PasteAdmin(admin.ModelAdmin):
    pass
