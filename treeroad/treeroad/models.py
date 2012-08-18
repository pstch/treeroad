from django.db import models

class Entity(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class UserEntity(Entity):
    last_modified_date = models.DateTimeField(auto_now=True)
    highlight = models.BooleanField(default=False)
    delete_notes = models.TextField(blank=True,null=True)
    class Meta:
        abstract = True

class UserDescriptedEntity(UserEntity):
    description = models.TextField(blank=True,null=True)
    class Meta:
        abtract = True