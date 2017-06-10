from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^perf/admin/', include(admin.site.urls)),
    url(r'^perf/', include('app.urls', namespace='app')),
    # url(r'^$', 'app.views.home', name='home'),
]
