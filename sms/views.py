import datetime, time

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test 
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.models import User

from forms import SmsForm, ProjectForm, SurveysForm, MessageForm
from models import Project, Membership, Message
from smsutil import SmsSender

DATETIME_FORMAT="%m/%d/%Y %H:%M"
TIME_FORMAT="%H:%M"

@login_required
@user_passes_test(lambda u: u.is_staff)
def sms(request):
   if request.method == 'POST': 
      form = SmsForm(request.POST)
      if form.is_valid():
         result = SmsSender().send(form.cleaned_data['message'], form.cleaned_data["phone_number"])
         print result.status, result.message
         return HttpResponseRedirect('/') 
   else:
      form = SmsForm() 

   return render_to_response('sms/sms.html',
                             {'form': form },
                             context_instance=RequestContext(request))
       
@login_required
@user_passes_test(lambda u: u.is_staff)
def new_project(request):
   if request.method == 'POST': 
      form = ProjectForm(request.POST) 
      if form.is_valid(): 
         newProject = Project()
         save_project(newProject, form)
         return HttpResponseRedirect('/sms/projects')
   else:
      form = ProjectForm(initial={'start_datetime':formatted_datetime(),
                                  'end_datetime' : formatted_datetime(),
                                  'messages_per_day': 1})
   return render_to_response('sms/newproject.html',
                             {'form': form },
                             context_instance=RequestContext(request))
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def projects(request):
   projects = Project.objects.all().order_by('name')
   return render_to_response('sms/projects.html',
                             { 'projects' : projects },
                             context_instance=RequestContext(request))
    

@login_required
@user_passes_test(lambda u: u.is_staff)
def project(request, project_id):
   p = get_object_or_404(Project, pk=project_id)
   form = ProjectForm({ 'name' : p.name,
                        'id' : p.id,
                        'survey_url' : p.survey_url,
                        'smartphone_message' : p.smartphone_message,
                        'text_message' : p.text_message,
                        'start_datetime' : format_datetime(p.start_datetime),
                        'end_datetime' : format_datetime(p.end_datetime),
                        'messages_per_day' : p.messages_per_day,
                        'day_start_time' : format_time(p.day_start_time),
                        'day_end_time' : format_time(p.day_end_time)
                        })
   return render_to_response('sms/project.html',
                             {'form': form },
                             context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def save_project(request):
   if request.method == 'POST': 
      form = ProjectForm(request.POST) 
      if form.is_valid(): 
         newProject = Project.objects.get(pk=form.cleaned_data['id'])
         save_project(newProject, form)
         return HttpResponseRedirect('/sms/projects') 
   else:
       form = ProjectForm()

   return render_to_response('sms/project.html',
                             {'form': form },
                             context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_project(request, project_id):
   p = get_object_or_404(Project, pk=project_id)
   p.delete()
   return HttpResponseRedirect('/sms/projects')


@login_required
@user_passes_test(lambda u: u.is_staff)
def surveys_select(request, username):
   user = get_object_or_404(User, username__iexact=username)
   if request.method == 'POST': 
      form = SurveysForm(request.POST) 
      if form.is_valid():
         save_memberships(user, project, form)
         return HttpResponseRedirect('/accounts/%s/' % username) 
   else:
      survey_queryset = get_surveys(user)
      print survey_queryset
      initial_dict={'surveys' : survey_queryset}
      form = SurveysForm(initial=initial_dict)  
     
   return render_to_response('userena/survey_form.html',
                             {'form': form },
                             context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def new_message(request):
   if request.method == 'POST': 
      form = MessageForm(request.POST) 
      if form.is_valid(): 
         newMessage = Message()
         save_message(newMessage, form)
         return HttpResponseRedirect('/') #/sms/messages
   else:
      form = MessageForm()
   return render_to_response('sms/newmessage.html',
                             {'form': form },
                             context_instance=RequestContext(request))
    
def get_surveys(user):
   memberships = Membership.objects.filter(user = user.id)
   return [membership.project for membership in memberships]

def save_memberships(user, project, form):
   print "Form data:"
   print "%d: %s %s" % (user.id, user.first_name, user.last_name)
   for project in form.cleaned_data['surveys']:
      print project.id, project.name
   print "Deleting existing table data:"
   memberships = Membership.objects.filter(user = user.id)
   for membership in memberships:
      print membership
      membership.delete()
   print "Saving form data:"
   for project in form.cleaned_data['surveys']:
      membership = Membership(user = user, project = project)
      print membership
      membership.save()
   return

def save_project(project, form):
   project.name = form.cleaned_data['name']
   project.survey_url = form.cleaned_data['survey_url']
   project.smartphone_message = form.cleaned_data['smartphone_message']
   project.text_message = form.cleaned_data['text_message']            
   project.start_datetime = clean_datetime(form.cleaned_data['start_datetime'])
   project.end_datetime = clean_datetime(form.cleaned_data['end_datetime'])
   project.messages_per_day = form.cleaned_data['messages_per_day']
   project.day_start_time = clean_time(form.cleaned_data['day_start_time'])
   project.day_end_time = clean_time(form.cleaned_data['day_end_time'])
   project.save()
   return

def save_message(message, form):
   message.project = form.cleaned_data['project']
   message.user_id = form.cleaned_data['user_id']
   message.phone_number = form.cleaned_data['phone_number']
   message.email = form.cleaned_data['email']
   message.message = form.cleaned_data['message']
   message.send_at = clean_datetime(form.cleaned_data['send_at'])
   message.sent = clean_datetime(form.cleaned_data['sent'])
   message.sent_status = form.cleaned_data['sent_status']
   message.sent_error_message = form.cleaned_data['sent_error_message']
   message.save()
   return

def clean_datetime(datetime_obj):
   if (datetime_obj is None):
      return datetime.datetime.now()
   return datetime_obj
      
def clean_time(time_obj):
   if (time_obj is None):
      now = datetime.datetime.now()
      return datetime.time(now.hour, now.minute)
   return time_obj
      
def formatted_datetime():
   return format_datetime(datetime.datetime.now())

def format_datetime(datetime_obj):
   return datetime_obj.strftime(DATETIME_FORMAT)

def format_time(datetime_obj):
   return datetime_obj.strftime(TIME_FORMAT)


