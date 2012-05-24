from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from colors import fields


# Create your models here.
class entity(models.Model):
    name = models.CharField(max_length=64,blank=True)
    description = models.TextField(blank=True, null=True)
    highlight = models.BooleanField(default=False)
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
    def get_absolute_url(self):
        return reverse('nodeDetail', args = [self.id])
class service(entity,pathLevel):
    node = models.ForeignKey(node,related_name="services")
    def get_absolute_url(self):
        return reverse('serviceDetail', args = [self.id])
class rrdFile(pathLevel):
    service = models.ForeignKey(service,related_name="rrdfiles")
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
    codename = models.SlugField(blank=True)
    service = models.ForeignKey(service,related_name="graphs")
    start = models.CharField(max_length=64,default="now-2h")
    end = models.CharField(max_length=64,default="now")
    width = models.PositiveSmallIntegerField(default=640)
    height = models.PositiveSmallIntegerField(default=480)
    path = models.CharField(max_length=64, blank=True, null=False)
    active = models.BooleanField(default=True)
    lastCommandLine = models.CharField(max_length=64, blank=True, null=False)
    def get_absolute_url(self):
        return reverse('graphDetail', args = [self.id])
    def save(self, *args, **kwargs):
        super(graph, self).save(*args,**kwargs)
        if not self.name:
            self.name = str(self.service.name).capitalize()
            self.codename = slugify(self.name)
        self.path = '/' + self.service.pathPart + '/' + str(self.codename) + '-' + str(self.id) +  '.png'
        super(graph, self).save(*args,**kwargs)
class dataDefinition(models.Model):
    graph = models.ForeignKey(graph, related_name="defs")
    data = models.ForeignKey(rrdDataSource)
    cf = models.CharField(max_length=64,default='AVERAGE')
    lastVname = models.CharField(max_length=64)
    lastInstruction = models.CharField(max_length=128)
    def lines(self):
        return self.defs.count()
    def vname(self):
        return self.data.name + '_' + str(self.id)
    def defInstruction(self):
        return 'DEF:' + self.vname() + '=' + self.data.rrdFile.path() + ':' + self.data.name + ':' + self.cf
    def save(self, *args, **kwargs):
        super(dataDefinition, self).save(*args, **kwargs) # Call the "real" save() method. FIXME: This is the wrong way
        if self.defs.count() == 0:
            _name = str(self.data.rrdFile.pathPart).split('.')[0] + '/' + self.data.name
            line = lineDefinition(name=_name,data=self)
            line.save()
        self.lastVname = self.vname()
        self.lastInstruction = self.defInstruction()
        super(dataDefinition, self).save(*args, **kwargs) # Call the "real" save() method. FIXME: This is the wrong way
    def __unicode__(self):
        return str(self.data)
class lineDefinition(models.Model):
    name = models.CharField(max_length=64)
    width = models.DecimalField(default=0.5, max_digits=2, decimal_places=1)
    data = models.ForeignKey(dataDefinition, related_name="defs") # Restricted only to related objects (datasource.rrdFile = graph.rrdFile)
    color = fields.ColorField(default='#000000')
    lastInstruction = models.CharField(max_length=128,blank=True)
    def defInstruction(self):
        return 'LINE' + str(self.width) + ':' + self.data.vname() + self.color + ':"' + self.name + '"'
    def save(self, *args, **kwargs):
        super(lineDefinition, self).save(*args, **kwargs) # Call the "real" save() method. FIXME: This is the wrong way
        self.lastInstruction = self.defInstruction()
        super(lineDefinition, self).save(*args, **kwargs) # Call the "real" save() method.
