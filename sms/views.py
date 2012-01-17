import datetime, logging, time, base64, string, csv

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test 
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.simple import direct_to_template
from django.conf import settings

from userena.decorators import secure_required

from forms import SmsForm, ProjectForm, SurveysForm, MessageForm, SignupFormOnePage, SignupUrlForm
from models import Project, Membership, Message, UserDetail
from SmsSender import SmsSender
from MessageGenerator import MessageGenerator

logger = logging.getLogger(__name__)

DATETIME_FORMAT="%m/%d/%Y %H:%M"
TIME_FORMAT="%H:%M"

DEFAULT_MESSAGES_PER_DAY = 7
DEFAULT_GUARD_TIME_MINUTES = 15
DEFAULT_DAY_START_TIME = "09:00"
DEFAULT_DAY_END_TIME = "21:00"


@login_required
@user_passes_test(lambda u: u.is_staff)
def sms(request):
   if request.method == 'POST': 
      form = SmsForm(request.POST)
      if form.is_valid():
         result = SmsSender().send(form.cleaned_data["phone_number"], form.cleaned_data['message'])
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
         save_project_from_form(newProject, form)
         return HttpResponseRedirect('/sms/projects')
   else:
      form = ProjectForm(initial={'start_datetime':formatted_datetime(),
                                  'end_datetime' : formatted_datetime(),
                                  'messages_per_day': DEFAULT_MESSAGES_PER_DAY,
                                  'guard_time_minutes': DEFAULT_GUARD_TIME_MINUTES,
                                  'day_start_time' : formatted_time(DEFAULT_DAY_START_TIME),
                                  'day_end_time' : formatted_time(DEFAULT_DAY_END_TIME) })
   return render_to_response('sms/new_project.html',
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
def edit_project(request, project_id):
   project = get_object_or_404(Project, pk=project_id)
   form = ProjectForm({ 'name' : project.name,
                        'id' : project.id,
                        'survey_url' : project.survey_url,
                        'smartphone_message' : project.smartphone_message,
                        'text_message' : project.text_message,
                        'start_datetime' : format_datetime(project.start_datetime),
                        'end_datetime' : format_datetime(project.end_datetime),
                        'messages_per_day' : project.messages_per_day,
                        'guard_time_minutes' : project.guard_time_minutes,
                        'synchronize_messages' : project.synchronize_messages,
                        'day_start_time' : format_time(project.day_start_time),
                        'day_end_time' : format_time(project.day_end_time),
                        'intake_survey_url' : project.intake_survey_url,
                        'intake_survey_query_string_parameter' : project.intake_survey_query_string_parameter,
                        })
   return render_to_response('sms/edit_project.html',
                             {'form': form,
                              'project' : project},
                             context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def save_project(request):
   if request.method == 'POST': 
      form = ProjectForm(request.POST) 
      if form.is_valid(): 
         newProject = Project.objects.get(pk=form.cleaned_data['id'])
         save_project_from_form(newProject, form)
         return HttpResponseRedirect('/sms/projects') 
   else:
       form = ProjectForm()

   return render_to_response('sms/edit_project.html',
                             {'form': form },
                             context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_project(request, project_id):
   p = get_object_or_404(Project, pk=project_id)
   p.delete()
   return HttpResponseRedirect('/sms/projects')


@login_required
def surveys_select(request, username):
   user = get_object_or_404(User, username__iexact=username)
   if request.method == 'POST': 
      form = SurveysForm(request.POST) 
      if form.is_valid():
         save_memberships_from_form(user, form)
         return HttpResponseRedirect('/accounts/%s/' % username) 
   else:
      survey_queryset = get_surveys(user)
      user_details = get_user_details(user)
      initial_dict={'surveys' : survey_queryset,
                    'user': user_details.user.id,
                    'phone_number': user_details.phone_number,
                    'smartphone': user_details.smartphone,
                    'no_messages': user_details.no_messages}
      form = SurveysForm(initial=initial_dict)  
     
   return render_to_response('userena/survey_form.html',
                             {'form': form },
                             context_instance=RequestContext(request))

@secure_required
def one_page_signup(request, surveys, signup_form=SignupFormOnePage,
           template_name='userena/signup.html'):
   form = SignupFormOnePage(initial = {'smartphone' : True })
   projects = get_projects_from_surveys_param(surveys)
   if len(projects) > 0:
      if request.method == 'POST':
         form = signup_form(request.POST, request.FILES)
         if form.is_valid():
            user = form.save()
            save_memberships_from_surveys_param(user, surveys)
            generate_messages_for_user(user)
            redirect_to = get_intake_survey_url(user, surveys)
            # A new signed user should logout the old one.
            if request.user.is_authenticated():
               logout(request)
            return redirect(redirect_to)
   else:
      return redirect("/")

   extra_context = dict()
   extra_context['form'] = form
   extra_context['has_intake_survey'] = has_intake_survey(surveys)
   return direct_to_template(request,
                             template_name,
                             extra_context=extra_context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def new_message(request):
   if request.method == 'POST': 
      form = MessageForm(request.POST) 
      if form.is_valid(): 
         newMessage = Message()
         save_message_from_form(newMessage, form)
         return HttpResponseRedirect('/sms/messages')
   else:
      form = MessageForm()
   return render_to_response('sms/new_message.html',
                             {'form': form },
                             context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def messages(request):
   sms_messages = Message.objects.all().order_by('send_at')
   return render_to_response('sms/messages.html',
                             { 'sms_messages' : sms_messages },
                             context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_message(request, message_id):
   m = get_object_or_404(Message, pk=message_id)
   form = MessageForm({ 'id' : m.id,
                        'project' : m.project,
                        'user_id' : m.user_id,
                        'phone_number' : m.phone_number,
                        'email' : m.email,
                        'message' : m.message,
                        'send_at' : format_datetime(m.send_at),
                        'sent' : m.sent,
                        'sent_status' : m.sent_status,
                        'sent_error_message' : m.sent_error_message,
                        })
   return render_to_response('sms/edit_message.html',
                             {'form': form },
                             context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_message(request, message_id):
   m = get_object_or_404(Message, pk=message_id)
   m.delete()
   return HttpResponseRedirect('/sms/messages')
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def save_message(request):
   if request.method == 'POST': 
      form = MessageForm(request.POST) 
      if form.is_valid(): 
         newMessage = Message.objects.get(pk=form.cleaned_data['id'])
         save_message_from_form(newMessage, form)
         return HttpResponseRedirect('/sms/messages') 
   else:
       form = MessageForm()

   return render_to_response('sms/edit_message.html',
                             {'form': form },
                             context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def generate_messages(request, project_id):
   messageGenerator = MessageGenerator()
   project = Project.objects.get(pk = project_id)
   Message.objects.filter(project = project_id).delete()
   memberships = Membership.objects.filter(project = project_id)
   for membership in memberships:
      messageGenerator.generateMessages(membership.user, membership.project)
   sms_messages = Message.objects.all().filter(project = project_id).order_by('send_at')
   return render_to_response('sms/messages.html',
                             { 'sms_messages' : sms_messages },
                             context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def messages_for_project(request, project_id):
   project = Project.objects.get(pk = project_id)
   sms_messages = Message.objects.all().filter(project = project_id).order_by('send_at')
   return render_to_response('sms/messages.html',
                             { 'sms_messages' : sms_messages },
                             context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_messages_for_project(request, project_id):
   project = Project.objects.get(pk = project_id)
   Message.objects.filter(project = project_id).delete()
   sms_messages = Message.objects.all().filter(project = project_id).order_by('send_at')
   return render_to_response('sms/messages.html',
                             { 'sms_messages' : sms_messages },
                             context_instance=RequestContext(request))


@login_required
@user_passes_test(lambda u: u.is_staff)
def project_messages_csv(request, project_id):
    project = Project.objects.get(pk = project_id)
    filename = "messages-%s" % project.name
    filename = filename.replace(' ', '-').lower()
    csv_rows = get_messages_for_project_csv_rows(project_id)
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    writer = csv.writer(response)
    for csv_row in csv_rows:
       writer.writerow(csv_row)
    return response


@login_required
@user_passes_test(lambda u: u.is_staff)
def make_signup_url(request):
   if request.method == 'POST': 
      form = SignupUrlForm(request.POST) 
      if form.is_valid():
         encoded_url = get_signup_url(form)
         return render_to_response('sms/signup_url.html',
                                   {'form': form,
                                    'signup_url': encoded_url },
                                   context_instance=RequestContext(request))
   else:
      initial_dict={}
      form = SignupUrlForm(initial=initial_dict)       
   return render_to_response('sms/signup_url.html',
                             {'form': form },
                             context_instance=RequestContext(request))

# Utility functions

def get_signup_url(form):
   encoded_url = None
   signup_code=""
   projects = form.cleaned_data['surveys']
   if len(projects) > 0:
      for project in projects:
         signup_code += "%s," % project.id
      signup_code = signup_code[:-1]
      encoded_url = settings.BASE_URL + "/signup/%s" % base64.b16encode(signup_code)
   return encoded_url

def generate_messages_for_user(user):
   messageGenerator = MessageGenerator()
   memberships = Membership.objects.filter(user=user)
   for membership in memberships:
      if (membership.messages_generated is False):
         messageGenerator.generateMessages(membership.user, membership.project)
         membership.messages_generated = True
         membership.save()

def get_messages_for_project_csv_rows(project_id):
   project = Project.objects.get(pk = project_id)
   sms_messages = Message.objects.filter(project = project_id).order_by('send_at')
   csv_rows = []
   csv_rows.append(['Message ID', 'Project ID', 'Project Name', 'User ID', 'User First Name', 'User Last Name', 'User Phone Number', 'Message Identifier', 'Send At', 'Sent Status'])
   for sms_message in sms_messages:
      user = User.objects.get(pk = sms_message.user_id)
      csv_row = []
      csv_row.append(sms_message.id)
      csv_row.append(sms_message.project.id)
      csv_row.append(sms_message.project.name)
      csv_row.append(sms_message.user_id)
      csv_row.append(user.first_name)
      csv_row.append(user.last_name)
      csv_row.append(sms_message.phone_number)
      csv_row.append(sms_message.identifier)
      csv_row.append(sms_message.send_at)
      csv_row.append(sms_message.sent_status)
      print csv_row
      csv_rows.append(csv_row)
   return csv_rows

def get_surveys(user):
   memberships = Membership.objects.filter(user = user.id)
   return [membership.project for membership in memberships]

def get_user_details(user):
   user_details_list = UserDetail.objects.filter(user = user.id)
   if len(user_details_list) == 0:
      user_details = UserDetail()
      user_details.user = user
      user_details.smartphone = True
      user_details.no_messages = False
      user_details.save()
      return user_details
   else:
      return user_details_list[0]

def save_memberships_from_form(user, form):
   delete_memberships_for_user(user)
   for project in form.cleaned_data['surveys']:
      membership = Membership(user = user, project = project)
      membership.save()
   user_details_list = UserDetail.objects.filter(user = user.id)
   if (len(user_details_list) > 0):
      user_details = user_details_list[0]
   else:
      user_details = UserDetail()
   user_details.phone_number = form.cleaned_data['phone_number']
   user_details.smartphone = form.cleaned_data['smartphone']
   user_details.no_messages = form.cleaned_data['no_messages']
   user_details.save()
   return

def save_memberships_from_surveys_param(user, surveys):
   projects = get_projects_from_surveys_param(surveys)
   if len(projects) > 0:
      delete_memberships_for_user(user)
      save_memberships_for_projects(user, projects)

def get_intake_survey_url(user, surveys):
   projects = get_projects_from_surveys_param(surveys)
   for project in projects:
      if project_has_intake_survey(project):
         identifier = MessageGenerator().getIdentifier(project, user)
         print user, identifier
         userDetail = UserDetail.objects.filter(user__id = user.id)[0]
         print userDetail
         userDetail.intake_survey_identifier = identifier
         userDetail.save()
         redirect_url = "%s?%s=%s" % (project.intake_survey_url, project.intake_survey_query_string_parameter, identifier)
         return redirect_url
   return reverse('userena_signup_complete',
                     kwargs={'username': user.username})

def has_intake_survey(surveys):
   projects = get_projects_from_surveys_param(surveys)
   for project in projects:
      if project_has_intake_survey(project):
         return True
   return None

def project_has_intake_survey(project):
   return (len(project.intake_survey_url) > 0 and len(project.intake_survey_query_string_parameter) > 0)

def get_projects_from_surveys_param(surveys):
   try:
      decodedSurveys = base64.b16decode(surveys)
      surveyIds = decodedSurveys.split(',')
      projectIds = [ string.atoi(projectId) for projectId in surveyIds ]
      projects = []
      for projectId in projectIds:
         projects.append(Project.objects.get(pk=projectId))
      return projects
   except TypeError:
      return []

def delete_memberships_for_user(user):
   memberships = Membership.objects.filter(user = user.id)
   for membership in memberships:
      membership.delete()

def save_memberships_for_projects(user, projects):
   for project in projects:
      membership = Membership(user = user, project = project)
      membership.save()

def save_project_from_form(project, form):
   project.name = form.cleaned_data['name']
   project.survey_url = form.cleaned_data['survey_url']
   project.smartphone_message = form.cleaned_data['smartphone_message']
   project.text_message = form.cleaned_data['text_message']            
   project.start_datetime = clean_datetime(form.cleaned_data['start_datetime'])
   project.end_datetime = clean_datetime(form.cleaned_data['end_datetime'])
   project.messages_per_day = form.cleaned_data['messages_per_day']
   project.guard_time_minutes = clean_integer(form.cleaned_data['guard_time_minutes'])
   project.synchronize_messages = clean_boolean(form.cleaned_data['synchronize_messages'])
   project.day_start_time = clean_time(form.cleaned_data['day_start_time'])
   project.day_end_time = clean_time(form.cleaned_data['day_end_time'])
   project.intake_survey_url = form.cleaned_data['intake_survey_url']
   project.intake_survey_query_string_parameter = form.cleaned_data['intake_survey_query_string_parameter']
   project.save()
   return

def save_message_from_form(message, form):
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

def clean_boolean(bool_obj):
   if (bool_obj is None):
      return False
   else:
      return True
      
def clean_integer(int_obj):
   if (int_obj is None):
      return 0
   else:
      return int_obj
      
def formatted_datetime():
   return format_datetime(datetime.datetime.now())

def format_datetime(datetime_obj):
   return datetime_obj.strftime(DATETIME_FORMAT)

def format_time(datetime_obj):
   return datetime_obj.strftime(TIME_FORMAT)

def formatted_time(time_string):
   time_obj = datetime.datetime.strptime(time_string, TIME_FORMAT)
   return datetime.time(time_obj.hour, time_obj.minute)



