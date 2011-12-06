from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

class Setting(models.Model):
   name = models.CharField(max_length=200)
   value = models.CharField(max_length=500)
   description = models.CharField(max_length=500)
   created = CreationDateTimeField()
   modifed = ModificationDateTimeField()
    
   def __unicode__(self):
      return self.name
   
class Project(models.Model):
   name = models.CharField(max_length=200)
   survey_url = models.CharField(max_length=200)
   smartphone_message = models.CharField(max_length=160)
   text_message = models.CharField(max_length=160)
   start_datetime = models.DateTimeField()
   end_datetime = models.DateTimeField()
   messages_per_day = models.IntegerField()
   day_start_time = models.TimeField()
   day_end_time = models.TimeField()
   members = models.ManyToManyField(User, through='Membership') 
   created = CreationDateTimeField()
   modifed = ModificationDateTimeField()
   
   def __unicode__(self):
      return self.name

class Membership(models.Model):
   user = models.ForeignKey(User)
   project = models.ForeignKey(Project)
   created = CreationDateTimeField()
   modifed = ModificationDateTimeField()
   
   def __unicode__(self):
      return "'%s': '%s'" % (self.user, self.project)
