from django.db import models

# Create your models here.
class entity(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    highlight = models.BooleanField(default=False)
    template = models.BooleanField(default=False) # Complex shit that I need to think about
    def __unicode__(self):
        return self.name
    class Meta:
        abstract = True
class pathLevel(models.Model):
    # Because the .rrd path is calculated based on model data, the .png file path will be consistent and coherent, at least as much as the .rrd files.
    # It should be expected that most of the path will be the same, expect of course for the filename extension
    pathPart = models.CharField(max_length=64)
    class Meta:
        abstract = True
    
class domain(entity):
    pass

class node(entity,pathLevel):
    domain = models.ForeignKey(domain, blank=True, null=True)
    pass
class service(entity,pathLevel):
    node = models.ForeignKey(node)
class rrdFile(pathLevel):
    service = models.ForeignKey(service)
    last_update = models.DateTimeField(blank=True, null=True)
    def __unicode__(self):
        return './' + self.service.node.pathPart + '/' + self.service.pathPart + '/' + self.pathPart
class rrdDataSource(entity):
    rrdFile = models.ForeignKey(rrdFile)
class graph(entity):
    service = models.ForeignKey(service)
    rrdfiles = models.ManyToManyField(rrdFile,blank=True,null=True) # optional. Used to filter the list of rrdDataSources in the dataDef admin form.
    start = models.CharField(max_length=64,default="now-2h")
    end = models.CharField(max_length=64,default="now")
    width = models.PositiveSmallIntegerField(default=640)
    height = models.PositiveSmallIntegerField(default=480)
class dataDefinition(entity):
    graph = models.ForeignKey(graph)
    data = models.ForeignKey(rrdDataSource)
    cf = models.CharField(max_length=64)
class lineDefinition(entity):
    width = models.PositiveSmallIntegerField(default=1)
    data = models.ForeignKey(dataDefinition) # Restricted only to related objects (datasource.rrdFile = graph.rrdFile)
    color = models.CharField(max_length=7, default='#000000')