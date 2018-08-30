from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import PrivateMessage


admin.site.register(PrivateMessage, MPTTModelAdmin)
