from django.db import models

### ABSTRACT MODELS ###
# LEVEL 0 #

class Entity(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True) # Admin: No
    class Meta:
        abstract = True
class PathPart(models.Model):
    path_part = models.CharField(max_length=64, blank=True) # Admin: Yes (But some autofilling, according to how collectd handles path computing)
    # TODO: (MAYBE) some path functions

# LEVEL 1 #

class AutoEntity(Entity):
    debug_info = models.TextField(blank=True,null=True) # Admin: Yes (Auto objects should only be visible when DEBUG is True)
    class Meta:
        abstract = True
class UserEntity(Entity):
    last_modified_date = models.DateTimeField(auto_now=True) # Admin: No
    highlight = models.BooleanField(default=False) # Admin: Yes
    delete_notes = models.TextField(blank=True,null=True) # Admin: Yes (Shown as a warning, if not null, when object UserEntity is deleted)
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
class Node(UserDescriptedEntity,PathPart):
    name = models.CharField(max_length=64) # Admin: Yes

# LEVEL 1 #

class Service(UserDescriptedEntity,PathPart):
    name = models.CharField(max_length=64) # Admin: Yes
    node = models.ForeignKey(Node) # Admin: Yes
    generic_service = models.ForeignKey(GenericService,blank=True) # Admin: Yes (but filled automatically if empty). TODO: A text in custom widget should explain the get_or_create comportement in save().
    def save(self, *args, **kwargs):
        # This routine tries to get the object from GenericService.objects, and create one if it doesn't exist, based on self.name. This should ensure GenericService consistenty.
        # TODO: When Service is deleted, if the parent GenericService has no momre childs, it should be deleted too.
        if not self.generic_service: self.generic_service = GenericService.objects.get_or_create(name=self.name)
        return self.save(*args, **kwargs) # Classic :)

# LEVEL 2 #

class Graph(UserDescriptedEntity): # Admin: Yes
    name = models.CharField(max_length=64,blank=True) # Admin: Yes (but filled automatically if empty, using the graph->service->node hierarchy) TODO: Fill name
    width = models.PositiveSmallIntegerField(default=700) # Admin: Yes
    height = models.PositiveSmallIntegerField(default=300) # Admin: Yes
    png_path = models.SlugField(max_length=64,blank=True) # Admin: Yes, RO (filled automatically) TODO: Computing png_path
    # FIXME: I try to use a SlugField for png_path, THAT MAY CHANGE.
    # TODO: If SlugField for png_path, set prepopulated_fields in admin.py
    service = models.ForeignKey(Service) # Admin: Yes TODO: (VERY LATER) Widget should be customized in order to restrict DataSource choices in the DataDef inline, using some jQuery code.
    # TODO: Lots of graph parameters
    # TODO: Auto views
# LEVEL 2.1 #

class RRDFile(PathPart): # Admin: Yes
    service = models.ForeignKey(Service) # Admin: Yes
    pass

# LEVEL 2.2 #

class DataSource(models.Model): # Admin: Yes
    name = models.CharField(max_length=64) # Admin: Yes
    RRD_file = models.ForeignKey(RRDFile)

# LEVEL 3 #

# TODO: Try to imagine a template system for the views, better than the DEFAULT_VIEWS approach
class View(UserDescriptedEntity): # Admin: Yes
    name = models.CharField(max_length=64, blank=True) # Admin: Yes (but filled automaticcally according to start and end) TODO: Compute name
    start = models.CharField(max_length=64,default="now-1h") # Admin: Yes
    end = models.CharField(max_length=64,default="now") # Admin: Yes

# TODO: Schematize the whole LineDef -> DataDef -> Graph structure as the BACKEND should see it
class DataDef(models.Model): # Admin: Yes + as inline of Graph
    graph = models.ForeignKey(Graph) # Admin: Yes (not in inline)
    data_source = models.ForeignKey(DataSource) # Admin: Yes (in the graph inline, altered by the javascript code in graph.service widget)
    # TODO: Auto lines

# LEVEL 4 #

class LineDef(models.Model): # Admin: Yes
    data_def = models.ForeignKey(DataDef) # Admin: Yes
    color = models.CharField(max_length=16) # Admin: Yes (This can be either a HTML color code or a named color that will be converted in the graph task)
    width = models.PositiveSmallIntegerField(default=0.1) # Admin: Yes