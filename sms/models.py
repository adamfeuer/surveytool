from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django_extensions.db.fields.encrypted import EncryptedCharField

class Setting(models.Model):
   name = models.CharField(max_length=200)
   value = models.CharField(max_length=500)
   description = models.CharField(max_length=500)
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
    
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
   guard_time_minutes = models.IntegerField()
   synchronize_messages = models.BooleanField()
   day_start_time = models.TimeField()
   day_end_time = models.TimeField()
   intake_survey_url = models.CharField(max_length=500, default="")
   intake_survey_query_string_parameter = models.CharField(max_length=100, default="")
   members = models.ManyToManyField(User, through='Membership') 
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   
   def __unicode__(self):
      return self.name

class Membership(models.Model):
   user = models.ForeignKey(User)
   project = models.ForeignKey(Project)
   messages_generated = models.BooleanField(default=False)
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   
   def __unicode__(self):
      return "'%s': '%s'" % (self.user, self.project)

class Message(models.Model):
   project = models.ForeignKey(Project)
   user_id = EncryptedCharField(max_length=100)
   identifier = EncryptedCharField(max_length=100)
   phone_number = EncryptedCharField(max_length=100)
   email = EncryptedCharField(max_length=200)
   message = EncryptedCharField(max_length=300)
   send_at = models.DateTimeField()
   sent = models.BooleanField()
   sent_status = models.BooleanField()
   sent_error_message = models.CharField(max_length=200)
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   
   def __unicode__(self):
      return "'%s': '%s %s'" % (self.project, self.phone_number, self.message)
   
class UserDetail(models.Model):
   user = models.ForeignKey(User)
   phone_number = models.CharField(max_length=100)
   smartphone = models.BooleanField()
   no_messages = models.BooleanField()
   intake_survey_identifier = EncryptedCharField(max_length=100, default="")
   created = CreationDateTimeField()
   modified = ModificationDateTimeField()
   
   def __unicode__(self):
      return "'%s': '%s'" % (self.user, self.phone_number)

