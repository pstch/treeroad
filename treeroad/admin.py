from django.contrib import admin
from treeroad.models import domain, node, service, rrdFile, rrdDataSource, graph, dataDefinition, lineDefinition

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
    list_display = ('pathPart','service','last_update')
    list_filter = ('service',)
    date_hierarchy = ('last_update')
    inlines = [rrdDataSourceInline,]
class graphAdmin(admin.ModelAdmin):
    list_display = ('name','service','description','highlight')
    list_filter = ('highlight','service')
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
            'fields':  ('template', 'rrdfiles')
        }),
    )
class rrdDataSourceAdmin(admin.ModelAdmin):
    list_display = ('name','rrdFile','description','highlight')
    list_filter = ('highlight','rrdFile')
    search_fields = ('rrdFile',)
class lineDefinitionAdmin(admin.ModelAdmin):
    pass
class dataDefinitionAdmin(admin.ModelAdmin):
    pass
admin.site.register(domain,domainAdmin)
admin.site.register(node,nodeAdmin)
admin.site.register(service,serviceAdmin)
admin.site.register(graph,graphAdmin)
admin.site.register(rrdFile,rrdFileAdmin)
admin.site.register(rrdDataSource,rrdDataSourceAdmin)
admin.site.register(lineDefinition,lineDefinitionAdmin)
admin.site.register(dataDefinition,dataDefinitionAdmin)
