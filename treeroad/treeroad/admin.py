from django.contrib import admin
from django.conf import settings
from models import GenericService, Node, Service, Graph, RRDFile, DataSource, View, ViewTemplate, DataDef, LineDef
from admin_forms import ViewForm
# Abstract models not in admin.py
# GenericService not in admin.py, except debug in mode

class GenericServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'debug_info')
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name','description','highlight','serviceCount')
    prepopulated_fields = {'slug_name' : ('name',),}
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'highlight')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('delete_notes', 'slug_name','path_part')
        }),
    )
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name','node','description','highlight','graphCount')
    prepopulated_fields = {'slug_name' : ('name',),}
    fieldsets = (
        (None, {
            'fields': ('name', 'node', 'description', 'highlight')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('delete_notes', 'generic_service', 'slug_name', 'path_part')
        }),
    )
class GraphAdmin(admin.ModelAdmin):
    list_display = ('name','service','description','highlight','dataSourceCount')
    prepopulated_fields = {'slug_name' : ('name',),}
    fieldsets = (
        (None, {
            'fields': ('name', 'service', 'description', 'highlight')
        }),
        ('Graph options', {
            'fields': ('width','height'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('delete_notes', 'slug_name', 'path_part')
        }),
    )
class ViewAdmin(admin.ModelAdmin):
    list_display = ('name','graph','description', 'start', 'end')
    prepopulated_fields = {'slug_name' : ('name',),}
    fieldsets = (
        (None, {
            'fields': ('graph',)
        }),
        ('Template-based', {
            'classes': ('collapse',),
            'fields': ('template',)
        }),
        ('Manual', {
            'classes': ('collapse',),
            'fields': ('name', 'description', 'highlight')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('delete_notes', 'slug_name')
        }),
    )
    form = ViewForm
class ViewTemplateAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'start', 'end')
    prepopulated_fields = {'slug_name' : ('name',),}
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'highlight')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('delete_notes', 'slug_name')
        }),
    )
# Register DEBUG only models
if hasattr(settings, 'DEBUG'):
    if getattr(settings, 'DEBUG'):
        admin.site.register(GenericService, GenericServiceAdmin)

# Register standard models
admin.site.register(Node,NodeAdmin)
admin.site.register(Graph,GraphAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(View,ViewAdmin)
admin.site.register(ViewTemplate,ViewTemplateAdmin)
