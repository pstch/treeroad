from django.contrib import admin
from adminplus import AdminSitePlus

from treeroad.views import parseTree, syncTree, graphTaskView
from treeroad.models import domain, node, service, rrdFile, rrdDataSource, graph, dataDefinition, lineDefinition

admin.site = AdminSitePlus()

class nodeInline(admin.TabularInline):
    model = node
class serviceInline(admin.TabularInline):
    model = service
class rrdFileInline(admin.TabularInline):
    model = rrdFile
class rrdDataSourceInline(admin.TabularInline):
    model = rrdDataSource
class graphInline(admin.TabularInline):
    model = graph
class dataDefinitionInline(admin.TabularInline):
    model = dataDefinition
    readonly_fields = ('lastVname','lastInstruction')
class lineDefinitionInline(admin.TabularInline):
    model = lineDefinition
    readonly_fields = ('lastInstruction',)
class domainAdmin(admin.ModelAdmin):
    list_display = ('name','description','highlight')
    list_filter = ('highlight',)
    inlines = [nodeInline,]
class nodeAdmin(admin.ModelAdmin):
    list_display = ('name','domain','description','highlight','pathPart')
    list_filter = ('highlight','domain')
    inlines = [serviceInline,]
class serviceAdmin(admin.ModelAdmin):
    list_display = ('name','node','description','highlight','pathPart')
    list_filter = ('highlight','node')
    inlines = [rrdFileInline,graphInline]
class rrdFileAdmin(admin.ModelAdmin):
    list_display = ('pathPart','service','lastUpdate')
    list_filter = ('service',)
    date_hierarchy = ('lastUpdate')
    inlines = [rrdDataSourceInline,]
class graphAdmin(admin.ModelAdmin):
    list_display = ('name','service','description','highlight')
    list_filter = ('highlight','service')
    prepopulated_fields = {"codename": ('name',)}
    readonly_fields = ('path','lastCommandLine')
    fieldsets = (
        (None , {
            'fields': ('name', 'service', 'description', 'highlight')
        }),
        ('Base graph settings', {
            'classes': ('collapse',),
            'fields':  ('width','height','start','end')
        }),
        ('Options', {
            'classes': ('collapse',),
            'fields':  ('template',)
        }),
        ('Computed paths/slugs/cmdlines', {
            'classes': ('collapse',),
            'fields':  ('codename','path','lastCommandLine')
        }))
    inlines = [dataDefinitionInline,]
class rrdDataSourceAdmin(admin.ModelAdmin):
    list_display = ('name','rrdFile')
    list_filter = ('rrdFile',)
    search_fields = ('rrdFile',)
class lineDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name','data','color','width')
    list_filter = ('data',)
    readonly_fields = ('lastInstruction',)
class dataDefinitionAdmin(admin.ModelAdmin):
    list_display = ('data','graph','lastVname','lastInstruction')
    list_filter = ('graph',)
    readonly_fields = ('lastVname','lastInstruction')
    inlines = [lineDefinitionInline,]

admin.site.register(domain,domainAdmin)
admin.site.register(node,nodeAdmin)
admin.site.register(service,serviceAdmin)
admin.site.register(graph,graphAdmin)
admin.site.register(rrdFile,rrdFileAdmin)
admin.site.register(rrdDataSource,rrdDataSourceAdmin)
admin.site.register(lineDefinition,lineDefinitionAdmin)
admin.site.register(dataDefinition,dataDefinitionAdmin)

admin.site.register_view('graph', graphTaskView, 'Run graphing task')
admin.site.register_view('sync', syncTree, 'Lookup data sources and sync them with the database')
admin.site.register_view('parse', parseTree, 'Lookup data sources')