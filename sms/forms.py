from django import forms
from django.contrib.auth.models import User
from sms.models import Project, Membership

def get_datetime_field():
   return StrippingDateTimeField(required=False, widget=forms.TextInput(attrs={'class':'jquery-datetime'}))
    
def get_time_field():
   return StrippingTimeField(required=False, widget=forms.TimeInput(format="%H:%M", attrs={'class':'jquery-time'}))

class StrippingTimeField(forms.TimeField):
   def to_python(self, value):
      return super(StrippingTimeField, self).to_python(value.strip())      
    
class StrippingDateTimeField(forms.DateTimeField):
   def to_python(self, value):
      return super(StrippingDateTimeField, self).to_python(value.strip())      
    
class ProjectModelMultipleChoiceField(forms.ModelMultipleChoiceField):
   def label_from_instance(self, project_obj):
      return "%s" % project_obj.name

class ProjectModelChoiceField(forms.ModelChoiceField):
   def label_from_instance(self, project_obj):
      return "%s" % project_obj.name

class SmsForm(forms.Form):
   message = forms.CharField(max_length=160,widget=forms.Textarea)
   phone_number = forms.CharField()

class ProjectForm(forms.Form):
   id = forms.IntegerField(widget=forms.HiddenInput, required=False)
   name = forms.CharField(max_length=200, required=True)
   survey_url = forms.CharField(max_length=200, required=False)
   smartphone_message = forms.CharField(max_length=160,widget=forms.Textarea, required=False)
   text_message = forms.CharField(max_length=160,widget=forms.Textarea, required=False, label='Non-smartphone message')
   start_datetime = get_datetime_field()
   end_datetime = get_datetime_field()
   messages_per_day = forms.IntegerField(required=True, min_value=0, max_value=9999)
   guard_time_minutes = forms.IntegerField(min_value=0, max_value=1440)
   synchronize_messages = forms.BooleanField(required=False)
   day_start_time = get_time_field()
   day_end_time = get_time_field()


class SurveysForm(forms.Form):
   surveys = ProjectModelMultipleChoiceField(queryset=Project.objects.all(), required=False)
   user_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
   phone_number = forms.CharField(max_length=100, required=False, label='Phone number starting with area code')
   smartphone = forms.BooleanField(required=False,label='This phone is a smartphone')
   no_messages = forms.BooleanField(required=False, label='Do not send me any text messages or emails')

class MessageForm(forms.Form):
   id = forms.IntegerField(widget=forms.HiddenInput, required=False)
   project = ProjectModelChoiceField(queryset=Project.objects.all())
   user_id = forms.CharField(max_length=100, required=False)
   phone_number = forms.CharField(max_length=100, required=False)
   email = forms.EmailField(required=False)
   message = forms.CharField(max_length=160, widget=forms.Textarea(attrs={'rows':2, 'cols':20}), required=False)
   send_at = get_datetime_field()
   sent = forms.BooleanField(required=False)
   sent_status = forms.BooleanField(required=False)
   sent_error_message = forms.CharField(max_length=200, required=False)
