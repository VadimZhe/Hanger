from django.contrib import admin

from .models import Words, Languages, InterfaceMessages

admin.site.register(Words)
admin.site.register(Languages)
admin.site.register(InterfaceMessages)