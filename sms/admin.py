from sms.models import Setting, Project
from django.contrib import admin

class SettingAdmin(admin.ModelAdmin):
    fields = ['name', 'value', 'description']


class ProjectAdmin(admin.ModelAdmin):
    fields = [ 'name', 'survey_url', 'smartphone_message', 'text_message' ]

admin.site.register(Setting, SettingAdmin)
admin.site.register(Project, ProjectAdmin)


