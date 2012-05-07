from django.db import models
from django.conf import settings

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
    lastUpdate = models.DateTimeField(blank=True, null=True)
    def path(self):
        return './' + self.service.node.pathPart + '/' + self.service.pathPart + '/' + self.pathPart
    def __unicode__(self):
        return self.path()
class rrdDataSource(models.Model):
    name = models.CharField(max_length=64)
    rrdFile = models.ForeignKey(rrdFile)
    def __unicode__(self):
        return './' + self.rrdFile.service.node.pathPart + './' + self.rrdFile.service.pathPart + '/' + self.rrdFile.pathPart + '/' + self.name
class graph(entity):
    codename = models.SlugField()
    service = models.ForeignKey(service)
    start = models.CharField(max_length=64,default="now-2h")
    end = models.CharField(max_length=64,default="now")
    width = models.PositiveSmallIntegerField(default=640)
    height = models.PositiveSmallIntegerField(default=480)
    path = models.CharField(max_length=64, blank=True, null=False)
    active = models.BooleanField(default=True)
    lastCommandLine = models.CharField(max_length=64, blank=True, null=False)
    def save(self, *args, **kwargs):
        super(graph, self).save(*args,**kwargs)
        self.path = settings.PNGROOT + '/' + self.service.pathPart + '/' + str(self.codename) + '-' + str(self.id) +  '.png'
        super(graph, self).save(*args,**kwargs)
class dataDefinition(models.Model):
    graph = models.ForeignKey(graph, related_name="defs")
    data = models.ForeignKey(rrdDataSource)
    cf = models.CharField(max_length=64,default='AVERAGE')
    lastVname = models.CharField(max_length=64)
    lastInstruction = models.CharField(max_length=128)
    def vname(self):
        return self.data.name + '_' + str(self.id)
    def defInstruction(self):
        return 'DEF:' + self.vname() + '=' + self.data.rrdFile.path() + ':' + self.data.name + ':' + self.cf
    def save(self, *args, **kwargs):
        super(dataDefinition, self).save(*args, **kwargs) # Call the "real" save() method.
        self.lastVname = self.vname()
        self.lastInstruction = self.defInstruction()
        super(dataDefinition, self).save(*args, **kwargs) # Call the "real" save() method.
class lineDefinition(models.Model):
    name = models.CharField(max_length=64)
    width = models.PositiveSmallIntegerField(default=1)
    data = models.ForeignKey(dataDefinition, related_name="defs") # Restricted only to related objects (datasource.rrdFile = graph.rrdFile)
    color = models.CharField(max_length=7, default='#000000')
    lastInstruction = models.CharField(max_length=128)
    def defInstruction(self):
        return 'LINE' + str(self.id) + ':' + self.data.vname() + self.color + ':"' + self.name + '"'
    def save(self, *args, **kwargs):
        super(lineDefinition, self).save(*args, **kwargs) # Call the "real" save() method.
        self.lastInstruction = self.defInstruction()
        super(lineDefinition, self).save(*args, **kwargs) # Call the "real" save() method.
