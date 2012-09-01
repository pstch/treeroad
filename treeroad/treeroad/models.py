from django.db import models
from django.template.defaultfilters import slugify
### ABSTRACT MODELS ###
# LEVEL 0 #

class Entity(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True) # Admin: No
    class Meta:
        abstract = True
class PathPart(models.Model):
    path_part = models.CharField(max_length=64, blank=True) # Admin: Yes (But some autofilling, according to how collectd handles path computing)
    # TODO: (MAYBE) some path functions
    class Meta:
        abstract = True
# LEVEL 1 #

class AutoEntity(Entity):
    debug_info = models.TextField(blank=True,null=True) # Admin: Yes (Auto objects should only be visible when DEBUG is True)
    class Meta:
        abstract = True
class UserEntity(Entity):
    last_modified_date = models.DateTimeField(auto_now=True) # Admin: No
    highlight = models.BooleanField(default=False) # Admin: Yes
    delete_notes = models.TextField(blank=True,null=True) # Admin: Yes (Shown as a warning, if not null, when object UserEntity is deleted)
    def __unicode__(self):
        if hasattr(self,'name'):
            return getattr(self,'name')
        else:
            return super(UserEntity, self).__str__()
    class Meta:
        abstract = True

# LEVEL 2 #

class UserDescriptedEntity(UserEntity):
    description = models.TextField(blank=True,null=True) # Admin: Yes
    class Meta:
        abstract = True

### MODELS ###
# LEVEL 0 #

class GenericService(AutoEntity): # Admin: If DEBUG
    name = models.CharField(max_length=64) # Admin: Yes (Parent only visible when DEBUG is True)
    def __unicode__(self):
        return self.name
class Node(UserDescriptedEntity,PathPart):
    name = models.CharField(max_length=64) # Admin: Yes
    slug_name = models.SlugField(max_length=64)
    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        self.path_part = self.slug_name
        super(Node, self).save( *args, **kwargs)

    def serviceCount(self):
        return self
    serviceCount.short_description = 'service count'
# LEVEL 1 #

class Service(UserDescriptedEntity,PathPart):
    name = models.CharField(max_length=64) # Admin: Yes
    slug_name = models.SlugField(max_length=64)
    node = models.ForeignKey(Node) # Admin: Yes
    generic_service = models.ForeignKey(GenericService,blank=True,null=True) # Admin: Yes (but filled automatically if empty). TODO: A text in custom widget should explain the get_or_create comportement in save().
    def graphCount(self):
        return self.service_set.objects.count()
    def save(self, *args, **kwargs):
        # This routine tries to get the object from GenericService.objects, and create one if it doesn't exist, based on self.name. This should ensure GenericService consistenty.
        if GenericService.objects.filter(name=self.name):
            _gs = GenericService.objects.get(name=self.name)
        else:
            _gs = GenericService(name=self.name)
        _gs.save()
        self.generic_service = _gs
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        self.path_part = self.slug_name
        return super(Service, self).save(*args, **kwargs) # Classic :)
    def delete(self, *args, **kwargs):
        if not self.generic_service.service_set.exists(name!=self.name): self.generic_service.delete()
        return super(Service, self).delete(*args, **kwargs)
            # TODO: Needs testing


# LEVEL 2 #

class Graph(UserDescriptedEntity,PathPart): # Admin: Yes, pathPart.path_part is RO
    name = models.CharField(max_length=64,blank=True) # Admin: Yes (but filled automatically if empty, using the graph->service->node hierarchy)
    slug_name = models.SlugField(max_length=64,blank=True)
    # TODO: Set prepopoulated_fields to at least slug_name,
    width = models.PositiveSmallIntegerField(default=700) # Admin: Yes
    height = models.PositiveSmallIntegerField(default=300) # Admin: Yes
    service = models.ForeignKey(Service) # Admin: Yes TODO: (VERY LATER) Widget should be customized in order to restrict DataSource choices in the DataDef inline, using some jQuery code.
    # TODO: Lots of graph parameters
    # TODO: Auto views
    def dataSourceCount(self):
        return self.graph_set.objects.count()
    def save(self, *args, **kwargs):
        super(Graph, self).save(*args, **kwargs)
        if not self.name:
            self.name = str(self.service.name) + ' graph'
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        self.path_part = str(self.id) + '-' + self.slug_name
        super(Graph, self).save(*args, **kwargs)


# LEVEL 2.1 #

class RRDFile(PathPart): # Admin: Yes
    service = models.ForeignKey(Service) # Admin: Yes
    pass

# LEVEL 2.2 #

class DataSource(models.Model): # Admin: Yes
    name = models.CharField(max_length=64) # Admin: Yes
    RRD_file = models.ForeignKey(RRDFile)

# LEVEL 3 #

class View(UserDescriptedEntity, PathPart): # Admin: Yes, pathPart.path_part is ROaph
    name = models.CharField(max_length=64, blank=True) # Admin: Yes (but filled automaticcally according to start and end)
    slug_name = models.SlugField(max_length=64, blank=True)
    graph = models.ForeignKey(Graph)
    # Set prepopulated_fields to at least slug_name
    start = models.CharField(max_length=64,default="now-1h") # Admin: Yes
    end = models.CharField(max_length=64,default="now") # Admin: Yes
    def save(self, *args, **kwargs):
        super(View, self).save(*args, **kwargs)
        if not self.name:
            self.name = str(self.start) + ' to ' + str(self.end)
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        self.path_part = str(self.id) + '-' + str(self.slug_name)
        super(View, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.graph.name + ' > ' + self.name
class ViewTemplate(UserDescriptedEntity): # Admin: Yes, pathPart.path_part is ROaph
    name = models.CharField(max_length=64, blank=True) # Admin: Yes (but filled automaticcally according to start and end)
    slug_name = models.SlugField(max_length=64, blank=True)
    # Set prepopulated_fields to at least slug_name
    start = models.CharField(max_length=64,default="now-1h") # Admin: Yes
    end = models.CharField(max_length=64,default="now") # Admin: Yes
    def save(self, *args, **kwargs):
        super(ViewTemplate, self).save(*args, **kwargs)
        if not self.name:
            self.name = str(self.start) + ' to ' + str(self.end)
        if not self.slug_name:
            self.slug_name = str(self.start) + '_to_' + str(self.end)
        super(ViewTemplate, self).save(*args, **kwargs)

# TODO: Schematize the whole LineDef -> DataDef -> Graph structure as the BACKEND should see it
class DataDef(models.Model): # Admin: Yes + as inline of Graph
    graph = models.ForeignKey(Graph) # Admin: Yes (not in inline)
    data_source = models.ForeignKey(DataSource) # Admin: Yes (in the graph inline, altered by the javascript code in graph.service widget)
    def save(self, *args, **kwargs):
        super(DataDef, self).save(*args, **kwargs)
        if not self.data_def_set:
            n = LineDef()
            n.data_def = self

            import random
            colors = (r, g, b)
            for c in colors:
                c = hex(random.randrange(0,255))
            n.color = '#' + str(r) + str(g) + str(b)

            n.save()

# LEVEL 4 #

class LineDef(models.Model): # Admin: Yes
    data_def = models.ForeignKey(DataDef) # Admin: Yes
    color = models.CharField(max_length=16,default='#000000') # Admin: Yes (This can be either a HTML color code or a named color that will be converted in the graph task)
    width = models.PositiveSmallIntegerField(default=0.1) # Admin: Yes