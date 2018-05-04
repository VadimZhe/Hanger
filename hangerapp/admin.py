from django.contrib import admin

from .models import Words, InterfaceMessages, Languages

admin.site.register(Words)
admin.site.register(Languages)
admin.site.register(InterfaceMessages)