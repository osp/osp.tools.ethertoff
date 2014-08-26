# -*- coding: utf-8 -*-

from django.contrib import admin

from etherpadlite.models import *

class PadAuthorAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)


class PadAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    readonly_fields = ('name',)
    exclude = ('display_name',)
    
    def has_add_permission(self, request):
        return False

admin.site.register(PadServer)
admin.site.register(PadGroup)
admin.site.register(PadAuthor, PadAuthorAdmin)
admin.site.register(Pad, PadAdmin)
