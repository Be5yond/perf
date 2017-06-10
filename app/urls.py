from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'app.views.host', name='host'),
    url(r'^hosts/shell$', 'app.views.shell', name='shell'),
    url(r'^hosts/(.*)$', 'app.views.host', name='host'),
    url(r'^tools', 'app.views.tool', name='tool'),
    url(r'^help', 'app.views.document', name='help'),
    url(r'^tasks/$', 'app.views_task.task', name='task'),
    url(r'^tasks/new', 'app.views_task.step', name='task_step'),
    url(r'^tasks/reports/(.*)$', 'app.views_task.reports', name='task_report'),
    url(r'^channel', 'app.views.channel', name='channel'),
    url(r'^api/log', 'app.views_task.get_log', name='api_log'),
]
