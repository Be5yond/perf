from django.contrib import admin
from models import *

# Register your models here.


class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'info')
    search_fields = ('ip',)


class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'prefix', 'suffix', 'detect', 'install', 'delete')
    search_fields = ('name',)


class ProfAdmin(admin.ModelAdmin):
    list_display = ('name', 'tool', 'params')
    search_fields = ('tool',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('host', 'profile', 'result', 'status')
    search_fields = ('profile',)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('task',)
    
admin.site.register(Host, HostAdmin)
admin.site.register(Tool, ToolAdmin)
admin.site.register(Profile, ProfAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Report, ReportAdmin)
