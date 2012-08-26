from django.contrib import admin
from django.conf import settings
from models import *

# Abstract models not in admin.py
# GenericService not in admin.py, except debug in mode

class GenericServiceAdmin(admin.ModelAdmin):
    pass
class NodeAdmin(admin.ModelAdmin):
    pass
class ViewTemplateAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug_name' : ('name',),}
# Register DEBUG only models
if hasattr(settings, 'DEBUG'):
    if getattr(settings, 'DEBUG'):
        admin.site.register(GenericService, GenericServiceAdmin)

# Register standard models
admin.site.register(Node,NodeAdmin  )
admin.site.register(ViewTemplate,ViewTemplateAdmin)
