from sms.models import Setting, Project, Membership, Message, UserDetail
from django.contrib import admin

class SettingAdmin(admin.ModelAdmin):
    fields = ['name', 'value', 'description']


class ProjectAdmin(admin.ModelAdmin):
    fields = ['name', 'survey_url', 'smartphone_message', 'text_message',
              'start_datetime', 'end_datetime', 'messages_per_day',
              'guard_time_minutes', 'synchronize_messages', 'day_start_time',
              'day_end_time']

class MembershipAdmin(admin.ModelAdmin):
   fields = ['user', 'project', 'messages_generated']

class MessageAdmin(admin.ModelAdmin):
   fields = ['project', 'user_id', 'phone_number', 'email', 'message', 'send_at',
             'sent', 'sent_status', 'sent_error_message']

class UserDetailAdmin(admin.ModelAdmin):
   fields = ['user', 'phone_number', 'smartphone', 'no_messages', 'intake_survey_identifier']

admin.site.register(Setting, SettingAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserDetail, UserDetailAdmin)



